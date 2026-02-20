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


if __name__ == "__main__":
    unittest.main()
