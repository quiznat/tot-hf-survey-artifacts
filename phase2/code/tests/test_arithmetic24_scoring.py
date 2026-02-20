"""Tests for Arithmetic24Task normalization and scoring."""

from __future__ import annotations

import unittest

from phase2_baselines.tasks import Arithmetic24Task


class Arithmetic24ScoringTests(unittest.TestCase):
    def setUp(self) -> None:
        self.task = Arithmetic24Task()
        self.numbers = [4, 4, 10, 10]

    def test_exact_candidate_scores_one(self) -> None:
        score = self.task.score_candidate("(10*10-4)/4", self.numbers)
        self.assertEqual(score, 1.0)

    def test_unicode_candidate_is_normalized_for_analysis(self) -> None:
        analysis = self.task.analyze_candidate("(10×10 - 4×4) = 24", self.numbers)
        self.assertTrue(analysis["parseable"])
        self.assertTrue(analysis["uses_required_numbers"])
        self.assertAlmostEqual(float(analysis["value"]), 84.0)
        self.assertFalse(analysis["is_exact"])

    def test_invalid_candidate_scores_lower_than_closer_candidate(self) -> None:
        far_score = self.task.score_candidate("(10*10-4*4)", self.numbers)
        closer_score = self.task.score_candidate("(10+10)+4+4", self.numbers)
        self.assertGreater(closer_score, far_score)


if __name__ == "__main__":
    unittest.main()
