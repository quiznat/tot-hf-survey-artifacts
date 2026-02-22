"""Base runner implementation shared across baseline strategies."""

from __future__ import annotations

from abc import ABC, abstractmethod
from time import perf_counter
from typing import Any, Dict

from ..interfaces import BenchmarkTask, ModelAdapter
from ..manifest import generate_run_id, utc_now_iso
from ..metrics import estimate_cost_usd
from ..models import Budget, PricingConfig, RunMetrics, RunnerExecution, SearchConfig


class BaseRunner(ABC):
    """Shared runner flow for prepare-run-result lifecycle."""

    runner_id = "base"

    def __init__(self, model: ModelAdapter, model_name: str, provider: str = "local", framework: str = "phase2-baselines@0.1") -> None:
        self.model = model
        self.model_name = model_name
        self.provider = provider
        self.framework = framework
        self.task: BenchmarkTask | None = None
        self.config: Dict[str, Any] = {}
        self._last_manifest: Dict[str, Any] | None = None

    def prepare(self, task: BenchmarkTask, config: Dict[str, Any]) -> None:
        self.task = task
        self.config = dict(config)

    def run(self, input_data: Any) -> Dict[str, Any]:
        if self.task is None:
            raise RuntimeError("Runner not prepared. Call prepare(task, config) first.")

        start = perf_counter()
        execution = self._execute(input_data)
        latency_ms = int((perf_counter() - start) * 1000)

        pricing = PricingConfig(
            input_per_1k=float(self.config.get("price_input_per_1k", 0.0)),
            output_per_1k=float(self.config.get("price_output_per_1k", 0.0)),
        )
        metrics = RunMetrics(
            success=1 if execution.outcome == "success" else 0,
            latency_ms=latency_ms,
            tokens_in=execution.tokens_in,
            tokens_out=execution.tokens_out,
            cost_usd=estimate_cost_usd(execution.tokens_in, execution.tokens_out, pricing),
        )

        budget = Budget(**self.config.get("budget", {}))
        search_cfg = SearchConfig(**self.config.get("search_config", {}))

        manifest: Dict[str, Any] = {
            "run_id": self.config.get("run_id", generate_run_id(prefix=self.runner_id.upper())),
            "timestamp_utc": utc_now_iso(),
            "task_id": self.task.task_id,
            "condition_id": self.config.get("condition_id", self.runner_id),
            "model_name": self.model_name,
            "provider": self.provider,
            "agent_framework": self.framework,
            "prompt_template_version": self.config.get("prompt_template_version", "v0"),
            "search_config": {
                "depth": search_cfg.depth,
                "breadth": search_cfg.breadth,
                "pruning": search_cfg.pruning,
                "stop_policy": search_cfg.stop_policy,
            },
            "tool_config": self.config.get("tool_config", []),
            "seed": self.config.get("seed"),
            "budget": {
                "token_budget": budget.token_budget,
                "time_budget_ms": budget.time_budget_ms,
                "cost_budget_usd": budget.cost_budget_usd,
            },
            "outcome": execution.outcome,
            "metrics": {
                "success": metrics.success,
                "latency_ms": metrics.latency_ms,
                "tokens_in": metrics.tokens_in,
                "tokens_out": metrics.tokens_out,
                "cost_usd": metrics.cost_usd,
            },
            "artifact_paths": self.config.get("artifact_paths", []),
            "notes": execution.notes,
            "final_answer": execution.final_answer,
            "trace": execution.trace,
        }
        if "item_id" in self.config:
            manifest["item_id"] = self.config["item_id"]
        if "input_data" in self.config:
            manifest["input_data"] = self.config["input_data"]
        if "panel_id" in self.config:
            manifest["panel_id"] = self.config["panel_id"]
        for key in (
            "evaluator_mode",
            "max_depth",
            "branch_factor",
            "frontier_width",
            "max_steps",
            "cot_sc_samples",
            "hf_temperature",
            "hf_top_p",
            "react_enable_tools",
            "capability_parity_policy",
            "task_tools_available",
            "condition_tools_exposed",
        ):
            if key in self.config:
                manifest[key] = self.config[key]
        if execution.extra:
            manifest["extra"] = execution.extra
        if execution.error_type:
            manifest["error_type"] = execution.error_type

        self._last_manifest = manifest
        return manifest

    def result(self) -> Dict[str, Any]:
        if self._last_manifest is None:
            raise RuntimeError("No run result available. Call run() first.")
        return self._last_manifest

    @abstractmethod
    def _execute(self, input_data: Any) -> RunnerExecution:
        """Run strategy-specific execution and return raw execution details."""
