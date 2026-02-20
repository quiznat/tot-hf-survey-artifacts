"""Tests for ToT prototype runner."""

from __future__ import annotations

import unittest

from phase2_baselines.adapters import ScriptedModel
from phase2_baselines.runners.tot import ToTRunner
from phase2_baselines.tasks import Arithmetic24Task


class ToTRunnerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.task = Arithmetic24Task()
        self.numbers = [4, 4, 10, 10]

    def test_tot_runner_success_with_generator_callbacks(self) -> None:
        model = ScriptedModel(responses=[])

        def generator(node, input_data, k):
            del input_data, k
            if node.depth == 0:
                return ["(10+4)+10+4", "(10*10-4)/4"]
            return []

        def evaluator(candidate, input_data):
            del input_data
            if candidate == "(10*10-4)/4":
                return 10.0
            return 1.0

        runner = ToTRunner(model=model, model_name="tot-test")
        runner.prepare(
            self.task,
            {
                "condition_id": "tot-prototype",
                "search_config": {
                    "depth": 3,
                    "breadth": 3,
                    "pruning": "topk_cumulative_score",
                    "stop_policy": "first_terminal_or_depth_limit",
                },
                "tool_config": [],
                "budget": {"token_budget": 2000, "time_budget_ms": 10000, "cost_budget_usd": 0.0},
                "max_depth": 3,
                "branch_factor": 3,
                "frontier_width": 2,
                "candidate_generator": generator,
                "candidate_evaluator": evaluator,
            },
        )

        manifest = runner.run(self.numbers)
        self.assertEqual(manifest["outcome"], "success")
        self.assertEqual(manifest["final_answer"], "(10*10-4)/4")
        self.assertIn("extra", manifest)
        self.assertEqual(manifest["extra"]["search_summary"]["stop_reason"], "terminal_solution")

    def test_tot_runner_failure_empty_frontier(self) -> None:
        model = ScriptedModel(responses=[])

        def generator(node, input_data, k):
            del node, input_data, k
            return []

        runner = ToTRunner(model=model, model_name="tot-test")
        runner.prepare(
            self.task,
            {
                "condition_id": "tot-prototype",
                "search_config": {
                    "depth": 2,
                    "breadth": 2,
                    "pruning": "topk_cumulative_score",
                    "stop_policy": "first_terminal_or_depth_limit",
                },
                "tool_config": [],
                "budget": {"token_budget": 1000, "time_budget_ms": 5000, "cost_budget_usd": 0.0},
                "max_depth": 2,
                "branch_factor": 2,
                "frontier_width": 2,
                "candidate_generator": generator,
            },
        )

        manifest = runner.run(self.numbers)
        self.assertEqual(manifest["outcome"], "failure")
        self.assertEqual(manifest["error_type"], "empty_frontier")

    def test_rule_based_evaluator_selects_best_frontier_candidate(self) -> None:
        model = ScriptedModel(responses=[])

        def generator(node, input_data, k):
            del node, input_data, k
            # First candidate is much farther from 24 than second candidate.
            return ["(10*10-4*4)", "(10+10)+4+4"]

        runner = ToTRunner(model=model, model_name="tot-test")
        runner.prepare(
            self.task,
            {
                "condition_id": "tot-prototype",
                "search_config": {
                    "depth": 1,
                    "breadth": 2,
                    "pruning": "topk_cumulative_score",
                    "stop_policy": "depth_limit",
                },
                "tool_config": [],
                "budget": {"token_budget": 1000, "time_budget_ms": 5000, "cost_budget_usd": 0.0},
                "max_depth": 1,
                "branch_factor": 2,
                "frontier_width": 1,
                "candidate_generator": generator,
                "evaluator_mode": "rule_based",
            },
        )

        manifest = runner.run(self.numbers)
        self.assertEqual(manifest["outcome"], "failure")
        self.assertEqual(manifest["error_type"], "depth_limit")
        self.assertEqual(manifest["final_answer"], "(10+10)+4+4")

    def test_model_self_eval_mode_uses_model_scores(self) -> None:
        model = ScriptedModel(
            responses=[
                "CANDIDATE: (10+10)+4+4\nCANDIDATE: (10+10+4)-4",
                "0.1",
                "0.9",
            ]
        )

        runner = ToTRunner(model=model, model_name="tot-test")
        runner.prepare(
            self.task,
            {
                "condition_id": "tot-prototype",
                "search_config": {
                    "depth": 1,
                    "breadth": 2,
                    "pruning": "topk_cumulative_score",
                    "stop_policy": "depth_limit",
                },
                "tool_config": [],
                "budget": {"token_budget": 1000, "time_budget_ms": 5000, "cost_budget_usd": 0.0},
                "max_depth": 1,
                "branch_factor": 2,
                "frontier_width": 1,
                "evaluator_mode": "model_self_eval",
            },
        )

        manifest = runner.run(self.numbers)
        self.assertEqual(manifest["outcome"], "failure")
        self.assertEqual(manifest["error_type"], "depth_limit")
        self.assertEqual(manifest["final_answer"], "(10+10+4)-4")


if __name__ == "__main__":
    unittest.main()
