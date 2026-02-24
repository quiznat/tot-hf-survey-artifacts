"""Smoke tests for baseline runner scaffolding."""

from __future__ import annotations

import sys
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import patch

from phase2_baselines.adapters import ScriptedModel
from phase2_baselines.runners import CoTRunner, CoTSelfConsistencyRunner, ReactRunner, SinglePathRunner
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

    def test_react_rejects_non_smolagents_provider(self) -> None:
        model = ScriptedModel(responses=["FINAL: (10*10-4)/4"])
        runner = ReactRunner(model=model, model_name="test-react", provider="local-scripted")
        runner.prepare(
            self.task,
            {
                "condition_id": "baseline-react",
                "search_config": {"depth": 1, "breadth": 1, "pruning": "none", "stop_policy": "max_steps_or_final"},
                "tool_config": [],
                "budget": {"token_budget": 1, "time_budget_ms": 1, "cost_budget_usd": 0.0},
                "max_steps": 1,
            },
        )
        with self.assertRaises(RuntimeError):
            runner.run(self.numbers)

    def test_react_text_loop_allows_non_smolagents_provider(self) -> None:
        model = ScriptedModel(
            responses=[
                "THOUGHT: compute expression\nFINAL: (10*10-4)/4",
            ]
        )
        runner = ReactRunner(model=model, model_name="test-react-text", provider="local-scripted")
        runner.prepare(
            self.task,
            {
                "condition_id": "baseline-react-text",
                "search_config": {"depth": 1, "breadth": 1, "pruning": "none", "stop_policy": "max_steps_or_final"},
                "tool_config": [],
                "react_enable_tools": False,
                "react_execution_mode": "text_loop",
                "budget": {"token_budget": 1, "time_budget_ms": 1, "cost_budget_usd": 0.0},
                "max_steps": 2,
            },
        )
        manifest = runner.run(self.numbers)
        self.assertEqual(manifest["outcome"], "success")
        self.assertEqual(manifest["condition_id"], "baseline-react-text")

    def test_react_smolagents_provider_uses_codeagent_runtime(self) -> None:
        fake_module = ModuleType("smolagents")

        class FakeTool:
            def __init__(self, *args, **kwargs) -> None:
                del args, kwargs

        class FakeCodeAgent:
            last_instance: "FakeCodeAgent | None" = None

            def __init__(self, tools, model, **kwargs) -> None:
                self.tools = tools
                self.model = model
                self.kwargs = kwargs
                FakeCodeAgent.last_instance = self

            def run(self, task, **kwargs):
                self.task = task
                self.run_kwargs = kwargs
                return SimpleNamespace(
                    output="FINAL: (10*10-4)/4",
                    token_usage=SimpleNamespace(input_tokens=77, output_tokens=11),
                    steps=[
                        {
                            "step_type": "action",
                            "model_output": "call calc",
                            "tool_calls": [{"name": "calc", "arguments": {"tool_input": "(10*10-4)/4"}}],
                            "observations": "24",
                        }
                    ],
                    state="success",
                )

        setattr(fake_module, "Tool", FakeTool)
        setattr(fake_module, "CodeAgent", FakeCodeAgent)

        class FakeSmolagentsAdapter:
            def __init__(self) -> None:
                self._model = object()

            def generate(self, prompt: str) -> str:
                del prompt
                return ""

        with patch.dict(sys.modules, {"smolagents": fake_module}):
            runner = ReactRunner(
                model=FakeSmolagentsAdapter(),
                model_name="test-react-smolagents",
                provider="smolagents-inference",
            )
            runner.prepare(
                self.task,
                {
                    "condition_id": "baseline-react",
                    "search_config": {"depth": 1, "breadth": 1, "pruning": "none", "stop_policy": "max_steps_or_final"},
                    "tool_config": ["calc"],
                    "budget": {"token_budget": 1, "time_budget_ms": 1, "cost_budget_usd": 0.0},
                    "max_steps": 4,
                    "react_enable_tools": True,
                },
            )
            manifest = runner.run(self.numbers)

        self.assertEqual(manifest["outcome"], "success")
        self.assertEqual(manifest["metrics"]["success"], 1)
        self.assertGreater(manifest["metrics"]["tokens_in"], 0)
        self.assertGreater(manifest["metrics"]["tokens_out"], 0)
        self.assertEqual(manifest["extra"]["provider_token_usage"]["input_tokens"], 77)
        self.assertEqual(manifest["extra"]["provider_token_usage"]["output_tokens"], 11)
        self.assertIn("smolagents code-agent runtime", manifest["notes"])

        created = FakeCodeAgent.last_instance
        assert created is not None
        self.assertEqual(len(created.tools), 1)
        self.assertEqual(created.kwargs.get("max_steps"), 4)
        self.assertEqual(created.run_kwargs.get("max_steps"), 4)
        self.assertTrue(created.run_kwargs.get("return_full_result"))

    def test_react_smolagents_provider_honors_tool_disable_flag(self) -> None:
        fake_module = ModuleType("smolagents")

        class FakeTool:
            def __init__(self, *args, **kwargs) -> None:
                del args, kwargs

        class FakeCodeAgent:
            last_instance: "FakeCodeAgent | None" = None

            def __init__(self, tools, model, **kwargs) -> None:
                self.tools = tools
                self.model = model
                self.kwargs = kwargs
                FakeCodeAgent.last_instance = self

            def run(self, task, **kwargs):
                del task, kwargs
                return SimpleNamespace(
                    output="(10*10-4)/4",
                    token_usage=SimpleNamespace(input_tokens=0, output_tokens=0),
                    steps=[],
                    state="success",
                )

        setattr(fake_module, "Tool", FakeTool)
        setattr(fake_module, "CodeAgent", FakeCodeAgent)

        class FakeSmolagentsAdapter:
            def __init__(self) -> None:
                self._model = object()

            def generate(self, prompt: str) -> str:
                del prompt
                return ""

        with patch.dict(sys.modules, {"smolagents": fake_module}):
            runner = ReactRunner(
                model=FakeSmolagentsAdapter(),
                model_name="test-react-smolagents",
                provider="smolagents-inference",
            )
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

        self.assertEqual(manifest["outcome"], "success")
        created = FakeCodeAgent.last_instance
        assert created is not None
        self.assertEqual(len(created.tools), 0)

    def test_cot_success(self) -> None:
        model = ScriptedModel(
            responses=[
                "We can use the numbers once each.\nFINAL: (10*10-4)/4",
            ]
        )
        runner = CoTRunner(model=model, model_name="test-cot")
        runner.prepare(
            self.task,
            {
                "condition_id": "baseline-cot",
                "search_config": {"depth": 1, "breadth": 1, "pruning": "none", "stop_policy": "single-cot-pass"},
                "tool_config": [],
                "budget": {"token_budget": 1, "time_budget_ms": 1, "cost_budget_usd": 0.0},
            },
        )
        manifest = runner.run(self.numbers)
        self.assertEqual(manifest["outcome"], "success")
        self.assertEqual(manifest["condition_id"], "baseline-cot")

    def test_cot_self_consistency_majority_vote(self) -> None:
        model = ScriptedModel(
            responses=[
                "Path one.\nFINAL: (10*10-4)/4",
                "Path two.\nFINAL: 24",
                "Path three.\nFINAL: (10*10-4)/4",
            ]
        )
        runner = CoTSelfConsistencyRunner(model=model, model_name="test-cot-sc")
        runner.prepare(
            self.task,
            {
                "condition_id": "baseline-cot-sc",
                "search_config": {"depth": 1, "breadth": 3, "pruning": "majority_vote", "stop_policy": "sample_consensus"},
                "tool_config": [],
                "budget": {"token_budget": 1, "time_budget_ms": 1, "cost_budget_usd": 0.0},
                "cot_sc_samples": 3,
            },
        )
        manifest = runner.run(self.numbers)
        self.assertEqual(manifest["outcome"], "success")
        self.assertEqual(manifest["final_answer"], "(10*10-4)/4")
        self.assertEqual(manifest["cot_sc_samples"], 3)


if __name__ == "__main__":
    unittest.main()
