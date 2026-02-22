"""Runnable built-in tool stand-ins used by the manuscript examples."""

from __future__ import annotations

import ast
import operator as op


class DuckDuckGoSearchTool:
    def __call__(self, query: str) -> str:
        return f"duckduckgo:{query}"


class WikipediaSearchTool:
    def __call__(self, query: str) -> str:
        return f"wikipedia:{query}"


class VisitWebpageTool:
    def __call__(self, url: str) -> str:
        return f"visited:{url}"


def _safe_eval(node):
    operators = {
        ast.Add: op.add,
        ast.Sub: op.sub,
        ast.Mult: op.mul,
        ast.Div: op.truediv,
        ast.Pow: op.pow,
        ast.USub: op.neg,
        ast.UAdd: op.pos,
    }
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name) and node.func.id == "sum":
            args = [_safe_eval(arg) for arg in node.args]
            return sum(args[0])
        if isinstance(node.func, ast.Name) and node.func.id == "range":
            args = [_safe_eval(arg) for arg in node.args]
            return range(*args)
        raise ValueError("Unsupported function call")
    if isinstance(node, ast.BinOp):
        return operators[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))
    if isinstance(node, ast.UnaryOp):
        return operators[type(node.op)](_safe_eval(node.operand))
    raise ValueError("Unsupported expression")


class PythonInterpreterTool:
    """Minimal safe arithmetic/python expression executor."""

    def __call__(self, expression: str) -> float:
        parsed = ast.parse(expression, mode="eval")
        return float(_safe_eval(parsed.body))
