"""Runnable transparency/explanation helpers for Section 6.4.1."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SelectedPath:
    justification: str


@dataclass
class Result:
    selected_path: SelectedPath


def format_tree(search_tree: list[str]) -> str:
    return "\n".join(f"- {node}" for node in search_tree)


def format_rejected_paths(search_tree: list[str]) -> str:
    rejected = search_tree[1:] if len(search_tree) > 1 else []
    return "\n".join(f"- {node}" for node in rejected) or "- none"


def explain_decision(task: str, search_tree: list[str], result: Result) -> str:
    """Generate a readable explanation from a ToT-like trace."""
    return f"""
Decision Process for: {task}

Alternative paths considered:
{format_tree(search_tree)}

Selected path reasoning:
{result.selected_path.justification}

Rejected alternatives and why:
{format_rejected_paths(search_tree)}
""".strip()
