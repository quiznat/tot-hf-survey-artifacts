"""ReAct-style baseline runner implementation."""

from __future__ import annotations

import re
from typing import Any, Mapping

from ..metrics import estimate_tokens
from ..models import RunnerExecution
from .base import BaseRunner


class ReactRunner(BaseRunner):
    """Baseline using a simple ReAct loop with tools."""

    runner_id = "baseline-react"

    def _execute(self, input_data: Any) -> RunnerExecution:
        assert self.task is not None

        max_steps = int(self.config.get("max_steps", 5))
        scratchpad_lines: list[str] = []
        tools = self.task.available_tools()
        tokens_in = 0
        tokens_out = 0

        final_answer = ""
        notes = "react baseline execution"

        for step in range(1, max_steps + 1):
            scratchpad = "\n".join(scratchpad_lines)
            if hasattr(self.task, "build_react_prompt"):
                prompt = self.task.build_react_prompt(input_data, scratchpad)  # type: ignore[attr-defined]
            else:
                prompt = self.task.build_prompt(input_data, scratchpad)

            output = self.model.generate(prompt).strip()
            tokens_in += estimate_tokens(prompt)
            tokens_out += estimate_tokens(output)
            scratchpad_lines.append(f"STEP {step} MODEL: {output}")

            final_answer = self._extract_tagged_value(output, "FINAL")
            action = self._extract_tagged_value(output, "ACTION")
            if final_answer:
                success = self.task.evaluate(final_answer, input_data)
                if success:
                    return RunnerExecution(
                        outcome="success",
                        final_answer=final_answer,
                        notes=notes,
                        trace=scratchpad_lines,
                        tokens_in=tokens_in,
                        tokens_out=tokens_out,
                    )

                # If FINAL is underspecified (for example "24"), recover from ACTION input.
                if action:
                    action_success, action_expr = self._execute_action(step, action, tools, input_data, scratchpad_lines)
                    if action_success:
                        return RunnerExecution(
                            outcome="success",
                            final_answer=action_expr,
                            notes=notes + " (recovered from ACTION expression)",
                            trace=scratchpad_lines,
                            tokens_in=tokens_in,
                            tokens_out=tokens_out,
                        )
                    continue

                return RunnerExecution(
                    outcome="failure",
                    final_answer=final_answer,
                    notes=notes,
                    trace=scratchpad_lines,
                    tokens_in=tokens_in,
                    tokens_out=tokens_out,
                )

            if action:
                action_success, action_expr = self._execute_action(step, action, tools, input_data, scratchpad_lines)
                if action_success:
                    return RunnerExecution(
                        outcome="success",
                        final_answer=action_expr,
                        notes=notes + " (action expression solved task)",
                        trace=scratchpad_lines,
                        tokens_in=tokens_in,
                        tokens_out=tokens_out,
                    )
                continue

            # Fallback: treat model output as a possible direct answer expression.
            candidate = self.task.extract_final_answer(output).strip()
            if candidate:
                success = self.task.evaluate(candidate, input_data)
                if success:
                    return RunnerExecution(
                        outcome="success",
                        final_answer=candidate,
                        notes=notes + " (fallback expression parse)",
                        trace=scratchpad_lines,
                        tokens_in=tokens_in,
                        tokens_out=tokens_out,
                    )

            scratchpad_lines.append(f"STEP {step} OBSERVATION: no-action")

        return RunnerExecution(
            outcome="timeout",
            final_answer=final_answer,
            notes="react baseline execution reached max_steps without FINAL",
            trace=scratchpad_lines,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            error_type="max_steps_exceeded",
        )

    @staticmethod
    def _extract_tagged_value(output: str, tag: str) -> str:
        pattern = re.compile(rf"{tag}\s*:\s*(.+)", flags=re.IGNORECASE)
        match = pattern.search(output)
        if match:
            return match.group(1).strip()
        return ""

    def _execute_action(
        self,
        step: int,
        action: str,
        tools: Mapping[str, Any],
        input_data: Any,
        scratchpad_lines: list[str],
    ) -> tuple[bool, str]:
        if " " in action:
            tool_name, tool_input = action.split(" ", 1)
        else:
            tool_name, tool_input = action, ""

        tool_name = tool_name.strip()
        tool_input = tool_input.strip()

        tool = tools.get(tool_name)
        if tool is None:
            observation = f"error: unknown tool '{tool_name}'"
        else:
            observation = tool(tool_input, input_data)
        scratchpad_lines.append(f"STEP {step} OBSERVATION: {observation}")

        if tool is not None and tool_input and self.task.evaluate(tool_input, input_data):
            return True, tool_input
        return False, ""
