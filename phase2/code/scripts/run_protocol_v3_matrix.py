#!/usr/bin/env python3
"""Orchestrate protocol-v3 matrix execution across tasks and models."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import os
from pathlib import Path
import subprocess
from typing import Dict, List


ROOT = Path("/Users/quiznat/Desktop/Tree_of_Thought/phase2")
RUN_SCRIPT = ROOT / "code/scripts/run_structured_lockset.py"

PANEL_MAP = {
    "game24-demo": ROOT / "benchmarks/panels/game24_lockset_v1.json",
    "subset-sum-demo": ROOT / "benchmarks/panels/subset_sum_lockset_v1.json",
    "linear2-demo": ROOT / "benchmarks/panels/linear2_lockset_v1.json",
    "digit-permutation-demo": ROOT / "benchmarks/panels/digit_permutation_lockset_v1.json",
}

MODEL_DEFAULT = [
    "Qwen/Qwen3-Coder-Next:novita",
    "Qwen/Qwen2.5-72B-Instruct",
    "Qwen/Qwen2.5-Coder-32B-Instruct",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run protocol-v3 task/model matrix")
    parser.add_argument(
        "--tasks",
        default="game24-demo,subset-sum-demo,linear2-demo,digit-permutation-demo",
        help="Comma-separated task IDs",
    )
    parser.add_argument(
        "--models",
        default=",".join(MODEL_DEFAULT),
        help="Comma-separated model IDs (no fallback allowed)",
    )
    parser.add_argument("--conditions", default="single,react,tot")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--max-workers", type=int, default=8)
    parser.add_argument("--tot-evaluator-mode", default="model_self_eval")
    parser.add_argument("--tot-max-depth", type=int, default=3)
    parser.add_argument("--tot-branch-factor", type=int, default=3)
    parser.add_argument("--tot-frontier-width", type=int, default=3)
    parser.add_argument("--hf-temperature", type=float, default=0.0)
    parser.add_argument("--hf-top-p", type=float, default=1.0)
    parser.add_argument("--seed-policy", default="item_hash")
    parser.add_argument("--bootstrap-samples", type=int, default=10000)
    parser.add_argument("--confidence-level", type=float, default=0.95)
    parser.add_argument("--report-only", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def _slug(text: str) -> str:
    return text.replace("/", "_").replace(":", "_").replace(".", "_").replace("-", "_").lower()


def _utcstamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _build_command(task_id: str, model_id: str, args: argparse.Namespace) -> List[str]:
    panel_file = PANEL_MAP.get(task_id)
    if panel_file is None:
        raise RuntimeError(f"No panel mapping configured for task: {task_id}")
    if not panel_file.exists():
        raise RuntimeError(f"Panel file missing for task {task_id}: {panel_file}")

    task_slug = _slug(task_id)
    model_slug = _slug(model_id)
    runs_dir = ROOT / "benchmarks/runs/protocol_v3_matrix" / task_slug / model_slug
    report_md = ROOT / "benchmarks/analysis" / f"{task_slug}_lockset_report_{model_slug}_v3.md"
    report_json = ROOT / "benchmarks/analysis" / f"{task_slug}_lockset_report_{model_slug}_v3.json"
    run_log = ROOT / "reproducibility/run-log-protocol-v3.md"

    cmd = [
        "python3",
        str(RUN_SCRIPT),
        "--task-id",
        task_id,
        "--panel-file",
        str(panel_file),
        "--provider",
        "hf",
        "--model-id",
        model_id,
        "--conditions",
        args.conditions,
        "--tot-evaluator-mode",
        args.tot_evaluator_mode,
        "--tot-max-depth",
        str(args.tot_max_depth),
        "--tot-branch-factor",
        str(args.tot_branch_factor),
        "--tot-frontier-width",
        str(args.tot_frontier_width),
        "--hf-temperature",
        str(args.hf_temperature),
        "--hf-top-p",
        str(args.hf_top_p),
        "--seed-policy",
        args.seed_policy,
        "--limit",
        str(args.limit),
        "--max-workers",
        str(args.max_workers),
        "--confidence-level",
        str(args.confidence_level),
        "--bootstrap-samples",
        str(args.bootstrap_samples),
        "--runs-dir",
        str(runs_dir),
        "--run-log",
        str(run_log),
        "--report-md",
        str(report_md),
        "--report-json",
        str(report_json),
    ]
    if args.report_only:
        cmd.append("--report-only")
    return cmd


def main() -> int:
    args = parse_args()
    tasks = [t.strip() for t in args.tasks.split(",") if t.strip()]
    models = [m.strip() for m in args.models.split(",") if m.strip()]
    if not tasks:
        raise RuntimeError("No tasks selected")
    if not models:
        raise RuntimeError("No models selected")

    print(f"protocol_v3_matrix_start={_utcstamp()}")
    print(f"tasks={tasks}")
    print(f"models={models}")
    print(f"report_only={args.report_only} dry_run={args.dry_run}")

    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "code/src")

    for task_id in tasks:
        for model_id in models:
            cmd = _build_command(task_id=task_id, model_id=model_id, args=args)
            print("\n### EXEC")
            print(" ".join(cmd))
            if args.dry_run:
                continue
            proc = subprocess.run(cmd, env=env, cwd=str(ROOT), check=False)
            if proc.returncode != 0:
                print(f"error: task={task_id} model={model_id} returncode={proc.returncode}")
                return proc.returncode

    print(f"protocol_v3_matrix_done={_utcstamp()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
