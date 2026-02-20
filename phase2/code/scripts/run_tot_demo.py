#!/usr/bin/env python3
"""Run ToT prototype demo and emit a manifest artifact."""

from __future__ import annotations

import argparse
from pathlib import Path

from phase2_baselines.adapters import ScriptedModel
from phase2_baselines.manifest import append_run_log, write_manifest
from phase2_baselines.runners.tot import ToTRunner
from phase2_baselines.tasks import Arithmetic24Task


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run phase2 ToT prototype demo")
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
    model = ScriptedModel(
        responses=[
            "CANDIDATE: (10+4)+10+4\nCANDIDATE: (10*10-4)/4",
        ]
    )
    runner = ToTRunner(model=model, model_name="scripted-tot-v1")
    runner.prepare(
        task=task,
        config={
            "condition_id": "tot-prototype",
            "prompt_template_version": "v1",
            "search_config": {
                "depth": 3,
                "breadth": 3,
                "pruning": "topk_cumulative_score",
                "stop_policy": "first_terminal_or_depth_limit",
            },
            "tool_config": [],
            "budget": {"token_budget": 4000, "time_budget_ms": 15000, "cost_budget_usd": 0.0},
            "seed": 0,
            "max_depth": 3,
            "branch_factor": 3,
            "frontier_width": 3,
        },
    )

    manifest = runner.run(numbers)

    runs_dir = Path(args.runs_dir)
    out_path = runs_dir / f"{manifest['run_id']}.json"

    manifest["artifact_paths"].append(str(out_path))
    write_manifest(manifest, out_path)
    append_run_log(Path(args.run_log), manifest)

    print(f"run_id={manifest['run_id']}")
    print(f"outcome={manifest['outcome']}")
    print(f"manifest={out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
