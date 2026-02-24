#!/usr/bin/env python3
"""Run paired lockset panels across baseline and ToT conditions for registered tasks."""

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
from phase2_baselines.catalog import (
    CONDITION_FAMILY_BASELINE_CHAIN_OF_THOUGHT_REASONING,
    CONDITION_FAMILY_BASELINE_CHAIN_OF_THOUGHT_SELF_CONSISTENCY_REASONING,
    CONDITION_FAMILY_BASELINE_REACT_CODE_AGENT_WITH_TASK_TOOLS,
    CONDITION_FAMILY_BASELINE_REACT_REASONING_TEXT_LOOP_NO_TOOLS,
    DEFAULT_STRUCTURED_LOCKSET_CANONICAL_KEYS,
    EXECUTION_SURFACE_PROMPT_REASONING_LOOP_V1,
    EXECUTION_SURFACE_SMOLAGENTS_CODE_AGENT_WITH_TASK_TOOLS_V1,
    MATRIX_A_REASONING_ONLY_CANONICAL_KEYS,
    MEMORY_SURFACE_ITEM_STATELESS_V1,
    TOOL_SURFACE_NO_TOOLS_V1,
    TOOL_SURFACE_TASK_REGISTERED_TOOLS_V1,
    TOT_VARIANT_TREE_OF_THOUGHTS_GENERALIZED_RECURSIVE_V1,
    ConditionSpec,
    condition_names,
    resolve_conditions,
)
from phase2_baselines.manifest import append_run_log, write_manifest
from phase2_baselines.pipeline import create_baseline_setup
from phase2_baselines.reporting import summarize_by_condition
from phase2_baselines.runners.tot import ToTRunner
from phase2_baselines.tasks import create_task, resolve_task_id, supported_tasks


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run paired lockset panel for a registered task")
    parser.add_argument(
        "--task-id",
        default="game24-demo",
        help=f"Registered task id/alias. Supported: {', '.join(supported_tasks())}",
    )
    parser.add_argument(
        "--panel-file",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/panels/game24_lockset_v1.json",
        help="JSON panel file with item_id + input_data entries",
    )
    parser.add_argument(
        "--conditions",
        default=",".join(DEFAULT_STRUCTURED_LOCKSET_CANONICAL_KEYS),
        help=(
            "Comma-separated condition keys/aliases from catalog "
            f"({','.join(condition_names())})"
        ),
    )
    parser.add_argument("--provider", choices=["smolagents"], default="smolagents")
    parser.add_argument("--model-id", default="", help="Model identifier for --provider smolagents")
    parser.add_argument("--hf-token-env", default="HF_TOKEN", help="Env var name for Hugging Face API token")
    parser.add_argument("--hf-timeout-seconds", type=int, default=120)
    parser.add_argument("--hf-max-new-tokens", type=int, default=192)
    parser.add_argument("--hf-temperature", type=float, default=0.0)
    parser.add_argument("--hf-top-p", type=float, default=1.0)
    parser.add_argument(
        "--cot-temperature",
        type=float,
        default=0.0,
        help="Sampling temperature for CoT baseline.",
    )
    parser.add_argument(
        "--cot-sc-temperature",
        type=float,
        default=0.7,
        help="Sampling temperature for CoT-SC baseline (scholarly self-consistency anchor).",
    )
    parser.add_argument(
        "--react-temperature",
        type=float,
        default=0.0,
        help="Sampling temperature for ReAct baseline.",
    )
    parser.add_argument("--cot-sc-samples", type=int, default=10, help="Sample count for cot_sc baseline")
    parser.add_argument(
        "--cot-sc-parallel-workers",
        type=int,
        default=0,
        help=(
            "Parallel workers for CoT-SC sample generation per item. "
            "0=auto (smolagents: cot_sc_samples)."
        ),
    )
    parser.add_argument(
        "--cot-answer-recovery",
        action="store_true",
        help="Enable non-scholarly answer-recovery pass for CoT/CoT-SC (default: off).",
    )
    parser.add_argument(
        "--tot-evaluator-mode",
        choices=["task_binary", "rule_based", "model_self_eval", "hybrid"],
        default="model_self_eval",
    )
    parser.add_argument(
        "--tot-mode",
        choices=["model_decompose_search"],
        default="model_decompose_search",
        help="ToT execution mode. model_decompose_search is the generic decomposition-first tree search.",
    )
    parser.add_argument(
        "--tot-gen-mode",
        choices=["model_decompose_search"],
        default="model_decompose_search",
        help="ToT-gen execution mode used when condition list includes tot_gen.",
    )
    parser.add_argument(
        "--tot-decomposition-rounds",
        type=int,
        default=1,
        help="Number of decomposition seeding rounds before normal ToT expansion.",
    )
    parser.add_argument("--tot-max-depth", type=int, default=3)
    parser.add_argument(
        "--tot-legacy-max-depth",
        type=int,
        default=-1,
        help="Override max depth for legacy ToT condition (tot). Use <=0 to fall back to --tot-max-depth.",
    )
    parser.add_argument(
        "--tot-gen-max-depth",
        type=int,
        default=-1,
        help="Override max depth for ToT-gen condition (tot_gen). Use <=0 to fall back to --tot-max-depth.",
    )
    parser.add_argument("--tot-branch-factor", type=int, default=3)
    parser.add_argument("--tot-frontier-width", type=int, default=3)
    parser.add_argument(
        "--capability-parity-policy",
        choices=["equalize_react_to_tot", "strict", "off"],
        default="equalize_react_to_tot",
        help=(
            "How to handle capability mismatch when paired react/tot or react/tot_gen conditions are selected. "
            "equalize_react_to_tot disables React tools to match current ToT access; "
            "strict fails fast on mismatch; off allows mismatch."
        ),
    )
    parser.add_argument(
        "--parity-profile",
        choices=["off", "matrix_a_reasoning_only"],
        default="off",
        help=(
            "Optional hard-fail parity profile. "
            "matrix_a_reasoning_only enforces prompt-loop execution and no tools for every selected condition."
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
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/structured_lockset_report.md",
        help="Markdown report output",
    )
    parser.add_argument(
        "--report-json",
        default="/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/structured_lockset_report.json",
        help="JSON report output",
    )
    return parser.parse_args()


def _load_panel(path: Path) -> Tuple[str, str | None, List[Dict[str, Any]]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError("Panel file must be an object with panel_id + items")
    panel_id = str(payload.get("panel_id", "lockset-unknown")).strip()
    panel_task_id = payload.get("task_id")
    if panel_task_id is not None:
        panel_task_id = str(panel_task_id).strip()
    items = payload.get("items", [])
    if not isinstance(items, list) or not items:
        raise RuntimeError("Panel file has no items")

    normalized: List[Dict[str, Any]] = []
    for idx, item in enumerate(items):
        if not isinstance(item, dict):
            raise RuntimeError(f"Invalid item at index {idx}")
        item_id = str(item.get("item_id", "")).strip() or f"item-{idx+1:04d}"
        input_data = item.get("input_data")
        if input_data is None and "numbers" in item:
            input_data = item.get("numbers")
        if input_data is None:
            raise RuntimeError(f"Item {item_id} must include input_data")
        normalized.append(
            {
                "item_id": item_id,
                "input_data": input_data,
                "oracle_solution": str(item.get("oracle_solution", "")).strip(),
            }
        )
    return panel_id, panel_task_id, normalized


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


def _enforce_parity_profile(
    *,
    parity_profile: str,
    condition_specs: List[ConditionSpec],
    condition_tools: Dict[str, List[str]],
) -> None:
    if parity_profile == "off":
        return

    issues: List[str] = []
    if parity_profile == "matrix_a_reasoning_only":
        required = set(MATRIX_A_REASONING_ONLY_CANONICAL_KEYS)
        selected = {spec.condition_key for spec in condition_specs}
        if selected != required:
            issues.append(
                "matrix_a_reasoning_only requires exact condition set "
                f"{sorted(required)}; got {sorted(selected)}"
            )

        for spec in condition_specs:
            if spec.execution_surface_id != EXECUTION_SURFACE_PROMPT_REASONING_LOOP_V1:
                issues.append(
                    f"{spec.key} execution_surface_id={spec.execution_surface_id} is not prompt-loop"
                )
            if spec.tool_surface_id != TOOL_SURFACE_NO_TOOLS_V1:
                issues.append(
                    f"{spec.key} tool_surface_id={spec.tool_surface_id} is not no-tools"
                )
            if condition_tools.get(spec.key):
                issues.append(f"{spec.key} exposes tools {condition_tools[spec.key]}; expected no tools")
            if spec.memory_surface_id != MEMORY_SURFACE_ITEM_STATELESS_V1:
                issues.append(
                    f"{spec.key} memory_surface_id={spec.memory_surface_id} is not item-stateless"
                )

    if issues:
        joined = "; ".join(issues)
        raise RuntimeError(f"parity profile `{parity_profile}` failed: {joined}")


def _resolve_capability_plan(
    task_id: str,
    condition_specs: List[ConditionSpec],
    policy: str,
    parity_profile: str,
) -> Dict[str, Any]:
    task = create_task(task_id)
    task_tools = sorted(task.available_tools().keys())

    condition_tools: Dict[str, List[str]] = {}
    condition_surfaces: Dict[str, Dict[str, str]] = {}
    adjustments: List[str] = []

    for spec in condition_specs:
        tools = list(task_tools) if spec.tool_surface_id == TOOL_SURFACE_TASK_REGISTERED_TOOLS_V1 else []
        condition_tools[spec.key] = tools
        condition_surfaces[spec.key] = {
            "condition_id": spec.condition_id,
            "algorithm_id": spec.algorithm_id,
            "algorithm_module_id": spec.algorithm_module_id,
            "execution_surface_id": spec.execution_surface_id,
            "tool_surface_id": spec.tool_surface_id,
            "memory_surface_id": spec.memory_surface_id,
            "react_execution_mode": spec.react_execution_mode or "",
            "tot_variant": spec.tot_variant or "",
        }

    react_codeagent_keys = [
        spec.key
        for spec in condition_specs
        if spec.execution_surface_id == EXECUTION_SURFACE_SMOLAGENTS_CODE_AGENT_WITH_TASK_TOOLS_V1
    ]
    tot_selected = any(bool(spec.tot_variant) for spec in condition_specs)
    if react_codeagent_keys and tot_selected:
        for react_key in react_codeagent_keys:
            react_tools = list(condition_tools.get(react_key, []))
            tot_tools = []
            if react_tools != tot_tools:
                if policy == "strict":
                    raise RuntimeError(
                        "capability parity violation: "
                        f"{react_key} exposes tools {react_tools} while ToT conditions expose {tot_tools}."
                    )
                if policy == "equalize_react_to_tot":
                    condition_tools[react_key] = list(tot_tools)
                    adjustments.append(f"{react_key}_tools_disabled_to_match_tot")
                else:
                    adjustments.append(f"{react_key}_tool_mismatch_allowed_by_policy_off")

    _enforce_parity_profile(
        parity_profile=parity_profile,
        condition_specs=condition_specs,
        condition_tools=condition_tools,
    )

    react_enable_tools_by_condition: Dict[str, bool] = {}
    for spec in condition_specs:
        if spec.react_execution_mode is not None:
            react_enable_tools_by_condition[spec.key] = bool(condition_tools.get(spec.key, []))

    return {
        "task_tools": task_tools,
        "condition_tools": condition_tools,
        "condition_surfaces": condition_surfaces,
        "react_enable_tools_by_condition": react_enable_tools_by_condition,
        "adjustments": adjustments,
    }


def _parse_utc(timestamp_utc: str) -> datetime:
    return datetime.fromisoformat(timestamp_utc.replace("Z", "+00:00"))


def _load_latest_existing_manifests(
    runs_dir: Path,
    panel_id: str,
    task_id: str,
    selected_items: List[Dict[str, Any]],
    condition_specs: List[ConditionSpec],
) -> List[Dict[str, Any]]:
    item_ids = {item["item_id"] for item in selected_items}
    target_conditions = {spec.condition_id for spec in condition_specs}

    latest: Dict[Tuple[str, str], Dict[str, Any]] = {}
    for path in sorted(runs_dir.glob("*.json")):
        try:
            manifest = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if str(manifest.get("panel_id", "")) != panel_id:
            continue
        if str(manifest.get("task_id", "")) != task_id:
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


def _run_baseline_condition(
    condition_spec: ConditionSpec,
    item: Dict[str, Any],
    seed: int,
    args: argparse.Namespace,
    react_enable_tools: bool,
    condition_tools: Dict[str, List[str]],
) -> Dict[str, Any]:
    condition_temperature = float(args.hf_temperature)
    if condition_spec.condition_family_id == CONDITION_FAMILY_BASELINE_CHAIN_OF_THOUGHT_REASONING:
        condition_temperature = float(args.cot_temperature)
    elif (
        condition_spec.condition_family_id
        == CONDITION_FAMILY_BASELINE_CHAIN_OF_THOUGHT_SELF_CONSISTENCY_REASONING
    ):
        condition_temperature = float(args.cot_sc_temperature)
    elif condition_spec.condition_family_id in {
        CONDITION_FAMILY_BASELINE_REACT_CODE_AGENT_WITH_TASK_TOOLS,
        CONDITION_FAMILY_BASELINE_REACT_REASONING_TEXT_LOOP_NO_TOOLS,
    }:
        condition_temperature = float(args.react_temperature)

    runner, task, config = create_baseline_setup(
        runner_name=condition_spec.runner_name,
        seed=seed,
        provider=args.provider,
        task_name=args.task_id,
        model_id=args.model_id or None,
        hf_token_env=args.hf_token_env,
        hf_timeout_seconds=args.hf_timeout_seconds,
        hf_max_new_tokens=args.hf_max_new_tokens,
        hf_temperature=condition_temperature,
        hf_top_p=args.hf_top_p,
        react_enable_tools=react_enable_tools,
        react_execution_mode=condition_spec.react_execution_mode,
        cot_sc_samples=args.cot_sc_samples,
        cot_sc_parallel_workers=args.cot_sc_parallel_workers,
        cot_answer_recovery=bool(args.cot_answer_recovery),
        react_strict_mode=True,
    )
    config["condition_id"] = condition_spec.condition_id
    config["condition_key"] = condition_spec.key
    config["algorithm_id"] = condition_spec.algorithm_id
    config["algorithm_module_id"] = condition_spec.algorithm_module_id
    config["execution_surface_id"] = condition_spec.execution_surface_id
    config["tool_surface_id"] = condition_spec.tool_surface_id
    config["memory_surface_id"] = condition_spec.memory_surface_id
    config["parity_profile_id"] = args.parity_profile
    config["item_id"] = item["item_id"]
    config["input_data"] = item["input_data"]
    config["panel_id"] = args.panel_id
    config["hf_temperature"] = condition_temperature
    config["hf_top_p"] = args.hf_top_p
    config["capability_parity_policy"] = args.capability_parity_policy
    config["task_tools_available"] = list(getattr(args, "task_tools_available", []))
    config["condition_tools_exposed"] = list(condition_tools.get(condition_spec.key, []))
    if (
        condition_spec.condition_family_id
        == CONDITION_FAMILY_BASELINE_CHAIN_OF_THOUGHT_SELF_CONSISTENCY_REASONING
    ):
        config["cot_sc_samples"] = int(args.cot_sc_samples)
        config["cot_sc_parallel_workers"] = int(config.get("cot_sc_parallel_workers", 1))
    # Ensure manifest tool_config exactly mirrors the enforced condition exposure.
    config["tool_config"] = list(condition_tools.get(condition_spec.key, []))
    runner.prepare(task=task, config=config)
    return runner.run(item["input_data"])


def _run_tot(
    condition_spec: ConditionSpec,
    item: Dict[str, Any],
    seed: int,
    args: argparse.Namespace,
    condition_tools: Dict[str, List[str]],
) -> Dict[str, Any]:
    task = create_task(args.task_id)
    model, model_name, provider_name = _build_model(args)
    runner = ToTRunner(model=model, model_name=model_name, provider=provider_name)
    condition_id = condition_spec.condition_id
    tot_mode = args.tot_mode
    max_depth = int(args.tot_max_depth)
    if condition_spec.tot_variant == TOT_VARIANT_TREE_OF_THOUGHTS_GENERALIZED_RECURSIVE_V1:
        tot_mode = args.tot_gen_mode
        if int(args.tot_gen_max_depth) > 0:
            max_depth = int(args.tot_gen_max_depth)
    elif int(args.tot_legacy_max_depth) > 0:
        max_depth = int(args.tot_legacy_max_depth)
    runner.prepare(
        task=task,
        config={
            "condition_id": condition_id,
            "prompt_template_version": "v1",
            "search_config": {
                "depth": max_depth,
                "breadth": args.tot_branch_factor,
                "pruning": "topk_cumulative_score",
                "stop_policy": "first_terminal_or_depth_limit",
            },
            "tool_config": list(condition_tools.get(condition_spec.key, [])),
            "budget": {"token_budget": 4000, "time_budget_ms": 15000, "cost_budget_usd": 0.0},
            "seed": seed,
            "max_depth": max_depth,
            "branch_factor": args.tot_branch_factor,
            "frontier_width": args.tot_frontier_width,
            "evaluator_mode": args.tot_evaluator_mode,
            "tot_mode": tot_mode,
            "decomposition_rounds": args.tot_decomposition_rounds,
            "hf_temperature": args.hf_temperature,
            "hf_top_p": args.hf_top_p,
            "item_id": item["item_id"],
            "input_data": item["input_data"],
            "panel_id": args.panel_id,
            "capability_parity_policy": args.capability_parity_policy,
            "task_tools_available": list(getattr(args, "task_tools_available", [])),
            "condition_tools_exposed": list(condition_tools.get(condition_spec.key, [])),
            "tot_variant": condition_spec.tot_variant or "",
            "condition_key": condition_spec.key,
            "algorithm_id": condition_spec.algorithm_id,
            "algorithm_module_id": condition_spec.algorithm_module_id,
            "execution_surface_id": condition_spec.execution_surface_id,
            "tool_surface_id": condition_spec.tool_surface_id,
            "memory_surface_id": condition_spec.memory_surface_id,
            "parity_profile_id": args.parity_profile,
        },
    )
    return runner.run(item["input_data"])


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

    def _condition_key(manifest: Dict[str, Any]) -> str:
        key = str(manifest.get("condition_key", "")).strip()
        if key:
            return key
        return str(manifest.get("condition_id", "")).strip()

    by_condition_successes: Dict[str, int] = {}
    by_condition_runs: Dict[str, int] = {}
    summary_manifests: List[Dict[str, Any]] = []
    condition_id_by_key: Dict[str, str] = {}

    for condition_key, surface in sorted(getattr(args, "condition_surfaces", {}).items()):
        legacy_condition_id = str(surface.get("condition_id", "")).strip()
        if condition_key and legacy_condition_id:
            condition_id_by_key[condition_key] = legacy_condition_id

    for manifest in manifests:
        condition_key = _condition_key(manifest)
        legacy_condition_id = str(manifest.get("condition_id", "")).strip()
        success = int(manifest.get("metrics", {}).get("success", 0))
        by_condition_runs[condition_key] = by_condition_runs.get(condition_key, 0) + 1
        by_condition_successes[condition_key] = by_condition_successes.get(condition_key, 0) + success
        if condition_key and legacy_condition_id and condition_key not in condition_id_by_key:
            condition_id_by_key[condition_key] = legacy_condition_id

        summary_manifest = dict(manifest)
        # Summary grouping must be keyed by canonical atomic condition key.
        summary_manifest["condition_id"] = condition_key
        summary_manifests.append(summary_manifest)

    summaries = summarize_by_condition(summary_manifests)
    generated_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    by_item: Dict[str, Dict[str, int]] = {}
    for manifest in manifests:
        item_id = str(manifest.get("item_id", ""))
        condition_key = _condition_key(manifest)
        if not item_id:
            continue
        by_item.setdefault(item_id, {})[condition_key] = int(manifest.get("metrics", {}).get("success", 0))

    paired_rows: List[Dict[str, Any]] = []
    condition_keys = sorted(by_condition_runs.keys())
    rng = random.Random(int(args.bootstrap_seed))
    for i, c1 in enumerate(condition_keys):
        for c2 in condition_keys[i + 1 :]:
            matched = 0
            c1_better = 0
            c2_better = 0
            ties = 0
            diffs: List[int] = []
            # Deterministic item ordering prevents order-sensitive bootstrap drift
            # between execution-time and report-only rebuilds.
            for item_id in sorted(by_item.keys()):
                values = by_item[item_id]
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
                    "condition_a_key": c1,
                    "condition_b_key": c2,
                    "condition_a_id": condition_id_by_key.get(c1, ""),
                    "condition_b_id": condition_id_by_key.get(c2, ""),
                    # Backward-compatible fields retained; values now map to canonical keys.
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
        "# Structured Lockset Report",
        "",
        f"Generated UTC: {generated_utc}",
        f"Task ID: {args.task_id}",
        f"Panel ID: {args.panel_id}",
        f"Provider: {args.provider}",
        f"Model: {args.model_id or 'default'}",
        f"ToT evaluator mode: {args.tot_evaluator_mode}",
        f"ToT mode: {args.tot_mode}",
        f"ToT-gen mode: {args.tot_gen_mode}",
        f"ToT decomposition rounds: {args.tot_decomposition_rounds}",
        f"ToT search settings: depth={args.tot_max_depth}, branch_factor={args.tot_branch_factor}, frontier_width={args.tot_frontier_width}",
        (
            "ToT per-condition depth overrides: "
            f"legacy={args.tot_legacy_max_depth if int(args.tot_legacy_max_depth) > 0 else 'base'}, "
            f"gen={args.tot_gen_max_depth if int(args.tot_gen_max_depth) > 0 else 'base'}"
        ),
        f"Seed policy: {args.seed_policy}",
        f"HF temperature: {args.hf_temperature}",
        f"CoT temperature: {args.cot_temperature}",
        f"CoT-SC temperature: {args.cot_sc_temperature}",
        f"ReAct temperature: {args.react_temperature}",
        f"HF top-p: {args.hf_top_p}",
        f"Capability parity policy: {getattr(args, 'capability_parity_policy', 'unknown')}",
        f"Parity profile: {getattr(args, 'parity_profile', 'off')}",
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
        (
            "Condition surfaces: "
            + "; ".join(
                (
                    f"{name}=(cond_id:{surface.get('condition_id','')},"
                    f"alg:{surface.get('algorithm_id','')},"
                    f"exec:{surface.get('execution_surface_id','')},"
                    f"tools:{surface.get('tool_surface_id','')},"
                    f"memory:{surface.get('memory_surface_id','')})"
                )
                for name, surface in sorted(getattr(args, "condition_surfaces", {}).items())
            )
            if getattr(args, "condition_surfaces", None)
            else "Condition surfaces: unknown"
        ),
        f"Items evaluated: {len(panel_items)}",
        f"Runs executed: {len(manifests)}",
        f"Confidence level: {args.confidence_level:.2f}",
        "",
        "## Condition Summary",
        "",
        "| Condition Key | Condition ID | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |",
        "|---|---|---:|---:|---:|---|---:|---:|---:|",
    ]
    for summary in summaries:
        condition_key = summary["condition_id"]
        legacy_condition_id = condition_id_by_key.get(condition_key, "")
        runs = int(by_condition_runs.get(condition_key, summary["runs"]))
        successes = int(by_condition_successes.get(condition_key, round(summary["success_rate"] * runs)))
        ci_low, ci_high = wilson_interval(successes=successes, n=runs)
        md_lines.append(
            "| {condition_key} | {condition_id} | {runs} | {successes} | {success:.3f} | [{ci_low:.3f}, {ci_high:.3f}] | {lat_mean:.1f} | {tin_mean:.1f} | {tout_mean:.1f} |".format(
                condition_key=condition_key,
                condition_id=legacy_condition_id or "-",
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
            "| Condition A Key | Condition A ID | Condition B Key | Condition B ID | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |",
            "|---|---|---|---|---:|---:|---:|---:|---:|---|---:|---:|",
        ]
    )

    def fmt_p(p: float) -> str:
        return f"{p:.2e}" if p < 1e-4 else f"{p:.6f}"

    for row in paired_rows:
        md_lines.append(
            "| {a_key} | {a_id} | {b_key} | {b_id} | {n} | {ab} | {bb} | {t} | {d:.3f} | [{dl:.3f}, {dh:.3f}] | {p} | {ph} |".format(
                a_key=row["condition_a_key"],
                a_id=row["condition_a_id"] or "-",
                b_key=row["condition_b_key"],
                b_id=row["condition_b_id"] or "-",
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
            "- Claims remain scoped to the specified task/panel/model configuration.",
        ]
    )

    report_md.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    condition_summaries_out: List[Dict[str, Any]] = []
    for summary in summaries:
        condition_key = str(summary["condition_id"])
        legacy_condition_id = condition_id_by_key.get(condition_key, "")
        condition_summaries_out.append(
            {
                "condition_key": condition_key,
                "condition_id": legacy_condition_id or condition_key,
                "condition_id_legacy": legacy_condition_id,
                "runs": summary["runs"],
                "success_rate": summary["success_rate"],
                "latency_ms_mean": summary["latency_ms_mean"],
                "latency_ms_std": summary["latency_ms_std"],
                "tokens_in_mean": summary["tokens_in_mean"],
                "tokens_in_std": summary["tokens_in_std"],
                "tokens_out_mean": summary["tokens_out_mean"],
                "tokens_out_std": summary["tokens_out_std"],
                "cost_usd_mean": summary["cost_usd_mean"],
                "cost_usd_std": summary["cost_usd_std"],
            }
        )
    report_json.write_text(
        json.dumps(
            {
                "generated_utc": generated_utc,
                "task_id": args.task_id,
                "panel_id": args.panel_id,
                "provider": args.provider,
                "model_id": args.model_id,
                "tot_evaluator_mode": args.tot_evaluator_mode,
                "tot_mode": args.tot_mode,
                "tot_gen_mode": args.tot_gen_mode,
                "tot_decomposition_rounds": args.tot_decomposition_rounds,
                "tot_max_depth": args.tot_max_depth,
                "tot_legacy_max_depth": args.tot_legacy_max_depth,
                "tot_gen_max_depth": args.tot_gen_max_depth,
                "tot_branch_factor": args.tot_branch_factor,
                "tot_frontier_width": args.tot_frontier_width,
                "seed_policy": args.seed_policy,
                "hf_temperature": args.hf_temperature,
                "cot_temperature": args.cot_temperature,
                "cot_sc_temperature": args.cot_sc_temperature,
                "react_temperature": args.react_temperature,
                "hf_top_p": args.hf_top_p,
                "capability_parity_policy": getattr(args, "capability_parity_policy", "unknown"),
                "parity_profile": getattr(args, "parity_profile", "off"),
                "task_tools_available": list(getattr(args, "task_tools_available", [])),
                "condition_tools_exposed": getattr(args, "condition_tools_map", {}),
                "condition_surfaces": getattr(args, "condition_surfaces", {}),
                "confidence_level": args.confidence_level,
                "bootstrap_samples": args.bootstrap_samples,
                "bootstrap_seed": args.bootstrap_seed,
                "items_evaluated": len(panel_items),
                "runs_executed": len(manifests),
                "condition_summaries": condition_summaries_out,
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
    resolved_task_id = resolve_task_id(str(args.task_id))
    args.task_id = resolved_task_id
    panel_id, panel_task_id, panel_items = _load_panel(Path(args.panel_file))
    if panel_task_id and resolve_task_id(panel_task_id) != resolved_task_id:
        print(
            f"error: panel task_id={panel_task_id} does not match --task-id={resolved_task_id}"
        )
        return 2
    args.panel_id = panel_id

    selected = _slice_items(panel_items, args.offset, args.limit)
    if not selected:
        print("error: selected item slice is empty")
        return 2

    conditions = [name.strip() for name in args.conditions.split(",") if name.strip()]
    try:
        condition_specs = resolve_conditions(conditions)
    except KeyError as exc:
        print(f"error: {exc}")
        print(f"valid_conditions={condition_names()}")
        return 2
    condition_ids = [spec.condition_id for spec in condition_specs]
    if len(set(condition_ids)) != len(condition_ids):
        print(
            "error: selected conditions map to duplicate condition_id values. "
            f"conditions={conditions} condition_ids={condition_ids}"
        )
        return 2

    try:
        capability_plan = _resolve_capability_plan(
            task_id=resolved_task_id,
            condition_specs=condition_specs,
            policy=args.capability_parity_policy,
            parity_profile=args.parity_profile,
        )
    except RuntimeError as exc:
        print(f"error: {exc}")
        return 2

    args.task_tools_available = list(capability_plan["task_tools"])
    args.condition_tools_map = dict(capability_plan["condition_tools"])
    args.condition_surfaces = dict(capability_plan["condition_surfaces"])
    args.react_enable_tools_by_condition = dict(capability_plan["react_enable_tools_by_condition"])
    print(f"capability_parity_policy={args.capability_parity_policy}")
    print(f"parity_profile={args.parity_profile}")
    print(f"task_tools_available={args.task_tools_available}")
    print(f"condition_tools_exposed={args.condition_tools_map}")
    print(f"condition_surfaces={args.condition_surfaces}")
    if capability_plan["adjustments"]:
        print(f"capability_parity_adjustments={capability_plan['adjustments']}")

    runs_dir = Path(args.runs_dir)
    run_log = Path(args.run_log)

    manifests: List[Dict[str, Any]] = []
    if args.report_only:
        manifests = _load_latest_existing_manifests(
            runs_dir=runs_dir,
            panel_id=args.panel_id,
            task_id=resolved_task_id,
            selected_items=selected,
            condition_specs=condition_specs,
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
        for condition_spec in condition_specs:
            if condition_spec.tot_variant is None:
                manifest = _run_baseline_condition(
                    condition_spec=condition_spec,
                    item=item,
                    seed=seed,
                    args=args,
                    react_enable_tools=bool(args.react_enable_tools_by_condition.get(condition_spec.key, False)),
                    condition_tools=dict(args.condition_tools_map),
                )
            else:
                manifest = _run_tot(
                    condition_spec=condition_spec,
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
                        f"task={args.task_id} item={item['item_id']} condition={manifest['condition_id']} "
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
                        f"task={args.task_id} item={item['item_id']} condition={manifest['condition_id']} "
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
