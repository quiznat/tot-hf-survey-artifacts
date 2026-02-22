#!/usr/bin/env python3
"""Run protocol-v4 smoke checks across all tasks with strict frozen settings."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import os
from pathlib import Path
import subprocess
import time
from typing import List


ROOT = Path("/Users/quiznat/Desktop/Tree_of_Thought/phase2")
RUN_SCRIPT = ROOT / "code/scripts/run_structured_lockset.py"

PANEL_MAP = {
    "game24-demo": ROOT / "benchmarks/panels/game24_lockset_v4.json",
    "subset-sum-demo": ROOT / "benchmarks/panels/subset_sum_lockset_v4.json",
    "linear2-demo": ROOT / "benchmarks/panels/linear2_lockset_v4.json",
    "digit-permutation-demo": ROOT / "benchmarks/panels/digit_permutation_lockset_v4.json",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run protocol-v4 smoke matrix")
    parser.add_argument(
        "--tasks",
        default="game24-demo,subset-sum-demo,linear2-demo,digit-permutation-demo",
        help="Comma-separated task IDs",
    )
    parser.add_argument("--model-id", default="Qwen/Qwen3-Coder-Next:novita")
    parser.add_argument("--conditions", default="single,react,tot")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--max-workers", type=int, default=8)
    parser.add_argument("--tot-evaluator-mode", default="model_self_eval")
    parser.add_argument("--tot-max-depth", type=int, default=3)
    parser.add_argument("--tot-branch-factor", type=int, default=3)
    parser.add_argument("--tot-frontier-width", type=int, default=3)
    parser.add_argument("--hf-timeout-seconds", type=int, default=180)
    parser.add_argument("--hf-temperature", type=float, default=0.0)
    parser.add_argument("--hf-top-p", type=float, default=1.0)
    parser.add_argument(
        "--capability-parity-policy",
        choices=["equalize_react_to_tot", "strict"],
        default="equalize_react_to_tot",
        help="Protocol-v4 requires matched capability exposure in paired comparisons.",
    )
    parser.add_argument("--seed-policy", default="item_hash")
    parser.add_argument("--bootstrap-samples", type=int, default=10000)
    parser.add_argument("--confidence-level", type=float, default=0.95)
    parser.add_argument(
        "--series-id",
        default="protocol_v4_smoke",
        help="Runs subdirectory under phase2/benchmarks/runs/",
    )
    parser.add_argument(
        "--report-tag",
        default="v4",
        help="Suffix tag for report file naming.",
    )
    parser.add_argument(
        "--run-log",
        default=str(ROOT / "reproducibility/run-log-protocol-v4.md"),
        help="Run log path",
    )
    parser.add_argument(
        "--max-attempts-per-task",
        type=int,
        default=3,
        help="Bounded infrastructure retries per task command (1 disables retries).",
    )
    parser.add_argument(
        "--retry-backoff-seconds",
        type=int,
        default=20,
        help="Base retry backoff; delay grows exponentially per failed attempt.",
    )
    parser.add_argument("--report-only", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def _slug(text: str) -> str:
    return text.replace("/", "_").replace(":", "_").replace(".", "_").replace("-", "_").lower()


def _utcstamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _build_command(task_id: str, args: argparse.Namespace) -> List[str]:
    panel_file = PANEL_MAP.get(task_id)
    if panel_file is None:
        raise RuntimeError(f"No panel mapping configured for task: {task_id}")
    if not panel_file.exists():
        raise RuntimeError(f"Missing v4 panel file for task {task_id}: {panel_file}")

    task_slug = _slug(task_id)
    model_slug = _slug(args.model_id)

    runs_dir = ROOT / "benchmarks/runs" / args.series_id / task_slug / model_slug
    report_md = ROOT / "benchmarks/analysis" / f"{task_slug}_smoke_report_{model_slug}_{args.report_tag}.md"
    report_json = ROOT / "benchmarks/analysis" / f"{task_slug}_smoke_report_{model_slug}_{args.report_tag}.json"

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
        args.model_id,
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
        "--hf-timeout-seconds",
        str(args.hf_timeout_seconds),
        "--hf-temperature",
        str(args.hf_temperature),
        "--hf-top-p",
        str(args.hf_top_p),
        "--capability-parity-policy",
        args.capability_parity_policy,
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
        str(args.run_log),
        "--report-md",
        str(report_md),
        "--report-json",
        str(report_json),
    ]
    if args.report_only:
        cmd.append("--report-only")
    return cmd


def _run_with_retries(
    *,
    cmd: List[str],
    env: dict,
    cwd: Path,
    max_attempts: int,
    retry_backoff_seconds: int,
    label: str,
) -> int:
    attempts = max(1, int(max_attempts))
    base_backoff = max(0, int(retry_backoff_seconds))
    last_rc = 0
    for attempt in range(1, attempts + 1):
        print(f"run={label} attempt={attempt}/{attempts}")
        proc = subprocess.run(cmd, env=env, cwd=str(cwd), check=False)
        last_rc = int(proc.returncode)
        if last_rc == 0:
            return 0
        if attempt < attempts:
            wait_seconds = base_backoff * (2 ** (attempt - 1))
            print(
                f"warn: run={label} returncode={last_rc}; "
                f"retry_in={wait_seconds}s"
            )
            if wait_seconds > 0:
                time.sleep(wait_seconds)
    return last_rc


def main() -> int:
    args = parse_args()
    tasks = [task.strip() for task in args.tasks.split(",") if task.strip()]
    if not tasks:
        raise RuntimeError("No tasks selected")

    print(f"protocol_v4_smoke_start={_utcstamp()}")
    print(f"tasks={tasks}")
    print(f"model={args.model_id}")
    print(f"report_only={args.report_only} dry_run={args.dry_run}")
    print(f"capability_parity_policy={args.capability_parity_policy}")
    print(
        "retry_policy="
        f"max_attempts_per_task={args.max_attempts_per_task},"
        f"backoff_seconds={args.retry_backoff_seconds}"
    )

    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "code/src")

    for task_id in tasks:
        cmd = _build_command(task_id=task_id, args=args)
        print("\n### EXEC")
        print(" ".join(cmd))
        if args.dry_run:
            continue
        rc = _run_with_retries(
            cmd=cmd,
            env=env,
            cwd=ROOT,
            max_attempts=args.max_attempts_per_task,
            retry_backoff_seconds=args.retry_backoff_seconds,
            label=f"task={task_id}",
        )
        if rc != 0:
            print(f"error: task={task_id} returncode={rc}")
            return rc

    print(f"protocol_v4_smoke_done={_utcstamp()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
