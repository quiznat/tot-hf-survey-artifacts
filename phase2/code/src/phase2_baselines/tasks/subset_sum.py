"""Subset-sum style task for structured reasoning evaluation."""

from __future__ import annotations

from collections import Counter
import re
from typing import Any, Callable, Mapping

from .base import BaseTask


class SubsetSumTask(BaseTask):
    """Select a valid subset whose sum matches a target."""

    task_id = "subset-sum-demo"

    def build_prompt(self, input_data: Any, scratchpad: str = "") -> str:
        payload = _normalize_input(input_data)
        base = (
            "Select one or more values from the provided list so their sum equals the target.\n"
            f"Numbers: {payload['numbers']}\n"
            f"Target: {payload['target']}\n"
            "Rules:\n"
            "- You may use each listed number at most once.\n"
            "- Return only a comma-separated list of chosen numbers (example: 4,9,2).\n"
            "- Do not include explanation text."
        )
        if not scratchpad:
            return base
        return f"{base}\n\nScratchpad:\n{scratchpad}"

    def evaluate(self, final_answer: str, input_data: Any) -> bool:
        payload = _normalize_input(input_data)
        selected = _parse_selected_numbers(final_answer)
        if not selected:
            return False
        available = Counter(payload["numbers"])
        used = Counter(selected)
        if any(count > available[number] for number, count in used.items()):
            return False
        return sum(selected) == int(payload["target"])

    def extract_final_answer(self, raw_output: str) -> str:
        direct = super().extract_final_answer(raw_output).strip()
        candidates = _extract_subset_candidates(raw_output)

        # Prefer lines closer to the end of the output.
        for candidate in reversed(candidates):
            selected = _parse_selected_numbers(candidate)
            if selected:
                return ",".join(str(x) for x in selected)

        # Conservative fallback: only accept direct when it already looks list-like.
        if re.search(r"-?\d+\s*,\s*-?\d+", direct):
            selected = _parse_selected_numbers(direct)
            if selected:
                return ",".join(str(x) for x in selected)
        return direct if direct else raw_output.strip()

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
            + f"\n\nGenerate up to {branch_factor} distinct candidate subsets."
            + "\nEach line must be a comma-separated list of integers from the provided numbers."
            + "\nDo not include words or explanations."
        )
        blocked = [candidate for candidate in (disallowed_candidates or []) if candidate]
        if blocked:
            prompt += "\nDo not repeat any of these previously explored candidates:\n"
            prompt += "\n".join(f"- {candidate}" for candidate in blocked)
        if attempt > 0:
            prompt += "\nPrevious candidates were duplicates or invalid; generate different alternatives."
        return prompt

    def score_candidate(self, candidate: str, input_data: Any) -> float:
        payload = _normalize_input(input_data)
        selected = _parse_selected_numbers(candidate)
        if not selected:
            return 0.0

        available = Counter(payload["numbers"])
        used = Counter(selected)
        if any(count > available[number] for number, count in used.items()):
            return 0.05

        total = sum(selected)
        target = int(payload["target"])
        if total == target:
            return 1.0

        diff = abs(total - target)
        closeness = max(0.0, 1.0 - min(diff, 40.0) / 40.0)
        return round(0.2 + 0.8 * closeness, 6)

    def available_tools(self) -> Mapping[str, Callable[[str, Any], str]]:
        return {
            "sum_list": self._tool_sum_list,
            "check_target": self._tool_check_target,
        }

    def _tool_sum_list(self, tool_input: str, input_data: Any) -> str:
        del input_data
        selected = _parse_selected_numbers(tool_input)
        if not selected:
            return "error: provide comma-separated integers"
        return str(sum(selected))

    def _tool_check_target(self, tool_input: str, input_data: Any) -> str:
        payload = _normalize_input(input_data)
        selected = _parse_selected_numbers(tool_input)
        if not selected:
            return "error: provide comma-separated integers"
        available = Counter(payload["numbers"])
        used = Counter(selected)
        if any(count > available[number] for number, count in used.items()):
            return "invalid: number usage exceeds provided list"
        total = sum(selected)
        return "match" if total == int(payload["target"]) else f"miss:{total}"


def _normalize_input(input_data: Any) -> dict[str, Any]:
    if not isinstance(input_data, dict):
        raise RuntimeError("SubsetSumTask input_data must be an object with numbers + target")
    numbers = input_data.get("numbers")
    target = input_data.get("target")
    if not isinstance(numbers, list) or len(numbers) < 2:
        raise RuntimeError("SubsetSumTask numbers must be a list with length >= 2")
    if not isinstance(target, (int, float)):
        raise RuntimeError("SubsetSumTask target must be numeric")
    return {"numbers": [int(x) for x in numbers], "target": int(target)}


def _parse_selected_numbers(raw: str) -> list[int]:
    cleaned = raw.strip()
    if cleaned.upper().startswith("FINAL:"):
        cleaned = cleaned.split(":", 1)[1].strip()
    cleaned = cleaned.replace("[", "").replace("]", "")
    matches = re.findall(r"-?\d+", cleaned)
    if not matches:
        return []
    return [int(x) for x in matches]


def _extract_subset_candidates(raw_output: str) -> list[str]:
    candidates: list[str] = []
    lines = [line.strip() for line in raw_output.splitlines() if line.strip()]

    for line in lines:
        text = re.sub(r"^\d+\s*[\)\.\-:]\s*", "", line)
        text = re.sub(r"^[\-\*\•]\s*", "", text)
        if ":" in text:
            prefix, rest = text.split(":", 1)
            if prefix.strip().lower() in {"final", "answer", "subset", "result"}:
                text = rest.strip()

        bracket_match = re.findall(r"\[[^\]]+\]", text)
        if bracket_match:
            candidates.extend(bracket_match)

        if "=" in text:
            left, _right = text.split("=", 1)
            if "+" in left or "," in left:
                text = left.strip()
        if "+" in text and "," not in text:
            nums = re.findall(r"-?\d+", text)
            if len(nums) >= 2:
                candidates.append(",".join(nums))
        if re.search(r"-?\d+\s*,\s*-?\d+", text):
            candidates.append(text)

    # Also scan full output for bracketed lists.
    for match in re.finditer(r"\[[^\]]+\]", raw_output):
        candidates.append(match.group(0))

    deduped: list[str] = []
    seen: set[str] = set()
    for candidate in candidates:
        cleaned = candidate.strip()
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        deduped.append(cleaned)
    return deduped
