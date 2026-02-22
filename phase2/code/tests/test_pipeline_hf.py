"""Tests for Hugging Face provider wiring in baseline pipeline."""

from __future__ import annotations

import os
import unittest

from phase2_baselines.pipeline import create_baseline_setup


class PipelineHFTests(unittest.TestCase):
    def test_hf_provider_requires_token(self) -> None:
        token_env = "HF_TOKEN_TEST_MISSING"
        if token_env in os.environ:
            del os.environ[token_env]

        with self.assertRaises(RuntimeError):
            create_baseline_setup(
                runner_name="single",
                provider="hf",
                model_id="Qwen/Qwen2.5-7B-Instruct",
                hf_token_env=token_env,
            )

    def test_react_tool_config_matches_task_tools(self) -> None:
        _, task, config = create_baseline_setup(
            runner_name="react",
            provider="scripted",
            task_name="linear2",
        )
        expected_tools = sorted(task.available_tools().keys())
        self.assertEqual(config["tool_config"], expected_tools)
        self.assertTrue(config["react_enable_tools"])

    def test_react_tools_can_be_disabled_for_parity(self) -> None:
        _, _task, config = create_baseline_setup(
            runner_name="react",
            provider="scripted",
            task_name="digit-permutation",
            react_enable_tools=False,
        )
        self.assertEqual(config["tool_config"], [])
        self.assertFalse(config["react_enable_tools"])

    def test_cot_config_has_no_tools(self) -> None:
        _, _task, config = create_baseline_setup(
            runner_name="cot",
            provider="scripted",
            task_name="game24",
        )
        self.assertEqual(config["condition_id"], "baseline-cot")
        self.assertEqual(config["tool_config"], [])

    def test_cot_sc_config_carries_sample_count(self) -> None:
        _, _task, config = create_baseline_setup(
            runner_name="cot_sc",
            provider="scripted",
            task_name="game24",
            cot_sc_samples=7,
        )
        self.assertEqual(config["condition_id"], "baseline-cot-sc")
        self.assertEqual(config["tool_config"], [])
        self.assertEqual(config["cot_sc_samples"], 7)


if __name__ == "__main__":
    unittest.main()
