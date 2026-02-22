"""Reusable baseline execution pipeline utilities."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List, Tuple

from .adapters import HuggingFaceInferenceModel, ScriptedModel
from .manifest import append_run_log, write_manifest
from .runners import CoTRunner, CoTSelfConsistencyRunner, ReactRunner, SinglePathRunner
from .tasks import create_task, resolve_task_id


def _build_baseline_config(
    runner_name: str,
    seed: int,
    task_tool_names: List[str],
    react_enable_tools: bool,
    cot_sc_samples: int,
) -> Dict[str, Any]:
    if runner_name == "single":
        return {
            "condition_id": "baseline-single-path",
            "prompt_template_version": "v1",
            "search_config": {"depth": 0, "breadth": 0, "pruning": "none", "stop_policy": "single-pass"},
            "tool_config": [],
            "budget": {"token_budget": 2000, "time_budget_ms": 10000, "cost_budget_usd": 0.0},
            "seed": seed,
        }

    if runner_name == "cot":
        return {
            "condition_id": "baseline-cot",
            "prompt_template_version": "v1",
            "search_config": {"depth": 1, "breadth": 1, "pruning": "none", "stop_policy": "single-cot-pass"},
            "tool_config": [],
            "budget": {"token_budget": 3000, "time_budget_ms": 12000, "cost_budget_usd": 0.0},
            "seed": seed,
        }

    if runner_name == "cot_sc":
        samples = max(1, int(cot_sc_samples))
        return {
            "condition_id": "baseline-cot-sc",
            "prompt_template_version": "v1",
            "search_config": {
                "depth": 1,
                "breadth": samples,
                "pruning": "majority_vote",
                "stop_policy": "sample_consensus",
            },
            "tool_config": [],
            "budget": {"token_budget": 6000, "time_budget_ms": 16000, "cost_budget_usd": 0.0},
            "seed": seed,
            "cot_sc_samples": samples,
        }

    if runner_name == "react":
        tool_config = list(task_tool_names) if react_enable_tools else []
        return {
            "condition_id": "baseline-react",
            "prompt_template_version": "v1",
            "search_config": {"depth": 1, "breadth": 1, "pruning": "none", "stop_policy": "max_steps_or_final"},
            "tool_config": tool_config,
            "budget": {"token_budget": 3000, "time_budget_ms": 12000, "cost_budget_usd": 0.0},
            "seed": seed,
            "max_steps": 5,
            "react_enable_tools": react_enable_tools,
        }

    raise ValueError(f"Unsupported runner_name: {runner_name}")


def _resolve_model(
    provider: str,
    runner_name: str,
    model_id: str | None,
    hf_token_env: str,
    hf_timeout_seconds: int,
    hf_max_new_tokens: int,
    hf_temperature: float,
    hf_top_p: float,
) -> Tuple[Any, str, str]:
    if provider == "scripted":
        if runner_name == "single":
            model = ScriptedModel(responses=["(10*10-4)/4"])
            return model, "scripted-single-v1", "local-scripted"
        if runner_name == "cot":
            model = ScriptedModel(
                responses=["Reasoning: use 10*10 then subtract 4 and divide by 4.\nFINAL: (10*10-4)/4"]
            )
            return model, "scripted-cot-v1", "local-scripted"
        if runner_name == "cot_sc":
            model = ScriptedModel(
                responses=[
                    "Reasoning path A.\nFINAL: (10*10-4)/4",
                    "Reasoning path B.\nFINAL: (10*10-4)/4",
                    "Reasoning path C.\nFINAL: (10*10-4)/4",
                ],
                fallback="Reasoning fallback.\nFINAL: (10*10-4)/4",
            )
            return model, "scripted-cot-sc-v1", "local-scripted"
        if runner_name == "react":
            model = ScriptedModel(
                responses=[
                    "THINK: I should test a candidate expression with calc.",
                    "ACTION: calc (10*10-4)/4",
                    "FINAL: (10*10-4)/4",
                ]
            )
            return model, "scripted-react-v1", "local-scripted"
        raise ValueError(f"Unsupported runner_name: {runner_name}")

    if provider == "hf":
        resolved_model_id = model_id or "Qwen/Qwen3-Coder-Next:novita"
        token = os.getenv(hf_token_env, "").strip()
        if not token:
            raise RuntimeError(
                f"Hugging Face provider requires ${hf_token_env} with a valid API token."
            )
        model = HuggingFaceInferenceModel(
            model_id=resolved_model_id,
            api_token=token,
            timeout_seconds=hf_timeout_seconds,
            max_new_tokens=hf_max_new_tokens,
            temperature=hf_temperature,
            top_p=hf_top_p,
        )
        return model, resolved_model_id, "huggingface-inference"

    raise ValueError(f"Unsupported provider: {provider}")


def create_baseline_setup(
    runner_name: str,
    seed: int = 0,
    provider: str = "scripted",
    task_name: str = "game24",
    model_id: str | None = None,
    hf_token_env: str = "HF_TOKEN",
    hf_timeout_seconds: int = 120,
    hf_max_new_tokens: int = 192,
    hf_temperature: float = 0.0,
    hf_top_p: float = 1.0,
    react_enable_tools: bool = True,
    cot_sc_samples: int = 5,
) -> Tuple[Any, Any, Dict[str, Any]]:
    """Create runner, task, and config for a named baseline condition."""
    task = create_task(task_name)
    task_id = resolve_task_id(task_name)
    model, resolved_model_id, resolved_provider = _resolve_model(
        provider=provider,
        runner_name=runner_name,
        model_id=model_id,
        hf_token_env=hf_token_env,
        hf_timeout_seconds=hf_timeout_seconds,
        hf_max_new_tokens=hf_max_new_tokens,
        hf_temperature=hf_temperature,
        hf_top_p=hf_top_p,
    )
    task_tool_names = sorted(task.available_tools().keys())
    config = _build_baseline_config(
        runner_name=runner_name,
        seed=seed,
        task_tool_names=task_tool_names,
        react_enable_tools=react_enable_tools,
        cot_sc_samples=cot_sc_samples,
    )
    config["task_id"] = task_id

    if runner_name == "single":
        runner = SinglePathRunner(model=model, model_name=resolved_model_id, provider=resolved_provider)
        return runner, task, config

    if runner_name == "cot":
        runner = CoTRunner(model=model, model_name=resolved_model_id, provider=resolved_provider)
        return runner, task, config

    if runner_name == "cot_sc":
        runner = CoTSelfConsistencyRunner(model=model, model_name=resolved_model_id, provider=resolved_provider)
        return runner, task, config

    if runner_name == "react":
        runner = ReactRunner(model=model, model_name=resolved_model_id, provider=resolved_provider)
        return runner, task, config

    raise ValueError(f"Unsupported runner_name: {runner_name}")


def execute_and_record(
    runner_name: str,
    runs_dir: Path,
    run_log: Path,
    input_data: Any | None = None,
    input_numbers: Any | None = None,
    seed: int = 0,
    provider: str = "scripted",
    task_name: str = "game24",
    model_id: str | None = None,
    hf_token_env: str = "HF_TOKEN",
    hf_timeout_seconds: int = 120,
    hf_max_new_tokens: int = 192,
    hf_temperature: float = 0.0,
    hf_top_p: float = 1.0,
    cot_sc_samples: int = 5,
) -> Dict[str, Any]:
    """Run one baseline condition and persist its manifest artifacts."""
    payload = input_data if input_data is not None else input_numbers
    if payload is None:
        raise RuntimeError("execute_and_record requires input_data or input_numbers")

    runner, task, config = create_baseline_setup(
        runner_name=runner_name,
        seed=seed,
        provider=provider,
        task_name=task_name,
        model_id=model_id,
        hf_token_env=hf_token_env,
        hf_timeout_seconds=hf_timeout_seconds,
        hf_max_new_tokens=hf_max_new_tokens,
        hf_temperature=hf_temperature,
        hf_top_p=hf_top_p,
        cot_sc_samples=cot_sc_samples,
    )
    runner.prepare(task=task, config=config)
    manifest = runner.run(payload)

    out_path = runs_dir / f"{manifest['run_id']}.json"
    manifest["artifact_paths"].append(str(out_path))
    write_manifest(manifest, out_path)
    append_run_log(run_log, manifest)

    return manifest
