#!/usr/bin/env python3
"""Build consolidated summary across protocol-v3 task/model reports."""

from __future__ import annotations

import argparse
import glob
import json
from pathlib import Path
from typing import Any, Dict, List


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build protocol-v3 matrix summary")
    parser.add_argument(
        "--reports-glob",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/*_lockset_report_*_v3.json",
        help="Glob pattern for protocol-v3 report JSON files",
    )
    parser.add_argument(
        "--out-md",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/protocol_v3_matrix_summary.md",
        help="Markdown output path",
    )
    parser.add_argument(
        "--out-json",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/protocol_v3_matrix_summary.json",
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


def main() -> int:
    args = parse_args()
    paths = sorted(glob.glob(args.reports_glob))
    if not paths:
        raise RuntimeError(f"No reports found for glob: {args.reports_glob}")

    records: List[Dict[str, Any]] = []
    for path in paths:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        cond = _condition_map(payload.get("condition_summaries", []))
        pair_tr = _pair_row(payload.get("paired_comparison", []), "tot-prototype", "baseline-react")
        pair_ts = _pair_row(payload.get("paired_comparison", []), "tot-prototype", "baseline-single-path")
        if "tot-prototype" not in cond or "baseline-react" not in cond or "baseline-single-path" not in cond:
            continue
        records.append(
            {
                "task_id": payload.get("task_id"),
                "panel_id": payload.get("panel_id"),
                "model_id": payload.get("model_id"),
                "items_evaluated": payload.get("items_evaluated"),
                "single_success_rate": cond["baseline-single-path"].get("success_rate"),
                "react_success_rate": cond["baseline-react"].get("success_rate"),
                "tot_success_rate": cond["tot-prototype"].get("success_rate"),
                "tot_latency_ms_mean": cond["tot-prototype"].get("latency_ms_mean"),
                "tot_tokens_in_mean": cond["tot-prototype"].get("tokens_in_mean"),
                "tot_tokens_out_mean": cond["tot-prototype"].get("tokens_out_mean"),
                "tot_minus_react": (pair_tr or {}).get("delta_success_rate"),
                "holm_p_tot_vs_react": (pair_tr or {}).get("mcnemar_p_holm"),
                "tot_minus_single": (pair_ts or {}).get("delta_success_rate"),
                "holm_p_tot_vs_single": (pair_ts or {}).get("mcnemar_p_holm"),
                "report_json": path,
            }
        )

    records.sort(key=lambda row: (str(row["task_id"]), str(row["model_id"])))

    out_md = Path(args.out_md)
    out_json = Path(args.out_json)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Protocol v3 Matrix Summary",
        "",
        f"Reports aggregated: {len(records)}",
        "",
        "| Task | Model | Single | ReAct | ToT | Δ ToT-ReAct | Holm p | Δ ToT-Single | Holm p | ToT Latency (ms) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in records:
        def _fmt(num: Any, decimals: int = 3) -> str:
            if num is None:
                return "n/a"
            try:
                return f"{float(num):.{decimals}f}"
            except Exception:
                return str(num)

        def _fmt_p(p: Any) -> str:
            if p is None:
                return "n/a"
            p = float(p)
            return f"{p:.2e}" if p < 1e-4 else f"{p:.6f}"

        lines.append(
            "| {task} | {model} | {s} | {r} | {t} | {dtr} | {ptr} | {dts} | {pts} | {lat} |".format(
                task=row["task_id"],
                model=row["model_id"],
                s=_fmt(row["single_success_rate"]),
                r=_fmt(row["react_success_rate"]),
                t=_fmt(row["tot_success_rate"]),
                dtr=_fmt(row["tot_minus_react"]),
                ptr=_fmt_p(row["holm_p_tot_vs_react"]),
                dts=_fmt(row["tot_minus_single"]),
                pts=_fmt_p(row["holm_p_tot_vs_single"]),
                lat=_fmt(row["tot_latency_ms_mean"], 1),
            )
        )

    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    out_json.write_text(json.dumps({"records": records}, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"out_md={out_md}")
    print(f"out_json={out_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
