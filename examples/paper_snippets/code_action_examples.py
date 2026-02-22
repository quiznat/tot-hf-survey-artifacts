"""Runnable code-as-action examples adapted from Section 3.4.1."""

from __future__ import annotations

import ast
import operator as op
from typing import Iterable


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
    if isinstance(node, ast.BinOp):
        return operators[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))
    if isinstance(node, ast.UnaryOp):
        return operators[type(node.op)](_safe_eval(node.operand))
    raise ValueError("Unsupported expression")


def calculator(expression: str) -> float:
    """Evaluate basic arithmetic expressions safely."""
    parsed = ast.parse(expression, mode="eval")
    return float(_safe_eval(parsed.body))


def search(query: str) -> list[dict]:
    return [
        {"source": "demo", "text": f"{query} day1 price 42000"},
        {"source": "demo", "text": f"{query} day2 price 43000"},
    ]


def parse_results(results: list[dict]) -> list[int]:
    prices = []
    for item in results:
        tokens = item["text"].split()
        for tok in tokens:
            if tok.isdigit():
                prices.append(int(tok))
    return prices


def create_chart(values: list[int], chart_type: str = "line") -> str:
    return f"{chart_type}-chart(points={len(values)}, min={min(values)}, max={max(values)})"


def summarize(chart: str) -> str:
    return f"Summary: {chart}"


def composable_pipeline(query: str) -> str:
    """Search, parse, chart, summarize pipeline."""
    results = search(query=query)
    values = parse_results(results)
    chart = create_chart(values, chart_type="line")
    return summarize(chart)


def get_stock_price(stock: str) -> float:
    mapping = {"AAPL": 175.5, "GOOGL": 188.1, "MSFT": 412.2}
    return mapping.get(stock, 0.0)


def alert(message: str) -> str:
    return message


def stock_alerts(stocks: Iterable[str], threshold: float = 100.0) -> list[str]:
    """Return alert messages for stocks above the threshold."""
    out: list[str] = []
    for stock in stocks:
        price = get_stock_price(stock)
        if price > threshold:
            out.append(alert(f"{stock} price alert: ${price}"))
    return out
