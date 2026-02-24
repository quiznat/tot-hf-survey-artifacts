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

    def extract_final_answer(self, raw_output: str) -> str:
        direct = super().extract_final_answer(raw_output).strip()

        # Strong signal for Game24: equations that explicitly conclude with 24.
        lines = [line.strip() for line in raw_output.splitlines() if line.strip()]
        for line in reversed(lines):
            if "=" not in line:
                continue
            left, right = line.split("=", 1)
            if not re.search(r"\b24(?:\.0+)?\b", right):
                continue
            candidate = _normalize_expression(left)
            if _looks_like_expression(candidate):
                return candidate
            for chunk in re.findall(r"[\d\(\)\+\-\*/\.\s]{5,}", left):
                chunk_candidate = _normalize_expression(chunk)
                if _looks_like_expression(chunk_candidate):
                    return chunk_candidate

        candidates = _extract_expression_candidates(raw_output)
        best = _select_best_expression(candidates)
        if best:
            return best
        normalized_direct = _normalize_expression(direct)
        if _looks_like_expression(normalized_direct):
            return normalized_direct
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
            + "\n\nGenerate candidate arithmetic expressions that use each provided number exactly once."
            + f"\nReturn up to {branch_factor} candidates, one per line."
            + "\nOutput only raw expressions using + - * / and parentheses."
            + "\nDo not include '=', explanations, or words."
        )
        blocked = [candidate for candidate in (disallowed_candidates or []) if candidate]
        if blocked:
            prompt += "\nDo not repeat any of these previously explored candidates:\n"
            prompt += "\n".join(f"- {candidate}" for candidate in blocked)
        if attempt > 0:
            prompt += "\nPrevious candidates repeated; generate distinct alternatives."
        return prompt

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


def _looks_like_expression(expr: str) -> bool:
    if not _safe_expression(expr):
        return False
    if len(re.findall(r"\d+", expr)) < 2:
        return False
    return bool(re.search(r"[\+\-\*/]", expr))


def _normalize_expression(raw: str) -> str:
    expr = raw.strip()

    # Remove common markdown/LaTeX wrappers.
    expr = expr.replace("$", "")
    expr = expr.replace("\\left", "").replace("\\right", "")
    expr = expr.replace("\\(", "(").replace("\\)", ")")

    # Convert LaTeX-style operators to arithmetic symbols.
    expr = expr.replace("\\times", "*")
    expr = expr.replace("\\cdot", "*")
    expr = expr.replace("\\div", "/")

    # Convert simple LaTeX fractions: \frac{a}{b} -> (a)/(b)
    # Repeat to handle multiple fractions in one expression.
    frac_pattern = re.compile(r"\\frac\s*\{([^{}]+)\}\s*\{([^{}]+)\}")
    while True:
        updated = frac_pattern.sub(r"(\1)/(\2)", expr)
        if updated == expr:
            break
        expr = updated

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

    # Remove leftover LaTeX command prefixes and braces.
    expr = expr.replace("{", "(").replace("}", ")")
    expr = expr.replace("\\", "")

    return expr


def _extract_expression_candidates(raw_output: str) -> list[str]:
    candidates: list[str] = []
    lines = [line.strip() for line in raw_output.splitlines() if line.strip()]

    for line in lines:
        text = line
        text = re.sub(r"^\*+\s*", "", text)
        text = re.sub(r"^\d+\s*[\)\.\-:]\s*", "", text)
        if ":" in text:
            prefix, rest = text.split(":", 1)
            if prefix.strip().lower() in {"final", "answer", "result", "expression"}:
                text = rest.strip()
        if "=" in text:
            left, right = text.split("=", 1)
            # Keep the side that looks more expression-like.
            if re.search(r"[\+\-\*/\(\)]", left) and re.search(r"\d", left):
                text = left.strip()
            elif re.search(r"[\+\-\*/\(\)]", right) and re.search(r"\d", right):
                text = right.strip()

        variants = [text]
        for chunk in re.findall(r"[\d\(\)\+\-\*/\.\s]{5,}", text):
            variants.append(chunk.strip())
        for variant in variants:
            normalized = _normalize_expression(variant)
            if _looks_like_expression(normalized):
                candidates.append(normalized)

    # Backtick/code candidates often hold the intended final expression.
    for match in re.finditer(r"`([^`]+)`", raw_output):
        normalized = _normalize_expression(match.group(1))
        if _looks_like_expression(normalized):
            candidates.append(normalized)

    # Dedupe while preserving order.
    deduped: list[str] = []
    seen: set[str] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        deduped.append(candidate)
    return deduped


def _select_best_expression(candidates: list[str]) -> str:
    valid = [candidate for candidate in candidates if _looks_like_expression(candidate)]
    if not valid:
        return ""

    def _rank(expr: str) -> tuple[int, int, int, int]:
        op_count = len(re.findall(r"[\+\-\*/]", expr))
        num_count = len(re.findall(r"\d+", expr))
        paren_count = expr.count("(") + expr.count(")")
        return (op_count, num_count, paren_count, len(expr))

    return max(valid, key=_rank)
