#!/usr/bin/env python3
"""Lightweight experiment dashboard server for Phase 2 artifacts."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
from typing import Any, Dict, List


def resolve_root() -> Path:
    env_root = os.environ.get("TOT_HF_ROOT", "").strip()
    if env_root:
        return Path(env_root).expanduser().resolve()
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "phase2").is_dir() and (parent / "README.md").exists():
            return parent
    return Path.cwd()


ROOT = resolve_root()
PHASE2 = ROOT / "phase2"
ANALYSIS_DIR = PHASE2 / "benchmarks/analysis"
RUNS_DIR = PHASE2 / "benchmarks/runs"
RUNTIME_DIR = PHASE2 / "reproducibility/runtime"
PROFILE_LABELS = {
    "tot_model_self_eval": "ToT self-eval (3/3/3)",
    "tot_hybrid": "ToT hybrid (3/3/3)",
    "tot_rule_based": "ToT rule-based (3/3/3)",
    "tot_model_self_eval_lite": "ToT self-eval lite (2/2/2)",
    "confirmatory": "confirmatory",
    "smoke": "smoke",
}
SERIES_VERSION_LABELS = {
    "v31": "v3.1",
    "v32": "v3.2",
    "v4_smoke": "v4-smoke",
    "v4_matrix": "v4-matrix",
    "v4": "v4",
}
DIAGNOSTIC_TASKS = {
    "linear2-demo": ("linear2_demo", PHASE2 / "benchmarks/panels/linear2_lockset_v1.json"),
    "digit-permutation-demo": (
        "digit_permutation_demo",
        PHASE2 / "benchmarks/panels/digit_permutation_lockset_v1.json",
    ),
}
DIAGNOSTIC_MODELS = {
    "Qwen/Qwen3-Coder-Next:novita": "qwen_qwen3_coder_next_novita",
    "Qwen/Qwen2.5-72B-Instruct": "qwen_qwen2_5_72b_instruct",
    "Qwen/Qwen2.5-Coder-32B-Instruct": "qwen_qwen2_5_coder_32b_instruct",
}
DIAGNOSTIC_PROFILES = [
    "tot_model_self_eval",
    "tot_hybrid",
    "tot_rule_based",
    "tot_model_self_eval_lite",
]
DIAGNOSTIC_CONDITIONS = ("baseline-react", "tot-prototype")
V4_TASKS = {
    "game24-demo": ("game24_demo", PHASE2 / "benchmarks/panels/game24_lockset_v4.json"),
    "subset-sum-demo": ("subset_sum_demo", PHASE2 / "benchmarks/panels/subset_sum_lockset_v4.json"),
    "linear2-demo": ("linear2_demo", PHASE2 / "benchmarks/panels/linear2_lockset_v4.json"),
    "digit-permutation-demo": (
        "digit_permutation_demo",
        PHASE2 / "benchmarks/panels/digit_permutation_lockset_v4.json",
    ),
}
V4_SMOKE_MODELS = {
    "Qwen/Qwen3-Coder-Next:novita": "qwen_qwen3_coder_next_novita",
}
V4_MATRIX_MODELS = {
    "Qwen/Qwen3-Coder-Next:novita": "qwen_qwen3_coder_next_novita",
    "Qwen/Qwen2.5-72B-Instruct": "qwen_qwen2_5_72b_instruct",
    "Qwen/Qwen2.5-Coder-32B-Instruct": "qwen_qwen2_5_coder_32b_instruct",
}
V4_CONDITIONS = ("baseline-single-path", "baseline-react", "tot-prototype")


def utc_now() -> str:
    return subprocess.check_output(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"], text=True).strip()


def safe_read_json(path: Path) -> Dict[str, Any] | List[Any] | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def tail_text(path: Path, lines: int = 30) -> str:
    if not path.exists():
        return ""
    try:
        output = subprocess.check_output(["tail", "-n", str(lines), str(path)], text=True)
        return output
    except Exception:
        return ""


def parse_pid_file(pid_path: Path) -> int | None:
    if not pid_path.exists():
        return None
    try:
        return int(pid_path.read_text(encoding="utf-8").strip())
    except Exception:
        return None


def is_pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def pid_info(pid: int) -> Dict[str, str]:
    if not is_pid_alive(pid):
        return {"elapsed": "", "command": ""}
    try:
        output = subprocess.check_output(
            ["ps", "-p", str(pid), "-o", "etime=,command="],
            text=True,
        ).strip()
        if not output:
            return {"elapsed": "", "command": ""}
        parts = output.split(maxsplit=1)
        if len(parts) == 1:
            return {"elapsed": parts[0], "command": ""}
        return {"elapsed": parts[0], "command": parts[1]}
    except Exception:
        return {"elapsed": "", "command": ""}


def list_runtime_processes() -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    if not RUNTIME_DIR.exists():
        return results

    pid_files = sorted(RUNTIME_DIR.glob("*.pid"), key=lambda p: p.stat().st_mtime, reverse=True)
    for pid_file in pid_files:
        pid = parse_pid_file(pid_file)
        if pid is None:
            continue
        alive = is_pid_alive(pid)
        info = pid_info(pid) if alive else {"elapsed": "", "command": ""}
        log_file = pid_file.with_suffix(".log")
        last_line = ""
        if log_file.exists():
            text = tail_text(log_file, lines=1).strip()
            last_line = text
        results.append(
            {
                "name": pid_file.stem,
                "pid": pid,
                "alive": alive,
                "elapsed": info.get("elapsed", ""),
                "command": info.get("command", ""),
                "pid_file": str(pid_file),
                "log_file": str(log_file),
                "last_line": last_line,
            }
        )
    return results


def load_panel_items(panel_path: Path, limit: int = 50) -> List[str]:
    payload = safe_read_json(panel_path)
    if not isinstance(payload, dict):
        return []
    items = payload.get("items", [])
    if not isinstance(items, list):
        return []
    out: List[str] = []
    for row in items[:limit]:
        if isinstance(row, dict):
            item_id = row.get("item_id")
            if isinstance(item_id, str):
                out.append(item_id)
    return out


def compute_series_progress(
    *,
    series_id: str,
    report_version_id: str,
    tasks: Dict[str, tuple[str, Path]],
    models: Dict[str, str],
    profiles: List[str],
    conditions: tuple[str, ...],
    panel_limit: int,
) -> Dict[str, Any]:
    base = RUNS_DIR / series_id
    condition_set = set(conditions)

    blocks: List[Dict[str, Any]] = []
    for task_id, (task_slug, panel_path) in tasks.items():
        panel_items = load_panel_items(panel_path, limit=panel_limit)
        block_total_pairs = len(panel_items) * len(conditions)
        for model_id, model_slug in models.items():
            for profile in profiles:
                run_dir = base / task_slug / model_slug
                if profile:
                    run_dir = run_dir / profile
                seen: Dict[str, set[str]] = {item_id: set() for item_id in panel_items}
                if run_dir.exists():
                    for manifest_path in run_dir.glob("*.json"):
                        payload = safe_read_json(manifest_path)
                        if not isinstance(payload, dict):
                            continue
                        item_id = payload.get("item_id")
                        cond = payload.get("condition_id")
                        if isinstance(item_id, str) and isinstance(cond, str):
                            if item_id in seen and cond in condition_set:
                                seen[item_id].add(cond)
                present_pairs = sum(len(seen[item_id]) for item_id in panel_items)
                complete_items = sum(1 for item_id in panel_items if len(seen[item_id]) == len(conditions))
                state = "not_started"
                if block_total_pairs and present_pairs == block_total_pairs:
                    state = "done"
                elif present_pairs > 0:
                    state = "partial"
                blocks.append(
                    {
                        "series_id": series_id,
                        "report_version_id": report_version_id,
                        "report_version_label": SERIES_VERSION_LABELS.get(report_version_id, report_version_id),
                        "task_id": task_id,
                        "model_id": model_id,
                        "profile": profile or "none",
                        "present_pairs": present_pairs,
                        "total_pairs": block_total_pairs,
                        "complete_items": complete_items,
                        "state": state,
                    }
                )

    done = sum(1 for block in blocks if block["state"] == "done")
    partial = sum(1 for block in blocks if block["state"] == "partial")
    not_started = sum(1 for block in blocks if block["state"] == "not_started")
    present_pairs = sum(int(block["present_pairs"]) for block in blocks)
    total_pairs = sum(int(block["total_pairs"]) for block in blocks)

    return {
        "series_id": series_id,
        "report_version_id": report_version_id,
        "report_version_label": SERIES_VERSION_LABELS.get(report_version_id, report_version_id),
        "done_blocks": done,
        "partial_blocks": partial,
        "not_started_blocks": not_started,
        "present_pairs": present_pairs,
        "total_pairs": total_pairs,
        "blocks": blocks,
    }


def compute_diagnostic_progress(series_id: str, report_version_id: str) -> Dict[str, Any]:
    return compute_series_progress(
        series_id=series_id,
        report_version_id=report_version_id,
        tasks=DIAGNOSTIC_TASKS,
        models=DIAGNOSTIC_MODELS,
        profiles=DIAGNOSTIC_PROFILES,
        conditions=DIAGNOSTIC_CONDITIONS,
        panel_limit=50,
    )


def compute_diagnostic_progress_all() -> Dict[str, Dict[str, Any]]:
    return {
        "v31": compute_diagnostic_progress("protocol_v31_diagnostic", "v31"),
        "v32": compute_diagnostic_progress("protocol_v32_diagnostic", "v32"),
        "v4_smoke": compute_series_progress(
            series_id="protocol_v4_smoke",
            report_version_id="v4_smoke",
            tasks=V4_TASKS,
            models=V4_SMOKE_MODELS,
            profiles=[""],
            conditions=V4_CONDITIONS,
            panel_limit=10,
        ),
        "v4_matrix": compute_series_progress(
            series_id="protocol_v4_confirmatory_matrix",
            report_version_id="v4_matrix",
            tasks=V4_TASKS,
            models=V4_MATRIX_MODELS,
            profiles=[""],
            conditions=V4_CONDITIONS,
            panel_limit=50,
        ),
    }


def _as_float(value: Any) -> float | None:
    try:
        return float(value)
    except Exception:
        return None


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


def _infer_report_tag(path: Path) -> tuple[str, str]:
    match = re.search(r"_(v[0-9][0-9a-z]*(?:_[0-9a-z]+)*)$", path.stem)
    if not match:
        return ("unknown", "")
    full = match.group(1)
    base = full.split("_", 1)[0]
    return (base, full)


def _infer_report_version(path: Path) -> tuple[str, str, str]:
    stem = path.stem
    if "_confirmatory_report_" in stem and stem.endswith("_v4"):
        return ("v4_matrix", SERIES_VERSION_LABELS.get("v4_matrix", "v4_matrix"), "v4")
    if "_smoke_report_" in stem and stem.endswith("_v4"):
        return ("v4_smoke", SERIES_VERSION_LABELS.get("v4_smoke", "v4_smoke"), "v4")
    base, full = _infer_report_tag(path)
    return (base, SERIES_VERSION_LABELS.get(base, base), full)


def _infer_profile_id(path: Path) -> str:
    stem = path.stem
    if "_confirmatory_report_" in stem:
        return "confirmatory"
    if "_smoke_report_" in stem:
        return "smoke"
    for profile_id in sorted(PROFILE_LABELS.keys(), key=len, reverse=True):
        marker = f"_{profile_id}_"
        if marker in f"_{stem}_":
            return profile_id
    return "unknown"


def list_series_reports(report_versions: set[str] | None = None) -> List[Dict[str, Any]]:
    paths: List[Path] = []
    paths.extend(ANALYSIS_DIR.glob("*_diag_report_*.json"))
    paths.extend(ANALYSIS_DIR.glob("*_confirmatory_report_*_v4.json"))
    paths.extend(ANALYSIS_DIR.glob("*_smoke_report_*_v4.json"))
    paths = sorted(paths, key=lambda p: p.stat().st_mtime, reverse=True)
    rows: List[Dict[str, Any]] = []
    for path in paths:
        version_id, version_label, report_tag = _infer_report_version(path)
        if report_versions and version_id not in report_versions:
            continue
        payload = safe_read_json(path)
        if not isinstance(payload, dict):
            continue
        condition_rows = payload.get("condition_summaries", [])
        paired_rows = payload.get("paired_comparison", [])
        if not isinstance(condition_rows, list):
            condition_rows = []
        if not isinstance(paired_rows, list):
            paired_rows = []
        cond = _condition_map([row for row in condition_rows if isinstance(row, dict)])
        react = cond.get("baseline-react", {})
        tot = cond.get("tot-prototype", {})
        pair_tr = _pair_row([row for row in paired_rows if isinstance(row, dict)], "tot-prototype", "baseline-react")
        profile_id = _infer_profile_id(path)
        md_path = path.with_suffix(".md")
        rows.append(
            {
                "report_version_id": version_id,
                "report_version_label": version_label,
                "report_tag": report_tag,
                "task_id": payload.get("task_id"),
                "model_id": payload.get("model_id"),
                "profile_id": profile_id,
                "profile_label": PROFILE_LABELS.get(profile_id, profile_id),
                "items_evaluated": payload.get("items_evaluated"),
                "runs_executed": payload.get("runs_executed"),
                "react_success_rate": react.get("success_rate"),
                "tot_success_rate": tot.get("success_rate"),
                "tot_minus_react": (pair_tr or {}).get("delta_success_rate"),
                "holm_p_tot_vs_react": (pair_tr or {}).get("mcnemar_p_holm"),
                "mcnemar_p_tot_vs_react": (pair_tr or {}).get("mcnemar_p_value"),
                "react_latency_ms_mean": react.get("latency_ms_mean"),
                "tot_latency_ms_mean": tot.get("latency_ms_mean"),
                "react_tokens_in_mean": react.get("tokens_in_mean"),
                "tot_tokens_in_mean": tot.get("tokens_in_mean"),
                "tot_evaluator_mode": payload.get("tot_evaluator_mode"),
                "tot_max_depth": payload.get("tot_max_depth"),
                "tot_branch_factor": payload.get("tot_branch_factor"),
                "tot_frontier_width": payload.get("tot_frontier_width"),
                "report_json_path": str(path),
                "report_md_path": str(md_path) if md_path.exists() else "",
                "mtime_epoch": int(path.stat().st_mtime),
            }
        )
    return rows


def load_series_detail(report_path: Path) -> Dict[str, Any] | None:
    payload = safe_read_json(report_path)
    if not isinstance(payload, dict):
        return None
    profile_id = _infer_profile_id(report_path)
    version_id, version_label, report_tag = _infer_report_version(report_path)
    md_path = report_path.with_suffix(".md")

    condition_rows = payload.get("condition_summaries", [])
    paired_rows = payload.get("paired_comparison", [])
    if not isinstance(condition_rows, list):
        condition_rows = []
    if not isinstance(paired_rows, list):
        paired_rows = []

    condition_rows = [row for row in condition_rows if isinstance(row, dict)]
    paired_rows = [row for row in paired_rows if isinstance(row, dict)]
    condition_rows.sort(key=lambda row: str(row.get("condition_id", "")))
    paired_rows.sort(key=lambda row: (str(row.get("condition_a", "")), str(row.get("condition_b", ""))))

    cond = _condition_map(condition_rows)
    react = cond.get("baseline-react", {})
    tot = cond.get("tot-prototype", {})
    pair_tr = _pair_row(paired_rows, "tot-prototype", "baseline-react")

    return {
        "report_version_id": version_id,
        "report_version_label": version_label,
        "report_tag": report_tag,
        "task_id": payload.get("task_id"),
        "model_id": payload.get("model_id"),
        "panel_id": payload.get("panel_id"),
        "provider": payload.get("provider"),
        "generated_utc": payload.get("generated_utc"),
        "items_evaluated": payload.get("items_evaluated"),
        "runs_executed": payload.get("runs_executed"),
        "profile_id": profile_id,
        "profile_label": PROFILE_LABELS.get(profile_id, profile_id),
        "tot_evaluator_mode": payload.get("tot_evaluator_mode"),
        "tot_max_depth": payload.get("tot_max_depth"),
        "tot_branch_factor": payload.get("tot_branch_factor"),
        "tot_frontier_width": payload.get("tot_frontier_width"),
        "seed_policy": payload.get("seed_policy"),
        "bootstrap_samples": payload.get("bootstrap_samples"),
        "confidence_level": payload.get("confidence_level"),
        "react_success_rate": react.get("success_rate"),
        "tot_success_rate": tot.get("success_rate"),
        "tot_minus_react": (pair_tr or {}).get("delta_success_rate"),
        "condition_summaries": condition_rows,
        "paired_comparison": paired_rows,
        "report_json_path": str(report_path),
        "report_md_path": str(md_path) if md_path.exists() else "",
    }


def load_v3_summary() -> Dict[str, Any]:
    summary_path = ANALYSIS_DIR / "protocol_v3_matrix_summary.json"
    payload = safe_read_json(summary_path)
    if not isinstance(payload, dict):
        return {"records": [], "tot_vs_react_positive": 0, "tot_vs_react_negative": 0}

    records = payload.get("records", [])
    if not isinstance(records, list):
        records = []

    pos = 0
    neg = 0
    for row in records:
        if not isinstance(row, dict):
            continue
        delta = row.get("tot_minus_react")
        try:
            value = float(delta)
        except Exception:
            continue
        if value > 0:
            pos += 1
        elif value < 0:
            neg += 1

    return {
        "records": records,
        "tot_vs_react_positive": pos,
        "tot_vs_react_negative": neg,
        "path": str(summary_path),
    }


def load_diagnostic_summary(report_version_id: str) -> Dict[str, Any]:
    if report_version_id == "v31":
        summary_path = ANALYSIS_DIR / "protocol_v31_diagnostic_summary.json"
    elif report_version_id == "v32":
        summary_path = ANALYSIS_DIR / "protocol_v32_diagnostic_summary.json"
    else:
        summary_path = ANALYSIS_DIR / f"protocol_{report_version_id}_diagnostic_summary.json"
    payload = safe_read_json(summary_path)
    if not isinstance(payload, dict):
        return {
            "records": [],
            "path": str(summary_path),
            "exists": False,
            "report_version_id": report_version_id,
            "report_version_label": SERIES_VERSION_LABELS.get(report_version_id, report_version_id),
        }
    records = payload.get("records", [])
    if not isinstance(records, list):
        records = []
    return {
        "records": records,
        "path": str(summary_path),
        "exists": True,
        "report_version_id": report_version_id,
        "report_version_label": SERIES_VERSION_LABELS.get(report_version_id, report_version_id),
    }


def load_v4_gate_status() -> Dict[str, Any]:
    gate_path = ANALYSIS_DIR / "protocol_v4_gate_report.json"
    payload = safe_read_json(gate_path)
    if not isinstance(payload, dict):
        return {
            "exists": False,
            "status": "unknown",
            "checks": [],
            "path": str(gate_path),
        }
    checks = payload.get("checks", [])
    if not isinstance(checks, list):
        checks = []
    return {
        "exists": True,
        "status": str(payload.get("status", "unknown")),
        "checks": checks,
        "path": str(gate_path),
    }


def load_v4_matrix_summary() -> Dict[str, Any]:
    summary_path = ANALYSIS_DIR / "protocol_v4_matrix_summary.json"
    payload = safe_read_json(summary_path)
    if not isinstance(payload, dict):
        return {"exists": False, "records": [], "path": str(summary_path)}
    records = payload.get("records", [])
    if not isinstance(records, list):
        records = []
    return {"exists": True, "records": records, "path": str(summary_path)}


def list_latest_analysis(limit: int = 25) -> List[Dict[str, Any]]:
    if not ANALYSIS_DIR.exists():
        return []
    files = sorted(ANALYSIS_DIR.glob("*"), key=lambda p: p.stat().st_mtime, reverse=True)
    out: List[Dict[str, Any]] = []
    for path in files[:limit]:
        out.append(
            {
                "name": path.name,
                "path": str(path),
                "size_bytes": path.stat().st_size,
                "mtime_epoch": int(path.stat().st_mtime),
            }
        )
    return out


def diagnose_access() -> Dict[str, Any]:
    probe = PHASE2 / "README.md"
    try:
        cwd = os.getcwd()
    except Exception:
        cwd = ""
    base = {
        "root": str(ROOT),
        "phase2": str(PHASE2),
        "python_executable": sys.executable,
        "cwd": cwd,
    }
    try:
        text = probe.read_text(encoding="utf-8")
        return {**base, "root_readable": True, "probe": str(probe), "probe_size": len(text)}
    except Exception as exc:
        return {**base, "root_readable": False, "probe": str(probe), "error": str(exc)}


def build_overview() -> Dict[str, Any]:
    diagnostic_progress = compute_diagnostic_progress_all()
    series_reports = list_series_reports({"v31", "v32", "v4_smoke", "v4_matrix"})
    return {
        "generated_utc": utc_now(),
        "access": diagnose_access(),
        "runtime_processes": list_runtime_processes(),
        "diagnostic_progress": diagnostic_progress,
        "v31_progress": diagnostic_progress.get("v31", {}),
        "v32_progress": diagnostic_progress.get("v32", {}),
        "v4_smoke_progress": diagnostic_progress.get("v4_smoke", {}),
        "v4_matrix_progress": diagnostic_progress.get("v4_matrix", {}),
        "v3_summary": load_v3_summary(),
        "v4_gate_status": load_v4_gate_status(),
        "v4_matrix_summary": load_v4_matrix_summary(),
        "diagnostic_summaries": {
            "v31": load_diagnostic_summary("v31"),
            "v32": load_diagnostic_summary("v32"),
        },
        "v31_summary": load_diagnostic_summary("v31"),
        "v32_summary": load_diagnostic_summary("v32"),
        "series_reports": series_reports,
        "v31_series": [row for row in series_reports if row.get("report_version_id") == "v31"],
        "latest_analysis": list_latest_analysis(),
    }


def html_template() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>ToT-HF Experiment Dashboard</title>
  <style>
    :root {
      --bg: #f5efe3;
      --card: #fff9ee;
      --line: #d9c8a6;
      --ink: #2f2a22;
      --muted: #6e6456;
      --accent: #8f6b2b;
      --good: #2f7f4f;
      --warn: #c57d16;
      --bad: #b13d2c;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: linear-gradient(135deg, #f9f3e8 0%, #efe4ce 100%);
      color: var(--ink);
    }
    .wrap { max-width: 1320px; margin: 0 auto; padding: 18px; }
    h1 { margin: 0 0 10px; font-size: 24px; }
    h2 { margin: 0 0 10px; font-size: 16px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--muted); }
    .small { color: var(--muted); font-size: 12px; }
    .grid { display: grid; gap: 12px; }
    .grid.cards { grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); }
    .card {
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 10px;
      padding: 12px;
      box-shadow: 0 1px 0 rgba(0, 0, 0, 0.03);
    }
    .metric { font-size: 24px; font-weight: 700; color: var(--accent); }
    .row { display: flex; gap: 10px; align-items: center; }
    .row.space { justify-content: space-between; }
    .pill {
      font-size: 11px; padding: 2px 8px; border-radius: 999px; border: 1px solid var(--line);
      background: #fdf7eb;
    }
    .pill.good { color: var(--good); border-color: #9fd2b4; background: #eef9f1; }
    .pill.warn { color: var(--warn); border-color: #e4bf87; background: #fff7ea; }
    .pill.bad { color: var(--bad); border-color: #e2a29a; background: #fff1ef; }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
    }
    th, td {
      text-align: left;
      border-bottom: 1px solid var(--line);
      padding: 6px 6px;
      vertical-align: top;
    }
    th { color: var(--muted); font-weight: 600; }
    .log {
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      white-space: pre-wrap;
      background: #f3e8ce;
      border: 1px solid var(--line);
      padding: 8px;
      border-radius: 8px;
      min-height: 120px;
      max-height: 260px;
      overflow: auto;
      font-size: 12px;
    }
    .progress {
      width: 100%;
      height: 10px;
      border-radius: 999px;
      border: 1px solid var(--line);
      background: #f6ecda;
      overflow: hidden;
    }
    .progress > span {
      display: block;
      height: 100%;
      background: linear-gradient(90deg, #2f7f4f 0%, #5ca473 100%);
      width: 0%;
    }
    a { color: #725018; text-decoration: none; }
    a:hover { text-decoration: underline; }
    .controls { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 8px; }
    .controls input, .controls select, .controls button {
      border: 1px solid var(--line);
      background: #fffdf7;
      color: var(--ink);
      border-radius: 8px;
      padding: 6px 8px;
      font-size: 12px;
    }
    .controls input { min-width: 220px; }
    .btn {
      border: 1px solid var(--line);
      background: #f8eed8;
      color: #614615;
      border-radius: 8px;
      padding: 4px 8px;
      font-size: 11px;
      cursor: pointer;
    }
    .btn:hover { background: #f2e2be; }
    .clickable-row:hover { background: #fbf1dc; }
    .clickable-row.selected { background: #efe2bf; }
    .split { display: grid; gap: 12px; grid-template-columns: 1.25fr 1fr; }
    .kvs { font-size: 12px; color: var(--ink); line-height: 1.5; }
    .kvs code { background: #f3e8ce; padding: 1px 4px; border-radius: 4px; }
    @media (max-width: 980px) {
      .split { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="row space">
      <div>
        <h1>ToT-HF Experiment Dashboard</h1>
        <div class="small">Auto-refresh: 8s | Served locally</div>
      </div>
      <div class="small" id="generatedUtc">...</div>
    </div>
    <div id="accessWarn" class="card" style="display:none; margin-top:10px; border-color:#e2a29a; background:#fff1ef;">
      <h2 style="color:#b13d2c;">Filesystem Access Warning</h2>
      <div class="small" id="accessWarnText"></div>
    </div>

    <div class="grid cards" id="topCards"></div>

    <div class="grid" style="margin-top:12px;">
      <div class="card">
        <h2>Protocol Series Progress</h2>
        <div class="controls" style="margin-bottom:6px;">
          <select id="progressVersionFilter">
            <option value="v31">v3.1</option>
            <option value="v32">v3.2</option>
            <option value="v4_smoke">v4-smoke</option>
            <option value="v4_matrix" selected>v4-matrix</option>
          </select>
        </div>
        <div class="progress"><span id="v31ProgressBar"></span></div>
        <div class="small" id="v31ProgressText" style="margin-top:6px;"></div>
        <table id="v31BlocksTable" style="margin-top:8px;">
          <thead>
            <tr>
              <th>Version</th><th>Task</th><th>Model</th><th>Profile</th><th>Pairs</th><th>Status</th>
            </tr>
          </thead>
          <tbody></tbody>
        </table>
      </div>

      <div class="card">
        <h2>Runtime Processes</h2>
        <table id="procTable">
          <thead>
            <tr>
              <th>Name</th><th>PID</th><th>Alive</th><th>Elapsed</th><th>Last line</th>
            </tr>
          </thead>
          <tbody></tbody>
        </table>
      </div>

      <div class="card">
        <h2>v3 Snapshot (Legacy)</h2>
        <div class="small" id="v3SummaryText"></div>
        <table id="v3Table" style="margin-top:8px;">
          <thead>
            <tr>
              <th>Task</th><th>Model</th><th>Δ(ToT-ReAct)</th><th>Holm p</th>
            </tr>
          </thead>
          <tbody></tbody>
        </table>
      </div>

      <div class="split">
        <div class="card">
          <h2>Series Results (v3 + v4)</h2>
          <div class="controls">
            <input id="seriesSearch" type="text" placeholder="Search task/model/profile...">
            <select id="seriesVersionFilter"><option value="">All versions</option></select>
            <select id="seriesTaskFilter"><option value="">All tasks</option></select>
            <select id="seriesModelFilter"><option value="">All models</option></select>
            <select id="seriesProfileFilter"><option value="">All profiles</option></select>
            <button id="seriesReset" class="btn">Reset</button>
          </div>
          <div class="small" id="seriesCountText"></div>
          <table id="seriesTable" style="margin-top:8px;">
            <thead>
              <tr>
                <th>Version</th><th>Task</th><th>Model</th><th>Profile</th><th>ReAct</th><th>ToT</th>
                <th>Δ</th><th>Holm p</th><th>View</th>
              </tr>
            </thead>
            <tbody></tbody>
          </table>
        </div>

        <div class="card">
          <h2>Selected Series Detail</h2>
          <div id="seriesDetailMeta" class="kvs small">Select a series to inspect condition-level metrics.</div>
          <div id="seriesDetailLinks" class="small" style="margin-top:6px;"></div>
          <table id="seriesConditionTable" style="margin-top:8px;">
            <thead>
              <tr>
                <th>Condition</th><th>Runs</th><th>Success</th><th>Latency (ms)</th><th>Tokens In</th><th>Tokens Out</th>
              </tr>
            </thead>
            <tbody></tbody>
          </table>
          <table id="seriesPairTable" style="margin-top:8px;">
            <thead>
              <tr>
                <th>A</th><th>B</th><th>Items</th><th>Δ(A-B)</th><th>CI</th><th>p</th><th>Holm</th>
              </tr>
            </thead>
            <tbody></tbody>
          </table>
        </div>
      </div>

      <div class="card">
        <h2>Latest Analysis Files</h2>
        <table id="filesTable">
          <thead>
            <tr>
              <th>File</th><th>Size</th><th>Modified</th><th>View</th>
            </tr>
          </thead>
          <tbody></tbody>
        </table>
      </div>

      <div class="card">
        <h2>Selected Log Tail</h2>
        <div class="row">
          <select id="logPicker" style="min-width: 360px;"></select>
          <button id="loadLogBtn">Load</button>
        </div>
        <div id="logTail" class="log" style="margin-top:8px;"></div>
      </div>
    </div>
  </div>

  <script>
    let selectedSeriesPath = "";
    let lastSeriesRows = [];
    let lastOverview = null;

    function esc(s) {
      return String(s ?? "").replace(/[&<>"']/g, function(m) {
        return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[m];
      });
    }

    function fmtEpoch(epoch) {
      if (!epoch) return "";
      return new Date(epoch * 1000).toLocaleString();
    }

    function fmtSize(bytes) {
      if (bytes < 1024) return bytes + " B";
      if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
      return (bytes / (1024 * 1024)).toFixed(1) + " MB";
    }

    function fmtNum(value, digits = 3) {
      const n = Number(value);
      return Number.isFinite(n) ? n.toFixed(digits) : "n/a";
    }

    function fmtRate(value) {
      const n = Number(value);
      return Number.isFinite(n) ? (n * 100).toFixed(1) + "%" : "n/a";
    }

    function fmtP(value) {
      const n = Number(value);
      if (!Number.isFinite(n)) return "n/a";
      if (n < 1e-4) return n.toExponential(2);
      return n.toFixed(6);
    }

    function statusPill(state) {
      if (state === "done") return '<span class="pill good">done</span>';
      if (state === "partial") return '<span class="pill warn">partial</span>';
      return '<span class="pill">not started</span>';
    }

    function alivePill(alive) {
      return alive ? '<span class="pill good">alive</span>' : '<span class="pill bad">dead</span>';
    }

    function uniqueSorted(values) {
      return Array.from(new Set(values.filter(Boolean))).sort((a, b) => String(a).localeCompare(String(b)));
    }

    function setSelectOptions(selectId, values, keepValue) {
      const select = document.getElementById(selectId);
      const current = keepValue ?? select.value;
      const label = selectId === "seriesTaskFilter" ? "All tasks" :
        (selectId === "seriesModelFilter" ? "All models" :
        (selectId === "seriesVersionFilter" ? "All versions" : "All profiles"));
      const options = ['<option value="">' + label + '</option>']
        .concat(values.map(v => '<option value="' + esc(v) + '">' + esc(v) + '</option>'));
      select.innerHTML = options.join("");
      if (current) select.value = current;
      if (select.value !== current) select.value = "";
    }

    async function fetchJson(url) {
      const r = await fetch(url, {cache: "no-store"});
      if (!r.ok) throw new Error("HTTP " + r.status);
      return await r.json();
    }

    async function loadLog(path) {
      if (!path) return;
      const data = await fetchJson("/api/log?path=" + encodeURIComponent(path));
      document.getElementById("logTail").textContent = data.tail || "";
    }

    function applySeriesFilters(rows) {
      const q = String(document.getElementById("seriesSearch").value || "").trim().toLowerCase();
      const version = document.getElementById("seriesVersionFilter").value;
      const task = document.getElementById("seriesTaskFilter").value;
      const model = document.getElementById("seriesModelFilter").value;
      const profile = document.getElementById("seriesProfileFilter").value;

      let out = rows.slice();
      if (version) out = out.filter(r => String(r.report_version_label || r.report_version_id || "") === version);
      if (task) out = out.filter(r => String(r.task_id || "") === task);
      if (model) out = out.filter(r => String(r.model_id || "") === model);
      if (profile) out = out.filter(r => String(r.profile_label || r.profile_id || "") === profile);
      if (q) {
        out = out.filter(r => {
          const hay = [
            r.report_version_label || r.report_version_id,
            r.task_id,
            r.model_id,
            r.profile_label || r.profile_id,
            r.report_json_path
          ].join(" ").toLowerCase();
          return hay.includes(q);
        });
      }
      out.sort((a, b) => {
        const da = Number(a.tot_minus_react);
        const db = Number(b.tot_minus_react);
        const va = Number.isFinite(da) ? da : -999;
        const vb = Number.isFinite(db) ? db : -999;
        if (vb !== va) return vb - va;
        return Number(b.mtime_epoch || 0) - Number(a.mtime_epoch || 0);
      });
      return out;
    }

    async function inspectSeries(path) {
      if (!path) return;
      selectedSeriesPath = path;
      const detail = await fetchJson("/api/series_detail?path=" + encodeURIComponent(path));

      const meta = [
        "Version: <code>" + esc(detail.report_version_label || detail.report_version_id) + "</code>",
        "Task: <code>" + esc(detail.task_id) + "</code>",
        "Model: <code>" + esc(detail.model_id) + "</code>",
        "Profile: <code>" + esc(detail.profile_label || detail.profile_id) + "</code>",
        "Items: <code>" + esc(detail.items_evaluated) + "</code>",
        "Runs: <code>" + esc(detail.runs_executed) + "</code>",
        "Evaluator: <code>" + esc(detail.tot_evaluator_mode) + "</code>",
        "ToT config: <code>d=" + esc(detail.tot_max_depth) + " b=" + esc(detail.tot_branch_factor) + " w=" + esc(detail.tot_frontier_width) + "</code>",
        "ToT - ReAct Δ: <code>" + esc(fmtNum(detail.tot_minus_react, 3)) + "</code>",
        "Generated: <code>" + esc(detail.generated_utc) + "</code>"
      ];
      document.getElementById("seriesDetailMeta").innerHTML = meta.join("<br>");

      const links = [
        "<a href='/api/file?path=" + encodeURIComponent(detail.report_json_path || "") + "' target='_blank'>open report json</a>"
      ];
      if (detail.report_md_path) {
        links.push("<a href='/api/file?path=" + encodeURIComponent(detail.report_md_path) + "' target='_blank'>open report markdown</a>");
      }
      document.getElementById("seriesDetailLinks").innerHTML = links.join(" | ");

      const conditionRows = detail.condition_summaries || [];
      document.querySelector("#seriesConditionTable tbody").innerHTML = conditionRows.map(r =>
        "<tr><td>" + esc(r.condition_id) + "</td><td>" + esc(r.runs) + "</td><td>" + esc(fmtRate(r.success_rate)) +
        "</td><td>" + esc(fmtNum(r.latency_ms_mean, 1)) + "</td><td>" + esc(fmtNum(r.tokens_in_mean, 1)) +
        "</td><td>" + esc(fmtNum(r.tokens_out_mean, 1)) + "</td></tr>"
      ).join("");

      const pairRows = detail.paired_comparison || [];
      document.querySelector("#seriesPairTable tbody").innerHTML = pairRows.map(r =>
        "<tr><td>" + esc(r.condition_a) + "</td><td>" + esc(r.condition_b) + "</td><td>" + esc(r.matched_items) +
        "</td><td>" + esc(fmtNum(r.delta_success_rate, 3)) + "</td><td>[" + esc(fmtNum(r.delta_ci_low, 3)) + ", " +
        esc(fmtNum(r.delta_ci_high, 3)) + "]</td><td>" + esc(fmtP(r.mcnemar_p_value)) + "</td><td>" +
        esc(fmtP(r.mcnemar_p_holm)) + "</td></tr>"
      ).join("");
    }

    function renderSeriesTable(rows) {
      const versionValues = uniqueSorted(rows.map(r => r.report_version_label || r.report_version_id));
      const taskValues = uniqueSorted(rows.map(r => r.task_id));
      const modelValues = uniqueSorted(rows.map(r => r.model_id));
      const profileValues = uniqueSorted(rows.map(r => r.profile_label || r.profile_id));
      setSelectOptions("seriesVersionFilter", versionValues);
      setSelectOptions("seriesTaskFilter", taskValues);
      setSelectOptions("seriesModelFilter", modelValues);
      setSelectOptions("seriesProfileFilter", profileValues);

      const filtered = applySeriesFilters(rows);
      document.getElementById("seriesCountText").textContent =
        "Showing " + filtered.length + " of " + rows.length + " series reports.";

      const tbody = document.querySelector("#seriesTable tbody");
      tbody.innerHTML = filtered.map(r => {
        const reportPath = String(r.report_json_path || "");
        const enc = encodeURIComponent(reportPath);
        const selected = reportPath === selectedSeriesPath ? " selected" : "";
        return "<tr class='clickable-row" + selected + "' data-path='" + enc + "'>" +
          "<td>" + esc(r.report_version_label || r.report_version_id) + "</td>" +
          "<td>" + esc(r.task_id) + "</td>" +
          "<td>" + esc(r.model_id) + "</td>" +
          "<td>" + esc(r.profile_label || r.profile_id) + "</td>" +
          "<td>" + esc(fmtRate(r.react_success_rate)) + "</td>" +
          "<td>" + esc(fmtRate(r.tot_success_rate)) + "</td>" +
          "<td>" + esc(fmtNum(r.tot_minus_react, 3)) + "</td>" +
          "<td>" + esc(fmtP(r.holm_p_tot_vs_react)) + "</td>" +
          "<td><button class='btn inspect-btn' data-path='" + enc + "'>inspect</button></td>" +
          "</tr>";
      }).join("");

      const hasSelected = selectedSeriesPath && rows.some(r => String(r.report_json_path || "") === selectedSeriesPath);
      if (hasSelected) {
        inspectSeries(selectedSeriesPath).catch(console.error);
      } else if (!selectedSeriesPath && filtered.length) {
        const firstPath = String(filtered[0].report_json_path || "");
        inspectSeries(firstPath).catch(console.error);
      }
    }

    function render(data) {
      document.getElementById("generatedUtc").textContent = "Updated: " + (data.generated_utc || "");
      const access = data.access || {};
      const accessWarn = document.getElementById("accessWarn");
      if (access.root_readable === false) {
        accessWarn.style.display = "block";
        const py = access.python_executable ? " Interpreter: " + access.python_executable + "." : "";
        const root = access.root ? " Root: " + access.root + "." : "";
        document.getElementById("accessWarnText").textContent =
          "Dashboard service cannot read workspace files (" + (access.error || "permission denied") +
          "). On macOS, grant Full Disk Access to the service python interpreter, then reinstall service." +
          py + root;
      } else {
        accessWarn.style.display = "none";
        document.getElementById("accessWarnText").textContent = "";
      }

      lastOverview = data;
      const diag = data.diagnostic_progress || {};
      const p31 = diag.v31 || data.v31_progress || {};
      const p32 = diag.v32 || data.v32_progress || {};
      const p4Smoke = diag.v4_smoke || data.v4_smoke_progress || {};
      const p4Matrix = diag.v4_matrix || data.v4_matrix_progress || {};
      const p31Pairs = Number(p31.present_pairs || 0);
      const p31Total = Number(p31.total_pairs || 0);
      const p31Pct = p31Total > 0 ? Math.round((p31Pairs / p31Total) * 100) : 0;
      const p32Pairs = Number(p32.present_pairs || 0);
      const p32Total = Number(p32.total_pairs || 0);
      const p32Pct = p32Total > 0 ? Math.round((p32Pairs / p32Total) * 100) : 0;
      const p4SmokePairs = Number(p4Smoke.present_pairs || 0);
      const p4SmokeTotal = Number(p4Smoke.total_pairs || 0);
      const p4SmokePct = p4SmokeTotal > 0 ? Math.round((p4SmokePairs / p4SmokeTotal) * 100) : 0;
      const p4MatrixPairs = Number(p4Matrix.present_pairs || 0);
      const p4MatrixTotal = Number(p4Matrix.total_pairs || 0);
      const p4MatrixPct = p4MatrixTotal > 0 ? Math.round((p4MatrixPairs / p4MatrixTotal) * 100) : 0;

      const v3 = data.v3_summary || {};
      const v3Pos = Number(v3.tot_vs_react_positive || 0);
      const v3Neg = Number(v3.tot_vs_react_negative || 0);
      const v4Gate = data.v4_gate_status || {};
      const v4GateStatus = String(v4Gate.status || "unknown");
      const v4GatePill = v4GateStatus === "ok" ? '<span class="pill good">ok</span>' :
        (v4GateStatus === "failed" ? '<span class="pill bad">failed</span>' : '<span class="pill">unknown</span>');
      const procCount = (data.runtime_processes || []).filter(p => p.alive).length;

      document.getElementById("topCards").innerHTML = [
        '<div class="card"><h2>v4 Matrix Pairs</h2><div class="metric">' + p4MatrixPairs + '/' + p4MatrixTotal + '</div><div class="small">' + p4MatrixPct + '% complete</div></div>',
        '<div class="card"><h2>v4 Smoke Pairs</h2><div class="metric">' + p4SmokePairs + '/' + p4SmokeTotal + '</div><div class="small">' + p4SmokePct + '% complete</div></div>',
        '<div class="card"><h2>v4 Gate</h2><div class="metric">' + v4GateStatus + '</div><div class="small">' + v4GatePill + '</div></div>',
        '<div class="card"><h2>v3.1 Pairs</h2><div class="metric">' + p31Pairs + '/' + p31Total + '</div><div class="small">' + p31Pct + '% complete</div></div>',
        '<div class="card"><h2>v3.2 Pairs</h2><div class="metric">' + p32Pairs + '/' + p32Total + '</div><div class="small">' + p32Pct + '% complete</div></div>',
        '<div class="card"><h2>v3 Direction</h2><div class="metric">' + v3Pos + ' / ' + v3Neg + '</div><div class="small">ToT>ReAct / ToT<ReAct blocks</div></div>',
        '<div class="card"><h2>Active Processes</h2><div class="metric">' + procCount + '</div><div class="small">from runtime PID files</div></div>'
      ].join("");

      const progressFilter = document.getElementById("progressVersionFilter");
      const selectedVersion = progressFilter && progressFilter.value ? progressFilter.value : "v4_matrix";
      const byVersion = {
        "v31": p31,
        "v32": p32,
        "v4_smoke": p4Smoke,
        "v4_matrix": p4Matrix
      };
      const active = byVersion[selectedVersion] || {};
      const activePairs = Number(active.present_pairs || 0);
      const activeTotal = Number(active.total_pairs || 0);
      const activePct = activeTotal > 0 ? Math.round((activePairs / activeTotal) * 100) : 0;
      const activeLabel = ({"v31":"v3.1","v32":"v3.2","v4_smoke":"v4-smoke","v4_matrix":"v4-matrix"})[selectedVersion] || selectedVersion;
      const activeDone = Number(active.done_blocks || 0);
      const activePartial = Number(active.partial_blocks || 0);
      const activeNotStarted = Number(active.not_started_blocks || 0);

      document.getElementById("v31ProgressBar").style.width = activePct + "%";
      document.getElementById("v31ProgressText").textContent =
        activeLabel + " pairs complete: " + activePairs + "/" + activeTotal + " (" + activePct + "%)" +
        " | blocks done/partial/not started: " + activeDone + "/" + activePartial + "/" + activeNotStarted;

      const blocks = (active.blocks || []).slice().sort((a,b) => {
        const ak = [a.task_id, a.model_id, a.profile].join("|");
        const bk = [b.task_id, b.model_id, b.profile].join("|");
        return ak.localeCompare(bk);
      });
      document.querySelector("#v31BlocksTable tbody").innerHTML = blocks.map(b =>
        "<tr><td>" + esc(b.report_version_label || b.report_version_id || activeLabel) + "</td><td>" +
        esc(b.task_id) + "</td><td>" + esc(b.model_id) + "</td><td>" + esc(b.profile) +
        "</td><td>" + esc(String(b.present_pairs) + "/" + String(b.total_pairs)) + "</td><td>" + statusPill(b.state) + "</td></tr>"
      ).join("");

      const procs = data.runtime_processes || [];
      document.querySelector("#procTable tbody").innerHTML = procs.map(p =>
        "<tr><td>" + esc(p.name) + "</td><td>" + esc(p.pid) + "</td><td>" + alivePill(!!p.alive) +
        "</td><td>" + esc(p.elapsed || "") + "</td><td>" + esc(p.last_line || "") + "</td></tr>"
      ).join("");

      const v3Rows = (v3.records || []).slice().sort((a,b) => {
        const ak = [a.task_id, a.model_id].join("|");
        const bk = [b.task_id, b.model_id].join("|");
        return ak.localeCompare(bk);
      });
      document.querySelector("#v3Table tbody").innerHTML = v3Rows.map(r =>
        "<tr><td>" + esc(r.task_id) + "</td><td>" + esc(r.model_id) + "</td><td>" + esc(fmtNum(r.tot_minus_react, 3)) +
        "</td><td>" + esc(fmtP(r.holm_p_tot_vs_react)) + "</td></tr>"
      ).join("");
      document.getElementById("v3SummaryText").textContent = "Summary source: " + (v3.path || "");

      lastSeriesRows = data.series_reports || data.v31_series || [];
      renderSeriesTable(lastSeriesRows);

      const files = data.latest_analysis || [];
      document.querySelector("#filesTable tbody").innerHTML = files.map(f =>
        "<tr><td>" + esc(f.name) + "</td><td>" + esc(fmtSize(f.size_bytes || 0)) + "</td><td>" + esc(fmtEpoch(f.mtime_epoch)) +
        "</td><td><a href='/api/file?path=" + encodeURIComponent(f.path) + "' target='_blank'>open</a></td></tr>"
      ).join("");

      const picker = document.getElementById("logPicker");
      const old = picker.value;
      picker.innerHTML = procs
        .filter(p => p.log_file)
        .map(p => "<option value='" + esc(p.log_file) + "'>" + esc(p.name + " :: " + p.log_file) + "</option>")
        .join("");
      if (old) picker.value = old;
      if (!picker.value && picker.options.length) picker.selectedIndex = 0;
    }

    async function refresh() {
      try {
        const data = await fetchJson("/api/overview");
        render(data);
      } catch (e) {
        console.error(e);
      }
    }

    document.getElementById("loadLogBtn").addEventListener("click", async function() {
      const path = document.getElementById("logPicker").value;
      await loadLog(path);
    });

    document.getElementById("seriesSearch").addEventListener("input", function() {
      renderSeriesTable(lastSeriesRows);
    });
    document.getElementById("seriesVersionFilter").addEventListener("change", function() {
      renderSeriesTable(lastSeriesRows);
    });
    document.getElementById("seriesTaskFilter").addEventListener("change", function() {
      renderSeriesTable(lastSeriesRows);
    });
    document.getElementById("seriesModelFilter").addEventListener("change", function() {
      renderSeriesTable(lastSeriesRows);
    });
    document.getElementById("seriesProfileFilter").addEventListener("change", function() {
      renderSeriesTable(lastSeriesRows);
    });
    document.getElementById("seriesReset").addEventListener("click", function() {
      document.getElementById("seriesSearch").value = "";
      document.getElementById("seriesVersionFilter").value = "";
      document.getElementById("seriesTaskFilter").value = "";
      document.getElementById("seriesModelFilter").value = "";
      document.getElementById("seriesProfileFilter").value = "";
      renderSeriesTable(lastSeriesRows);
    });
    document.getElementById("progressVersionFilter").addEventListener("change", function() {
      if (lastOverview) render(lastOverview);
    });
    document.querySelector("#seriesTable tbody").addEventListener("click", async function(evt) {
      const row = evt.target.closest("tr[data-path]");
      if (!row) return;
      const enc = row.getAttribute("data-path");
      if (!enc) return;
      const path = decodeURIComponent(enc);
      await inspectSeries(path);
      renderSeriesTable(lastSeriesRows);
    });

    refresh();
    setInterval(refresh, 8000);
    setInterval(async () => {
      const path = document.getElementById("logPicker").value;
      if (path) await loadLog(path);
    }, 8000);
  </script>
</body>
</html>
"""


