"""Tests for smolagents-only provider wiring in baseline pipeline."""

from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from phase2_baselines.catalog import get_condition_spec
from phase2_baselines.pipeline import create_baseline_setup


class PipelineHFTests(unittest.TestCase):
    def test_pipeline_rejects_non_smolagents_provider(self) -> None:
        with self.assertRaises(ValueError):
            create_baseline_setup(
                runner_name="single",
                provider="hf",
                model_id="Qwen/Qwen2.5-7B-Instruct",
                hf_token_env="HF_TOKEN",
            )

        with self.assertRaises(ValueError):
            create_baseline_setup(
                runner_name="single",
                provider="scripted",
                model_id="Qwen/Qwen2.5-7B-Instruct",
                hf_token_env="HF_TOKEN",
            )

    def test_smolagents_provider_requires_token(self) -> None:
        token_env = "HF_TOKEN_TEST_MISSING"
        if token_env in os.environ:
            del os.environ[token_env]

        with self.assertRaises(RuntimeError):
            create_baseline_setup(
                runner_name="single",
                provider="smolagents",
                model_id="Qwen/Qwen3-Coder-Next:novita",
                hf_token_env=token_env,
            )

    def test_react_tool_config_matches_task_tools(self) -> None:
        with patch(
            "phase2_baselines.pipeline._resolve_model",
            return_value=(object(), "Qwen/Qwen3-Coder-Next:novita", "smolagents-inference"),
        ):
            _, task, config = create_baseline_setup(
                runner_name="react",
                provider="smolagents",
                task_name="linear2",
            )
        expected_tools = sorted(task.available_tools().keys())
        self.assertEqual(config["tool_config"], expected_tools)
        self.assertTrue(config["react_enable_tools"])

    def test_react_tools_can_be_disabled_for_parity(self) -> None:
        with patch(
            "phase2_baselines.pipeline._resolve_model",
            return_value=(object(), "Qwen/Qwen3-Coder-Next:novita", "smolagents-inference"),
        ):
            _, _task, config = create_baseline_setup(
                runner_name="react",
                provider="smolagents",
                task_name="digit-permutation",
                react_enable_tools=False,
            )
        self.assertEqual(config["tool_config"], [])
        self.assertFalse(config["react_enable_tools"])

    def test_react_text_mode_has_atomic_condition_id_and_no_tools(self) -> None:
        with patch(
            "phase2_baselines.pipeline._resolve_model",
            return_value=(object(), "Qwen/Qwen3-Coder-Next:novita", "smolagents-inference"),
        ):
            _, _task, config = create_baseline_setup(
                runner_name="react_text",
                provider="smolagents",
                task_name="game24",
            )
        self.assertEqual(
            config["condition_id"],
            get_condition_spec("baseline_react_reasoning_text_loop_only_v1").condition_id,
        )
        self.assertEqual(config["tool_config"], [])
        self.assertEqual(
            config["react_execution_mode"],
            "react_execution_mode.reasoning_text_loop_no_tools.v1",
        )

    def test_cot_config_has_no_tools(self) -> None:
        with patch(
            "phase2_baselines.pipeline._resolve_model",
            return_value=(object(), "Qwen/Qwen3-Coder-Next:novita", "smolagents-inference"),
        ):
            _, _task, config = create_baseline_setup(
                runner_name="cot",
                provider="smolagents",
                task_name="game24",
            )
        self.assertEqual(
            config["condition_id"],
            get_condition_spec("baseline_chain_of_thought_reasoning_only_v1").condition_id,
        )
        self.assertEqual(config["tool_config"], [])

    def test_cot_sc_config_carries_sample_count(self) -> None:
        with patch(
            "phase2_baselines.pipeline._resolve_model",
            return_value=(object(), "Qwen/Qwen3-Coder-Next:novita", "smolagents-inference"),
        ):
            _, _task, config = create_baseline_setup(
                runner_name="cot_sc",
                provider="smolagents",
                task_name="game24",
                cot_sc_samples=7,
            )
        self.assertEqual(
            config["condition_id"],
            get_condition_spec(
                "baseline_chain_of_thought_self_consistency_reasoning_only_v1"
            ).condition_id,
        )
        self.assertEqual(config["tool_config"], [])
        self.assertEqual(config["cot_sc_samples"], 7)
        self.assertEqual(config["cot_sc_parallel_workers"], 7)

    def test_cot_sc_config_allows_parallel_worker_override(self) -> None:
        with patch(
            "phase2_baselines.pipeline._resolve_model",
            return_value=(object(), "Qwen/Qwen3-Coder-Next:novita", "smolagents-inference"),
        ):
            _, _task, config = create_baseline_setup(
                runner_name="cot_sc",
                provider="smolagents",
                task_name="game24",
                cot_sc_samples=7,
                cot_sc_parallel_workers=3,
            )
        self.assertEqual(config["cot_sc_parallel_workers"], 3)


if __name__ == "__main__":
    unittest.main()
