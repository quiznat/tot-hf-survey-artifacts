#!/usr/bin/env python3
"""Run local baseline scaffold and emit a manifest artifact."""

from __future__ import annotations

import argparse
from pathlib import Path

from phase2_baselines.pipeline import execute_and_record


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run phase2 baseline scaffold")
    parser.add_argument("--runner", choices=["single", "cot", "cot_sc", "react"], default="single")
    parser.add_argument("--provider", choices=["scripted", "hf"], default="scripted")
    parser.add_argument("--model-id", default="", help="Model identifier for --provider hf")
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
    try:
        manifest = execute_and_record(
            runner_name=args.runner,
            input_numbers=numbers,
            runs_dir=Path(args.runs_dir),
            run_log=Path(args.run_log),
            seed=0,
            provider=args.provider,
            model_id=args.model_id or None,
            hf_token_env=args.hf_token_env,
            hf_timeout_seconds=args.hf_timeout_seconds,
            hf_max_new_tokens=args.hf_max_new_tokens,
            hf_temperature=args.hf_temperature,
            hf_top_p=args.hf_top_p,
            cot_sc_samples=args.cot_sc_samples,
        )
    except Exception as exc:
        print(f"error: {exc}")
        return 2

    print(f"run_id={manifest['run_id']}")
    print(f"outcome={manifest['outcome']}")
    print(f"manifest={manifest['artifact_paths'][-1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
