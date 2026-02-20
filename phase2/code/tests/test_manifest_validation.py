"""Validation tests for run manifest utilities."""

from __future__ import annotations

import unittest

from phase2_baselines.manifest import REQUIRED_FIELDS, validate_manifest


class ManifestValidationTests(unittest.TestCase):
    def _valid_manifest(self) -> dict:
        return {
            "run_id": "RUN-TEST-0001",
            "timestamp_utc": "2026-02-20T01:30:00Z",
            "task_id": "game24-demo",
            "condition_id": "baseline-single-path",
            "model_name": "scripted-single-v1",
            "provider": "local",
            "agent_framework": "phase2-baselines@0.1",
            "prompt_template_version": "v1",
            "search_config": {"depth": 0, "breadth": 0, "pruning": "none", "stop_policy": "single-pass"},
            "tool_config": [],
            "seed": 0,
            "budget": {"token_budget": 1000, "time_budget_ms": 5000, "cost_budget_usd": 0.0},
            "outcome": "success",
            "metrics": {"success": 1, "latency_ms": 10, "tokens_in": 20, "tokens_out": 5, "cost_usd": 0.0},
            "artifact_paths": ["/tmp/run.json"],
            "notes": "ok",
        }

    def test_validate_manifest_accepts_required_fields(self) -> None:
        manifest = self._valid_manifest()
        validate_manifest(manifest)

    def test_validate_manifest_rejects_missing_required(self) -> None:
        for required in REQUIRED_FIELDS:
            manifest = self._valid_manifest()
            del manifest[required]
            with self.assertRaises(ValueError):
                validate_manifest(manifest)

    def test_validate_manifest_rejects_non_utc_timestamp(self) -> None:
        manifest = self._valid_manifest()
        manifest["timestamp_utc"] = "2026-02-20T01:30:00+00:00"
        with self.assertRaises(ValueError):
            validate_manifest(manifest)


if __name__ == "__main__":
    unittest.main()
