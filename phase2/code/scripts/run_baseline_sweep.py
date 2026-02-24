#!/usr/bin/env python3
"""Run repeated baseline experiments and generate a variance report."""

from __future__ import annotations

import argparse
from pathlib import Path

from phase2_baselines.catalog import (
    condition_names,
    resolve_conditions,
)
from phase2_baselines.pipeline import execute_and_record
from phase2_baselines.reporting import write_variance_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run repeated baseline sweep and build variance report")
    parser.add_argument("--runs-per-condition", type=int, default=5)
    parser.add_argument(
        "--conditions",
        default=(
            "baseline_single_path_reasoning_only_v1,"
            "baseline_chain_of_thought_reasoning_only_v1,"
            "baseline_chain_of_thought_self_consistency_reasoning_only_v1,"
            "baseline_react_code_agent_with_task_tools_v1"
        ),
        help=f"Comma-separated condition keys/aliases ({','.join(condition_names())})",
    )
    parser.add_argument("--runners", dest="conditions", help=argparse.SUPPRESS)
    parser.add_argument("--provider", choices=["smolagents"], default="smolagents")
    parser.add_argument("--model-id", default="", help="Model identifier for --provider smolagents")
    parser.add_argument("--hf-token-env", default="HF_TOKEN", help="Env var name for Hugging Face API token")
    parser.add_argument("--hf-timeout-seconds", type=int, default=120)
    parser.add_argument("--hf-max-new-tokens", type=int, default=192)
    parser.add_argument("--hf-temperature", type=float, default=0.0)
    parser.add_argument("--hf-top-p", type=float, default=1.0)
    parser.add_argument("--cot-sc-samples", type=int, default=5, help="Sample count for cot_sc baseline")
    parser.add_argument("--numbers", default="4,4,10,10", help="Comma-separated integers")
    parser.add_argument(
        "--runs-dir",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/runs",
        help="Directory for run manifests",
    )
    parser.add_argument(
        "--run-log",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/reproducibility/run-log.md",
        help="Markdown run log file",
    )
    parser.add_argument(
        "--report-md",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/baseline_variance_report.md",
        help="Markdown summary report output",
    )
    parser.add_argument(
        "--report-json",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/baseline_variance_report.json",
        help="JSON summary report output",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    condition_keys = [name.strip() for name in args.conditions.split(",") if name.strip()]
    condition_specs = resolve_conditions(condition_keys)
    for spec in condition_specs:
        if spec.tot_variant:
            print(
                "error: run_baseline_sweep.py supports baseline runners only. "
                f"ToT condition selected: {spec.condition_key}"
            )
            return 2
    numbers = [int(part.strip()) for part in args.numbers.split(",") if part.strip()]

    manifests = []
    runs_dir = Path(args.runs_dir)
    run_log = Path(args.run_log)

    for seed in range(args.runs_per_condition):
        for condition_spec in condition_specs:
            try:
                manifest = execute_and_record(
                    runner_name=condition_spec.runner_name,
                    input_numbers=numbers,
                    runs_dir=runs_dir,
                    run_log=run_log,
                    seed=seed,
                    provider=args.provider,
                    model_id=args.model_id or None,
                    hf_token_env=args.hf_token_env,
                    hf_timeout_seconds=args.hf_timeout_seconds,
                    hf_max_new_tokens=args.hf_max_new_tokens,
                    hf_temperature=args.hf_temperature,
                    hf_top_p=args.hf_top_p,
                    cot_sc_samples=args.cot_sc_samples,
                    react_execution_mode=condition_spec.react_execution_mode,
                )
            except Exception as exc:
                print(f"error: {exc}")
                return 2
            manifests.append(manifest)
            print(
                f"condition={condition_spec.condition_key} seed={seed} run_id={manifest['run_id']} "
                f"outcome={manifest['outcome']}"
            )

    report_path = write_variance_report(
        manifests=manifests,
        report_md_path=Path(args.report_md),
        report_json_path=Path(args.report_json),
        report_title="Baseline Variance Report",
        note_lines=[
            f"- Provider: {args.provider}",
            "- Report includes all outcomes (success/failure/timeout) from this sweep invocation.",
        ],
    )

    print(f"report={report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
