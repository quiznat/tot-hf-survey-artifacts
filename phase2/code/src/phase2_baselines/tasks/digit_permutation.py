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
