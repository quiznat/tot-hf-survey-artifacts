"""Arithmetic benchmark task used for local baseline scaffolding."""

from __future__ import annotations

import re
from typing import Any, Callable, Mapping

from .base import BaseTask


class Arithmetic24Task(BaseTask):
    """Simple task requiring an expression that evaluates to 24."""

    task_id = "game24-demo"

    def build_prompt(self, input_data: Any, scratchpad: str = "") -> str:
        numbers = list(input_data)
        base = (
            "Use each number exactly once to produce 24. "
            f"Numbers: {numbers}. "
            "Return only one expression in the final answer."
        )
        if not scratchpad:
            return base
        return f"{base}\n\nScratchpad:\n{scratchpad}"

    def evaluate(self, final_answer: str, input_data: Any) -> bool:
        analysis = self.analyze_candidate(final_answer, input_data)
        return bool(analysis["is_exact"])

    def score_candidate(self, candidate: str, input_data: Any) -> float:
        """Rule-based score in [0, 1] for ToT pruning."""
        analysis = self.analyze_candidate(candidate, input_data)
        if analysis["is_exact"]:
            return 1.0
        if not analysis["parseable"]:
            return 0.0
        if not analysis["uses_required_numbers"]:
            return 0.05

        value = float(analysis["value"])
        diff = abs(value - 24.0)
        # 0 diff -> 1.0, 20+ diff -> near 0.2
        closeness = max(0.0, 1.0 - min(diff, 20.0) / 25.0)
        return round(0.2 + 0.8 * closeness, 6)

    def analyze_candidate(self, candidate: str, input_data: Any) -> dict[str, Any]:
        numbers = [int(x) for x in input_data]
        expr = _normalize_expression(candidate)
        if not _safe_expression(expr):
            return {
                "expression": expr,
                "parseable": False,
                "uses_required_numbers": False,
                "value": None,
                "is_exact": False,
            }
        used = sorted(int(x) for x in re.findall(r"\d+", expr))
        uses_required_numbers = used == sorted(numbers)
        try:
            value = eval(expr, {"__builtins__": {}}, {})  # noqa: S307 - guarded by whitelist
        except Exception:
            return {
                "expression": expr,
                "parseable": False,
                "uses_required_numbers": uses_required_numbers,
                "value": None,
                "is_exact": False,
            }

        is_exact = uses_required_numbers and abs(float(value) - 24.0) < 1e-9
        return {
            "expression": expr,
            "parseable": True,
            "uses_required_numbers": uses_required_numbers,
            "value": float(value),
            "is_exact": is_exact,
        }

    def available_tools(self) -> Mapping[str, Callable[[str, Any], str]]:
        return {"calc": self._tool_calc}

    def _tool_calc(self, tool_input: str, input_data: Any) -> str:
        del input_data
        expr = _normalize_expression(tool_input)
        if not _safe_expression(expr):
            return "error: unsafe expression"
        try:
            value = eval(expr, {"__builtins__": {}}, {})  # noqa: S307 - guarded by whitelist
        except Exception as exc:
            return f"error: {exc}"
        return str(value)


def _safe_expression(expr: str) -> bool:
    if not expr:
        return False
    # Allow digits, arithmetic operators, decimal points, spaces, and parentheses.
    return bool(re.fullmatch(r"[\d\s\+\-\*/\(\)\.]+", expr))


def _normalize_expression(raw: str) -> str:
    expr = raw.strip()

    # Normalize common Unicode math operators from model outputs.
    replacements = {
        "×": "*",
        "÷": "/",
        "−": "-",
        "–": "-",
        "—": "-",
    }
    for source, target in replacements.items():
        expr = expr.replace(source, target)

    # If model returns "expr = value", keep only the expression part.
    if "=" in expr:
        expr = expr.split("=", 1)[0].strip()

    # Drop explanatory tails like "-> invalid".
    if "->" in expr:
        expr = expr.split("->", 1)[0].strip()
    if "→" in expr:
        expr = expr.split("→", 1)[0].strip()

    # Remove a final trailing period often emitted in natural language.
    expr = expr.rstrip(".")

    return expr
