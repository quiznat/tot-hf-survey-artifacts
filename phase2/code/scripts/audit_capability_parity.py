#!/usr/bin/env python3
"""Audit capability parity between paired conditions across code and run artifacts."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from phase2_baselines.tasks import create_task, supported_tasks


ROOT = Path("/Users/quiznat/Desktop/Tree_of_Thought/phase2")
RUNS_ROOT = ROOT / "benchmarks/runs"


def _discover_series_names() -> List[str]:
    if not RUNS_ROOT.exists():
        return []
    return sorted(path.name for path in RUNS_ROOT.iterdir() if path.is_dir())


@dataclass
class ConditionAudit:
    runs: int = 0
    action_traces: int = 0
    tool_set_counts: Dict[str, int] | None = None

    def __post_init__(self) -> None:
        if self.tool_set_counts is None:
            self.tool_set_counts = {}

    def add(self, tool_set: str, has_action: bool) -> None:
        self.runs += 1
        self.tool_set_counts[tool_set] = self.tool_set_counts.get(tool_set, 0) + 1
        if has_action:
            self.action_traces += 1

    def action_rate(self) -> float:
        if self.runs <= 0:
            return 0.0
        return self.action_traces / self.runs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit paired-condition capability parity")
    discovered = _discover_series_names()
    parser.add_argument(
        "--series",
        default=",".join(discovered),
        help="Comma-separated run subdirectories under phase2/benchmarks/runs",
    )
    parser.add_argument(
        "--out-md",
        default=str(ROOT / "benchmarks/analysis/capability_parity_audit.md"),
        help="Markdown report output path",
    )
    parser.add_argument(
        "--out-json",
        default=str(ROOT / "benchmarks/analysis/capability_parity_audit.json"),
        help="JSON report output path",
    )
    return parser.parse_args()


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _serialize_tool_set(tools: Any) -> str:
    if not isinstance(tools, list):
        return ""
    clean = sorted(str(x).strip() for x in tools if str(x).strip())
    return ",".join(clean)


def _task_tools() -> Dict[str, List[str]]:
    out: Dict[str, List[str]] = {}
    for task_id in supported_tasks():
        task = create_task(task_id)
        out[task_id] = sorted(task.available_tools().keys())
    return out


def _scan_series(series_name: str) -> Dict[str, Dict[str, ConditionAudit]]:
    series_dir = RUNS_ROOT / series_name
    by_task: Dict[str, Dict[str, ConditionAudit]] = {}
    if not series_dir.exists():
        return by_task

    for path in series_dir.rglob("*.json"):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(payload, dict):
            continue
        task_id = str(payload.get("task_id", "")).strip()
        condition_id = str(payload.get("condition_id", "")).strip()
        if not task_id or not condition_id:
            continue

        trace = payload.get("trace", [])
        has_action = False
        if isinstance(trace, list):
            joined = "\n".join(str(x) for x in trace)
            has_action = "ACTION:" in joined

        tool_set = _serialize_tool_set(payload.get("tool_config", []))
        by_task.setdefault(task_id, {})
        by_task[task_id].setdefault(condition_id, ConditionAudit())
        by_task[task_id][condition_id].add(tool_set=tool_set, has_action=has_action)

    return by_task


def _sorted_tool_sets(audit: ConditionAudit | None) -> List[Tuple[str, int]]:
    if audit is None or audit.tool_set_counts is None:
        return []
    items = [(key, count) for key, count in audit.tool_set_counts.items()]
    items.sort(key=lambda row: (-row[1], row[0]))
    return items


def _format_tool_set_label(raw: str) -> str:
    return raw if raw else "(none)"


def _code_checks() -> List[Dict[str, Any]]:
    checks: List[Dict[str, Any]] = []

    targets = [
        (
            ROOT / "code/src/phase2_baselines/runners/react.py",
            "react_enable_tools = bool(self.config.get(\"react_enable_tools\", True))",
            "React runner supports explicit tool enable/disable policy.",
        ),
        (
            ROOT / "code/scripts/run_structured_lockset.py",
            "def _resolve_capability_plan(",
            "Structured lockset runner enforces capability parity policy before execution.",
        ),
        (
            ROOT / "code/scripts/run_game24_lockset.py",
            "def _resolve_capability_plan(",
            "Legacy Game24 lockset runner enforces the same capability parity policy.",
        ),
        (
            ROOT / "code/src/phase2_baselines/pipeline.py",
            "tool_config = list(task_tool_names) if react_enable_tools else []",
            "Baseline pipeline reflects task-accurate React tool exposure in manifests.",
        ),
    ]

    for file_path, needle, description in targets:
        line_no = 0
        status = "missing"
        if file_path.exists():
            lines = file_path.read_text(encoding="utf-8").splitlines()
            for idx, line in enumerate(lines, start=1):
                if needle in line:
                    line_no = idx
                    status = "ok"
                    break
        checks.append(
            {
                "file": str(file_path),
                "line": line_no,
                "needle": needle,
                "description": description,
                "status": status,
            }
        )
    return checks


def _build_audit_payload(series_names: List[str]) -> Dict[str, Any]:
    task_tools = _task_tools()
    code_checks = _code_checks()

    series_results: Dict[str, Any] = {}
    findings: List[Dict[str, Any]] = []

    for series_name in series_names:
        task_condition_map = _scan_series(series_name)
        series_results[series_name] = {"tasks": {}}

        for task_id in sorted(task_condition_map.keys()):
            conds = task_condition_map[task_id]
            react = conds.get("baseline-react")
            tot = conds.get("tot-prototype")
            single = conds.get("baseline-single-path")
            declared_task_tools = task_tools.get(task_id, [])
            declared_task_set = ",".join(declared_task_tools)

            task_entry: Dict[str, Any] = {
                "task_tools": declared_task_tools,
                "conditions": {},
            }

            for cond_name, audit in sorted(conds.items()):
                task_entry["conditions"][cond_name] = {
                    "runs": audit.runs,
                    "action_traces": audit.action_traces,
                    "action_rate": round(audit.action_rate(), 6),
                    "tool_sets": [
                        {"tools": tool_set, "runs": count}
                        for tool_set, count in _sorted_tool_sets(audit)
                    ],
                }

            series_results[series_name]["tasks"][task_id] = task_entry

            react_sets = {tool_set for tool_set, _ in _sorted_tool_sets(react)}
            tot_sets = {tool_set for tool_set, _ in _sorted_tool_sets(tot)}
            react_none_only = react_sets == {""}
            tot_none_only = tot_sets == {""}

            if react is not None and tot is not None and react_sets != tot_sets:
                findings.append(
                    {
                        "severity": "high",
                        "type": "paired_condition_tool_mismatch",
                        "series": series_name,
                        "task_id": task_id,
                        "react_tool_sets": sorted(react_sets),
                        "tot_tool_sets": sorted(tot_sets),
                        "message": "React and ToT tool exposure differ within paired comparisons.",
                    }
                )

            if react is not None and react_sets:
                # If both paired conditions expose no tools, this can be an intentional parity equalization policy.
                if not (react_none_only and tot_none_only) and declared_task_set not in react_sets:
                    findings.append(
                        {
                            "severity": "medium",
                            "type": "react_manifest_tool_declaration_mismatch",
                            "series": series_name,
                            "task_id": task_id,
                            "task_tools": declared_task_tools,
                            "react_tool_sets": sorted(react_sets),
                            "message": "React manifest tool_config differs from task.available_tools() declaration.",
                        }
                    )

            if single is not None:
                single_sets = {tool_set for tool_set, _ in _sorted_tool_sets(single)}
                if single_sets - {""}:
                    findings.append(
                        {
                            "severity": "low",
                            "type": "single_condition_has_tools",
                            "series": series_name,
                            "task_id": task_id,
                            "single_tool_sets": sorted(single_sets),
                            "message": "Single-path condition should not expose tools.",
                        }
                    )

    return {
        "generated_utc": _utc_now(),
        "series": series_names,
        "task_tools": task_tools,
        "code_checks": code_checks,
        "series_results": series_results,
        "findings": findings,
    }


def _write_outputs(payload: Dict[str, Any], out_md: Path, out_json: Path) -> None:
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines: List[str] = []
    lines.append("# Capability Parity Audit")
    lines.append("")
    lines.append(f"Generated UTC: {payload['generated_utc']}")
    lines.append("")
    lines.append("## Task Tool Declarations")
    lines.append("")
    lines.append("| Task | Declared Tools |")
    lines.append("|---|---|")
    for task_id, tools in sorted(payload["task_tools"].items()):
        tool_label = ", ".join(tools) if tools else "none"
        lines.append(f"| `{task_id}` | `{tool_label}` |")

    lines.append("")
    lines.append("## Code Guardrails")
    lines.append("")
    lines.append("| Status | File | Line | Description |")
    lines.append("|---|---|---:|---|")
    for check in payload["code_checks"]:
        status = "ok" if check["status"] == "ok" else "missing"
        line = int(check.get("line", 0) or 0)
        lines.append(
            f"| `{status}` | `{check['file']}` | {line} | {check['description']} |"
        )

    lines.append("")
    lines.append("## Series Audit")
    lines.append("")
    for series_name in payload["series"]:
        lines.append(f"### {series_name}")
        lines.append("")
        lines.append("| Task | Condition | Runs | Action Rate | Tool Sets (runs) |")
        lines.append("|---|---|---:|---:|---|")
        tasks = payload["series_results"].get(series_name, {}).get("tasks", {})
        for task_id in sorted(tasks.keys()):
            conds = tasks[task_id].get("conditions", {})
            for cond_name in sorted(conds.keys()):
                cond = conds[cond_name]
                tool_sets = cond.get("tool_sets", [])
                tool_label = ", ".join(
                    f"{_format_tool_set_label(item['tools'])} ({item['runs']})" for item in tool_sets
                ) or "(none)"
                lines.append(
                    f"| `{task_id}` | `{cond_name}` | {cond['runs']} | {cond['action_rate']:.3f} | {tool_label} |"
                )
        lines.append("")

    lines.append("## Findings")
    lines.append("")
    findings = payload.get("findings", [])
    if not findings:
        lines.append("No capability parity findings.")
    else:
        lines.append("| Severity | Type | Series | Task | Message |")
        lines.append("|---|---|---|---|---|")
        for finding in findings:
            lines.append(
                "| `{severity}` | `{type}` | `{series}` | `{task}` | {message} |".format(
                    severity=finding.get("severity", ""),
                    type=finding.get("type", ""),
                    series=finding.get("series", ""),
                    task=finding.get("task_id", ""),
                    message=finding.get("message", ""),
                )
            )

    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    series_names = [name.strip() for name in str(args.series).split(",") if name.strip()]
    payload = _build_audit_payload(series_names=series_names)
    _write_outputs(payload=payload, out_md=Path(args.out_md), out_json=Path(args.out_json))
    print(f"audit_md={args.out_md}")
    print(f"audit_json={args.out_json}")
    print(f"findings={len(payload.get('findings', []))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
