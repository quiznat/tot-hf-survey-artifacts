#!/usr/bin/env python3
"""Execute protocol-v4 gate checks before confirmatory matrix launch."""

from __future__ import annotations

import argparse
import copy
import glob
import json
import os
from pathlib import Path
import subprocess
from typing import Any, Dict, List


ROOT = Path("/Users/quiznat/Desktop/Tree_of_Thought/phase2")
SMOKE_SCRIPT = ROOT / "code/scripts/run_protocol_v4_smoke.py"
AUDIT_SCRIPT = ROOT / "code/scripts/audit_capability_parity.py"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run protocol-v4 pre-launch gate checks")
    parser.add_argument("--model-id", default="Qwen/Qwen3-Coder-Next:novita")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--max-workers", type=int, default=8)
    parser.add_argument(
        "--max-attempts-per-task",
        type=int,
        default=3,
        help="Bounded infrastructure retries for per-task smoke commands.",
    )
    parser.add_argument(
        "--retry-backoff-seconds",
        type=int,
        default=20,
        help="Base backoff for smoke retries (exponential).",
    )
    parser.add_argument(
        "--capability-parity-policy",
        choices=["equalize_react_to_tot", "strict"],
        default="equalize_react_to_tot",
    )
    parser.add_argument("--skip-tests", action="store_true")
    parser.add_argument("--skip-smoke", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--out-md",
        default=str(ROOT / "benchmarks/analysis/protocol_v4_gate_report.md"),
        help="Markdown gate report path",
    )
    parser.add_argument(
        "--out-json",
        default=str(ROOT / "benchmarks/analysis/protocol_v4_gate_report.json"),
        help="JSON gate report path",
    )
    return parser.parse_args()


def _run(cmd: List[str], env: Dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=str(ROOT), env=env, text=True, capture_output=True, check=False)


def _load_smoke_reports() -> Dict[str, Dict[str, Any]]:
    pattern = str(ROOT / "benchmarks/analysis/*_smoke_report_*_v4.json")
    reports: Dict[str, Dict[str, Any]] = {}
    for path in sorted(glob.glob(pattern)):
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        task_id = str(payload.get("task_id", "")).strip()
        if not task_id:
            continue
        reports[path] = payload
    return reports


def _canonical(payload: Dict[str, Any]) -> Dict[str, Any]:
    condition_summaries = list(payload.get("condition_summaries") or [])
    if condition_summaries:
        condition_summaries = sorted(
            condition_summaries,
            key=lambda row: str(row.get("condition_id", "")),
        )

    paired_comparison = list(payload.get("paired_comparison") or [])
    if paired_comparison:
        paired_comparison = sorted(
            paired_comparison,
            key=lambda row: (
                str(row.get("condition_a", "")),
                str(row.get("condition_b", "")),
            ),
        )

    return {
        "task_id": payload.get("task_id"),
        "panel_id": payload.get("panel_id"),
        "model_id": payload.get("model_id"),
        "provider": payload.get("provider"),
        "tot_evaluator_mode": payload.get("tot_evaluator_mode"),
        "tot_max_depth": payload.get("tot_max_depth"),
        "tot_branch_factor": payload.get("tot_branch_factor"),
        "tot_frontier_width": payload.get("tot_frontier_width"),
        "seed_policy": payload.get("seed_policy"),
        "hf_temperature": payload.get("hf_temperature"),
        "hf_top_p": payload.get("hf_top_p"),
        "capability_parity_policy": payload.get("capability_parity_policy"),
        "task_tools_available": payload.get("task_tools_available"),
        "condition_tools_exposed": payload.get("condition_tools_exposed"),
        "items_evaluated": payload.get("items_evaluated"),
        "runs_executed": payload.get("runs_executed"),
        "condition_summaries": condition_summaries,
        "paired_comparison": paired_comparison,
    }


