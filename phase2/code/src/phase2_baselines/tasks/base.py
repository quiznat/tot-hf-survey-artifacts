"""Base task implementation with default helpers."""

from __future__ import annotations

from typing import Any, Callable, Dict, Mapping


class BaseTask:
    """Default task helper implementations."""

    task_id = "base-task"

    def build_prompt(self, input_data: Any, scratchpad: str = "") -> str:
        if scratchpad:
            return f"Solve task with input: {input_data}\n\nScratchpad:\n{scratchpad}\n\nProvide final answer."
        return f"Solve task with input: {input_data}. Provide final answer."

    def extract_final_answer(self, raw_output: str) -> str:
        lines = [line.strip() for line in raw_output.splitlines() if line.strip()]
        for line in reversed(lines):
            if line.upper().startswith("FINAL:"):
                return line.split(":", 1)[1].strip()
        return raw_output.strip()

    def evaluate(self, final_answer: str, input_data: Any) -> bool:
        del final_answer, input_data
        return False

    def available_tools(self) -> Mapping[str, Callable[[str, Any], str]]:
        return {}

    def build_react_prompt(self, input_data: Any, scratchpad: str) -> str:
        tools = ", ".join(sorted(self.available_tools().keys())) or "none"
        return (
            "You are solving a benchmark task using a ReAct loop.\n"
            f"Task input: {input_data}\n"
            f"Available tools: {tools}\n"
            "Respond using one of:\n"
            "- THINK: <reasoning>\n"
            "- ACTION: <tool_name> <tool_input>\n"
            "- FINAL: <answer>\n\n"
            f"Scratchpad:\n{scratchpad}\n"
        )
