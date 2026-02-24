"""ReAct-style baseline runner implementation."""

from __future__ import annotations

import re
from typing import Any, Mapping

from ..catalog.react_execution_mode_normalize import normalize_react_execution_mode
from ..catalog.react_execution_mode_reasoning_text_loop_no_tools_v1 import (
    REACT_EXECUTION_MODE_REASONING_TEXT_LOOP_NO_TOOLS_V1,
)
from ..catalog.react_execution_mode_smolagents_code_agent_with_task_tools_v1 import (
    REACT_EXECUTION_MODE_SMOLAGENTS_CODE_AGENT_WITH_TASK_TOOLS_V1,
)
from ..metrics import estimate_tokens
from ..models import RunnerExecution
from .base import BaseRunner


class ReactRunner(BaseRunner):
    """Baseline using a simple ReAct loop with tools."""

    runner_id = "runner_adapter.react"

    def _execute(self, input_data: Any) -> RunnerExecution:
        mode = normalize_react_execution_mode(
            str(
                self.config.get(
                    "react_execution_mode",
                    REACT_EXECUTION_MODE_SMOLAGENTS_CODE_AGENT_WITH_TASK_TOOLS_V1,
                )
            )
        )
        if mode == REACT_EXECUTION_MODE_REASONING_TEXT_LOOP_NO_TOOLS_V1:
            return self._execute_legacy(input_data)
        if mode == REACT_EXECUTION_MODE_SMOLAGENTS_CODE_AGENT_WITH_TASK_TOOLS_V1:
            if self.provider != "smolagents-inference":
                raise RuntimeError(
                    "ReactRunner in code-agent mode requires provider=smolagents-inference; "
                    f"got provider={self.provider}"
                )
            return self._execute_smolagents(input_data)
        raise RuntimeError(f"Unsupported react_execution_mode: {mode}")

    def _execute_smolagents(self, input_data: Any) -> RunnerExecution:
        assert self.task is not None

        try:
            from smolagents import CodeAgent, Tool  # type: ignore
        except Exception as exc:  # pragma: no cover - import path depends on runtime
            raise RuntimeError(
                "smolagents ReAct path requires Python >=3.10 with the `smolagents` package installed."
            ) from exc

        raw_model = getattr(self.model, "_model", None)
        if raw_model is None:
            raise RuntimeError(
                "smolagents ReAct path requires SmolagentsInferenceModel (missing internal `_model`)."
            )

        max_steps = int(self.config.get("max_steps", 5))
        strict_mode = bool(self.config.get("react_strict_mode", True))
        react_enable_tools = bool(self.config.get("react_enable_tools", True))
        task_tools = self.task.available_tools()
        tools = task_tools if react_enable_tools else {}
        bound_tools = self._bind_smolagents_tools(
            tool_base_cls=Tool,
            task_tools=tools,
            input_data=input_data,
        )

        prompt = self._build_smolagents_prompt(input_data, tools)
        agent = CodeAgent(
            tools=bound_tools,
            model=raw_model,
            max_steps=max_steps,
            stream_outputs=False,
        )
        run_result = agent.run(
            prompt,
            max_steps=max_steps,
            return_full_result=True,
        )

        output = str(getattr(run_result, "output", run_result) or "").strip()
        final_answer = self.task.extract_final_answer(output).strip() or output
        success = self.task.evaluate(final_answer, input_data)

        if not strict_mode and not success:
            fallback_answer = self.task.extract_final_answer(output).strip()
            if fallback_answer and self.task.evaluate(fallback_answer, input_data):
                final_answer = fallback_answer
                success = True

        token_usage = getattr(run_result, "token_usage", None)
        provider_tokens_in = int(getattr(token_usage, "input_tokens", 0) or 0)
        provider_tokens_out = int(getattr(token_usage, "output_tokens", 0) or 0)
        # Use one token estimator across conditions for parity in comparative tables.
        tokens_in = estimate_tokens(prompt)
        tokens_out = estimate_tokens(output)

        trace = [f"PROMPT: {prompt}"]
        steps = getattr(run_result, "steps", None)
        if isinstance(steps, list):
            for index, step in enumerate(steps, start=1):
                if not isinstance(step, Mapping):
                    trace.append(f"STEP {index}: {step}")
                    continue
                step_type = str(step.get("step_type", step.get("type", "step")))
                model_output = str(step.get("model_output", "")).strip()
                observations = step.get("observations", step.get("observation", ""))
                tool_calls = step.get("tool_calls")
                error = step.get("error")
                if model_output:
                    trace.append(f"STEP {index} {step_type} MODEL: {model_output}")
                if tool_calls:
                    trace.append(f"STEP {index} TOOL_CALLS: {tool_calls}")
                if observations:
                    trace.append(f"STEP {index} OBSERVATION: {observations}")
                if error:
                    trace.append(f"STEP {index} ERROR: {error}")
        trace.append(f"OUTPUT: {output}")
        trace.append(f"FINAL: {final_answer}")

        state = str(getattr(run_result, "state", "")).strip().lower()
        if success:
            outcome = "success"
            notes = "react baseline execution via smolagents code-agent runtime"
            error_type: str | None = None
        elif state == "max_steps_error":
            outcome = "timeout"
            notes = "react baseline execution via smolagents code-agent runtime reached max_steps"
            error_type = "max_steps_exceeded"
        else:
            outcome = "failure"
            notes = "react baseline execution via smolagents code-agent runtime"
            error_type = None

        return RunnerExecution(
            outcome=outcome,
            final_answer=final_answer,
            notes=notes,
            trace=trace,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            error_type=error_type,
            extra={
                "provider_token_usage": {
                    "input_tokens": provider_tokens_in,
                    "output_tokens": provider_tokens_out,
                }
            },
        )

    def _execute_legacy(self, input_data: Any) -> RunnerExecution:
        assert self.task is not None

        max_steps = int(self.config.get("max_steps", 5))
        strict_mode = bool(self.config.get("react_strict_mode", True))
        scratchpad_lines: list[str] = []
        react_enable_tools = bool(self.config.get("react_enable_tools", True))
        task_tools = self.task.available_tools()
        tools = task_tools if react_enable_tools else {}
        tokens_in = 0
        tokens_out = 0

        final_answer = ""
        notes = "react baseline execution (reasoning text loop, no tools)"

        for step in range(1, max_steps + 1):
            scratchpad = "\n".join(scratchpad_lines)
            if hasattr(self.task, "build_react_prompt"):
                try:
                    prompt = self.task.build_react_prompt(  # type: ignore[attr-defined]
                        input_data,
                        scratchpad,
                        tools_override=tools,
                    )
                except TypeError:
                    # Backward-compat fallback for tasks with older build_react_prompt signature.
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

                if strict_mode:
                    return RunnerExecution(
                        outcome="failure",
                        final_answer=final_answer,
                        notes=notes,
                        trace=scratchpad_lines,
                        tokens_in=tokens_in,
                        tokens_out=tokens_out,
                    )

                # Non-strict mode: if FINAL is underspecified (for example "24"), recover from ACTION input.
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
                if not strict_mode and action_success:
                    return RunnerExecution(
                        outcome="success",
                        final_answer=action_expr,
                        notes=notes + " (action expression solved task)",
                        trace=scratchpad_lines,
                        tokens_in=tokens_in,
                        tokens_out=tokens_out,
                    )
                continue

            if not strict_mode:
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
            notes="react baseline execution (reasoning text loop, no tools) reached max_steps without FINAL",
            trace=scratchpad_lines,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            error_type="max_steps_exceeded",
        )

    @staticmethod
    def _bind_smolagents_tools(tool_base_cls: type, task_tools: Mapping[str, Any], input_data: Any) -> list[Any]:
        bound_tools: list[Any] = []

        for tool_name, tool_fn in task_tools.items():
            if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", tool_name):
                continue

            class BoundTaskTool(tool_base_cls):
                def __init__(self, name: str, fn: Any, bound_input: Any) -> None:
                    super().__init__()
                    self.name = name
                    self.description = (
                        f"Task tool `{name}`. "
                        "Use this when the benchmark item requires explicit computation or verification."
                    )
                    self.inputs = {
                        "tool_input": {
                            "type": "string",
                            "description": "Input text for the tool.",
                        }
                    }
                    self.output_type = "string"
                    self._fn = fn
                    self._bound_input = bound_input

                def forward(self, tool_input: str) -> str:
                    try:
                        return str(self._fn(tool_input, self._bound_input))
                    except Exception as exc:
                        return f"error: {exc}"

            bound_tools.append(BoundTaskTool(tool_name, tool_fn, input_data))
        return bound_tools

    def _build_smolagents_prompt(self, input_data: Any, tools: Mapping[str, Any]) -> str:
        assert self.task is not None
        task_prompt = self.task.build_prompt(input_data)
        tool_names = sorted(tools.keys())
        if tool_names:
            tools_line = ", ".join(tool_names)
        else:
            tools_line = "none"
        return (
            "Solve this benchmark item using iterative reasoning with optional tool calls.\n"
            f"Task:\n{task_prompt}\n\n"
            f"Available tools: {tools_line}\n"
            "When finished, return only the final answer in the exact task-required format."
        )

    @staticmethod
    def _extract_tagged_value(output: str, tag: str) -> str:
        # Support both simple tags (FINAL:/ACTION:) and paper-like ReAct tags
        # (Action k: ... / Finish[...]).
        if tag.upper() == "FINAL":
            pattern = re.compile(r"FINAL\s*:\s*(.+)", flags=re.IGNORECASE)
            match = pattern.search(output)
            if match:
                return match.group(1).strip()
            finish = re.search(r"finish\[(.+?)\]", output, flags=re.IGNORECASE | re.DOTALL)
            if finish:
                return finish.group(1).strip()
            return ""

        if tag.upper() == "ACTION":
            action_pattern = re.compile(r"action\s*\d*\s*:\s*(.+)", flags=re.IGNORECASE)
            match = action_pattern.search(output)
            if match:
                return match.group(1).strip()
            tag_pattern = re.compile(r"ACTION\s*:\s*(.+)", flags=re.IGNORECASE)
            match = tag_pattern.search(output)
            if match:
                return match.group(1).strip()

            # Allow direct one-line tool call forms like: calc[...]
            direct = output.strip().splitlines()[-1].strip() if output.strip() else ""
            if re.match(r"^[A-Za-z_][A-Za-z0-9_]*\s*\[.*\]\s*$", direct) and not direct.lower().startswith("finish["):
                return direct
            return ""

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
        bracket = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*\[(.*)\]\s*$", action, flags=re.DOTALL)
        if bracket:
            tool_name = bracket.group(1)
            tool_input = bracket.group(2)
        elif " " in action:
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
