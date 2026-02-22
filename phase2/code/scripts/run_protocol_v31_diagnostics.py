#!/usr/bin/env python3
"""Run protocol-v3.1 diagnostics focused on task-dependent ToT vs ReAct behavior."""

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
    "linear2-demo": ROOT / "benchmarks/panels/linear2_lockset_v1.json",
    "digit-permutation-demo": ROOT / "benchmarks/panels/digit_permutation_lockset_v1.json",
}

MODEL_DEFAULT = [
    "Qwen/Qwen3-Coder-Next:novita",
    "Qwen/Qwen2.5-72B-Instruct",
    "Qwen/Qwen2.5-Coder-32B-Instruct",
]

PROFILE_CONFIG: Dict[str, Dict[str, object]] = {
    "tot_model_self_eval": {
        "conditions": "react,tot",
        "tot_evaluator_mode": "model_self_eval",
        "tot_max_depth": 3,
        "tot_branch_factor": 3,
        "tot_frontier_width": 3,
    },
    "tot_hybrid": {
        "conditions": "react,tot",
        "tot_evaluator_mode": "hybrid",
        "tot_max_depth": 3,
        "tot_branch_factor": 3,
        "tot_frontier_width": 3,
    },
    "tot_rule_based": {
        "conditions": "react,tot",
        "tot_evaluator_mode": "rule_based",
        "tot_max_depth": 3,
        "tot_branch_factor": 3,
        "tot_frontier_width": 3,
    },
    "tot_model_self_eval_lite": {
        "conditions": "react,tot",
        "tot_evaluator_mode": "model_self_eval",
        "tot_max_depth": 2,
        "tot_branch_factor": 2,
        "tot_frontier_width": 2,
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run protocol-v3.1 diagnostic matrix")
    parser.add_argument(
        "--tasks",
        default="linear2-demo,digit-permutation-demo",
        help="Comma-separated task IDs",
    )
    parser.add_argument(
        "--models",
        default=",".join(MODEL_DEFAULT),
        help="Comma-separated model IDs (no fallback allowed)",
    )
    parser.add_argument(
        "--profiles",
        default="tot_model_self_eval,tot_hybrid,tot_rule_based,tot_model_self_eval_lite",
        help="Comma-separated profile IDs",
    )
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--max-workers", type=int, default=8)
    parser.add_argument("--hf-timeout-seconds", type=int, default=180)
    parser.add_argument("--hf-temperature", type=float, default=0.0)
    parser.add_argument("--hf-top-p", type=float, default=1.0)
    parser.add_argument("--seed-policy", default="item_hash")
    parser.add_argument("--bootstrap-samples", type=int, default=10000)
    parser.add_argument("--confidence-level", type=float, default=0.95)
    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Continue executing subsequent blocks if one block fails.",
    )
    parser.add_argument("--report-only", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def _slug(text: str) -> str:
    return text.replace("/", "_").replace(":", "_").replace(".", "_").replace("-", "_").lower()


def _utcstamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _build_command(task_id: str, model_id: str, profile_id: str, args: argparse.Namespace) -> List[str]:
    panel_file = PANEL_MAP.get(task_id)
    if panel_file is None:
        raise RuntimeError(f"No panel mapping configured for task: {task_id}")
    if not panel_file.exists():
        raise RuntimeError(f"Panel file missing for task {task_id}: {panel_file}")
    if profile_id not in PROFILE_CONFIG:
        raise RuntimeError(f"Unknown profile: {profile_id}")

    cfg = PROFILE_CONFIG[profile_id]
    task_slug = _slug(task_id)
    model_slug = _slug(model_id)

    runs_dir = ROOT / "benchmarks/runs/protocol_v31_diagnostic" / task_slug / model_slug / profile_id
    report_md = ROOT / "benchmarks/analysis" / f"{task_slug}_diag_report_{model_slug}_{profile_id}_v31.md"
    report_json = ROOT / "benchmarks/analysis" / f"{task_slug}_diag_report_{model_slug}_{profile_id}_v31.json"
    run_log = ROOT / "reproducibility/run-log-protocol-v31.md"

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
        str(cfg["conditions"]),
        "--tot-evaluator-mode",
        str(cfg["tot_evaluator_mode"]),
        "--tot-max-depth",
        str(cfg["tot_max_depth"]),
        "--tot-branch-factor",
        str(cfg["tot_branch_factor"]),
        "--tot-frontier-width",
        str(cfg["tot_frontier_width"]),
        "--hf-temperature",
        str(args.hf_temperature),
        "--hf-top-p",
        str(args.hf_top_p),
        "--hf-timeout-seconds",
        str(args.hf_timeout_seconds),
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
    profiles = [p.strip() for p in args.profiles.split(",") if p.strip()]

    if not tasks:
        raise RuntimeError("No tasks selected")
    if not models:
        raise RuntimeError("No models selected")
    if not profiles:
        raise RuntimeError("No profiles selected")

    unknown_profiles = [p for p in profiles if p not in PROFILE_CONFIG]
    if unknown_profiles:
        raise RuntimeError(f"Unknown profile(s): {unknown_profiles}")

    print(f"protocol_v31_diagnostics_start={_utcstamp()}")
    print(f"tasks={tasks}")
    print(f"models={models}")
    print(f"profiles={profiles}")
    print(f"report_only={args.report_only} dry_run={args.dry_run}")
    print(f"continue_on_error={args.continue_on_error}")

    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "code/src")

    failures: List[Dict[str, str | int]] = []

    for task_id in tasks:
        for model_id in models:
            for profile_id in profiles:
                cfg = PROFILE_CONFIG[profile_id]
                cmd = _build_command(task_id=task_id, model_id=model_id, profile_id=profile_id, args=args)
                print("\n### EXEC")
                print(f"profile={profile_id} config={cfg}")
                print(" ".join(cmd))
                if args.dry_run:
                    continue
                proc = subprocess.run(cmd, env=env, cwd=str(ROOT), check=False)
                if proc.returncode != 0:
                    error_msg = "error: task={task} model={model} profile={profile} returncode={code}".format(
                        task=task_id,
                        model=model_id,
                        profile=profile_id,
                        code=proc.returncode,
                    )
                    print(error_msg)
                    failures.append(
                        {
                            "task_id": task_id,
                            "model_id": model_id,
                            "profile_id": profile_id,
                            "returncode": proc.returncode,
                        }
                    )
                    if not args.continue_on_error:
                        return proc.returncode

    print(f"protocol_v31_diagnostics_done={_utcstamp()}")
    if failures:
        print("protocol_v31_diagnostics_failures={count}".format(count=len(failures)))
        for failure in failures:
            print(
                "failure_block task={task} model={model} profile={profile} returncode={code}".format(
                    task=failure["task_id"],
                    model=failure["model_id"],
                    profile=failure["profile_id"],
                    code=failure["returncode"],
                )
            )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
