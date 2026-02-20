#!/usr/bin/env python3
"""Run ToT prototype demo and emit a manifest artifact."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from phase2_baselines.adapters import HuggingFaceInferenceModel, ScriptedModel
from phase2_baselines.manifest import append_run_log, write_manifest
from phase2_baselines.runners.tot import ToTRunner
from phase2_baselines.tasks import Arithmetic24Task


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run phase2 ToT prototype demo")
    parser.add_argument("--provider", choices=["scripted", "hf"], default="scripted")
    parser.add_argument("--model-id", default="", help="Model identifier for --provider hf")
    parser.add_argument("--hf-token-env", default="HF_TOKEN", help="Env var name for Hugging Face API token")
    parser.add_argument("--hf-timeout-seconds", type=int, default=120)
    parser.add_argument("--hf-max-new-tokens", type=int, default=192)
    parser.add_argument("--hf-temperature", type=float, default=0.0)
    parser.add_argument("--hf-top-p", type=float, default=1.0)
    parser.add_argument(
        "--evaluator-mode",
        choices=["task_binary", "rule_based", "model_self_eval", "hybrid"],
        default="model_self_eval",
        help="Candidate evaluation strategy for ToT search",
    )
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


def _build_model(args: argparse.Namespace):
    if args.provider == "scripted":
        return (
            ScriptedModel(
                responses=[
                    "CANDIDATE: (10+4)+10+4\nCANDIDATE: (10*10-4)/4",
                ]
            ),
            "scripted-tot-v1",
            "local-scripted",
        )

    model_id = args.model_id or "Qwen/Qwen3-Coder-Next:novita"
    token = os.getenv(args.hf_token_env, "").strip()
    if not token:
        raise RuntimeError(
            f"Hugging Face provider requires ${args.hf_token_env} with a valid API token."
        )
    return (
        HuggingFaceInferenceModel(
            model_id=model_id,
            api_token=token,
            timeout_seconds=args.hf_timeout_seconds,
            max_new_tokens=args.hf_max_new_tokens,
            temperature=args.hf_temperature,
            top_p=args.hf_top_p,
        ),
        model_id,
        "huggingface-inference",
    )


def main() -> int:
    args = parse_args()
    numbers = [int(part.strip()) for part in args.numbers.split(",") if part.strip()]

    try:
        task = Arithmetic24Task()
        model, model_name, provider_name = _build_model(args)
        runner = ToTRunner(model=model, model_name=model_name, provider=provider_name)
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
                "evaluator_mode": args.evaluator_mode,
            },
        )

        manifest = runner.run(numbers)

        runs_dir = Path(args.runs_dir)
        out_path = runs_dir / f"{manifest['run_id']}.json"

        manifest["artifact_paths"].append(str(out_path))
        write_manifest(manifest, out_path)
        append_run_log(Path(args.run_log), manifest)
    except Exception as exc:
        print(f"error: {exc}")
        return 2

    print(f"run_id={manifest['run_id']}")
    print(f"outcome={manifest['outcome']}")
    print(f"manifest={out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
