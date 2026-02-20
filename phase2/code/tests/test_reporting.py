"""Tests for condition-level baseline reporting utilities."""

from __future__ import annotations

import unittest

from phase2_baselines.reporting import summarize_by_condition


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


if __name__ == "__main__":
    unittest.main()
