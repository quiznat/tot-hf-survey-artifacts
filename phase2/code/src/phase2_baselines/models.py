"""Typed data models for runner configuration and execution."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class Budget:
    """Run budget constraints."""

    token_budget: int = 0
    time_budget_ms: int = 0
    cost_budget_usd: float = 0.0


@dataclass
class SearchConfig:
    """Search configuration for manifest compatibility."""

    depth: int = 0
    breadth: int = 0
    pruning: str = "none"
    stop_policy: str = "default"


@dataclass
class PricingConfig:
    """Token pricing model for cost estimates."""

    input_per_1k: float = 0.0
    output_per_1k: float = 0.0


@dataclass
class RunMetrics:
    """Metrics tracked for each execution."""

    success: int
    latency_ms: int
    tokens_in: int
    tokens_out: int
    cost_usd: float


@dataclass
class RunnerExecution:
    """Raw execution result before manifest assembly."""

    outcome: str
    final_answer: str
    notes: str = ""
    trace: List[str] = field(default_factory=list)
    tokens_in: int = 0
    tokens_out: int = 0
    error_type: str | None = None
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ThoughtNode:
    """Node in the ToT search tree."""

    node_id: str
    parent_id: str | None
    depth: int
    candidate: str
    score: float
    cumulative_score: float
    is_terminal: bool = False


@dataclass
class SearchSummary:
    """Compact summary of a ToT search run."""

    max_depth: int
    branch_factor: int
    frontier_width: int
    expanded_nodes: int = 0
    generated_nodes: int = 0
    terminal_nodes: int = 0
    peak_frontier_size: int = 0
    stop_reason: str = ""
