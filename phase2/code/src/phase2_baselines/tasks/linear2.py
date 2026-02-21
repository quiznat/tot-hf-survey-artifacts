"""2-variable linear system solving task."""

from __future__ import annotations

import math
import re
from typing import Any, Callable, Mapping

from .base import BaseTask


class LinearSystem2Task(BaseTask):
    """Solve a pair of linear equations in x and y."""

    task_id = "linear2-demo"

    def build_prompt(self, input_data: Any, scratchpad: str = "") -> str:
        payload = _normalize_input(input_data)
        eq1 = payload["equations"][0]
        eq2 = payload["equations"][1]
        base = (
            "Solve the linear system for x and y.\n"
            f"Equation 1: {eq1[0]}*x + {eq1[1]}*y = {eq1[2]}\n"
            f"Equation 2: {eq2[0]}*x + {eq2[1]}*y = {eq2[2]}\n"
            "Return only: x=<value>,y=<value>\n"
            "Use decimal values when needed."
        )
        if not scratchpad:
            return base
        return f"{base}\n\nScratchpad:\n{scratchpad}"

    def evaluate(self, final_answer: str, input_data: Any) -> bool:
        payload = _normalize_input(input_data)
        solution = _parse_solution(final_answer)
        if solution is None:
            return False
        x_val, y_val = solution
        return _residual_ok(payload["equations"], x_val, y_val)

    def score_candidate(self, candidate: str, input_data: Any) -> float:
        payload = _normalize_input(input_data)
        solution = _parse_solution(candidate)
        if solution is None:
            return 0.0
        x_val, y_val = solution
        if _residual_ok(payload["equations"], x_val, y_val):
            return 1.0
        residual = _residual_sum(payload["equations"], x_val, y_val)
        closeness = max(0.0, 1.0 - min(residual, 50.0) / 50.0)
        return round(0.2 + 0.8 * closeness, 6)

    def available_tools(self) -> Mapping[str, Callable[[str, Any], str]]:
        return {
            "solve2": self._tool_solve2,
            "check_xy": self._tool_check_xy,
        }

    def _tool_solve2(self, tool_input: str, input_data: Any) -> str:
        del tool_input
        payload = _normalize_input(input_data)
        (a, b, c), (d, e, f_val) = payload["equations"]
        det = (a * e) - (b * d)
        if abs(det) < 1e-12:
            return "error: singular system"
        x_val = ((c * e) - (b * f_val)) / det
        y_val = ((a * f_val) - (c * d)) / det
        return f"x={x_val:.6f},y={y_val:.6f}"

    def _tool_check_xy(self, tool_input: str, input_data: Any) -> str:
        payload = _normalize_input(input_data)
        solution = _parse_solution(tool_input)
        if solution is None:
            return "error: expected x=<value>,y=<value>"
        x_val, y_val = solution
        if _residual_ok(payload["equations"], x_val, y_val):
            return "match"
        return f"residual={_residual_sum(payload['equations'], x_val, y_val):.6f}"


def _normalize_input(input_data: Any) -> dict[str, Any]:
    if not isinstance(input_data, dict):
        raise RuntimeError("LinearSystem2Task input_data must be an object")
    equations = input_data.get("equations")
    if not isinstance(equations, list) or len(equations) != 2:
        raise RuntimeError("LinearSystem2Task equations must be length-2 list")
    parsed: list[tuple[float, float, float]] = []
    for idx, row in enumerate(equations):
        if not isinstance(row, list) or len(row) != 3:
            raise RuntimeError(f"LinearSystem2Task equation[{idx}] must contain 3 numeric values")
        a, b, c = row
        parsed.append((float(a), float(b), float(c)))
    return {"equations": parsed}


def _parse_solution(raw: str) -> tuple[float, float] | None:
    text = raw.strip()
    if text.upper().startswith("FINAL:"):
        text = text.split(":", 1)[1].strip()

    x_match = re.search(r"x\s*=\s*([-+]?\d*\.?\d+)", text, flags=re.IGNORECASE)
    y_match = re.search(r"y\s*=\s*([-+]?\d*\.?\d+)", text, flags=re.IGNORECASE)
    if x_match and y_match:
        try:
            return float(x_match.group(1)), float(y_match.group(1))
        except ValueError:
            return None

    matches = re.findall(r"[-+]?\d*\.?\d+", text)
    if len(matches) >= 2:
        try:
            return float(matches[0]), float(matches[1])
        except ValueError:
            return None
    return None


def _residual_sum(equations: list[tuple[float, float, float]], x_val: float, y_val: float) -> float:
    residual = 0.0
    for a, b, c in equations:
        residual += abs((a * x_val) + (b * y_val) - c)
    return residual


def _residual_ok(equations: list[tuple[float, float, float]], x_val: float, y_val: float) -> bool:
    if not math.isfinite(x_val) or not math.isfinite(y_val):
        return False
    return _residual_sum(equations, x_val, y_val) < 1e-6
