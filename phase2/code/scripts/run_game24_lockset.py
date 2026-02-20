#!/usr/bin/env python3
"""Run paired Game24 lockset panel across baseline and ToT conditions."""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

from phase2_baselines.adapters import HuggingFaceInferenceModel, ScriptedModel
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
    parser.add_argument("--conditions", default="single,react,tot", help="Comma-separated: single,react,tot")
    parser.add_argument("--provider", choices=["scripted", "hf"], default="hf")
    parser.add_argument("--model-id", default="", help="Model identifier for --provider hf")
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
    parser.add_argument("--offset", type=int, default=0, help="Start index within panel items")
    parser.add_argument("--limit", type=int, default=0, help="Number of items from panel (0 = all)")
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


def _build_model(args: argparse.Namespace):
    if args.provider == "scripted":
        return (
            ScriptedModel(
                responses=[
                    "CANDIDATE: (10+4)+10+4\nCANDIDATE: (10*10-4)/4",
                ]
            ),
            "scripted-tot-v1",
            "local-scripted",
        )

    model_id = args.model_id or "Qwen/Qwen3-Coder-Next:novita"
    token = os.getenv(args.hf_token_env, "").strip()
    if not token:
        raise RuntimeError(f"Hugging Face provider requires ${args.hf_token_env} with a valid API token.")
    return (
        HuggingFaceInferenceModel(
            model_id=model_id,
            api_token=token,
            timeout_seconds=args.hf_timeout_seconds,
            max_new_tokens=args.hf_max_new_tokens,
            temperature=args.hf_temperature,
            top_p=args.hf_top_p,
        ),
        model_id,
        "huggingface-inference",
    )


def _run_single_or_react(
    condition: str,
    item: Dict[str, Any],
    seed: int,
    args: argparse.Namespace,
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
    )
    config["item_id"] = item["item_id"]
    config["input_data"] = item["numbers"]
    config["panel_id"] = args.panel_id
    runner.prepare(task=task, config=config)
    return runner.run(item["numbers"])


def _run_tot(item: Dict[str, Any], seed: int, args: argparse.Namespace) -> Dict[str, Any]:
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
            "tool_config": [],
            "budget": {"token_budget": 4000, "time_budget_ms": 15000, "cost_budget_usd": 0.0},
            "seed": seed,
            "max_depth": args.tot_max_depth,
            "branch_factor": args.tot_branch_factor,
            "frontier_width": args.tot_frontier_width,
            "evaluator_mode": args.tot_evaluator_mode,
            "item_id": item["item_id"],
            "input_data": item["numbers"],
            "panel_id": args.panel_id,
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
    for i, c1 in enumerate(condition_ids):
        for c2 in condition_ids[i + 1 :]:
            matched = 0
            c1_better = 0
            c2_better = 0
            ties = 0
            for item_id, values in by_item.items():
                if c1 not in values or c2 not in values:
                    continue
                matched += 1
                v1 = values[c1]
                v2 = values[c2]
                if v1 > v2:
                    c1_better += 1
                elif v2 > v1:
                    c2_better += 1
                else:
                    ties += 1
            paired_rows.append(
                {
                    "condition_a": c1,
                    "condition_b": c2,
                    "matched_items": matched,
                    "a_better": c1_better,
                    "b_better": c2_better,
                    "ties": ties,
                    "delta_success_rate": round((c1_better - c2_better) / matched, 6) if matched else 0.0,
                }
            )

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
        f"Items evaluated: {len(panel_items)}",
        f"Runs executed: {len(manifests)}",
        "",
        "## Condition Summary",
        "",
        "| Condition | Runs | Success Rate | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for summary in summaries:
        md_lines.append(
            "| {condition} | {runs} | {success:.3f} | {lat_mean:.1f} | {tin_mean:.1f} | {tout_mean:.1f} |".format(
                condition=summary["condition_id"],
                runs=summary["runs"],
                success=summary["success_rate"],
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
            "| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N |",
            "|---|---|---:|---:|---:|---:|---:|",
        ]
    )
    for row in paired_rows:
        md_lines.append(
            "| {a} | {b} | {n} | {ab} | {bb} | {t} | {d:.3f} |".format(
                a=row["condition_a"],
                b=row["condition_b"],
                n=row["matched_items"],
                ab=row["a_better"],
                bb=row["b_better"],
                t=row["ties"],
                d=row["delta_success_rate"],
            )
        )

    md_lines.extend(
        [
            "",
            "## Notes",
            "- This is a paired-condition report; each row compares outcomes on shared item IDs only.",
            "- Use this pilot report for protocol validation and effect-size estimation before larger panels.",
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

    conditions = [name.strip() for name in args.conditions.split(",") if name.strip()]
    valid = {"single", "react", "tot"}
    unknown = [name for name in conditions if name not in valid]
    if unknown:
        print(f"error: unsupported conditions: {unknown}")
        return 2

    runs_dir = Path(args.runs_dir)
    run_log = Path(args.run_log)

    manifests: List[Dict[str, Any]] = []
    for item_index, item in enumerate(selected):
        for condition in conditions:
            try:
                if condition in {"single", "react"}:
                    manifest = _run_single_or_react(condition=condition, item=item, seed=item_index, args=args)
                else:
                    manifest = _run_tot(item=item, seed=item_index, args=args)
                out_path = _write_manifest_and_log(manifest, runs_dir, run_log)
                manifests.append(manifest)
                print(
                    f"item={item['item_id']} condition={manifest['condition_id']} "
                    f"run_id={manifest['run_id']} outcome={manifest['outcome']} path={out_path}"
                )
            except Exception as exc:
                print(f"error: item={item['item_id']} condition={condition}: {exc}")
                return 2

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
