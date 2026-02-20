#!/usr/bin/env python3
"""Aggregate run manifests into an evaluation metrics table."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

from phase2_baselines.reporting import load_manifests_from_dir, summarize_by_condition


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build evaluation metrics table from run manifests")
    parser.add_argument(
        "--runs-dir",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/runs",
        help="Directory containing run manifest JSON files",
    )
    parser.add_argument(
        "--conditions",
        default="baseline-single-path,baseline-react,tot-prototype",
        help="Comma-separated condition IDs to include",
    )
    parser.add_argument(
        "--task-id",
        default="",
        help="Optional task_id filter (e.g., game24-demo)",
    )
    parser.add_argument(
        "--provider",
        default="",
        help="Optional provider filter (e.g., huggingface-inference)",
    )
    parser.add_argument(
        "--out-md",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/evaluation_v1_metrics.md",
        help="Markdown output path",
    )
    parser.add_argument(
        "--out-json",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/evaluation_v1_metrics.json",
        help="JSON output path",
    )
    return parser.parse_args()


def _render_markdown(
    summaries: List[Dict[str, Any]],
    total_runs: int,
    filters: Dict[str, Any],
) -> str:
    lines = [
        "# Evaluation v1 Metrics Summary",
        "",
        f"Total runs summarized: {total_runs}",
        f"Condition filter: {filters.get('conditions', 'all')}",
        f"Task filter: {filters.get('task_id', 'none')}",
        f"Provider filter: {filters.get('provider', 'none')}",
        "",
        "| Condition | Runs | Success Rate | Latency Mean (ms) | Latency Std (ms) | Tokens In Mean | Tokens Out Mean | Cost Mean (USD) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for summary in summaries:
        lines.append(
            "| {condition} | {runs} | {success:.3f} | {lat_mean:.3f} | {lat_std:.3f} | "
            "{tin_mean:.3f} | {tout_mean:.3f} | {cost_mean:.8f} |".format(
                condition=summary["condition_id"],
                runs=summary["runs"],
                success=summary["success_rate"],
                lat_mean=summary["latency_ms_mean"],
                lat_std=summary["latency_ms_std"],
                tin_mean=summary["tokens_in_mean"],
                tout_mean=summary["tokens_out_mean"],
                cost_mean=summary["cost_usd_mean"],
            )
        )

    lines.extend(
        [
            "",
            "## Notes",
            "- This table is generated from run manifests only.",
            "- Include both successes and failures to avoid survivorship bias.",
        ]
    )

    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    runs_dir = Path(args.runs_dir)

    conditions = [item.strip() for item in args.conditions.split(",") if item.strip()]
    task_filter = args.task_id.strip()
    provider_filter = args.provider.strip()

    manifests = load_manifests_from_dir(runs_dir)
    filtered: List[Dict[str, Any]] = []

    for manifest in manifests:
        condition_id = str(manifest.get("condition_id", ""))
        task_id = str(manifest.get("task_id", ""))
        provider = str(manifest.get("provider", ""))
        if conditions and condition_id not in conditions:
            continue
        if task_filter and task_id != task_filter:
            continue
        if provider_filter and provider != provider_filter:
            continue
        filtered.append(manifest)

    summaries = summarize_by_condition(filtered)

    out_md = Path(args.out_md)
    out_json = Path(args.out_json)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)

    markdown = _render_markdown(
        summaries=summaries,
        total_runs=len(filtered),
        filters={
            "conditions": ", ".join(conditions),
            "task_id": task_filter or "none",
            "provider": provider_filter or "none",
        },
    )
    out_md.write_text(markdown, encoding="utf-8")

    out_json.write_text(
        json.dumps(
            {
                "total_runs": len(filtered),
                "filters": {"conditions": conditions, "task_id": task_filter, "provider": provider_filter},
                "summaries": summaries,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"out_md={out_md}")
    print(f"out_json={out_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
