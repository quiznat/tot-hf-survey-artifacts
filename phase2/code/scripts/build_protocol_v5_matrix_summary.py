#!/usr/bin/env python3
"""Build consolidated summary across protocol-v5 base-pattern reports."""

from __future__ import annotations

import argparse
import glob
import json
from pathlib import Path
from typing import Any, Dict, List


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build protocol-v5 matrix summary")
    parser.add_argument(
        "--reports-glob",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/*_base_report_*_v5.json",
        help="Glob pattern for protocol-v5 report JSON files",
    )
    parser.add_argument(
        "--out-md",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/protocol_v5_matrix_summary.md",
        help="Markdown output path",
    )
    parser.add_argument(
        "--out-json",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/protocol_v5_matrix_summary.json",
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


def main() -> int:
    args = parse_args()

    paths = sorted(glob.glob(args.reports_glob))
    if not paths:
        raise RuntimeError(f"No reports found for glob: {args.reports_glob}")

    records: List[Dict[str, Any]] = []
    for path in paths:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        cond = _condition_map(payload.get("condition_summaries", []))
        pairs = payload.get("paired_comparison", [])

        required = {
            "baseline-single-path",
            "baseline-cot",
            "baseline-cot-sc",
            "baseline-react",
            "tot-prototype",
        }
        if not required.issubset(set(cond.keys())):
            continue

        pair_tot_react = _pair_row(pairs, "tot-prototype", "baseline-react")
        pair_tot_cot = _pair_row(pairs, "tot-prototype", "baseline-cot")
        pair_tot_cotsc = _pair_row(pairs, "tot-prototype", "baseline-cot-sc")
        pair_cotsc_cot = _pair_row(pairs, "baseline-cot-sc", "baseline-cot")

        records.append(
            {
                "task_id": payload.get("task_id"),
                "panel_id": payload.get("panel_id"),
                "model_id": payload.get("model_id"),
                "items_evaluated": payload.get("items_evaluated"),
                "single_success_rate": cond["baseline-single-path"].get("success_rate"),
                "cot_success_rate": cond["baseline-cot"].get("success_rate"),
                "cot_sc_success_rate": cond["baseline-cot-sc"].get("success_rate"),
                "react_success_rate": cond["baseline-react"].get("success_rate"),
                "tot_success_rate": cond["tot-prototype"].get("success_rate"),
                "tot_minus_react": (pair_tot_react or {}).get("delta_success_rate"),
                "holm_p_tot_vs_react": (pair_tot_react or {}).get("mcnemar_p_holm"),
                "tot_minus_cot": (pair_tot_cot or {}).get("delta_success_rate"),
                "holm_p_tot_vs_cot": (pair_tot_cot or {}).get("mcnemar_p_holm"),
                "tot_minus_cot_sc": (pair_tot_cotsc or {}).get("delta_success_rate"),
                "holm_p_tot_vs_cot_sc": (pair_tot_cotsc or {}).get("mcnemar_p_holm"),
                "cot_sc_minus_cot": (pair_cotsc_cot or {}).get("delta_success_rate"),
                "holm_p_cot_sc_vs_cot": (pair_cotsc_cot or {}).get("mcnemar_p_holm"),
                "tot_latency_ms_mean": cond["tot-prototype"].get("latency_ms_mean"),
                "report_json": path,
            }
        )

    records.sort(key=lambda row: (str(row.get("task_id", "")), str(row.get("model_id", ""))))

    out_md = Path(args.out_md)
    out_json = Path(args.out_json)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Protocol v5 Base-Pattern Matrix Summary",
        "",
        f"Reports aggregated: {len(records)}",
        "",
        "| Task | Model | Single | CoT | CoT-SC | ReAct | ToT | ToT-ReAct | Holm p | ToT-CoT | Holm p | ToT-CoT-SC | Holm p | CoT-SC-CoT | Holm p |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for row in records:
        lines.append(
            "| {task} | {model} | {single} | {cot} | {cot_sc} | {react} | {tot} | {tr} | {ptr} | {tc} | {ptc} | {tcs} | {ptcs} | {csc} | {pcsc} |".format(
                task=row["task_id"],
                model=row["model_id"],
                single=_fmt(row["single_success_rate"]),
                cot=_fmt(row["cot_success_rate"]),
                cot_sc=_fmt(row["cot_sc_success_rate"]),
                react=_fmt(row["react_success_rate"]),
                tot=_fmt(row["tot_success_rate"]),
                tr=_fmt(row["tot_minus_react"]),
                ptr=_fmt_p(row["holm_p_tot_vs_react"]),
                tc=_fmt(row["tot_minus_cot"]),
                ptc=_fmt_p(row["holm_p_tot_vs_cot"]),
                tcs=_fmt(row["tot_minus_cot_sc"]),
                ptcs=_fmt_p(row["holm_p_tot_vs_cot_sc"]),
                csc=_fmt(row["cot_sc_minus_cot"]),
                pcsc=_fmt_p(row["holm_p_cot_sc_vs_cot"]),
            )
        )

    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    out_json.write_text(json.dumps({"records": records}, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"out_md={out_md}")
    print(f"out_json={out_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
