#!/usr/bin/env python3
"""Build consolidated summary for protocol-v3.1 diagnostic reports."""

from __future__ import annotations

import argparse
import glob
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any, Dict, List


PROFILE_LABELS = {
    "tot_model_self_eval": "ToT self-eval (3/3/3)",
    "tot_hybrid": "ToT hybrid (3/3/3)",
    "tot_rule_based": "ToT rule-based (3/3/3)",
    "tot_model_self_eval_lite": "ToT self-eval lite (2/2/2)",
}

PROFILE_ORDER = list(PROFILE_LABELS.keys())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build protocol-v3.1 diagnostic summary")
    parser.add_argument(
        "--reports-glob",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/*_diag_report_*_v31.json",
        help="Glob pattern for protocol-v3.1 report JSON files",
    )
    parser.add_argument(
        "--out-md",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/protocol_v31_diagnostic_summary.md",
        help="Markdown output path",
    )
    parser.add_argument(
        "--out-json",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/protocol_v31_diagnostic_summary.json",
        help="JSON output path",
    )
    return parser.parse_args()


def _condition_map(rows: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    return {str(row.get("condition_id", "")): row for row in rows}


def _pair_row(rows: List[Dict[str, Any]], a: str, b: str) -> Dict[str, Any] | None:
    for row in rows:
        if row.get("condition_a") == a and row.get("condition_b") == b:
            return row
        if row.get("condition_a") == b and row.get("condition_b") == a:
            return {
                "condition_a": a,
                "condition_b": b,
                "matched_items": row.get("matched_items"),
                "a_better": row.get("b_better"),
                "b_better": row.get("a_better"),
                "ties": row.get("ties"),
                "delta_success_rate": -float(row.get("delta_success_rate", 0.0)),
                "delta_ci_low": -float(row.get("delta_ci_high", 0.0)),
                "delta_ci_high": -float(row.get("delta_ci_low", 0.0)),
                "mcnemar_p_value": row.get("mcnemar_p_value"),
                "mcnemar_p_holm": row.get("mcnemar_p_holm"),
            }
    return None


def _profile_from_path(path: Path) -> str:
    stem = path.stem
    if stem.endswith("_v31"):
        stem = stem[:-4]
    for profile_id in sorted(PROFILE_ORDER, key=len, reverse=True):
        suffix = f"_{profile_id}"
        if stem.endswith(suffix):
            return profile_id
    return "unknown"


def _fmt(value: Any, decimals: int = 3) -> str:
    if value is None:
        return "n/a"
    try:
        return f"{float(value):.{decimals}f}"
    except Exception:
        return str(value)


def _fmt_p(value: Any) -> str:
    if value is None:
        return "n/a"
    as_float = float(value)
    if as_float < 1e-4:
        return f"{as_float:.2e}"
    return f"{as_float:.6f}"


def main() -> int:
    args = parse_args()
    paths = [Path(p) for p in sorted(glob.glob(args.reports_glob))]
    if not paths:
        raise RuntimeError(f"No reports found for glob: {args.reports_glob}")

    records: List[Dict[str, Any]] = []
    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        cond = _condition_map(payload.get("condition_summaries", []))
        pair_tr = _pair_row(payload.get("paired_comparison", []), "tot-prototype", "baseline-react")
        if "tot-prototype" not in cond or "baseline-react" not in cond:
            continue
        profile_id = _profile_from_path(path)
        records.append(
            {
                "task_id": payload.get("task_id"),
                "panel_id": payload.get("panel_id"),
                "model_id": payload.get("model_id"),
                "profile_id": profile_id,
                "profile_label": PROFILE_LABELS.get(profile_id, profile_id),
                "items_evaluated": payload.get("items_evaluated"),
                "react_success_rate": cond["baseline-react"].get("success_rate"),
                "tot_success_rate": cond["tot-prototype"].get("success_rate"),
                "tot_minus_react": (pair_tr or {}).get("delta_success_rate"),
                "holm_p_tot_vs_react": (pair_tr or {}).get("mcnemar_p_holm"),
                "react_latency_ms_mean": cond["baseline-react"].get("latency_ms_mean"),
                "tot_latency_ms_mean": cond["tot-prototype"].get("latency_ms_mean"),
                "react_tokens_in_mean": cond["baseline-react"].get("tokens_in_mean"),
                "tot_tokens_in_mean": cond["tot-prototype"].get("tokens_in_mean"),
                "tot_evaluator_mode": payload.get("tot_evaluator_mode"),
                "tot_max_depth": payload.get("tot_max_depth"),
                "tot_branch_factor": payload.get("tot_branch_factor"),
                "tot_frontier_width": payload.get("tot_frontier_width"),
                "report_json": str(path),
            }
        )

    def _sort_key(row: Dict[str, Any]) -> tuple[str, str, int]:
        profile = str(row.get("profile_id", ""))
        idx = PROFILE_ORDER.index(profile) if profile in PROFILE_ORDER else 999
        return str(row.get("task_id", "")), str(row.get("model_id", "")), idx

    records.sort(key=_sort_key)

    task_profile_summary: List[Dict[str, Any]] = []
    grouped_tp: Dict[tuple[str, str], List[Dict[str, Any]]] = defaultdict(list)
    for row in records:
        grouped_tp[(str(row["task_id"]), str(row["profile_id"]))].append(row)
    for (task_id, profile_id), rows in sorted(grouped_tp.items()):
        task_profile_summary.append(
            {
                "task_id": task_id,
                "profile_id": profile_id,
                "profile_label": PROFILE_LABELS.get(profile_id, profile_id),
                "models": len(rows),
                "mean_react_success": mean(float(row["react_success_rate"]) for row in rows),
                "mean_tot_success": mean(float(row["tot_success_rate"]) for row in rows),
                "mean_tot_minus_react": mean(float(row["tot_minus_react"]) for row in rows),
                "tot_wins_over_react": sum(1 for row in rows if float(row["tot_minus_react"]) > 0),
                "tot_losses_vs_react": sum(1 for row in rows if float(row["tot_minus_react"]) < 0),
            }
        )

    best_by_task_model: List[Dict[str, Any]] = []
    grouped_tm: Dict[tuple[str, str], List[Dict[str, Any]]] = defaultdict(list)
    for row in records:
        grouped_tm[(str(row["task_id"]), str(row["model_id"]))].append(row)
    for (task_id, model_id), rows in sorted(grouped_tm.items()):
        best = max(rows, key=lambda row: (float(row["tot_minus_react"]), float(row["tot_success_rate"])))
        best_by_task_model.append(
            {
                "task_id": task_id,
                "model_id": model_id,
                "best_profile_id": best["profile_id"],
                "best_profile_label": best["profile_label"],
                "best_tot_minus_react": best["tot_minus_react"],
                "best_tot_success_rate": best["tot_success_rate"],
                "best_holm_p_tot_vs_react": best["holm_p_tot_vs_react"],
            }
        )

    out_md = Path(args.out_md)
    out_json = Path(args.out_json)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Protocol v3.1 Diagnostic Summary",
        "",
        f"Reports aggregated: {len(records)}",
        "",
        "## Task x Model x Profile",
        "",
        "| Task | Model | Profile | ReAct | ToT | Delta ToT-ReAct | Holm p | ReAct Lat (ms) | ToT Lat (ms) |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in records:
        lines.append(
            "| {task} | {model} | {profile} | {react} | {tot} | {delta} | {p} | {rlat} | {tlat} |".format(
                task=row["task_id"],
                model=row["model_id"],
                profile=row["profile_label"],
                react=_fmt(row["react_success_rate"]),
                tot=_fmt(row["tot_success_rate"]),
                delta=_fmt(row["tot_minus_react"]),
                p=_fmt_p(row["holm_p_tot_vs_react"]),
                rlat=_fmt(row["react_latency_ms_mean"], decimals=1),
                tlat=_fmt(row["tot_latency_ms_mean"], decimals=1),
            )
        )

    lines.extend(
        [
            "",
            "## Task x Profile (Mean Across Models)",
            "",
            "| Task | Profile | Models | Mean ReAct | Mean ToT | Mean Delta ToT-ReAct | ToT Wins | ToT Losses |",
            "|---|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for row in task_profile_summary:
        lines.append(
            "| {task} | {profile} | {models} | {react} | {tot} | {delta} | {wins} | {losses} |".format(
                task=row["task_id"],
                profile=row["profile_label"],
                models=row["models"],
                react=_fmt(row["mean_react_success"]),
                tot=_fmt(row["mean_tot_success"]),
                delta=_fmt(row["mean_tot_minus_react"]),
                wins=row["tot_wins_over_react"],
                losses=row["tot_losses_vs_react"],
            )
        )

    lines.extend(
        [
            "",
            "## Best Profile Per Task x Model",
            "",
            "| Task | Model | Best Profile | Best Delta ToT-ReAct | ToT Success | Holm p |",
            "|---|---|---|---:|---:|---:|",
        ]
    )
    for row in best_by_task_model:
        lines.append(
            "| {task} | {model} | {profile} | {delta} | {tot} | {p} |".format(
                task=row["task_id"],
                model=row["model_id"],
                profile=row["best_profile_label"],
                delta=_fmt(row["best_tot_minus_react"]),
                tot=_fmt(row["best_tot_success_rate"]),
                p=_fmt_p(row["best_holm_p_tot_vs_react"]),
            )
        )

    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    out_json.write_text(
        json.dumps(
            {
                "records": records,
                "task_profile_summary": task_profile_summary,
                "best_by_task_model": best_by_task_model,
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
