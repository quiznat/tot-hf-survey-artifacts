"""Runnable tool examples adapted from Section 3.6 of the manuscript."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import Callable, Optional


# Minimal local stand-in for smolagents' @tool decorator.
def tool(func: Callable) -> Callable:
    func.is_tool = True  # type: ignore[attr-defined]
    return func


@tool
def fetch_stock_price(ticker: str, date: Optional[str] = None) -> str:
    """Fetch demo stock price data for a ticker/date pair."""
    current = {
        "AAPL": "$175.50",
        "MSFT": "$412.20",
        "GOOGL": "$188.10",
    }
    historical = {
        ("AAPL", "2025-01-15"): "$184.63",
        ("MSFT", "2025-01-15"): "$389.70",
    }

    if date is not None:
        return historical.get((ticker.upper(), date), "Price data not available")
    return current.get(ticker.upper(), "Price data not available")


def fetch_url(url: str) -> str:
    if not url.startswith(("http://", "https://")):
        raise ValueError("URL must start with http:// or https://")
    return f"<html><body>{url} :: Demo content for testing.</body></html>"


def extract_text(content: str) -> str:
    return content.replace("<html><body>", "").replace("</body></html>", "")


def summarize(text: str, limit: int = 64) -> str:
    compact = " ".join(text.split())
    return compact[:limit] + ("..." if len(compact) > limit else "")


@tool
def analyze_website(url: str) -> str:
    """Analyze a website and return key information (demo flow)."""
    content = fetch_url(url)
    text = extract_text(content)
    return summarize(text)


def news_search(query: str, days: int = 7) -> str:
    return f"news({days}d): {query}"


def web_search(query: str) -> str:
    return f"web: {query}"


@tool
def smart_search(query: str, require_recent: bool = False) -> str:
    """Search with conditional logic."""
    if require_recent:
        return news_search(query, days=7)
    return web_search(query)


@dataclass
class DatabaseTool:
    """Stateful SQLite-backed demo tool."""

    connection: sqlite3.Connection | None = None

    def connect(self) -> None:
        self.connection = sqlite3.connect(":memory:")
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS sample (id INTEGER PRIMARY KEY, name TEXT)"
        )
        self.connection.execute(
            "INSERT INTO sample (name) VALUES ('alice'), ('bob')"
        )
        self.connection.commit()

    @tool
    def query(self, sql: str) -> str:
        """Execute SQL query on connected database."""
        if self.connection is None:
            self.connect()
        rows = self.connection.execute(sql).fetchall()
        return str(rows)

    @tool
    def schema(self) -> str:
        """Return database schema."""
        return self.get_schema()

    def get_schema(self) -> str:
        if self.connection is None:
            self.connect()
        row = self.connection.execute(
            "SELECT sql FROM sqlite_master WHERE type='table' AND name='sample'"
        ).fetchone()
        return row[0] if row else ""


def fetch_stock_price_schema() -> dict:
    """Representative schema object for fetch_stock_price."""
    return {
        "name": "fetch_stock_price",
        "description": "Fetch the current or historical stock price...",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The stock ticker symbol...",
                },
                "date": {
                    "type": "string",
                    "description": "Optional date in YYYY-MM-DD format...",
                },
            },
            "required": ["ticker"],
        },
    }
