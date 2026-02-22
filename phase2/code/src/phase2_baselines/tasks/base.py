"""Base task implementation with default helpers."""

from __future__ import annotations

from typing import Any, Callable, Mapping


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

    def build_tot_candidate_prompt(
        self,
        input_data: Any,
        scratchpad: str,
        branch_factor: int,
        disallowed_candidates: list[str] | None = None,
        attempt: int = 0,
    ) -> str:
        prompt = (
            self.build_prompt(input_data, scratchpad=scratchpad)
            + f"\n\nGenerate up to {branch_factor} distinct candidate final answers."
            + "\nReturn exactly one candidate per line."
            + "\nDo not include explanations."
        )
        blocked = [candidate for candidate in (disallowed_candidates or []) if candidate]
        if blocked:
            prompt += "\nDo not repeat any of these previously explored candidates:\n"
            prompt += "\n".join(f"- {candidate}" for candidate in blocked)
        if attempt > 0:
            prompt += "\nPrevious candidates were duplicates or invalid; generate different alternatives."
        return prompt

    def build_react_prompt(
        self,
        input_data: Any,
        scratchpad: str,
        tools_override: Mapping[str, Callable[[str, Any], str]] | None = None,
    ) -> str:
        tool_map = tools_override if tools_override is not None else self.available_tools()
        tools = ", ".join(sorted(tool_map.keys())) or "none"
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
