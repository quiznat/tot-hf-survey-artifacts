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
        numbers = [int(x) for x in input_data]
        expr = final_answer.strip()
        if not _safe_expression(expr):
            return False
        used = sorted(int(x) for x in re.findall(r"\d+", expr))
        if used != sorted(numbers):
            return False
        try:
            value = eval(expr, {"__builtins__": {}}, {})  # noqa: S307 - guarded by whitelist
        except Exception:
            return False
        return abs(float(value) - 24.0) < 1e-9

    def available_tools(self) -> Mapping[str, Callable[[str, Any], str]]:
        return {"calc": self._tool_calc}

    def _tool_calc(self, tool_input: str, input_data: Any) -> str:
        del input_data
        expr = tool_input.strip()
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
