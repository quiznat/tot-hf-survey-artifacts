"""Tests for protocol-v3 task adapters and registry."""

from __future__ import annotations

import unittest

from phase2_baselines.tasks import create_task, resolve_task_id, supported_tasks


class SubsetSumTaskTests(unittest.TestCase):
    def setUp(self) -> None:
        self.task = create_task("subset-sum")
        self.input_data = {"numbers": [2, 4, 7, 9], "target": 13}

    def test_subset_sum_accepts_valid_selection(self) -> None:
        self.assertTrue(self.task.evaluate("4,9", self.input_data))

    def test_subset_sum_rejects_invalid_usage(self) -> None:
        self.assertFalse(self.task.evaluate("9,9", self.input_data))
        self.assertFalse(self.task.evaluate("2,4", self.input_data))

    def test_subset_sum_extracts_answer_from_verbose_reasoning(self) -> None:
        raw = (
            "Try combinations.\n"
            "2 + 4 + 7 = 13, this matches target.\n"
            "Answer: 2,4,7"
        )
        extracted = self.task.extract_final_answer(raw)
        self.assertTrue(self.task.evaluate(extracted, self.input_data))


class Linear2TaskTests(unittest.TestCase):
    def setUp(self) -> None:
        self.task = create_task("linear2")
        # x=2, y=3
        self.input_data = {"equations": [[1, 1, 5], [2, -1, 1]]}

    def test_linear2_accepts_correct_solution(self) -> None:
        self.assertTrue(self.task.evaluate("x=2,y=3", self.input_data))
        self.assertTrue(self.task.evaluate("FINAL: 2,3", self.input_data))

    def test_linear2_rejects_incorrect_solution(self) -> None:
        self.assertFalse(self.task.evaluate("x=1,y=1", self.input_data))

    def test_linear2_extracts_xy_from_reasoning(self) -> None:
        raw = (
            "Equation 1 gives x + y = 5.\n"
            "Equation 2 gives 2x - y = 1.\n"
            "Therefore x = 2, y = 3."
        )
        extracted = self.task.extract_final_answer(raw)
        self.assertTrue(self.task.evaluate(extracted, self.input_data))


class DigitPermutationTaskTests(unittest.TestCase):
    def setUp(self) -> None:
        self.task = create_task("digit-permutation")
        self.input_data = {"digits": [3, 2, 2, 5], "divisor": 6, "oracle_max": 5322}

    def test_digit_permutation_accepts_oracle_optimum(self) -> None:
        self.assertTrue(self.task.evaluate("5322", self.input_data))

    def test_digit_permutation_rejects_non_optimal_valid_number(self) -> None:
        self.assertFalse(self.task.evaluate("5232", self.input_data))

    def test_digit_permutation_extracts_integer_from_verbose_reasoning(self) -> None:
        raw = (
            "Check divisibility candidates: 5232, 5322, 5223.\n"
            "Largest valid answer is 5322."
        )
        extracted = self.task.extract_final_answer(raw)
        self.assertEqual(extracted, "5322")


class Arithmetic24ExtractionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.task = create_task("game24")
        self.input_data = [4, 4, 10, 10]

    def test_arithmetic24_extracts_expression_from_verbose_reasoning(self) -> None:
        raw = (
            "Try some options.\n"
            "(10+10)+4+4 = 28 (too high)\n"
            "Use (10*10-4)/4 = 24, so this works."
        )
        extracted = self.task.extract_final_answer(raw)
        self.assertTrue(self.task.evaluate(extracted, self.input_data))


class TaskRegistryTests(unittest.TestCase):
    def test_registry_alias_resolution(self) -> None:
        self.assertEqual(resolve_task_id("subset-sum"), "subset-sum-demo")
        self.assertEqual(resolve_task_id("linear2"), "linear2-demo")
        self.assertEqual(resolve_task_id("digit-permutation"), "digit-permutation-demo")

    def test_supported_tasks_contains_v3_set(self) -> None:
        task_ids = set(supported_tasks())
        self.assertIn("game24-demo", task_ids)
        self.assertIn("subset-sum-demo", task_ids)
        self.assertIn("linear2-demo", task_ids)
        self.assertIn("digit-permutation-demo", task_ids)


if __name__ == "__main__":
    unittest.main()
