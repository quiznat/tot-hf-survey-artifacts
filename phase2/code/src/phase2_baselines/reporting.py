"""Reporting helpers for sweep summary reports."""

from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timezone
from math import sqrt
from pathlib import Path
from typing import Any, Dict, Iterable, List


def _mean(values: List[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def _stddev(values: List[float]) -> float:
    if len(values) < 2:
        return 0.0
    mean = _mean(values)
    variance = sum((value - mean) ** 2 for value in values) / (len(values) - 1)
    return sqrt(variance)


def summarize_by_condition(manifests: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Aggregate run manifests into condition-level summary statistics."""
    grouped: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for manifest in manifests:
        grouped[manifest["condition_id"]].append(manifest)

    summaries: List[Dict[str, Any]] = []
    for condition_id, rows in sorted(grouped.items()):
        success_vals = [float(row["metrics"]["success"]) for row in rows]
        latency_vals = [float(row["metrics"]["latency_ms"]) for row in rows]
        tokens_in_vals = [float(row["metrics"]["tokens_in"]) for row in rows]
        tokens_out_vals = [float(row["metrics"]["tokens_out"]) for row in rows]
        cost_vals = [float(row["metrics"]["cost_usd"]) for row in rows]

        summaries.append(
            {
                "condition_id": condition_id,
                "runs": len(rows),
                "success_rate": _mean(success_vals),
                "latency_ms_mean": _mean(latency_vals),
                "latency_ms_std": _stddev(latency_vals),
                "tokens_in_mean": _mean(tokens_in_vals),
                "tokens_in_std": _stddev(tokens_in_vals),
                "tokens_out_mean": _mean(tokens_out_vals),
                "tokens_out_std": _stddev(tokens_out_vals),
                "cost_usd_mean": _mean(cost_vals),
                "cost_usd_std": _stddev(cost_vals),
            }
        )

    return summaries


def write_variance_report(
    manifests: List[Dict[str, Any]],
    report_md_path: Path,
    report_json_path: Path | None = None,
    report_title: str = "Variance Report",
    note_lines: List[str] | None = None,
) -> Path:
    """Write markdown (and optional JSON) summary report for sweep runs."""
    summaries = summarize_by_condition(manifests)
    generated_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    report_md_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        f"# {report_title}",
        "",
        f"Generated UTC: {generated_utc}",
        f"Total runs summarized: {len(manifests)}",
        "",
        "| Condition | Runs | Success Rate | Latency Mean (ms) | Latency Std (ms) | Tokens In Mean | Tokens In Std | Tokens Out Mean | Tokens Out Std | Cost Mean (USD) | Cost Std (USD) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for summary in summaries:
        lines.append(
            "| {condition} | {runs} | {success:.3f} | {lat_mean:.3f} | {lat_std:.3f} | "
            "{tin_mean:.3f} | {tin_std:.3f} | {tout_mean:.3f} | {tout_std:.3f} | {cost_mean:.8f} | {cost_std:.8f} |".format(
                condition=summary["condition_id"],
                runs=summary["runs"],
                success=summary["success_rate"],
                lat_mean=summary["latency_ms_mean"],
                lat_std=summary["latency_ms_std"],
                tin_mean=summary["tokens_in_mean"],
                tin_std=summary["tokens_in_std"],
                tout_mean=summary["tokens_out_mean"],
                tout_std=summary["tokens_out_std"],
                cost_mean=summary["cost_usd_mean"],
                cost_std=summary["cost_usd_std"],
            )
        )

    if note_lines is None:
        note_lines = [
            "- This report is generated directly from run manifests.",
            "- Include both successes and failures when comparing variance across conditions.",
        ]
    lines.extend(["", "## Notes", *note_lines])

    report_md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if report_json_path is not None:
        report_json_path.parent.mkdir(parents=True, exist_ok=True)
        report_json_path.write_text(
            json.dumps({"generated_utc": generated_utc, "summaries": summaries}, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    return report_md_path


def load_manifests_from_dir(runs_dir: Path) -> List[Dict[str, Any]]:
    """Load all JSON run manifests from a runs directory."""
    manifests: List[Dict[str, Any]] = []
    for path in sorted(runs_dir.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if isinstance(payload, dict):
            manifests.append(payload)
    return manifests
