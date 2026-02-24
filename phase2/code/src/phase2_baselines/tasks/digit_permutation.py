"""Digit permutation optimization task."""

from __future__ import annotations

from collections import Counter
import itertools
import math
import re
from typing import Any, Callable, Mapping

from .base import BaseTask


class DigitPermutationTask(BaseTask):
    """Find the maximal valid permutation under a divisibility constraint."""

    task_id = "digit-permutation-demo"

    def build_prompt(self, input_data: Any, scratchpad: str = "") -> str:
        payload = _normalize_input(input_data)
        base = (
            "Form the largest possible 4-digit integer using the provided digits exactly once.\n"
            f"Digits: {payload['digits']}\n"
            f"The number must be divisible by {payload['divisor']}.\n"
            "Return only the integer."
        )
        if not scratchpad:
            return base
        return f"{base}\n\nScratchpad:\n{scratchpad}"

    def evaluate(self, final_answer: str, input_data: Any) -> bool:
        payload = _normalize_input(input_data)
        candidate = _parse_integer(final_answer)
        if candidate is None:
            return False
        if not _uses_same_digits(candidate, payload["digits"]):
            return False
        if candidate % payload["divisor"] != 0:
            return False
        oracle = payload.get("oracle_max")
        if oracle is None:
            return True
        return candidate == oracle

    def extract_final_answer(self, raw_output: str) -> str:
        direct = super().extract_final_answer(raw_output).strip()
        direct_is_single_number = bool(re.fullmatch(r"\s*-?\d+\s*", direct))
        direct_value = _parse_integer(direct) if direct_is_single_number else None
        if direct_value is not None and len(str(abs(direct_value))) >= 4:
            return str(direct_value)

        answer_line_candidates, all_candidates = _extract_integer_candidates(raw_output)
        if answer_line_candidates:
            return str(answer_line_candidates[-1])
        candidates = all_candidates
        if candidates:
            return str(max(candidates))

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
            + f"\n\nGenerate up to {branch_factor} distinct candidate integers."
            + "\nEach line must be a single 4-digit integer using the provided digits exactly once."
            + "\nDo not include words, commas, equations, or explanations."
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
        value = _parse_integer(candidate)
        if value is None:
            return 0.0
        if not _uses_same_digits(value, payload["digits"]):
            return 0.05
        if value % payload["divisor"] != 0:
            return 0.2
        oracle = payload.get("oracle_max")
        if oracle is None:
            return 1.0
        if oracle <= 0:
            return 0.0
        if value == oracle:
            return 1.0
        return round(max(0.0, min(0.95, value / float(oracle))), 6)

    def available_tools(self) -> Mapping[str, Callable[[str, Any], str]]:
        return {
            "is_divisible": self._tool_is_divisible,
            "best_divisible": self._tool_best_divisible,
        }

    def _tool_is_divisible(self, tool_input: str, input_data: Any) -> str:
        payload = _normalize_input(input_data)
        value = _parse_integer(tool_input)
        if value is None:
            return "error: provide an integer"
        return "yes" if value % payload["divisor"] == 0 else "no"

    def _tool_best_divisible(self, tool_input: str, input_data: Any) -> str:
        del tool_input
        payload = _normalize_input(input_data)
        best = _best_valid_number(payload["digits"], payload["divisor"])
        if best is None:
            return "none"
        return str(best)


def _normalize_input(input_data: Any) -> dict[str, Any]:
    if not isinstance(input_data, dict):
        raise RuntimeError("DigitPermutationTask input_data must be an object")
    digits = input_data.get("digits")
    divisor = input_data.get("divisor")
    if not isinstance(digits, list) or len(digits) != 4:
        raise RuntimeError("DigitPermutationTask digits must be a list of 4 integers")
    if not isinstance(divisor, int) or divisor == 0:
        raise RuntimeError("DigitPermutationTask divisor must be a non-zero integer")
    payload: dict[str, Any] = {
        "digits": [int(x) for x in digits],
        "divisor": int(divisor),
    }
    oracle = input_data.get("oracle_max")
    if isinstance(oracle, int):
        payload["oracle_max"] = oracle
    return payload


def _parse_integer(raw: str) -> int | None:
    text = raw.strip()
    if text.upper().startswith("FINAL:"):
        text = text.split(":", 1)[1].strip()
    match = re.search(r"-?\d+", text)
    if not match:
        return None
    try:
        return int(match.group(0))
    except ValueError:
        return None


def _uses_same_digits(value: int, digits: list[int]) -> bool:
    if not math.isfinite(float(value)):
        return False
    text = str(abs(value))
    if len(text) != 4:
        return False
    if text[0] == "0":
        return False
    return Counter(int(ch) for ch in text) == Counter(int(d) for d in digits)


def _best_valid_number(digits: list[int], divisor: int) -> int | None:
    best: int | None = None
    for perm in itertools.permutations(digits, 4):
        if perm[0] == 0:
            continue
        value = (perm[0] * 1000) + (perm[1] * 100) + (perm[2] * 10) + perm[3]
        if value % divisor != 0:
            continue
        if best is None or value > best:
            best = value
    return best


def _extract_integer_candidates(raw_output: str) -> tuple[list[int], list[int]]:
    answer_line_candidates: list[int] = []
    all_candidates: list[int] = []

    # Prefer explicit answer-like lines.
    lines = [line.strip() for line in raw_output.splitlines() if line.strip()]
    for line in lines:
        text = re.sub(r"^\d+\s*[\)\.\-:]\s*", "", line)
        answer_like = False
        if ":" in text:
            prefix, rest = text.split(":", 1)
            if prefix.strip().lower() in {"final", "answer", "result"}:
                text = rest.strip()
                answer_like = True
        if re.search(r"\b(answer|final|result)\b", text, flags=re.IGNORECASE):
            answer_like = True
        value = _parse_integer(text)
        if value is not None:
            all_candidates.append(value)
            if answer_like:
                answer_line_candidates.append(value)

    # Fallback: scan all 4+ digit integers in full text.
    for match in re.finditer(r"(?<!\d)\d{4,}(?!\d)", raw_output):
        try:
            all_candidates.append(int(match.group(0)))
        except ValueError:
            continue

    # Preserve order, remove duplicates.
    deduped_answers: list[int] = []
    seen_answers: set[int] = set()
    for value in answer_line_candidates:
        if value in seen_answers:
            continue
        seen_answers.add(value)
        deduped_answers.append(value)

    deduped_all: list[int] = []
    seen_all: set[int] = set()
    for value in all_candidates:
        if value in seen_all:
            continue
        seen_all.add(value)
        deduped_all.append(value)
    return deduped_answers, deduped_all
