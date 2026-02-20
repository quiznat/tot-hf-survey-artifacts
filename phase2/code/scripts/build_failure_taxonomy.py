#!/usr/bin/env python3
"""Build a lightweight failure taxonomy from run manifests."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List

from phase2_baselines.reporting import load_manifests_from_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build failure taxonomy from run manifests")
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
        help="Optional task_id filter",
    )
    parser.add_argument(
        "--provider",
        default="",
        help="Optional provider filter (e.g., huggingface-inference)",
    )
    parser.add_argument(
        "--out-md",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/failure_taxonomy.md",
        help="Markdown taxonomy output",
    )
    parser.add_argument(
        "--out-json",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/failure_taxonomy.json",
        help="JSON taxonomy output",
    )
    return parser.parse_args()


def classify_failure(manifest: Dict[str, Any]) -> str:
    error_type = str(manifest.get("error_type", "")).strip().lower()
    final_answer = str(manifest.get("final_answer", ""))
    trace = "\n".join(str(line) for line in manifest.get("trace", []))

    if error_type == "empty_frontier":
        return "search_empty_frontier"
    if error_type == "depth_limit":
        if any(token in final_answer for token in ["\\frac", "$", "\\times", "×", "÷", "=", "→"]):
            return "format_or_notation_mismatch"
        if "invalid" in trace.lower():
            return "invalid_candidate_retained"
        return "depth_limit_no_solution"

    if "unsafe expression" in trace.lower():
        return "unsafe_expression_filtered"

    if any(token in final_answer for token in ["\\frac", "$", "\\times", "×", "÷"]):
        return "format_or_notation_mismatch"

    return "other_failure"


def main() -> int:
    args = parse_args()
    runs_dir = Path(args.runs_dir)
    out_md = Path(args.out_md)
    out_json = Path(args.out_json)

    conditions = [item.strip() for item in args.conditions.split(",") if item.strip()]
    task_filter = args.task_id.strip()
    provider_filter = args.provider.strip()

    manifests = load_manifests_from_dir(runs_dir)

    failures: List[Dict[str, Any]] = []
    for manifest in manifests:
        if str(manifest.get("outcome", "")).strip().lower() == "success":
            continue
        if conditions and str(manifest.get("condition_id", "")) not in conditions:
            continue
        if task_filter and str(manifest.get("task_id", "")) != task_filter:
            continue
        if provider_filter and str(manifest.get("provider", "")) != provider_filter:
            continue
        failures.append(manifest)

    grouped: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for manifest in failures:
        grouped[classify_failure(manifest)].append(manifest)

    rows = []
    for bucket, items in sorted(grouped.items(), key=lambda kv: len(kv[1]), reverse=True):
        rows.append(
            {
                "bucket": bucket,
                "count": len(items),
                "sample_run_ids": [item.get("run_id", "") for item in items[:5]],
                "conditions": sorted({str(item.get("condition_id", "")) for item in items}),
            }
        )

    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)

    md_lines = [
        "# Failure Taxonomy",
        "",
        f"Total failures summarized: {len(failures)}",
        f"Condition filter: {', '.join(conditions) if conditions else 'all'}",
        f"Task filter: {task_filter or 'none'}",
        f"Provider filter: {provider_filter or 'none'}",
        "",
        "| Bucket | Count | Conditions | Sample Run IDs |",
        "|---|---:|---|---|",
    ]

    for row in rows:
        md_lines.append(
            "| {bucket} | {count} | {conditions} | {samples} |".format(
                bucket=row["bucket"],
                count=row["count"],
                conditions=", ".join(row["conditions"]),
                samples=", ".join(row["sample_run_ids"]),
            )
        )

    md_lines.extend(
        [
            "",
            "## Notes",
            "- Buckets are heuristic and intended for iterative debugging guidance.",
            "- Keep all failed runs archived; taxonomy should evolve with evaluator/prompt updates.",
        ]
    )

    out_md.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    out_json.write_text(
        json.dumps(
            {
                "total_failures": len(failures),
                "filters": {
                    "conditions": conditions,
                    "task_id": task_filter,
                    "provider": provider_filter,
                },
                "buckets": rows,
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
