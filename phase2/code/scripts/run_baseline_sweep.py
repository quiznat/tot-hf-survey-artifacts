#!/usr/bin/env python3
"""Run repeated baseline experiments and generate a variance report."""

from __future__ import annotations

import argparse
from pathlib import Path

from phase2_baselines.pipeline import execute_and_record
from phase2_baselines.reporting import write_variance_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run repeated baseline sweep and build variance report")
    parser.add_argument("--runs-per-condition", type=int, default=5)
    parser.add_argument("--runners", default="single,react", help="Comma-separated baseline runner names")
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
    runners = [name.strip() for name in args.runners.split(",") if name.strip()]
    numbers = [int(part.strip()) for part in args.numbers.split(",") if part.strip()]

    manifests = []
    runs_dir = Path(args.runs_dir)
    run_log = Path(args.run_log)

    for seed in range(args.runs_per_condition):
        for runner_name in runners:
            manifest = execute_and_record(
                runner_name=runner_name,
                input_numbers=numbers,
                runs_dir=runs_dir,
                run_log=run_log,
                seed=seed,
            )
            manifests.append(manifest)
            print(
                f"runner={runner_name} seed={seed} run_id={manifest['run_id']} "
                f"outcome={manifest['outcome']}"
            )

    report_path = write_variance_report(
        manifests=manifests,
        report_md_path=Path(args.report_md),
        report_json_path=Path(args.report_json),
    )

    print(f"report={report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
