"""Tests for ToT prototype runner."""

from __future__ import annotations

import unittest

from phase2_baselines.adapters import ScriptedModel
from phase2_baselines.runners.tot import ToTRunner
from phase2_baselines.tasks import Arithmetic24Task, create_task


class RecordingScriptedModel(ScriptedModel):
    def __init__(self, responses: list[str], fallback: str = "") -> None:
        super().__init__(responses=responses, fallback=fallback)
        self.prompts: list[str] = []

    def generate(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return super().generate(prompt)


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

    def test_task_specific_candidate_prompt_linear2(self) -> None:
        task = create_task("linear2")
        input_data = {"equations": [[1, 0, 2], [0, 1, 3]]}
        model = RecordingScriptedModel(responses=["x=2,y=3"])

        runner = ToTRunner(model=model, model_name="tot-test")
        runner.prepare(
            task,
            {
                "condition_id": "tot-prototype",
                "search_config": {
                    "depth": 1,
                    "breadth": 1,
                    "pruning": "topk_cumulative_score",
                    "stop_policy": "first_terminal_or_depth_limit",
                },
                "tool_config": [],
                "budget": {"token_budget": 500, "time_budget_ms": 5000, "cost_budget_usd": 0.0},
                "max_depth": 1,
                "branch_factor": 1,
                "frontier_width": 1,
                "evaluator_mode": "rule_based",
            },
        )

        manifest = runner.run(input_data)
        self.assertEqual(manifest["outcome"], "success")
        self.assertIn("x=<value>,y=<value>", model.prompts[0])
        self.assertNotIn("arithmetic expressions", model.prompts[0])

    def test_task_specific_candidate_prompt_digit_permutation(self) -> None:
        task = create_task("digit-permutation")
        input_data = {"digits": [5, 3, 2, 2], "divisor": 3, "oracle_max": 5322}
        model = RecordingScriptedModel(responses=["5322"])

        runner = ToTRunner(model=model, model_name="tot-test")
        runner.prepare(
            task,
            {
                "condition_id": "tot-prototype",
                "search_config": {
                    "depth": 1,
                    "breadth": 1,
                    "pruning": "topk_cumulative_score",
                    "stop_policy": "first_terminal_or_depth_limit",
                },
                "tool_config": [],
                "budget": {"token_budget": 500, "time_budget_ms": 5000, "cost_budget_usd": 0.0},
                "max_depth": 1,
                "branch_factor": 1,
                "frontier_width": 1,
                "evaluator_mode": "rule_based",
            },
        )

        manifest = runner.run(input_data)
        self.assertEqual(manifest["outcome"], "success")
        self.assertIn("single 4-digit integer", model.prompts[0])
        self.assertNotIn("arithmetic expressions", model.prompts[0])


if __name__ == "__main__":
    unittest.main()
