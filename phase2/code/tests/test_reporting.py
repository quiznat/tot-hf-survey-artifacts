"""Tests for condition-level baseline reporting utilities."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
import unittest

from phase2_baselines.reporting import load_manifests_from_dir, summarize_by_condition


class ReportingTests(unittest.TestCase):
    def test_summarize_by_condition(self) -> None:
        manifests = [
            {
                "condition_id": "baseline-single-path",
                "metrics": {"success": 1, "latency_ms": 10, "tokens_in": 20, "tokens_out": 5, "cost_usd": 0.01},
            },
            {
                "condition_id": "baseline-single-path",
                "metrics": {"success": 0, "latency_ms": 30, "tokens_in": 24, "tokens_out": 7, "cost_usd": 0.02},
            },
            {
                "condition_id": "baseline-react",
                "metrics": {"success": 1, "latency_ms": 50, "tokens_in": 40, "tokens_out": 10, "cost_usd": 0.03},
            },
        ]

        summaries = summarize_by_condition(manifests)
        by_condition = {row["condition_id"]: row for row in summaries}

        self.assertAlmostEqual(by_condition["baseline-single-path"]["success_rate"], 0.5)
        self.assertEqual(by_condition["baseline-single-path"]["runs"], 2)
        self.assertEqual(by_condition["baseline-react"]["runs"], 1)

    def test_load_manifests_from_dir(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "valid-a.json").write_text(json.dumps({"condition_id": "a", "metrics": {}}), encoding="utf-8")
            (root / "valid-b.json").write_text(json.dumps({"condition_id": "b", "metrics": {}}), encoding="utf-8")
            (root / "invalid.json").write_text("{not-json", encoding="utf-8")
            (root / "not-a-dict.json").write_text(json.dumps([1, 2, 3]), encoding="utf-8")

            manifests = load_manifests_from_dir(root)
            self.assertEqual(len(manifests), 2)


if __name__ == "__main__":
    unittest.main()