class DashboardHandler(BaseHTTPRequestHandler):
    def _send_json(self, payload: Dict[str, Any], status: int = 200) -> None:
        data = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _send_text(self, text: str, status: int = 200, ctype: str = "text/plain; charset=utf-8") -> None:
        data = text.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format: str, *args: Any) -> None:
        return

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)

        if path == "/":
            self._send_text(html_template(), ctype="text/html; charset=utf-8")
            return

        if path == "/api/overview":
            self._send_json(build_overview())
            return

        if path == "/api/log":
            raw = (qs.get("path") or [""])[0]
            req = Path(raw)
            try:
                req.resolve().relative_to(ROOT)
            except Exception:
                self._send_json({"error": "path outside workspace"}, status=400)
                return
            tail = tail_text(req, lines=50)
            self._send_json({"path": str(req), "tail": tail})
            return

        if path == "/api/file":
            raw = (qs.get("path") or [""])[0]
            req = Path(raw)
            try:
                req.resolve().relative_to(ROOT)
            except Exception:
                self._send_text("invalid path", status=400)
                return
            if not req.exists() or req.is_dir():
                self._send_text("not found", status=404)
                return
            max_bytes = 300_000
            try:
                data = req.read_bytes()[:max_bytes]
                text = data.decode("utf-8", errors="replace")
            except Exception:
                self._send_text("unable to read file", status=500)
                return
            self._send_text(text, ctype="text/plain; charset=utf-8")
            return

        if path == "/api/series_detail":
            raw = (qs.get("path") or [""])[0]
            req = Path(raw)
            try:
                resolved = req.resolve()
                resolved.relative_to(ROOT.resolve())
            except Exception:
                self._send_json({"error": "invalid path"}, status=400)
                return
            if not resolved.exists() or resolved.is_dir():
                self._send_json({"error": "not found"}, status=404)
                return
            detail = load_series_detail(resolved)
            if detail is None:
                self._send_json({"error": "unable to parse report"}, status=500)
                return
            self._send_json(detail)
            return

        self._send_text("not found", status=404)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Phase2 experiment dashboard server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8787)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    server = ThreadingHTTPServer((args.host, args.port), DashboardHandler)
    print(f"dashboard_start host={args.host} port={args.port}", flush=True)
    try:
        server.serve_forever(poll_interval=0.5)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    print("dashboard_stop", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
