#!/usr/bin/env python3
"""Generate submission-facing protocol-v3 tables/figure data from matrix summary JSON."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any, Dict, List


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build protocol-v3 submission tables and figure data")
    parser.add_argument(
        "--summary-json",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/protocol_v3_matrix_summary.json",
        help="Path to protocol v3 matrix summary JSON",
    )
    parser.add_argument(
        "--out-md",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/protocol_v3_submission_tables.md",
        help="Markdown output path",
    )
    parser.add_argument(
        "--out-dir",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis",
        help="Directory for CSV outputs",
    )
    return parser.parse_args()


def _as_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except Exception:
        return None


def _fmt(value: Any, decimals: int = 3) -> str:
    as_float = _as_float(value)
    if as_float is None:
        return "n/a"
    return f"{as_float:.{decimals}f}"


def _fmt_p(value: Any) -> str:
    as_float = _as_float(value)
    if as_float is None:
        return "n/a"
    if as_float < 1e-4:
        return f"{as_float:.2e}"
    return f"{as_float:.6f}"


def write_csv(path: Path, rows: List[Dict[str, Any]], fieldnames: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({name: row.get(name) for name in fieldnames})


def main() -> int:
    args = parse_args()
    summary_path = Path(args.summary_json)
    out_md = Path(args.out_md)
    out_dir = Path(args.out_dir)

    payload = json.loads(summary_path.read_text(encoding="utf-8"))
    records: List[Dict[str, Any]] = list(payload.get("records", []))
    records.sort(key=lambda row: (str(row.get("task_id", "")), str(row.get("model_id", ""))))

    matrix_rows: List[Dict[str, Any]] = []
    for row in records:
        matrix_rows.append(
            {
                "task_id": row.get("task_id"),
                "model_id": row.get("model_id"),
                "single_success_rate": row.get("single_success_rate"),
                "react_success_rate": row.get("react_success_rate"),
                "tot_success_rate": row.get("tot_success_rate"),
                "tot_minus_react": row.get("tot_minus_react"),
                "holm_p_tot_vs_react": row.get("holm_p_tot_vs_react"),
                "tot_minus_single": row.get("tot_minus_single"),
                "holm_p_tot_vs_single": row.get("holm_p_tot_vs_single"),
                "tot_latency_ms_mean": row.get("tot_latency_ms_mean"),
            }
        )

    by_task: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for row in matrix_rows:
        by_task[str(row["task_id"])].append(row)

    task_rows: List[Dict[str, Any]] = []
    for task_id in sorted(by_task):
        rows = by_task[task_id]
        task_rows.append(
            {
                "task_id": task_id,
                "models": len(rows),
                "single_success_rate_mean": mean(float(row["single_success_rate"]) for row in rows),
                "react_success_rate_mean": mean(float(row["react_success_rate"]) for row in rows),
                "tot_success_rate_mean": mean(float(row["tot_success_rate"]) for row in rows),
                "tot_minus_react_mean": mean(float(row["tot_minus_react"]) for row in rows),
                "tot_minus_single_mean": mean(float(row["tot_minus_single"]) for row in rows),
                "tot_wins_over_react": sum(1 for row in rows if float(row["tot_minus_react"]) > 0),
                "tot_losses_vs_react": sum(1 for row in rows if float(row["tot_minus_react"]) < 0),
            }
        )

    figure_tot_vs_react: List[Dict[str, Any]] = []
    figure_tot_vs_single: List[Dict[str, Any]] = []
    for row in matrix_rows:
        p_react = _as_float(row["holm_p_tot_vs_react"])
        p_single = _as_float(row["holm_p_tot_vs_single"])
        figure_tot_vs_react.append(
            {
                "task_id": row["task_id"],
                "model_id": row["model_id"],
                "effect_delta": row["tot_minus_react"],
                "holm_p_value": row["holm_p_tot_vs_react"],
                "significant_0_05": bool(p_react is not None and p_react < 0.05),
            }
        )
        figure_tot_vs_single.append(
            {
                "task_id": row["task_id"],
                "model_id": row["model_id"],
                "effect_delta": row["tot_minus_single"],
                "holm_p_value": row["holm_p_tot_vs_single"],
                "significant_0_05": bool(p_single is not None and p_single < 0.05),
            }
        )

    matrix_csv = out_dir / "protocol_v3_table_matrix.csv"
    task_csv = out_dir / "protocol_v3_table_task_aggregate.csv"
    react_fig_csv = out_dir / "protocol_v3_figure_effect_tot_vs_react.csv"
    single_fig_csv = out_dir / "protocol_v3_figure_effect_tot_vs_single.csv"

    write_csv(
        matrix_csv,
        matrix_rows,
        [
            "task_id",
            "model_id",
            "single_success_rate",
            "react_success_rate",
            "tot_success_rate",
            "tot_minus_react",
            "holm_p_tot_vs_react",
            "tot_minus_single",
            "holm_p_tot_vs_single",
            "tot_latency_ms_mean",
        ],
    )
    write_csv(
        task_csv,
        task_rows,
        [
            "task_id",
            "models",
            "single_success_rate_mean",
            "react_success_rate_mean",
            "tot_success_rate_mean",
            "tot_minus_react_mean",
            "tot_minus_single_mean",
            "tot_wins_over_react",
            "tot_losses_vs_react",
        ],
    )
    write_csv(
        react_fig_csv,
        figure_tot_vs_react,
        ["task_id", "model_id", "effect_delta", "holm_p_value", "significant_0_05"],
    )
    write_csv(
        single_fig_csv,
        figure_tot_vs_single,
        ["task_id", "model_id", "effect_delta", "holm_p_value", "significant_0_05"],
    )

    lines: List[str] = [
        "# Protocol v3 Submission Tables and Figure Data",
        "",
        "Generated from `protocol_v3_matrix_summary.json`.",
        "",
        "## Table S1: Task x Model Matrix",
        "",
        "| Task | Model | Single | ReAct | ToT | Delta ToT-ReAct | Holm p | Delta ToT-Single | Holm p | ToT Latency (ms) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in matrix_rows:
        lines.append(
            "| {task} | {model} | {single} | {react} | {tot} | {dtr} | {ptr} | {dts} | {pts} | {lat} |".format(
                task=row["task_id"],
                model=row["model_id"],
                single=_fmt(row["single_success_rate"]),
                react=_fmt(row["react_success_rate"]),
                tot=_fmt(row["tot_success_rate"]),
                dtr=_fmt(row["tot_minus_react"]),
                ptr=_fmt_p(row["holm_p_tot_vs_react"]),
                dts=_fmt(row["tot_minus_single"]),
                pts=_fmt_p(row["holm_p_tot_vs_single"]),
                lat=_fmt(row["tot_latency_ms_mean"], decimals=1),
            )
        )

    lines.extend(
        [
            "",
            "## Table S2: Task-Aggregated Means Across Models",
            "",
            "| Task | Models | Mean Single | Mean ReAct | Mean ToT | Mean Delta ToT-ReAct | Mean Delta ToT-Single | ToT Wins vs ReAct | ToT Losses vs ReAct |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for row in task_rows:
        lines.append(
            "| {task} | {models} | {single} | {react} | {tot} | {dtr} | {dts} | {wins} | {losses} |".format(
                task=row["task_id"],
                models=row["models"],
                single=_fmt(row["single_success_rate_mean"]),
                react=_fmt(row["react_success_rate_mean"]),
                tot=_fmt(row["tot_success_rate_mean"]),
                dtr=_fmt(row["tot_minus_react_mean"]),
                dts=_fmt(row["tot_minus_single_mean"]),
                wins=row["tot_wins_over_react"],
                losses=row["tot_losses_vs_react"],
            )
        )

    lines.extend(
        [
            "",
            "## Figure Data Exports",
            f"- ToT vs ReAct effect-size points: `{react_fig_csv}`",
            f"- ToT vs Single-path effect-size points: `{single_fig_csv}`",
            "",
            "## Table Data Exports",
            f"- Matrix table CSV: `{matrix_csv}`",
            f"- Task-aggregate table CSV: `{task_csv}`",
        ]
    )

    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"out_md={out_md}")
    print(f"matrix_csv={matrix_csv}")
    print(f"task_csv={task_csv}")
    print(f"react_fig_csv={react_fig_csv}")
    print(f"single_fig_csv={single_fig_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
