#!/usr/bin/env python3
"""Build deep diagnostic analysis for protocol-v3.1 series reports and manifests."""

from __future__ import annotations

import argparse
import glob
import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median
from typing import Any, Dict, List, Tuple


PROFILE_LABELS = {
    "tot_model_self_eval": "ToT self-eval (3/3/3)",
    "tot_hybrid": "ToT hybrid (3/3/3)",
    "tot_rule_based": "ToT rule-based (3/3/3)",
    "tot_model_self_eval_lite": "ToT self-eval lite (2/2/2)",
}

PROFILE_ORDER = [
    "tot_model_self_eval",
    "tot_hybrid",
    "tot_rule_based",
    "tot_model_self_eval_lite",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build protocol-v3.1 deep diagnostic analysis")
    parser.add_argument(
        "--reports-glob",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/*_diag_report_*_v31.json",
        help="Glob pattern for protocol-v3.1 report JSON files",
    )
    parser.add_argument(
        "--runs-root",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/runs/protocol_v31_diagnostic",
        help="Root directory for protocol-v3.1 run manifests",
    )
    parser.add_argument(
        "--out-md",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/protocol_v31_deep_analysis.md",
        help="Markdown output path",
    )
    parser.add_argument(
        "--out-json",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/protocol_v31_deep_analysis.json",
        help="JSON output path",
    )
    return parser.parse_args()


def _as_float(value: Any) -> float | None:
    try:
        return float(value)
    except Exception:
        return None


def _fmt(value: Any, digits: int = 3) -> str:
    v = _as_float(value)
    if v is None:
        return "n/a"
    return f"{v:.{digits}f}"


def _fmt_p(value: Any) -> str:
    v = _as_float(value)
    if v is None:
        return "n/a"
    if v < 1e-4:
        return f"{v:.2e}"
    return f"{v:.6f}"


def _infer_profile_id(path: Path) -> str:
    stem = path.stem
    for profile_id in sorted(PROFILE_ORDER, key=len, reverse=True):
        if f"_{profile_id}_" in stem or stem.endswith(f"_{profile_id}"):
            return profile_id
    return "unknown"


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
                "discordant_pairs": row.get("discordant_pairs"),
                "delta_success_rate": -float(row.get("delta_success_rate", 0.0)),
                "delta_ci_low": -float(row.get("delta_ci_high", 0.0)),
                "delta_ci_high": -float(row.get("delta_ci_low", 0.0)),
                "mcnemar_p_value": row.get("mcnemar_p_value"),
                "mcnemar_p_holm": row.get("mcnemar_p_holm"),
            }
    return None


def _classify_failure(manifest: Dict[str, Any]) -> str:
    error_type = str(manifest.get("error_type", "")).strip().lower()
    trace = "\n".join(str(line) for line in manifest.get("trace", []))
    final_answer = str(manifest.get("final_answer", ""))

    if error_type:
        return error_type
    if "depth_limit" in trace.lower():
        return "depth_limit"
    if "empty frontier" in trace.lower():
        return "empty_frontier"
    if "timeout" in trace.lower():
        return "timeout"
    if not final_answer.strip():
        return "empty_answer"
    return "other_failure"


def load_series(report_paths: List[Path]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for path in report_paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        cond_rows = payload.get("condition_summaries", [])
        pair_rows = payload.get("paired_comparison", [])
        if not isinstance(cond_rows, list):
            cond_rows = []
        if not isinstance(pair_rows, list):
            pair_rows = []

        cond = _condition_map([row for row in cond_rows if isinstance(row, dict)])
        react = cond.get("baseline-react", {})
        tot = cond.get("tot-prototype", {})
        if not react or not tot:
            continue

        pair_tr = _pair_row([row for row in pair_rows if isinstance(row, dict)], "tot-prototype", "baseline-react")
        if pair_tr is None:
            continue

        react_success = _as_float(react.get("success_rate"))
        tot_success = _as_float(tot.get("success_rate"))
        delta = _as_float(pair_tr.get("delta_success_rate"))
        react_latency = _as_float(react.get("latency_ms_mean"))
        tot_latency = _as_float(tot.get("latency_ms_mean"))
        react_tokens = _as_float(react.get("tokens_in_mean"))
        tot_tokens = _as_float(tot.get("tokens_in_mean"))

        latency_ratio = None
        if react_latency and react_latency > 0 and tot_latency is not None:
            latency_ratio = tot_latency / react_latency
        token_ratio = None
        if react_tokens and react_tokens > 0 and tot_tokens is not None:
            token_ratio = tot_tokens / react_tokens

        profile_id = _infer_profile_id(path)
        out.append(
            {
                "task_id": payload.get("task_id"),
                "model_id": payload.get("model_id"),
                "profile_id": profile_id,
                "profile_label": PROFILE_LABELS.get(profile_id, profile_id),
                "items_evaluated": payload.get("items_evaluated"),
                "react_success_rate": react_success,
                "tot_success_rate": tot_success,
                "tot_minus_react": delta,
                "delta_ci_low": _as_float(pair_tr.get("delta_ci_low")),
                "delta_ci_high": _as_float(pair_tr.get("delta_ci_high")),
                "mcnemar_p_value": _as_float(pair_tr.get("mcnemar_p_value")),
                "mcnemar_p_holm": _as_float(pair_tr.get("mcnemar_p_holm")),
                "tot_better": int(pair_tr.get("a_better", 0)),
                "react_better": int(pair_tr.get("b_better", 0)),
                "ties": int(pair_tr.get("ties", 0)),
                "discordant_pairs": int(pair_tr.get("discordant_pairs", 0)),
                "react_latency_ms_mean": react_latency,
                "tot_latency_ms_mean": tot_latency,
                "latency_ratio_tot_over_react": latency_ratio,
                "react_tokens_in_mean": react_tokens,
                "tot_tokens_in_mean": tot_tokens,
                "token_ratio_tot_over_react": token_ratio,
                "tot_evaluator_mode": payload.get("tot_evaluator_mode"),
                "tot_max_depth": payload.get("tot_max_depth"),
                "tot_branch_factor": payload.get("tot_branch_factor"),
                "tot_frontier_width": payload.get("tot_frontier_width"),
                "report_json": str(path),
            }
        )
    return out


def summarize_group(rows: List[Dict[str, Any]], group_keys: Tuple[str, ...]) -> List[Dict[str, Any]]:
    grouped: Dict[Tuple[Any, ...], List[Dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[tuple(row.get(k) for k in group_keys)].append(row)

    summaries: List[Dict[str, Any]] = []
    for key, items in grouped.items():
        deltas = [row["tot_minus_react"] for row in items if isinstance(row.get("tot_minus_react"), float)]
        react_rates = [row["react_success_rate"] for row in items if isinstance(row.get("react_success_rate"), float)]
        tot_rates = [row["tot_success_rate"] for row in items if isinstance(row.get("tot_success_rate"), float)]
        latency_ratios = [
            row["latency_ratio_tot_over_react"]
            for row in items
            if isinstance(row.get("latency_ratio_tot_over_react"), float)
        ]
        token_ratios = [
            row["token_ratio_tot_over_react"]
            for row in items
            if isinstance(row.get("token_ratio_tot_over_react"), float)
        ]

        summary: Dict[str, Any] = {k: v for k, v in zip(group_keys, key)}
        summary.update(
            {
                "series_count": len(items),
                "mean_tot_minus_react": mean(deltas) if deltas else None,
                "median_tot_minus_react": median(deltas) if deltas else None,
                "mean_react_success": mean(react_rates) if react_rates else None,
                "mean_tot_success": mean(tot_rates) if tot_rates else None,
                "tot_wins": sum(1 for d in deltas if d > 0),
                "tot_losses": sum(1 for d in deltas if d < 0),
                "tot_ties": sum(1 for d in deltas if abs(d) < 1e-12),
                "significant_losses_holm_p_lt_0_05": sum(
                    1
                    for row in items
                    if isinstance(row.get("tot_minus_react"), float)
                    and row["tot_minus_react"] < 0
                    and isinstance(row.get("mcnemar_p_holm"), float)
                    and row["mcnemar_p_holm"] < 0.05
                ),
                "mean_latency_ratio_tot_over_react": mean(latency_ratios) if latency_ratios else None,
                "mean_token_ratio_tot_over_react": mean(token_ratios) if token_ratios else None,
            }
        )
        summaries.append(summary)

    summaries.sort(
        key=lambda row: (
            *(str(row.get(k, "")) for k in group_keys),
        )
    )
    return summaries


def load_failure_summary(runs_root: Path) -> Dict[str, Any]:
    if not runs_root.exists():
        return {
            "tot_failures": 0,
            "tot_successes": 0,
            "failure_buckets": [],
            "by_model": [],
            "by_task": [],
            "by_profile": [],
        }

    latest: Dict[Tuple[str, str, str, str, str], Dict[str, Any]] = {}
    for path in sorted(runs_root.rglob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(payload, dict):
            continue
        if str(payload.get("condition_id", "")) != "tot-prototype":
            continue
        task_id = str(payload.get("task_id", ""))
        model_name = str(payload.get("model_name", ""))
        item_id = str(payload.get("item_id", ""))
        panel_id = str(payload.get("panel_id", ""))
        profile_id = path.parent.name
        payload["profile_id"] = profile_id
        if not task_id or not model_name or not item_id:
            continue
        ts = str(payload.get("timestamp_utc", ""))
        key = (task_id, model_name, panel_id, item_id, profile_id)
        curr = latest.get(key)
        if curr is None or ts > str(curr.get("timestamp_utc", "")):
            latest[key] = payload

    manifests = list(latest.values())
    failures = [m for m in manifests if str(m.get("outcome", "")).lower() != "success"]
    successes = [m for m in manifests if str(m.get("outcome", "")).lower() == "success"]

    bucket_counter: Counter[str] = Counter()
    by_model_fail: Counter[str] = Counter()
    by_model_total: Counter[str] = Counter()
    by_task_fail: Counter[str] = Counter()
    by_task_total: Counter[str] = Counter()
    by_profile_fail: Counter[str] = Counter()
    by_profile_total: Counter[str] = Counter()
    for m in manifests:
        model = str(m.get("model_name", ""))
        task = str(m.get("task_id", ""))
        profile = str(m.get("profile_id", "")) or "unknown"
        by_model_total[model] += 1
        by_task_total[task] += 1
        by_profile_total[profile] += 1
        if str(m.get("outcome", "")).lower() != "success":
            bucket_counter[_classify_failure(m)] += 1
            by_model_fail[model] += 1
            by_task_fail[task] += 1
            by_profile_fail[profile] += 1

    by_model = []
    for model in sorted(by_model_total):
        total = by_model_total[model]
        fail = by_model_fail.get(model, 0)
        by_model.append(
            {
                "model_id": model,
                "tot_runs": total,
                "tot_failures": fail,
                "failure_rate": (fail / total) if total else None,
            }
        )

    by_task = []
    for task in sorted(by_task_total):
        total = by_task_total[task]
        fail = by_task_fail.get(task, 0)
        by_task.append(
            {
                "task_id": task,
                "tot_runs": total,
                "tot_failures": fail,
                "failure_rate": (fail / total) if total else None,
            }
        )

    by_profile = []
    for profile in sorted(by_profile_total):
        total = by_profile_total[profile]
        fail = by_profile_fail.get(profile, 0)
        by_profile.append(
            {
                "profile_id": profile,
                "tot_runs": total,
                "tot_failures": fail,
                "failure_rate": (fail / total) if total else None,
            }
        )

    failure_buckets = [
        {"bucket": bucket, "count": count, "share": (count / len(failures)) if failures else None}
        for bucket, count in bucket_counter.most_common()
    ]

    return {
        "tot_failures": len(failures),
        "tot_successes": len(successes),
        "failure_buckets": failure_buckets,
        "by_model": by_model,
        "by_task": by_task,
        "by_profile": by_profile,
    }


def detect_signals(series: List[Dict[str, Any]], failure_summary: Dict[str, Any]) -> List[str]:
    notes: List[str] = []
    if not series:
        return notes

    deltas = [row["tot_minus_react"] for row in series if isinstance(row.get("tot_minus_react"), float)]
    if deltas:
        mean_delta = mean(deltas)
        if mean_delta < 0:
            notes.append(
                "Across completed v3.1 series, mean ToT-ReAct delta is negative, indicating net regression relative to ReAct."
            )
        else:
            notes.append("Across completed v3.1 series, mean ToT-ReAct delta is non-negative.")

    by_task = summarize_group(series, ("task_id",))
    if len(by_task) >= 2:
        sorted_tasks = sorted(
            [row for row in by_task if isinstance(row.get("mean_tot_minus_react"), float)],
            key=lambda row: row["mean_tot_minus_react"],
        )
        if sorted_tasks:
            worst = sorted_tasks[0]
            best = sorted_tasks[-1]
            if worst["mean_tot_minus_react"] < 0 < best["mean_tot_minus_react"]:
                notes.append(
                    "Performance is task-dependent: ToT underperforms on some tasks while outperforming on others."
                )

    by_profile = summarize_group(series, ("profile_id", "profile_label"))
    if by_profile:
        sorted_profiles = sorted(
            [row for row in by_profile if isinstance(row.get("mean_tot_minus_react"), float)],
            key=lambda row: row["mean_tot_minus_react"],
        )
        if len(sorted_profiles) >= 2:
            if sorted_profiles[-1]["mean_tot_minus_react"] - sorted_profiles[0]["mean_tot_minus_react"] > 0.1:
                notes.append(
                    "Outcome is strongly evaluator/profile-dependent, suggesting evaluator calibration is a first-order factor."
                )

    buckets = failure_summary.get("failure_buckets", [])
    if buckets:
        top = buckets[0]
        if top.get("bucket") == "depth_limit" and isinstance(top.get("share"), float) and top["share"] > 0.6:
            notes.append(
                "Most ToT failures are depth-limit terminations, consistent with search budget/pruning constraints rather than random noise."
            )

    significant_losses = sum(
        1
        for row in series
        if isinstance(row.get("tot_minus_react"), float)
        and row["tot_minus_react"] < 0
        and isinstance(row.get("mcnemar_p_holm"), float)
        and row["mcnemar_p_holm"] < 0.05
    )
    if significant_losses > 0:
        notes.append(
            f"{significant_losses} series show statistically significant ToT underperformance (Holm-adjusted p < 0.05)."
        )
    return notes


def build_markdown(
    series: List[Dict[str, Any]],
    by_task: List[Dict[str, Any]],
    by_model: List[Dict[str, Any]],
    by_profile: List[Dict[str, Any]],
    by_task_profile: List[Dict[str, Any]],
    failure_summary: Dict[str, Any],
    signals: List[str],
) -> str:
    lines = [
        "# Protocol v3.1 Deep Analysis",
        "",
        f"Series analyzed: {len(series)}",
        "",
        "## Executive Signals",
    ]
    if signals:
        for note in signals:
            lines.append(f"- {note}")
    else:
        lines.append("- No strong signal detected from current data snapshot.")

    lines.extend(
        [
            "",
            "## Series Ranking (ToT - ReAct Delta)",
            "",
            "| Task | Model | Profile | ReAct | ToT | Delta | Holm p | ToT better | ReAct better | Latency x |",
            "|---|---|---|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    ranked = sorted(
        series,
        key=lambda row: (
            row["tot_minus_react"] if isinstance(row.get("tot_minus_react"), float) else -999.0,
            str(row.get("task_id", "")),
            str(row.get("model_id", "")),
        ),
    )
    for row in ranked:
        lines.append(
            "| {task} | {model} | {profile} | {react} | {tot} | {delta} | {p} | {tb} | {rb} | {lat} |".format(
                task=row.get("task_id"),
                model=row.get("model_id"),
                profile=row.get("profile_label"),
                react=_fmt(row.get("react_success_rate")),
                tot=_fmt(row.get("tot_success_rate")),
                delta=_fmt(row.get("tot_minus_react")),
                p=_fmt_p(row.get("mcnemar_p_holm")),
                tb=row.get("tot_better"),
                rb=row.get("react_better"),
                lat=_fmt(row.get("latency_ratio_tot_over_react")),
            )
        )

    lines.extend(
        [
            "",
            "## Aggregate by Task",
            "",
            "| Task | Series | Mean Delta | Mean ReAct | Mean ToT | ToT wins | ToT losses | Sig. losses | Mean Latency x |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for row in by_task:
        lines.append(
            "| {task} | {n} | {delta} | {react} | {tot} | {wins} | {losses} | {sig} | {lat} |".format(
                task=row.get("task_id"),
                n=row.get("series_count"),
                delta=_fmt(row.get("mean_tot_minus_react")),
                react=_fmt(row.get("mean_react_success")),
                tot=_fmt(row.get("mean_tot_success")),
                wins=row.get("tot_wins"),
                losses=row.get("tot_losses"),
                sig=row.get("significant_losses_holm_p_lt_0_05"),
                lat=_fmt(row.get("mean_latency_ratio_tot_over_react")),
            )
        )

    lines.extend(
        [
            "",
            "## Aggregate by Model",
            "",
            "| Model | Series | Mean Delta | Mean ReAct | Mean ToT | ToT wins | ToT losses | Sig. losses | Mean Latency x |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for row in by_model:
        lines.append(
            "| {model} | {n} | {delta} | {react} | {tot} | {wins} | {losses} | {sig} | {lat} |".format(
                model=row.get("model_id"),
                n=row.get("series_count"),
                delta=_fmt(row.get("mean_tot_minus_react")),
                react=_fmt(row.get("mean_react_success")),
                tot=_fmt(row.get("mean_tot_success")),
                wins=row.get("tot_wins"),
                losses=row.get("tot_losses"),
                sig=row.get("significant_losses_holm_p_lt_0_05"),
                lat=_fmt(row.get("mean_latency_ratio_tot_over_react")),
            )
        )

    lines.extend(
        [
            "",
            "## Aggregate by Profile",
            "",
            "| Profile | Series | Mean Delta | Mean ReAct | Mean ToT | ToT wins | ToT losses | Sig. losses | Mean Latency x |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for row in by_profile:
        lines.append(
            "| {profile} | {n} | {delta} | {react} | {tot} | {wins} | {losses} | {sig} | {lat} |".format(
                profile=row.get("profile_label"),
                n=row.get("series_count"),
                delta=_fmt(row.get("mean_tot_minus_react")),
                react=_fmt(row.get("mean_react_success")),
                tot=_fmt(row.get("mean_tot_success")),
                wins=row.get("tot_wins"),
                losses=row.get("tot_losses"),
                sig=row.get("significant_losses_holm_p_lt_0_05"),
                lat=_fmt(row.get("mean_latency_ratio_tot_over_react")),
            )
        )

    lines.extend(
        [
            "",
            "## Aggregate by Task x Profile",
            "",
            "| Task | Profile | Series | Mean Delta | ToT wins | ToT losses | Sig. losses |",
            "|---|---|---:|---:|---:|---:|---:|",
        ]
    )
    for row in by_task_profile:
        lines.append(
            "| {task} | {profile} | {n} | {delta} | {wins} | {losses} | {sig} |".format(
                task=row.get("task_id"),
                profile=row.get("profile_label"),
                n=row.get("series_count"),
                delta=_fmt(row.get("mean_tot_minus_react")),
                wins=row.get("tot_wins"),
                losses=row.get("tot_losses"),
                sig=row.get("significant_losses_holm_p_lt_0_05"),
            )
        )

    lines.extend(
        [
            "",
            "## ToT Failure Buckets (Latest Item-Condition Manifests)",
            "",
            f"ToT successes: {failure_summary.get('tot_successes', 0)}",
            f"ToT failures: {failure_summary.get('tot_failures', 0)}",
            "",
            "| Bucket | Count | Share |",
            "|---|---:|---:|",
        ]
    )
    for row in failure_summary.get("failure_buckets", []):
        lines.append(
            "| {bucket} | {count} | {share} |".format(
                bucket=row.get("bucket"),
                count=row.get("count"),
                share=_fmt(row.get("share")),
            )
        )

    lines.extend(
        [
            "",
            "## ToT Failure Rate by Model",
            "",
            "| Model | ToT runs | ToT failures | Failure rate |",
            "|---|---:|---:|---:|",
        ]
    )
    for row in failure_summary.get("by_model", []):
        lines.append(
            "| {model} | {runs} | {fail} | {rate} |".format(
                model=row.get("model_id"),
                runs=row.get("tot_runs"),
                fail=row.get("tot_failures"),
                rate=_fmt(row.get("failure_rate")),
            )
        )

    lines.extend(
        [
            "",
            "## ToT Failure Rate by Profile",
            "",
            "| Profile | ToT runs | ToT failures | Failure rate |",
            "|---|---:|---:|---:|",
        ]
    )
    for row in failure_summary.get("by_profile", []):
        lines.append(
            "| {profile} | {runs} | {fail} | {rate} |".format(
                profile=row.get("profile_id"),
                runs=row.get("tot_runs"),
                fail=row.get("tot_failures"),
                rate=_fmt(row.get("failure_rate")),
            )
        )

    lines.extend(
        [
            "",
            "## ToT Failure Rate by Task",
            "",
            "| Task | ToT runs | ToT failures | Failure rate |",
            "|---|---:|---:|---:|",
        ]
    )
    for row in failure_summary.get("by_task", []):
        lines.append(
            "| {task} | {runs} | {fail} | {rate} |".format(
                task=row.get("task_id"),
                runs=row.get("tot_runs"),
                fail=row.get("tot_failures"),
                rate=_fmt(row.get("failure_rate")),
            )
        )

    lines.extend(
        [
            "",
            "## Interpretation Guardrails",
            "- This report is diagnostic, not causal proof.",
            "- A negative ToT delta can result from evaluator pruning, depth/branch budget, prompt mismatch, or task/tool interface effects.",
            "- Depth-limit concentration specifically suggests search-budget pressure and/or weak candidate scoring calibration.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    report_paths = [Path(p) for p in sorted(glob.glob(args.reports_glob))]
    if not report_paths:
        raise RuntimeError(f"No report files found for glob: {args.reports_glob}")

    series = load_series(report_paths)
    if not series:
        raise RuntimeError("No valid v3.1 series rows parsed from reports.")

    by_task = summarize_group(series, ("task_id",))
    by_model = summarize_group(series, ("model_id",))
    by_profile = summarize_group(series, ("profile_id", "profile_label"))
    by_task_profile = summarize_group(series, ("task_id", "profile_id", "profile_label"))
    failure_summary = load_failure_summary(Path(args.runs_root))
    signals = detect_signals(series, failure_summary)

    out_md = Path(args.out_md)
    out_json = Path(args.out_json)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)

    out_md.write_text(
        build_markdown(
            series=series,
            by_task=by_task,
            by_model=by_model,
            by_profile=by_profile,
            by_task_profile=by_task_profile,
            failure_summary=failure_summary,
            signals=signals,
        ),
        encoding="utf-8",
    )
    out_json.write_text(
        json.dumps(
            {
                "series": series,
                "aggregate_by_task": by_task,
                "aggregate_by_model": by_model,
                "aggregate_by_profile": by_profile,
                "aggregate_by_task_profile": by_task_profile,
                "failure_summary_tot": failure_summary,
                "signals": signals,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"out_md={out_md}")
    print(f"out_json={out_json}")
    print(f"series_rows={len(series)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
