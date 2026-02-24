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

    def build_cot_prompt(self, input_data: Any, sample_index: int = 1, total_samples: int = 1) -> str:
        prompt = self.build_prompt(input_data)
        sample_note = ""
        if total_samples > 1:
            sample_note = f"Sample {sample_index}/{total_samples}: produce an independently reasoned attempt.\n"
        return (
            f"{prompt}\n\n"
            f"{sample_note}"
            "Think step by step before answering.\n"
            "End with exactly one line:\n"
            "FINAL: <answer>\n"
        )

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

    def build_tot_decomposition_prompt(
        self,
        input_data: Any,
        current_path: str,
        branch_factor: int,
        disallowed_candidates: list[str] | None = None,
        attempt: int = 0,
    ) -> str:
        blocked = [candidate for candidate in (disallowed_candidates or []) if candidate]
        task_spec = self.build_prompt(input_data)
        prompt = (
            "You are initializing a Tree-of-Thought search.\n"
            "Task specification:\n"
            f"{task_spec}\n"
            f"Generate up to {branch_factor} thoughts about how to decompose or solve this problem.\n"
            "If you choose decomposition, include subproblem nodes and recombination instructions.\n"
            "Return one thought per line using one of these exact forms:\n"
            "- DECOMP: insight=<core contributor insight>; subnodes=<node1 | node2 | ...>; recombine=<how to combine subnode outputs>\n"
            "- STEP: <concrete progress step>\n"
            "- FINAL: <candidate final answer>\n"
            "Do not output explanations outside those lines."
        )
        if current_path:
            prompt += f"\nExisting path context:\n{current_path}"
        if blocked:
            prompt += "\nDo not repeat these prior states:\n"
            prompt += "\n".join(f"- {candidate}" for candidate in blocked)
        if attempt > 0:
            prompt += "\nPrevious output repeated states; generate novel alternatives."
        return prompt

    def build_tot_step_prompt(
        self,
        input_data: Any,
        current_path: str,
        branch_factor: int,
        disallowed_candidates: list[str] | None = None,
        attempt: int = 0,
    ) -> str:
        blocked = [candidate for candidate in (disallowed_candidates or []) if candidate]
        task_spec = self.build_prompt(input_data)
        prompt = (
            "You are expanding a Tree-of-Thought reasoning path.\n"
            "Task specification:\n"
            f"{task_spec}\n"
            "Current path:\n"
            f"{current_path or '(empty)'}\n\n"
            f"Generate up to {branch_factor} thoughts about how to decompose further or solve from here.\n"
            "If decomposing, list contributor insight, subnodes, and recombine instructions.\n"
            "When solving, show how the solution reconnects to prior decomposition insight.\n"
            "Return one thought per line using one of these exact forms:\n"
            "- DECOMP: insight=<core contributor insight>; subnodes=<node1 | node2 | ...>; recombine=<how to combine subnode outputs>\n"
            "- STEP: <concrete reasoning step>\n"
            "- FINAL: <candidate final answer>\n"
            "No extra commentary."
        )
        if blocked:
            prompt += "\nDo not repeat these prior states:\n"
            prompt += "\n".join(f"- {candidate}" for candidate in blocked)
        if attempt > 0:
            prompt += "\nPrevious outputs repeated states; generate different alternatives."
        return prompt

    def extract_tot_final_answer(self, thought_state: str, input_data: Any) -> str:
        del input_data
        lines = [line.strip() for line in thought_state.splitlines() if line.strip()]
        for line in reversed(lines):
            upper = line.upper()
            if upper.startswith("FINAL:"):
                return line.split(":", 1)[1].strip()
            if upper.startswith("ANSWER:"):
                return line.split(":", 1)[1].strip()
            if upper.startswith("SOLUTION:"):
                return line.split(":", 1)[1].strip()
        return ""

    def score_thought_state(self, thought_state: str, input_data: Any) -> float:
        answer = self.extract_tot_final_answer(thought_state, input_data)
        if not answer:
            return 0.5
        if self.evaluate(answer, input_data):
            return 1.0
        scorer = getattr(self, "score_candidate", None)
        if callable(scorer):
            try:
                return float(scorer(answer, input_data))
            except Exception:
                return 0.2
        return 0.2

    def build_react_prompt(
        self,
        input_data: Any,
        scratchpad: str,
        tools_override: Mapping[str, Callable[[str, Any], str]] | None = None,
    ) -> str:
        tool_map = tools_override if tools_override is not None else self.available_tools()
        tool_names = sorted(tool_map.keys())
        tools = ", ".join(tool_names) if tool_names else "none"
        action_hints = ""
        if tool_names:
            action_hints = "\n".join(f"- {name}[<input>]" for name in tool_names)
        else:
            action_hints = "- (no tools available)"
        return (
            "You are solving a benchmark task using ReAct (Reason + Act).\n"
            f"Task input: {input_data}\n"
            f"Available tools: {tools}\n"
            "Allowed action formats:\n"
            f"{action_hints}\n"
            "- Finish[<final answer>]\n\n"
            "Output format for this turn:\n"
            "Thought <k>: <short reasoning>\n"
            "Action <k>: <tool>[<input>]  OR  Finish[<answer>]\n\n"
            "Interaction history:\n"
            f"{scratchpad or '(empty)'}\n"
        )
