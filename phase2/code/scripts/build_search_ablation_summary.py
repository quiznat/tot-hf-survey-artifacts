#!/usr/bin/env python3
"""Build a consolidated summary for protocol-v2 search-policy ablations."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build search-policy ablation summary from lockset reports")
    parser.add_argument(
        "--protocol-id",
        default="TOT-HF-P2-EPV2-2026-02-20",
        help="Protocol identifier for summary header",
    )
    parser.add_argument(
        "--primary-report-json",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/game24_lockset_report_qwen3codernext.json",
        help="Primary (default search config) lockset report JSON",
    )
    parser.add_argument(
        "--a1-report-json",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/game24_lockset_report_qwen3codernext_search_a1.json",
        help="A1 search ablation report JSON (shallower preset)",
    )
    parser.add_argument(
        "--a2-report-json",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/game24_lockset_report_qwen3codernext_search_a2.json",
        help="A2 search ablation report JSON (wider preset)",
    )
    parser.add_argument(
        "--out-md",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/game24_lockset_search_ablation_summary.md",
        help="Markdown output path",
    )
    parser.add_argument(
        "--out-json",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/game24_lockset_search_ablation_summary.json",
        help="JSON output path",
    )
    return parser.parse_args()


def _load_report(path: Path) -> Dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError(f"Expected JSON object in {path}")
    return payload


def _condition_row(report: Dict[str, Any], condition_id: str) -> Dict[str, Any]:
    for row in report.get("condition_summaries", []):
        if str(row.get("condition_id", "")) == condition_id:
            return row
    raise RuntimeError(f"Missing condition '{condition_id}' in report payload")


def _pair_row(report: Dict[str, Any], condition_a: str, condition_b: str) -> Dict[str, Any]:
    for row in report.get("paired_comparison", []):
        a = str(row.get("condition_a", ""))
        b = str(row.get("condition_b", ""))
        if a == condition_a and b == condition_b:
            return row
    raise RuntimeError(f"Missing paired comparison '{condition_a}' vs '{condition_b}' in report payload")


def _preset_record(label: str, report: Dict[str, Any]) -> Dict[str, Any]:
    single = _condition_row(report, "baseline-single-path")
    react = _condition_row(report, "baseline-react")
    tot = _condition_row(report, "tot-prototype")

    react_vs_tot = _pair_row(report, "baseline-react", "tot-prototype")

    depth = int(report.get("tot_max_depth", 3))
    branch = int(report.get("tot_branch_factor", 3))
    frontier = int(report.get("tot_frontier_width", 3))

    return {
        "label": label,
        "model_id": str(report.get("model_id", "")),
        "panel_id": str(report.get("panel_id", "")),
        "provider": str(report.get("provider", "")),
        "items_evaluated": int(report.get("items_evaluated", 0)),
        "tot_evaluator_mode": str(report.get("tot_evaluator_mode", "")),
        "tot_max_depth": depth,
        "tot_branch_factor": branch,
        "tot_frontier_width": frontier,
        "single_success_rate": float(single.get("success_rate", 0.0)),
        "react_success_rate": float(react.get("success_rate", 0.0)),
        "tot_success_rate": float(tot.get("success_rate", 0.0)),
        "tot_minus_react": float(tot.get("success_rate", 0.0)) - float(react.get("success_rate", 0.0)),
        "tot_minus_single": float(tot.get("success_rate", 0.0)) - float(single.get("success_rate", 0.0)),
        "tot_latency_ms_mean": float(tot.get("latency_ms_mean", 0.0)),
        "tot_tokens_in_mean": float(tot.get("tokens_in_mean", 0.0)),
        "tot_tokens_out_mean": float(tot.get("tokens_out_mean", 0.0)),
        "paired_tot_vs_react": {
            "a_better": int(react_vs_tot.get("a_better", 0)),
            "b_better": int(react_vs_tot.get("b_better", 0)),
            "ties": int(react_vs_tot.get("ties", 0)),
            "delta_success_rate_react_minus_tot": float(react_vs_tot.get("delta_success_rate", 0.0)),
            "delta_ci_low_react_minus_tot": float(react_vs_tot.get("delta_ci_low", 0.0)),
            "delta_ci_high_react_minus_tot": float(react_vs_tot.get("delta_ci_high", 0.0)),
            "mcnemar_p_value": float(react_vs_tot.get("mcnemar_p_value", 1.0)),
            "mcnemar_p_holm": float(react_vs_tot.get("mcnemar_p_holm", 1.0)),
        },
    }


def _fmt_p(p_value: float) -> str:
    return f"{p_value:.2e}" if p_value < 1e-4 else f"{p_value:.6f}"


def _validate_shared_context(records: List[Dict[str, Any]]) -> Tuple[str, str, str]:
    model_ids = {record["model_id"] for record in records}
    panel_ids = {record["panel_id"] for record in records}
    providers = {record["provider"] for record in records}
    if len(model_ids) != 1:
        raise RuntimeError(f"Ablation reports do not share a single model_id: {sorted(model_ids)}")
    if len(panel_ids) != 1:
        raise RuntimeError(f"Ablation reports do not share a single panel_id: {sorted(panel_ids)}")
    if len(providers) != 1:
        raise RuntimeError(f"Ablation reports do not share a single provider: {sorted(providers)}")
    return next(iter(model_ids)), next(iter(panel_ids)), next(iter(providers))


def main() -> int:
    args = parse_args()
    primary = _load_report(Path(args.primary_report_json))
    a1 = _load_report(Path(args.a1_report_json))
    a2 = _load_report(Path(args.a2_report_json))

    records = [
        _preset_record("primary", primary),
        _preset_record("A1", a1),
        _preset_record("A2", a2),
    ]
    model_id, panel_id, provider = _validate_shared_context(records)

    generated_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    out_md = Path(args.out_md)
    out_json = Path(args.out_json)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)

    md_lines = [
        "# Game24 Lockset Search Ablation Summary (Protocol v2)",
        "",
        f"Generated UTC: {generated_utc}  ",
        f"Protocol ID: `{args.protocol_id}`  ",
        f"Panel ID: `{panel_id}`  ",
        f"Provider: `{provider}`  ",
        f"Model: `{model_id}`",
        "",
        "## Condition Success by Search Preset",
        "",
        "| Preset | ToT Depth | ToT Branch | ToT Frontier | Single Success | ReAct Success | ToT Success | ToT - ReAct | ToT - Single |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for record in records:
        md_lines.append(
            "| {label} | {depth} | {branch} | {frontier} | {single:.3f} | {react:.3f} | {tot:.3f} | {dtr:+.3f} | {dts:+.3f} |".format(
                label=record["label"],
                depth=record["tot_max_depth"],
                branch=record["tot_branch_factor"],
                frontier=record["tot_frontier_width"],
                single=record["single_success_rate"],
                react=record["react_success_rate"],
                tot=record["tot_success_rate"],
                dtr=record["tot_minus_react"],
                dts=record["tot_minus_single"],
            )
        )

    md_lines.extend(
        [
            "",
            "## Paired Significance (ToT vs ReAct)",
            "",
            "| Preset | ReAct Better | ToT Better | Ties | McNemar p | Holm p | Delta CI (ReAct - ToT) |",
            "|---|---:|---:|---:|---:|---:|---|",
        ]
    )
    for record in records:
        paired = record["paired_tot_vs_react"]
        md_lines.append(
            "| {label} | {a} | {b} | {ties} | {p} | {ph} | [{dl:.3f}, {dh:.3f}] |".format(
                label=record["label"],
                a=paired["a_better"],
                b=paired["b_better"],
                ties=paired["ties"],
                p=_fmt_p(paired["mcnemar_p_value"]),
                ph=_fmt_p(paired["mcnemar_p_holm"]),
                dl=paired["delta_ci_low_react_minus_tot"],
                dh=paired["delta_ci_high_react_minus_tot"],
            )
        )

    md_lines.extend(
        [
            "",
            "## Cost/Latency Snapshot (ToT Condition)",
            "",
            "| Preset | ToT Latency Mean (ms) | ToT Tokens In Mean | ToT Tokens Out Mean |",
            "|---|---:|---:|---:|",
        ]
    )
    for record in records:
        md_lines.append(
            "| {label} | {lat:.1f} | {tin:.1f} | {tout:.1f} |".format(
                label=record["label"],
                lat=record["tot_latency_ms_mean"],
                tin=record["tot_tokens_in_mean"],
                tout=record["tot_tokens_out_mean"],
            )
        )

    md_lines.extend(
        [
            "",
            "## Interpretation",
            "- Compare presets on both success and latency/cost; a higher-success preset is not automatically preferred if latency/token inflation is disproportionate.",
            "- Claims should remain panel/model-specific under the frozen protocol and avoid cross-task generalization.",
        ]
    )
    out_md.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    out_json.write_text(
        json.dumps(
            {
                "generated_utc": generated_utc,
                "protocol_id": args.protocol_id,
                "panel_id": panel_id,
                "provider": provider,
                "model_id": model_id,
                "records": records,
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
