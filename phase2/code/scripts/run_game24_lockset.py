#!/usr/bin/env python3
"""Run paired Game24 lockset panel across baseline and ToT conditions."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import math
from pathlib import Path
import random
from statistics import NormalDist
from typing import Any, Dict, Iterable, List, Tuple

from phase2_baselines.adapters import SmolagentsInferenceModel
from phase2_baselines.manifest import append_run_log, write_manifest
from phase2_baselines.pipeline import create_baseline_setup
from phase2_baselines.reporting import summarize_by_condition
from phase2_baselines.runners.tot import ToTRunner
from phase2_baselines.tasks import Arithmetic24Task


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run paired Game24 lockset panel")
    parser.add_argument(
        "--panel-file",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/panels/game24_lockset_v1.json",
        help="JSON panel file with item_id + numbers entries",
    )
    parser.add_argument(
        "--conditions",
        default=(
            "baseline_single_path_reasoning_only_v1,"
            "baseline_react_code_agent_with_task_tools_v1,"
            "baseline_tree_of_thoughts_search_reasoning_only_v1"
        ),
        help="Comma-separated condition keys/aliases for {single, react, tot}.",
    )
    parser.add_argument("--provider", choices=["smolagents"], default="smolagents")
    parser.add_argument("--model-id", default="", help="Model identifier for --provider smolagents")
    parser.add_argument("--hf-token-env", default="HF_TOKEN", help="Env var name for Hugging Face API token")
    parser.add_argument("--hf-timeout-seconds", type=int, default=120)
    parser.add_argument("--hf-max-new-tokens", type=int, default=192)
    parser.add_argument("--hf-temperature", type=float, default=0.0)
    parser.add_argument("--hf-top-p", type=float, default=1.0)
    parser.add_argument(
        "--tot-evaluator-mode",
        choices=["task_binary", "rule_based", "model_self_eval", "hybrid"],
        default="model_self_eval",
    )
    parser.add_argument("--tot-max-depth", type=int, default=3)
    parser.add_argument("--tot-branch-factor", type=int, default=3)
    parser.add_argument("--tot-frontier-width", type=int, default=3)
    parser.add_argument(
        "--capability-parity-policy",
        choices=["equalize_react_to_tot", "strict", "off"],
        default="equalize_react_to_tot",
        help=(
            "How to handle capability mismatch when paired react/tot conditions are selected. "
            "equalize_react_to_tot disables React tools to match current ToT access; "
            "strict fails fast on mismatch; off allows mismatch."
        ),
    )
    parser.add_argument("--offset", type=int, default=0, help="Start index within panel items")
    parser.add_argument("--limit", type=int, default=0, help="Number of items from panel (0 = all)")
    parser.add_argument(
        "--max-workers",
        type=int,
        default=1,
        help="Parallel item workers. 1 keeps sequential execution.",
    )
    parser.add_argument(
        "--seed-policy",
        choices=["item_index", "item_hash"],
        default="item_hash",
        help="Deterministic seed assignment policy per item.",
    )
    parser.add_argument(
        "--confidence-level",
        type=float,
        default=0.95,
        help="Confidence level for interval reporting.",
    )
    parser.add_argument(
        "--bootstrap-samples",
        type=int,
        default=10000,
        help="Bootstrap samples for paired-delta confidence intervals.",
    )
    parser.add_argument(
        "--bootstrap-seed",
        type=int,
        default=20260220,
        help="Seed for paired-delta bootstrap confidence intervals.",
    )
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="Skip new runs and rebuild report from existing manifests in runs-dir.",
    )
    parser.add_argument(
        "--runs-dir",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/runs",
        help="Directory for run manifests",
    )
    parser.add_argument(
        "--run-log",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/reproducibility/run-log.md",
        help="Markdown run log file",
    )
    parser.add_argument(
        "--report-md",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/game24_lockset_report.md",
        help="Markdown report output",
    )
    parser.add_argument(
        "--report-json",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/game24_lockset_report.json",
        help="JSON report output",
    )
    return parser.parse_args()


def _load_panel(path: Path) -> Tuple[str, List[Dict[str, Any]]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError("Panel file must be an object with panel_id + items")
    panel_id = str(payload.get("panel_id", "game24-lockset-unknown")).strip()
    items = payload.get("items", [])
    if not isinstance(items, list) or not items:
        raise RuntimeError("Panel file has no items")

    normalized: List[Dict[str, Any]] = []
    for idx, item in enumerate(items):
        if not isinstance(item, dict):
            raise RuntimeError(f"Invalid item at index {idx}")
        item_id = str(item.get("item_id", "")).strip() or f"item-{idx+1:04d}"
        numbers = item.get("numbers")
        if not isinstance(numbers, list) or len(numbers) != 4:
            raise RuntimeError(f"Item {item_id} must include 4-number list")
        normalized.append(
            {
                "item_id": item_id,
                "numbers": [int(x) for x in numbers],
                "oracle_solution": str(item.get("oracle_solution", "")).strip(),
            }
        )
    return panel_id, normalized


def _slice_items(items: List[Dict[str, Any]], offset: int, limit: int) -> List[Dict[str, Any]]:
    if offset < 0:
        raise RuntimeError("offset must be >= 0")
    if offset >= len(items):
        return []
    sliced = items[offset:]
    if limit > 0:
        sliced = sliced[:limit]
    return sliced


def _seed_for_item(item_id: str, item_index: int, seed_policy: str) -> int:
    if seed_policy == "item_hash":
        digest = hashlib.sha256(item_id.encode("utf-8")).digest()
        return int.from_bytes(digest[:4], "big", signed=False)
    return item_index


def _normalize_condition_aliases(raw_conditions: List[str]) -> List[str]:
    alias_to_legacy = {
        "single": "single",
        "baseline_single_path_reasoning_only_v1": "single",
        "baseline-single-path": "single",
        "react": "react",
        "react_codeagent": "react",
        "baseline_react_code_agent_with_task_tools_v1": "react",
        "baseline-react": "react",
        "tot": "tot",
        "baseline_tree_of_thoughts_search_reasoning_only_v1": "tot",
        "tot-prototype": "tot",
    }

    normalized: List[str] = []
    for condition in raw_conditions:
        key = condition.strip()
        legacy = alias_to_legacy.get(key)
        if not legacy:
            raise RuntimeError(f"unsupported conditions: {key}")
        if legacy not in normalized:
            normalized.append(legacy)
    return normalized


def _resolve_capability_plan(conditions: List[str], policy: str) -> Dict[str, Any]:
    task_tools = sorted(Arithmetic24Task().available_tools().keys())

    react_selected = "react" in conditions
    tot_selected = "tot" in conditions
    react_tools = list(task_tools) if react_selected else []
    tot_tools = [] if tot_selected else []
    react_enable_tools = bool(react_tools)
    adjustments: List[str] = []

    if react_selected and tot_selected and react_tools != tot_tools:
        if policy == "strict":
            raise RuntimeError(
                "capability parity violation: react exposes tools "
                f"{react_tools} while tot exposes {tot_tools}. "
                "Use --capability-parity-policy equalize_react_to_tot to run a fair tool-symmetric comparison."
            )
        if policy == "equalize_react_to_tot":
            react_tools = list(tot_tools)
            react_enable_tools = bool(react_tools)
            adjustments.append("react_tools_disabled_to_match_tot")
        else:
            adjustments.append("mismatch_allowed_by_policy_off")

    condition_tools: Dict[str, List[str]] = {}
    if "single" in conditions:
        condition_tools["single"] = []
    if "react" in conditions:
        condition_tools["react"] = react_tools
    if "tot" in conditions:
        condition_tools["tot"] = tot_tools

    return {
        "task_tools": task_tools,
        "condition_tools": condition_tools,
        "react_enable_tools": react_enable_tools,
        "adjustments": adjustments,
    }


def _parse_utc(timestamp_utc: str) -> datetime:
    return datetime.fromisoformat(timestamp_utc.replace("Z", "+00:00"))


def _load_latest_existing_manifests(
    runs_dir: Path,
    panel_id: str,
    selected_items: List[Dict[str, Any]],
    conditions: List[str],
) -> List[Dict[str, Any]]:
    item_ids = {item["item_id"] for item in selected_items}
    condition_map = {
        "single": "baseline-single-path",
        "react": "baseline-react",
        "tot": "tot-prototype",
    }
    target_conditions = {condition_map[name] for name in conditions}

    latest: Dict[Tuple[str, str], Dict[str, Any]] = {}
    for path in sorted(runs_dir.glob("*.json")):
        try:
            manifest = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if str(manifest.get("panel_id", "")) != panel_id:
            continue
        item_id = str(manifest.get("item_id", ""))
        condition_id = str(manifest.get("condition_id", ""))
        if item_id not in item_ids or condition_id not in target_conditions:
            continue
        key = (item_id, condition_id)
        current = latest.get(key)
        if current is None or _parse_utc(str(manifest.get("timestamp_utc", ""))) > _parse_utc(
            str(current.get("timestamp_utc", ""))
        ):
            latest[key] = manifest

    manifests = list(latest.values())
    expected = len(item_ids) * len(target_conditions)
    if len(manifests) < expected:
        missing = expected - len(manifests)
        raise RuntimeError(
            f"report-only mode found {len(manifests)}/{expected} required manifests "
            f"(missing {missing})."
        )
    return manifests


def _build_model(args: argparse.Namespace):
    model_id = args.model_id or "Qwen/Qwen3-Coder-Next:novita"
    token = os.getenv(args.hf_token_env, "").strip()
    if not token:
        raise RuntimeError(f"smolagents provider requires ${args.hf_token_env} with a valid API token.")
    return (
        SmolagentsInferenceModel(
            model_id=model_id,
            api_token=token,
            timeout_seconds=args.hf_timeout_seconds,
            max_new_tokens=args.hf_max_new_tokens,
            temperature=args.hf_temperature,
            top_p=args.hf_top_p,
        ),
        model_id,
        "smolagents-inference",
    )


def _run_single_or_react(
    condition: str,
    item: Dict[str, Any],
    seed: int,
    args: argparse.Namespace,
    react_enable_tools: bool,
    condition_tools: Dict[str, List[str]],
) -> Dict[str, Any]:
    runner, task, config = create_baseline_setup(
        runner_name=condition,
        seed=seed,
        provider=args.provider,
        model_id=args.model_id or None,
        hf_token_env=args.hf_token_env,
        hf_timeout_seconds=args.hf_timeout_seconds,
        hf_max_new_tokens=args.hf_max_new_tokens,
        hf_temperature=args.hf_temperature,
        hf_top_p=args.hf_top_p,
        react_enable_tools=react_enable_tools,
    )
    config["item_id"] = item["item_id"]
    config["input_data"] = item["numbers"]
    config["panel_id"] = args.panel_id
    config["hf_temperature"] = args.hf_temperature
    config["hf_top_p"] = args.hf_top_p
    config["capability_parity_policy"] = args.capability_parity_policy
    config["task_tools_available"] = list(getattr(args, "task_tools_available", []))
    config["condition_tools_exposed"] = list(condition_tools.get(condition, []))
    config["tool_config"] = list(condition_tools.get(condition, []))
    runner.prepare(task=task, config=config)
    return runner.run(item["numbers"])


def _run_tot(item: Dict[str, Any], seed: int, args: argparse.Namespace, condition_tools: Dict[str, List[str]]) -> Dict[str, Any]:
    task = Arithmetic24Task()
    model, model_name, provider_name = _build_model(args)
    runner = ToTRunner(model=model, model_name=model_name, provider=provider_name)
    runner.prepare(
        task=task,
        config={
            "condition_id": "tot-prototype",
            "prompt_template_version": "v1",
            "search_config": {
                "depth": args.tot_max_depth,
                "breadth": args.tot_branch_factor,
                "pruning": "topk_cumulative_score",
                "stop_policy": "first_terminal_or_depth_limit",
            },
            "tool_config": list(condition_tools.get("tot", [])),
            "budget": {"token_budget": 4000, "time_budget_ms": 15000, "cost_budget_usd": 0.0},
            "seed": seed,
            "max_depth": args.tot_max_depth,
            "branch_factor": args.tot_branch_factor,
            "frontier_width": args.tot_frontier_width,
            "evaluator_mode": args.tot_evaluator_mode,
            "hf_temperature": args.hf_temperature,
            "hf_top_p": args.hf_top_p,
            "item_id": item["item_id"],
            "input_data": item["numbers"],
            "panel_id": args.panel_id,
            "capability_parity_policy": args.capability_parity_policy,
            "task_tools_available": list(getattr(args, "task_tools_available", [])),
            "condition_tools_exposed": list(condition_tools.get("tot", [])),
        },
    )
    return runner.run(item["numbers"])


def _write_manifest_and_log(manifest: Dict[str, Any], runs_dir: Path, run_log: Path) -> Path:
    out_path = runs_dir / f"{manifest['run_id']}.json"
    manifest["artifact_paths"].append(str(out_path))
    write_manifest(manifest, out_path)
    append_run_log(run_log, manifest)
    return out_path


def _build_report(
    manifests: List[Dict[str, Any]],
    args: argparse.Namespace,
    panel_items: List[Dict[str, Any]],
    report_md: Path,
    report_json: Path,
) -> None:
    confidence_level = float(args.confidence_level)
    if confidence_level <= 0.0 or confidence_level >= 1.0:
        raise RuntimeError("--confidence-level must be between 0 and 1 (exclusive)")

    z_score = NormalDist().inv_cdf((1.0 + confidence_level) / 2.0)
    alpha = 1.0 - confidence_level
    lower_q = alpha / 2.0
    upper_q = 1.0 - alpha / 2.0

    def wilson_interval(successes: int, n: int) -> Tuple[float, float]:
        if n <= 0:
            return 0.0, 0.0
        p_hat = successes / n
        denom = 1.0 + (z_score * z_score) / n
        center = (p_hat + (z_score * z_score) / (2.0 * n)) / denom
        half = (
            z_score
            * math.sqrt((p_hat * (1.0 - p_hat) / n) + ((z_score * z_score) / (4.0 * n * n)))
            / denom
        )
        return max(0.0, center - half), min(1.0, center + half)

    def exact_mcnemar_p(a_better: int, b_better: int) -> float:
        n = a_better + b_better
        if n == 0:
            return 1.0
        k = min(a_better, b_better)
        tail = sum(math.comb(n, i) for i in range(0, k + 1)) / (2**n)
        return min(1.0, 2.0 * tail)

    def percentile(sorted_values: List[float], q: float) -> float:
        if not sorted_values:
            return 0.0
        if len(sorted_values) == 1:
            return sorted_values[0]
        pos = q * (len(sorted_values) - 1)
        lo = int(math.floor(pos))
        hi = int(math.ceil(pos))
        if lo == hi:
            return sorted_values[lo]
        weight = pos - lo
        return sorted_values[lo] * (1.0 - weight) + sorted_values[hi] * weight

    by_condition_successes: Dict[str, int] = {}
    by_condition_runs: Dict[str, int] = {}
    for manifest in manifests:
        condition_id = str(manifest.get("condition_id", ""))
        success = int(manifest.get("metrics", {}).get("success", 0))
        by_condition_runs[condition_id] = by_condition_runs.get(condition_id, 0) + 1
        by_condition_successes[condition_id] = by_condition_successes.get(condition_id, 0) + success

    summaries = summarize_by_condition(manifests)
    generated_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    # Pairwise success deltas at item level.
    by_item: Dict[str, Dict[str, int]] = {}
    for manifest in manifests:
        item_id = str(manifest.get("item_id", ""))
        condition_id = str(manifest.get("condition_id", ""))
        if not item_id:
            continue
        by_item.setdefault(item_id, {})[condition_id] = int(manifest.get("metrics", {}).get("success", 0))

    paired_rows: List[Dict[str, Any]] = []
    condition_ids = sorted({str(manifest.get("condition_id", "")) for manifest in manifests})
    rng = random.Random(int(args.bootstrap_seed))
    for i, c1 in enumerate(condition_ids):
        for c2 in condition_ids[i + 1 :]:
            matched = 0
            c1_better = 0
            c2_better = 0
            ties = 0
            diffs: List[int] = []
            for item_id, values in by_item.items():
                if c1 not in values or c2 not in values:
                    continue
                matched += 1
                v1 = values[c1]
                v2 = values[c2]
                diffs.append(v1 - v2)
                if v1 > v2:
                    c1_better += 1
                elif v2 > v1:
                    c2_better += 1
                else:
                    ties += 1
            delta = (c1_better - c2_better) / matched if matched else 0.0

            boot_means: List[float] = []
            if matched > 0 and int(args.bootstrap_samples) > 0:
                for _ in range(int(args.bootstrap_samples)):
                    sample_sum = 0
                    for _ in range(matched):
                        sample_sum += diffs[rng.randrange(matched)]
                    boot_means.append(sample_sum / matched)
            boot_means.sort()
            delta_ci_low = percentile(boot_means, lower_q) if boot_means else 0.0
            delta_ci_high = percentile(boot_means, upper_q) if boot_means else 0.0

            p_value = exact_mcnemar_p(c1_better, c2_better)
            paired_rows.append(
                {
                    "condition_a": c1,
                    "condition_b": c2,
                    "matched_items": matched,
                    "a_better": c1_better,
                    "b_better": c2_better,
                    "ties": ties,
                    "discordant_pairs": c1_better + c2_better,
                    "delta_success_rate": round(delta, 6),
                    "delta_ci_low": round(delta_ci_low, 6),
                    "delta_ci_high": round(delta_ci_high, 6),
                    "mcnemar_p_value": p_value,
                }
            )

    # Holm-Bonferroni correction over pairwise tests.
    order = sorted(range(len(paired_rows)), key=lambda idx: paired_rows[idx]["mcnemar_p_value"])
    adjusted = [0.0] * len(paired_rows)
    running_max = 0.0
    m_tests = len(paired_rows)
    for rank, idx in enumerate(order, start=1):
        raw = float(paired_rows[idx]["mcnemar_p_value"])
        corrected = min(1.0, raw * (m_tests - rank + 1))
        running_max = max(running_max, corrected)
        adjusted[idx] = running_max
    for idx, value in enumerate(adjusted):
        paired_rows[idx]["mcnemar_p_holm"] = value

    report_md.parent.mkdir(parents=True, exist_ok=True)
    report_json.parent.mkdir(parents=True, exist_ok=True)

    md_lines = [
        "# Game24 Lockset Report",
        "",
        f"Generated UTC: {generated_utc}",
        f"Panel ID: {args.panel_id}",
        f"Provider: {args.provider}",
        f"Model: {args.model_id or 'default'}",
        f"ToT evaluator mode: {args.tot_evaluator_mode}",
        f"ToT search settings: depth={args.tot_max_depth}, branch_factor={args.tot_branch_factor}, frontier_width={args.tot_frontier_width}",
        f"Seed policy: {args.seed_policy}",
        f"HF temperature: {args.hf_temperature}",
        f"HF top-p: {args.hf_top_p}",
        f"Capability parity policy: {getattr(args, 'capability_parity_policy', 'unknown')}",
        f"Task tools available: {', '.join(getattr(args, 'task_tools_available', [])) or 'none'}",
        (
            "Condition tools exposed: "
            + "; ".join(
                f"{name}=[{', '.join(tools) if tools else 'none'}]"
                for name, tools in sorted(getattr(args, "condition_tools_map", {}).items())
            )
            if getattr(args, "condition_tools_map", None)
            else "Condition tools exposed: unknown"
        ),
        f"Items evaluated: {len(panel_items)}",
        f"Runs executed: {len(manifests)}",
        f"Confidence level: {args.confidence_level:.2f}",
        "",
        "## Condition Summary",
        "",
        "| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |",
        "|---|---:|---:|---:|---|---:|---:|---:|",
    ]
    for summary in summaries:
        condition_id = summary["condition_id"]
        runs = int(by_condition_runs.get(condition_id, summary["runs"]))
        successes = int(by_condition_successes.get(condition_id, round(summary["success_rate"] * runs)))
        ci_low, ci_high = wilson_interval(successes=successes, n=runs)
        md_lines.append(
            "| {condition} | {runs} | {successes} | {success:.3f} | [{ci_low:.3f}, {ci_high:.3f}] | {lat_mean:.1f} | {tin_mean:.1f} | {tout_mean:.1f} |".format(
                condition=condition_id,
                runs=runs,
                successes=successes,
                success=summary["success_rate"],
                ci_low=ci_low,
                ci_high=ci_high,
                lat_mean=summary["latency_ms_mean"],
                tin_mean=summary["tokens_in_mean"],
                tout_mean=summary["tokens_out_mean"],
            )
        )

    md_lines.extend(
        [
            "",
            "## Paired Success Comparison",
            "",
            "| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |",
            "|---|---|---:|---:|---:|---:|---:|---|---:|---:|",
        ]
    )
    def fmt_p(p: float) -> str:
        return f"{p:.2e}" if p < 1e-4 else f"{p:.6f}"

    for row in paired_rows:
        md_lines.append(
            "| {a} | {b} | {n} | {ab} | {bb} | {t} | {d:.3f} | [{dl:.3f}, {dh:.3f}] | {p} | {ph} |".format(
                a=row["condition_a"],
                b=row["condition_b"],
                n=row["matched_items"],
                ab=row["a_better"],
                bb=row["b_better"],
                t=row["ties"],
                d=row["delta_success_rate"],
                dl=row["delta_ci_low"],
                dh=row["delta_ci_high"],
                p=fmt_p(float(row["mcnemar_p_value"])),
                ph=fmt_p(float(row["mcnemar_p_holm"])),
            )
        )

    md_lines.extend(
        [
            "",
            "## Notes",
            "- This is a paired-condition report; each row compares outcomes on shared item IDs only.",
            "- Small item slices are for protocol validation; full locksets are the primary panel summary.",
        ]
    )

    report_md.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    report_json.write_text(
        json.dumps(
            {
                "generated_utc": generated_utc,
                "panel_id": args.panel_id,
                "provider": args.provider,
                "model_id": args.model_id,
                "tot_evaluator_mode": args.tot_evaluator_mode,
                "tot_max_depth": args.tot_max_depth,
                "tot_branch_factor": args.tot_branch_factor,
                "tot_frontier_width": args.tot_frontier_width,
                "seed_policy": args.seed_policy,
                "hf_temperature": args.hf_temperature,
                "hf_top_p": args.hf_top_p,
                "capability_parity_policy": getattr(args, "capability_parity_policy", "unknown"),
                "task_tools_available": list(getattr(args, "task_tools_available", [])),
                "condition_tools_exposed": getattr(args, "condition_tools_map", {}),
                "confidence_level": args.confidence_level,
                "bootstrap_samples": args.bootstrap_samples,
                "bootstrap_seed": args.bootstrap_seed,
                "items_evaluated": len(panel_items),
                "runs_executed": len(manifests),
                "condition_summaries": summaries,
                "paired_comparison": paired_rows,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    args = parse_args()
    panel_id, panel_items = _load_panel(Path(args.panel_file))
    args.panel_id = panel_id

    selected = _slice_items(panel_items, args.offset, args.limit)
    if not selected:
        print("error: selected item slice is empty")
        return 2

    raw_conditions = [name.strip() for name in args.conditions.split(",") if name.strip()]
    try:
        conditions = _normalize_condition_aliases(raw_conditions)
    except RuntimeError as exc:
        print(f"error: {exc}")
        return 2

    try:
        capability_plan = _resolve_capability_plan(
            conditions=conditions,
            policy=args.capability_parity_policy,
        )
    except RuntimeError as exc:
        print(f"error: {exc}")
        return 2

    args.task_tools_available = list(capability_plan["task_tools"])
    args.condition_tools_map = dict(capability_plan["condition_tools"])
    args.react_enable_tools = bool(capability_plan["react_enable_tools"])
    print(f"capability_parity_policy={args.capability_parity_policy}")
    print(f"task_tools_available={args.task_tools_available}")
    print(f"condition_tools_exposed={args.condition_tools_map}")
    if capability_plan["adjustments"]:
        print(f"capability_parity_adjustments={capability_plan['adjustments']}")

    runs_dir = Path(args.runs_dir)
    run_log = Path(args.run_log)

    manifests: List[Dict[str, Any]] = []
    if args.report_only:
        manifests = _load_latest_existing_manifests(
            runs_dir=runs_dir,
            panel_id=args.panel_id,
            selected_items=selected,
            conditions=conditions,
        )
        _build_report(
            manifests=manifests,
            args=args,
            panel_items=selected,
            report_md=Path(args.report_md),
            report_json=Path(args.report_json),
        )
        print(f"report_md={args.report_md}")
        print(f"report_json={args.report_json}")
        return 0

    def _run_item(item_index: int, item: Dict[str, Any]) -> List[Dict[str, Any]]:
        seed = _seed_for_item(
            item_id=str(item["item_id"]),
            item_index=item_index,
            seed_policy=str(args.seed_policy),
        )
        item_manifests: List[Dict[str, Any]] = []
        for condition in conditions:
            if condition in {"single", "react"}:
                manifest = _run_single_or_react(
                    condition=condition,
                    item=item,
                    seed=seed,
                    args=args,
                    react_enable_tools=bool(args.react_enable_tools),
                    condition_tools=dict(args.condition_tools_map),
                )
            else:
                manifest = _run_tot(
                    item=item,
                    seed=seed,
                    args=args,
                    condition_tools=dict(args.condition_tools_map),
                )
            item_manifests.append(manifest)
        return item_manifests

    max_workers = max(1, int(args.max_workers))
    if max_workers == 1:
        for item_index, item in enumerate(selected):
            try:
                for manifest in _run_item(item_index=item_index, item=item):
                    out_path = _write_manifest_and_log(manifest, runs_dir, run_log)
                    manifests.append(manifest)
                    print(
                        f"item={item['item_id']} condition={manifest['condition_id']} "
                        f"run_id={manifest['run_id']} outcome={manifest['outcome']} path={out_path}"
                    )
            except Exception as exc:
                print(f"error: item={item['item_id']}: {exc}")
                return 2
    else:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_map = {
                executor.submit(_run_item, item_index, item): (item_index, item)
                for item_index, item in enumerate(selected)
            }
            for future in as_completed(future_map):
                item_index, item = future_map[future]
                try:
                    item_manifests = future.result()
                except Exception as exc:
                    print(f"error: item={item['item_id']} index={item_index}: {exc}")
                    return 2

                for manifest in item_manifests:
                    out_path = _write_manifest_and_log(manifest, runs_dir, run_log)
                    manifests.append(manifest)
                    print(
                        f"item={item['item_id']} condition={manifest['condition_id']} "
                        f"run_id={manifest['run_id']} outcome={manifest['outcome']} path={out_path}"
                    )

    _build_report(
        manifests=manifests,
        args=args,
        panel_items=selected,
        report_md=Path(args.report_md),
        report_json=Path(args.report_json),
    )
    print(f"report_md={args.report_md}")
    print(f"report_json={args.report_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
