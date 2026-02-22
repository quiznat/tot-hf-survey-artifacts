"""Smoke tests for baseline runner scaffolding."""

from __future__ import annotations

import unittest

from phase2_baselines.adapters import ScriptedModel
from phase2_baselines.runners import ReactRunner, SinglePathRunner
from phase2_baselines.tasks import Arithmetic24Task


class RunnerSmokeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.task = Arithmetic24Task()
        self.numbers = [4, 4, 10, 10]

    def test_single_path_success(self) -> None:
        model = ScriptedModel(responses=["(10*10-4)/4"])
        runner = SinglePathRunner(model=model, model_name="test-single")
        runner.prepare(
            self.task,
            {
                "condition_id": "baseline-single-path",
                "search_config": {"depth": 0, "breadth": 0, "pruning": "none", "stop_policy": "single-pass"},
                "tool_config": [],
                "budget": {"token_budget": 1, "time_budget_ms": 1, "cost_budget_usd": 0.0},
                "item_id": "test-item-001",
                "panel_id": "test-panel-v1",
                "input_data": self.numbers,
            },
        )
        manifest = runner.run(self.numbers)
        self.assertEqual(manifest["outcome"], "success")
        self.assertEqual(manifest["metrics"]["success"], 1)
        self.assertEqual(manifest["item_id"], "test-item-001")
        self.assertEqual(manifest["panel_id"], "test-panel-v1")
        self.assertEqual(manifest["input_data"], self.numbers)

    def test_react_success(self) -> None:
        model = ScriptedModel(
            responses=[
                "ACTION: calc (10*10-4)/4",
                "FINAL: (10*10-4)/4",
            ]
        )
        runner = ReactRunner(model=model, model_name="test-react")
        runner.prepare(
            self.task,
            {
                "condition_id": "baseline-react",
                "search_config": {"depth": 1, "breadth": 1, "pruning": "none", "stop_policy": "max_steps_or_final"},
                "tool_config": ["calc"],
                "budget": {"token_budget": 1, "time_budget_ms": 1, "cost_budget_usd": 0.0},
                "max_steps": 5,
            },
        )
        manifest = runner.run(self.numbers)
        self.assertEqual(manifest["outcome"], "success")
        self.assertEqual(manifest["metrics"]["success"], 1)

    def test_react_fallback_expression_parse(self) -> None:
        model = ScriptedModel(
            responses=[
                "$\\\\frac{10*10-4}{4}$",
            ]
        )
        runner = ReactRunner(model=model, model_name="test-react")
        runner.prepare(
            self.task,
            {
                "condition_id": "baseline-react",
                "search_config": {"depth": 1, "breadth": 1, "pruning": "none", "stop_policy": "max_steps_or_final"},
                "tool_config": ["calc"],
                "budget": {"token_budget": 1, "time_budget_ms": 1, "cost_budget_usd": 0.0},
                "max_steps": 2,
            },
        )
        manifest = runner.run(self.numbers)
        self.assertEqual(manifest["outcome"], "success")

    def test_react_action_plus_numeric_final_recovers_expression(self) -> None:
        model = ScriptedModel(
            responses=[
                "ACTION: calc (10*10-4)/4\nFINAL: 24",
            ]
        )
        runner = ReactRunner(model=model, model_name="test-react")
        runner.prepare(
            self.task,
            {
                "condition_id": "baseline-react",
                "search_config": {"depth": 1, "breadth": 1, "pruning": "none", "stop_policy": "max_steps_or_final"},
                "tool_config": ["calc"],
                "budget": {"token_budget": 1, "time_budget_ms": 1, "cost_budget_usd": 0.0},
                "max_steps": 2,
            },
        )
        manifest = runner.run(self.numbers)
        self.assertEqual(manifest["outcome"], "success")
        self.assertEqual(manifest["final_answer"], "(10*10-4)/4")

    def test_react_can_disable_tools_for_capability_parity(self) -> None:
        model = ScriptedModel(
            responses=[
                "ACTION: calc (10*10-4)/4",
                "ACTION: calc (10*10-4)/4",
            ]
        )
        runner = ReactRunner(model=model, model_name="test-react")
        runner.prepare(
            self.task,
            {
                "condition_id": "baseline-react",
                "search_config": {"depth": 1, "breadth": 1, "pruning": "none", "stop_policy": "max_steps_or_final"},
                "tool_config": [],
                "react_enable_tools": False,
                "budget": {"token_budget": 1, "time_budget_ms": 1, "cost_budget_usd": 0.0},
                "max_steps": 2,
            },
        )
        manifest = runner.run(self.numbers)
        self.assertEqual(manifest["outcome"], "timeout")
        self.assertIn("unknown tool 'calc'", "\n".join(manifest["trace"]))


if __name__ == "__main__":
    unittest.main()
