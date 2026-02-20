"""Manifest creation, validation, and storage utilities."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict
from uuid import uuid4

REQUIRED_FIELDS = [
    "run_id",
    "timestamp_utc",
    "task_id",
    "condition_id",
    "model_name",
    "provider",
    "agent_framework",
    "prompt_template_version",
    "search_config",
    "tool_config",
    "seed",
    "budget",
    "outcome",
    "metrics",
    "artifact_paths",
    "notes",
]


def utc_now_iso() -> str:
    """Return current UTC timestamp in ISO-8601 format."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def generate_run_id(prefix: str = "RUN") -> str:
    """Generate a compact run identifier."""
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"{prefix}-{stamp}-{uuid4().hex[:6]}"


def validate_manifest(manifest: Dict[str, Any]) -> None:
    """Validate minimal required fields for a run manifest."""
    missing = [key for key in REQUIRED_FIELDS if key not in manifest]
    if missing:
        raise ValueError(f"Manifest missing required fields: {missing}")
    if not str(manifest["timestamp_utc"]).endswith("Z"):
        raise ValueError("timestamp_utc must be UTC (suffix Z)")


def write_manifest(manifest: Dict[str, Any], out_path: Path) -> Path:
    """Write a run manifest JSON file."""
    validate_manifest(manifest)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return out_path


def append_run_log(log_path: Path, manifest: Dict[str, Any]) -> None:
    """Append one markdown table row to the run log."""
    row = (
        f"| {manifest['run_id']} | {manifest['timestamp_utc']} | {manifest['task_id']} | "
        f"{manifest['condition_id']} | {manifest['outcome']} | {manifest['notes'] or '-'} |\n"
    )
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(row)
