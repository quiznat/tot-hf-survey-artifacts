#!/usr/bin/env python3
"""Run local baseline scaffold and emit a manifest artifact."""

from __future__ import annotations

import argparse
from pathlib import Path

from phase2_baselines.pipeline import execute_and_record


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
    manifest = execute_and_record(
        runner_name=args.runner,
        input_numbers=numbers,
        runs_dir=Path(args.runs_dir),
        run_log=Path(args.run_log),
        seed=0,
    )

    print(f"run_id={manifest['run_id']}")
    print(f"outcome={manifest['outcome']}")
    print(f"manifest={manifest['artifact_paths'][-1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
