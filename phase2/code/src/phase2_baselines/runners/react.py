"""ReAct-style baseline runner implementation."""

from __future__ import annotations

from typing import Any

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

            upper = output.upper()
            if upper.startswith("FINAL:"):
                final_answer = output.split(":", 1)[1].strip()
                success = self.task.evaluate(final_answer, input_data)
                return RunnerExecution(
                    outcome="success" if success else "failure",
                    final_answer=final_answer,
                    notes=notes,
                    trace=scratchpad_lines,
                    tokens_in=tokens_in,
                    tokens_out=tokens_out,
                )

            if upper.startswith("ACTION:"):
                action = output.split(":", 1)[1].strip()
                if " " in action:
                    tool_name, tool_input = action.split(" ", 1)
                else:
                    tool_name, tool_input = action, ""

                tool = tools.get(tool_name)
                if tool is None:
                    observation = f"error: unknown tool '{tool_name}'"
                else:
                    observation = tool(tool_input, input_data)
                scratchpad_lines.append(f"STEP {step} OBSERVATION: {observation}")
                continue

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
