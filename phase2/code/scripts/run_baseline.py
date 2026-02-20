#!/usr/bin/env python3
"""Run local baseline scaffold and emit a manifest artifact."""

from __future__ import annotations

import argparse
from pathlib import Path

from phase2_baselines.adapters import ScriptedModel
from phase2_baselines.manifest import append_run_log, write_manifest
from phase2_baselines.runners import ReactRunner, SinglePathRunner
from phase2_baselines.tasks import Arithmetic24Task


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run phase2 baseline scaffold")
    parser.add_argument("--runner", choices=["single", "react"], default="single")
    parser.add_argument("--numbers", default="4,4,10,10", help="Comma-separated integers")
    parser.add_argument(
        "--runs-dir",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/runs",
        help="Directory for manifest outputs",
    )
    parser.add_argument(
        "--run-log",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/reproducibility/run-log.md",
        help="Markdown run log file",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    numbers = [int(part.strip()) for part in args.numbers.split(",") if part.strip()]

    task = Arithmetic24Task()

    if args.runner == "single":
        model = ScriptedModel(responses=["(10*10-4)/4"])
        runner = SinglePathRunner(model=model, model_name="scripted-single-v1")
        config = {
            "condition_id": "baseline-single-path",
            "prompt_template_version": "v1",
            "search_config": {"depth": 0, "breadth": 0, "pruning": "none", "stop_policy": "single-pass"},
            "tool_config": [],
            "budget": {"token_budget": 2000, "time_budget_ms": 10000, "cost_budget_usd": 0.0},
            "seed": 0,
        }
    else:
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
            "seed": 0,
            "max_steps": 5,
        }

    runner.prepare(task=task, config=config)
    manifest = runner.run(numbers)

    runs_dir = Path(args.runs_dir)
    out_path = runs_dir / f"{manifest['run_id']}.json"

    # Include manifest output path in artifact index before writing final record.
    manifest["artifact_paths"].append(str(out_path))
    write_manifest(manifest, out_path)

    append_run_log(Path(args.run_log), manifest)

    print(f"run_id={manifest['run_id']}")
    print(f"outcome={manifest['outcome']}")
    print(f"manifest={out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