def main() -> int:
    args = parse_args()
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "code/src")

    result: Dict[str, Any] = {
        "status": "ok",
        "checks": [],
    }

    if not args.skip_tests:
        test_cmd = [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(ROOT / "code/tests"),
        ]
        if args.dry_run:
            result["checks"].append({"name": "unit_tests", "status": "dry_run", "cmd": test_cmd})
        else:
            proc = _run(test_cmd, env=env)
            passed = proc.returncode == 0
            result["checks"].append(
                {
                    "name": "unit_tests",
                    "status": "passed" if passed else "failed",
                    "cmd": test_cmd,
                    "returncode": proc.returncode,
                    "stdout": proc.stdout[-4000:],
                    "stderr": proc.stderr[-4000:],
                }
            )
            if not passed:
                result["status"] = "failed"

    smoke_cmd = [
        "python3",
        str(SMOKE_SCRIPT),
        "--model-id",
        args.model_id,
        "--limit",
        str(args.limit),
        "--max-workers",
        str(args.max_workers),
        "--max-attempts-per-task",
        str(args.max_attempts_per_task),
        "--retry-backoff-seconds",
        str(args.retry_backoff_seconds),
        "--capability-parity-policy",
        args.capability_parity_policy,
    ]

    if not args.skip_smoke:
        if args.dry_run:
            result["checks"].append({"name": "smoke_execution", "status": "dry_run", "cmd": smoke_cmd})
        else:
            proc = _run(smoke_cmd, env=env)
            passed = proc.returncode == 0
            result["checks"].append(
                {
                    "name": "smoke_execution",
                    "status": "passed" if passed else "failed",
                    "cmd": smoke_cmd,
                    "returncode": proc.returncode,
                    "stdout": proc.stdout[-4000:],
                    "stderr": proc.stderr[-4000:],
                }
            )
            if not passed:
                result["status"] = "failed"

    if not args.dry_run and result["status"] == "ok":
        audit_md = ROOT / "benchmarks/analysis/protocol_v4_smoke_capability_audit.md"
        audit_json = ROOT / "benchmarks/analysis/protocol_v4_smoke_capability_audit.json"
        audit_cmd = [
            "python3",
            str(AUDIT_SCRIPT),
            "--series",
            "protocol_v4_smoke",
            "--out-md",
            str(audit_md),
            "--out-json",
            str(audit_json),
        ]
        proc = _run(audit_cmd, env=env)
        passed = proc.returncode == 0
        finding_count = None
        if passed and audit_json.exists():
            payload = json.loads(audit_json.read_text(encoding="utf-8"))
            finding_count = len(payload.get("findings", []))
            passed = finding_count == 0
        result["checks"].append(
            {
                "name": "capability_audit_smoke",
                "status": "passed" if passed else "failed",
                "cmd": audit_cmd,
                "returncode": proc.returncode,
                "finding_count": finding_count,
                "stdout": proc.stdout[-4000:],
                "stderr": proc.stderr[-4000:],
                "artifact_md": str(audit_md),
                "artifact_json": str(audit_json),
            }
        )
        if not passed:
            result["status"] = "failed"

    if not args.dry_run and result["status"] == "ok":
        parity_cmd = smoke_cmd + ["--report-only"]
        proc_first = _run(parity_cmd, env=env)
        parity_ok = proc_first.returncode == 0
        mismatch_paths: List[str] = []
        proc_second = None

        if parity_ok:
            baseline = _load_smoke_reports()
            baseline_canonical = {path: _canonical(payload) for path, payload in baseline.items()}

            proc_second = _run(parity_cmd, env=env)
            parity_ok = proc_second.returncode == 0
            if parity_ok:
                after = _load_smoke_reports()
                after_canonical = {path: _canonical(payload) for path, payload in after.items()}
                if set(after_canonical.keys()) != set(baseline_canonical.keys()):
                    parity_ok = False
                else:
                    for path in sorted(baseline_canonical.keys()):
                        if baseline_canonical[path] != after_canonical[path]:
                            mismatch_paths.append(path)
                    if mismatch_paths:
                        parity_ok = False

        stdout_tail = (proc_first.stdout[-2000:] if proc_first.stdout else "") + (
            ("\n\n--- second pass ---\n" + proc_second.stdout[-2000:]) if proc_second and proc_second.stdout else ""
        )
        stderr_tail = (proc_first.stderr[-2000:] if proc_first.stderr else "") + (
            ("\n\n--- second pass ---\n" + proc_second.stderr[-2000:]) if proc_second and proc_second.stderr else ""
        )

        result["checks"].append(
            {
                "name": "report_only_parity_smoke",
                "status": "passed" if parity_ok else "failed",
                "cmd": [parity_cmd, parity_cmd],
                "returncode": proc_second.returncode if proc_second else proc_first.returncode,
                "mismatch_paths": mismatch_paths,
                "stdout": stdout_tail,
                "stderr": stderr_tail,
            }
        )
        if not parity_ok:
            result["status"] = "failed"

    out_md = Path(args.out_md)
    out_json = Path(args.out_json)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)

    out_json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Protocol v4 Gate Report",
        "",
        f"Status: {result['status']}",
        "",
        "| Check | Status |",
        "|---|---|",
    ]
    for check in result["checks"]:
        lines.append(f"| {check['name']} | {check['status']} |")
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"out_md={out_md}")
    print(f"out_json={out_json}")

    return 0 if result["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
