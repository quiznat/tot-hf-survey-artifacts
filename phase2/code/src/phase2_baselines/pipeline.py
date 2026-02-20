"""Reusable baseline execution pipeline utilities."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Tuple

from .adapters import ScriptedModel
from .manifest import append_run_log, write_manifest
from .runners import ReactRunner, SinglePathRunner
from .tasks import Arithmetic24Task


def create_baseline_setup(runner_name: str, seed: int = 0) -> Tuple[Any, Arithmetic24Task, Dict[str, Any]]:
    """Create runner, task, and config for a named baseline condition."""
    task = Arithmetic24Task()

    if runner_name == "single":
        model = ScriptedModel(responses=["(10*10-4)/4"])
        runner = SinglePathRunner(model=model, model_name="scripted-single-v1")
        config = {
            "condition_id": "baseline-single-path",
            "prompt_template_version": "v1",
            "search_config": {"depth": 0, "breadth": 0, "pruning": "none", "stop_policy": "single-pass"},
            "tool_config": [],
            "budget": {"token_budget": 2000, "time_budget_ms": 10000, "cost_budget_usd": 0.0},
            "seed": seed,
        }
        return runner, task, config

    if runner_name == "react":
        model = ScriptedModel(
            responses=[
                "THINK: I should test a candidate expression with calc.",
                "ACTION: calc (10*10-4)/4",
                "FINAL: (10*10-4)/4",
            ]
        )
        runner = ReactRunner(model=model, model_name="scripted-react-v1")
        config = {
            "condition_id": "baseline-react",
            "prompt_template_version": "v1",
            "search_config": {"depth": 1, "breadth": 1, "pruning": "none", "stop_policy": "max_steps_or_final"},
            "tool_config": ["calc"],
            "budget": {"token_budget": 3000, "time_budget_ms": 12000, "cost_budget_usd": 0.0},
            "seed": seed,
            "max_steps": 5,
        }
        return runner, task, config

    raise ValueError(f"Unsupported runner_name: {runner_name}")


def execute_and_record(
    runner_name: str,
    input_numbers: List[int],
    runs_dir: Path,
    run_log: Path,
    seed: int = 0,
) -> Dict[str, Any]:
    """Run one baseline condition and persist its manifest artifacts."""
    runner, task, config = create_baseline_setup(runner_name=runner_name, seed=seed)
    runner.prepare(task=task, config=config)
    manifest = runner.run(input_numbers)

    out_path = runs_dir / f"{manifest['run_id']}.json"
    manifest["artifact_paths"].append(str(out_path))
    write_manifest(manifest, out_path)
    append_run_log(run_log, manifest)

    return manifest
