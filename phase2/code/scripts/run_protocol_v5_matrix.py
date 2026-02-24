#!/usr/bin/env python3
"""Run protocol-v5 base-pattern matrix with frozen task/model settings."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import os
from pathlib import Path
import subprocess
import sys
import time
from typing import List


ROOT = Path("/Users/quiznat/Desktop/Tree_of_Thought/phase2")
RUN_SCRIPT = ROOT / "code/scripts/run_structured_lockset.py"
DEFAULT_PYTHON_BIN = str(ROOT / ".venv311/bin/python") if (ROOT / ".venv311/bin/python").exists() else sys.executable

PANEL_MAP = {
    "game24-demo": ROOT / "benchmarks/panels/game24_lockset_v4.json",
    "subset-sum-demo": ROOT / "benchmarks/panels/subset_sum_lockset_v4.json",
    "linear2-demo": ROOT / "benchmarks/panels/linear2_lockset_v4.json",
    "digit-permutation-demo": ROOT / "benchmarks/panels/digit_permutation_lockset_v4.json",
}

MODEL_DEFAULT = [
    "Qwen/Qwen3-Coder-Next:novita",
    "Qwen/Qwen2.5-72B-Instruct",
    "Qwen/Qwen2.5-Coder-32B-Instruct",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run protocol-v5 base-pattern matrix")
    parser.add_argument(
        "--tasks",
        default="game24-demo,subset-sum-demo,linear2-demo,digit-permutation-demo",
        help="Comma-separated task IDs",
    )
    parser.add_argument(
        "--models",
        default=",".join(MODEL_DEFAULT),
        help="Comma-separated model IDs (no substitution in-run)",
    )
    parser.add_argument(
        "--provider",
        choices=["smolagents"],
        default="smolagents",
        help="Model backend for baseline and ToT lanes.",
    )
    parser.add_argument(
        "--python-bin",
        default=DEFAULT_PYTHON_BIN,
        help="Python executable used for launching run_structured_lockset.py.",
    )
    parser.add_argument(
        "--conditions",
        default=(
            "baseline_single_path_reasoning_only_v1,"
            "baseline_chain_of_thought_reasoning_only_v1,"
            "baseline_chain_of_thought_self_consistency_reasoning_only_v1,"
            "baseline_react_code_agent_with_task_tools_v1,"
            "baseline_tree_of_thoughts_search_reasoning_only_v1,"
            "baseline_tree_of_thoughts_generalized_recursive_reasoning_only_v1"
        ),
    )
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--max-workers", type=int, default=12)
    parser.add_argument("--tot-evaluator-mode", default="model_self_eval")
    parser.add_argument(
        "--tot-mode",
        choices=["model_decompose_search"],
        default="model_decompose_search",
    )
    parser.add_argument(
        "--tot-gen-mode",
        choices=["model_decompose_search"],
        default="model_decompose_search",
    )
    parser.add_argument("--tot-decomposition-rounds", type=int, default=1)
    parser.add_argument("--tot-max-depth", type=int, default=4)
    parser.add_argument(
        "--tot-legacy-max-depth",
        type=int,
        default=-1,
        help="Override legacy ToT depth. <=0 means follow --tot-max-depth.",
    )
    parser.add_argument(
        "--tot-gen-max-depth",
        type=int,
        default=-1,
        help="Override ToT-gen depth. <=0 means follow --tot-max-depth (parity default).",
    )
    parser.add_argument("--tot-branch-factor", type=int, default=3)
    parser.add_argument("--tot-frontier-width", type=int, default=3)
    parser.add_argument("--cot-sc-samples", type=int, default=10)
    parser.add_argument("--hf-timeout-seconds", type=int, default=180)
    parser.add_argument(
        "--hf-max-new-tokens",
        type=int,
        default=512,
        help="Generation cap per call. Raise for CoT/COT-SC to reduce truncation.",
    )
    parser.add_argument("--hf-temperature", type=float, default=0.0)
    parser.add_argument("--hf-top-p", type=float, default=1.0)
    parser.add_argument("--cot-temperature", type=float, default=0.0)
    parser.add_argument("--cot-sc-temperature", type=float, default=0.7)
    parser.add_argument("--react-temperature", type=float, default=0.0)
    parser.add_argument("--cot-answer-recovery", action="store_true")
    parser.add_argument(
        "--capability-parity-policy",
        choices=["equalize_react_to_tot", "strict"],
        default="equalize_react_to_tot",
        help="Protocol-v5 requires matched capability exposure in paired react/tot or react/tot_gen comparisons.",
    )
    parser.add_argument("--seed-policy", default="item_hash")
    parser.add_argument("--bootstrap-samples", type=int, default=10000)
    parser.add_argument("--confidence-level", type=float, default=0.95)
    parser.add_argument(
        "--series-id",
        default="protocol_v5_base_matrix",
        help="Runs subdirectory under phase2/benchmarks/runs/",
    )
    parser.add_argument(
        "--report-tag",
        default="v5",
        help="Suffix tag for report file naming.",
    )
    parser.add_argument(
        "--run-log",
        default=str(ROOT / "reproducibility/run-log-protocol-v5.md"),
        help="Run log path",
    )
    parser.add_argument(
        "--max-attempts-per-block",
        type=int,
        default=3,
        help="Bounded infrastructure retries per task/model block (1 disables retries).",
    )
    parser.add_argument(
        "--retry-backoff-seconds",
        type=int,
        default=30,
        help="Base retry backoff; delay grows exponentially per failed attempt.",
    )
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
        raise RuntimeError(f"Missing v5 panel file for task {task_id}: {panel_file}")

    task_slug = _slug(task_id)
    model_slug = _slug(model_id)

    runs_dir = ROOT / "benchmarks/runs" / args.series_id / task_slug / model_slug
    report_md = ROOT / "benchmarks/analysis" / f"{task_slug}_base_report_{model_slug}_{args.report_tag}.md"
    report_json = ROOT / "benchmarks/analysis" / f"{task_slug}_base_report_{model_slug}_{args.report_tag}.json"

    cmd = [
        args.python_bin,
        str(RUN_SCRIPT),
        "--task-id",
        task_id,
        "--panel-file",
        str(panel_file),
        "--provider",
        args.provider,
        "--model-id",
        model_id,
        "--conditions",
        args.conditions,
        "--tot-evaluator-mode",
        args.tot_evaluator_mode,
        "--tot-mode",
        args.tot_mode,
        "--tot-gen-mode",
        args.tot_gen_mode,
        "--tot-decomposition-rounds",
        str(args.tot_decomposition_rounds),
        "--tot-max-depth",
        str(args.tot_max_depth),
        "--tot-legacy-max-depth",
        str(args.tot_legacy_max_depth),
        "--tot-gen-max-depth",
        str(args.tot_gen_max_depth),
        "--tot-branch-factor",
        str(args.tot_branch_factor),
        "--tot-frontier-width",
        str(args.tot_frontier_width),
        "--cot-sc-samples",
        str(args.cot_sc_samples),
        "--hf-timeout-seconds",
        str(args.hf_timeout_seconds),
        "--hf-max-new-tokens",
        str(args.hf_max_new_tokens),
        "--hf-temperature",
        str(args.hf_temperature),
        "--hf-top-p",
        str(args.hf_top_p),
        "--cot-temperature",
        str(args.cot_temperature),
        "--cot-sc-temperature",
        str(args.cot_sc_temperature),
        "--react-temperature",
        str(args.react_temperature),
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
    if args.cot_answer_recovery:
        cmd.append("--cot-answer-recovery")
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
            print(f"warn: run={label} returncode={last_rc}; retry_in={wait_seconds}s")
            if wait_seconds > 0:
                time.sleep(wait_seconds)
    return last_rc


def main() -> int:
    args = parse_args()
    tasks = [task.strip() for task in args.tasks.split(",") if task.strip()]
    models = [model.strip() for model in args.models.split(",") if model.strip()]
    if not tasks:
        raise RuntimeError("No tasks selected")
    if not models:
        raise RuntimeError("No models selected")

    print(f"protocol_v5_matrix_start={_utcstamp()}")
    print(f"tasks={tasks}")
    print(f"models={models}")
    print(f"provider={args.provider}")
    print(f"python_bin={args.python_bin}")
    print(f"conditions={args.conditions}")
    print(f"report_only={args.report_only} dry_run={args.dry_run}")
    print(f"capability_parity_policy={args.capability_parity_policy}")
    print(
        "retry_policy="
        f"max_attempts_per_block={args.max_attempts_per_block},"
        f"backoff_seconds={args.retry_backoff_seconds}"
    )

    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "code/src")

    for task_id in tasks:
        for model_id in models:
            cmd = _build_command(task_id=task_id, model_id=model_id, args=args)
            print("\n### EXEC")
            print(" ".join(cmd))
            if args.dry_run:
                continue
            rc = _run_with_retries(
                cmd=cmd,
                env=env,
                cwd=ROOT,
                max_attempts=args.max_attempts_per_block,
                retry_backoff_seconds=args.retry_backoff_seconds,
                label=f"task={task_id} model={model_id}",
            )
            if rc != 0:
                print(f"error: task={task_id} model={model_id} returncode={rc}")
                return rc

    print(f"protocol_v5_matrix_done={_utcstamp()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
