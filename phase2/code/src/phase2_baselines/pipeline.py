"""Reusable baseline execution pipeline utilities."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List, Tuple

from .adapters import HuggingFaceInferenceModel, ScriptedModel
from .manifest import append_run_log, write_manifest
from .runners import ReactRunner, SinglePathRunner
from .tasks import Arithmetic24Task


def _build_baseline_config(runner_name: str, seed: int) -> Dict[str, Any]:
    if runner_name == "single":
        return {
            "condition_id": "baseline-single-path",
            "prompt_template_version": "v1",
            "search_config": {"depth": 0, "breadth": 0, "pruning": "none", "stop_policy": "single-pass"},
            "tool_config": [],
            "budget": {"token_budget": 2000, "time_budget_ms": 10000, "cost_budget_usd": 0.0},
            "seed": seed,
        }

    if runner_name == "react":
        return {
            "condition_id": "baseline-react",
            "prompt_template_version": "v1",
            "search_config": {"depth": 1, "breadth": 1, "pruning": "none", "stop_policy": "max_steps_or_final"},
            "tool_config": ["calc"],
            "budget": {"token_budget": 3000, "time_budget_ms": 12000, "cost_budget_usd": 0.0},
            "seed": seed,
            "max_steps": 5,
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
        resolved_model_id = model_id or "Qwen/Qwen2.5-7B-Instruct"
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
    model_id: str | None = None,
    hf_token_env: str = "HF_TOKEN",
    hf_timeout_seconds: int = 120,
    hf_max_new_tokens: int = 192,
    hf_temperature: float = 0.0,
    hf_top_p: float = 1.0,
) -> Tuple[Any, Arithmetic24Task, Dict[str, Any]]:
    """Create runner, task, and config for a named baseline condition."""
    task = Arithmetic24Task()
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
    config = _build_baseline_config(runner_name=runner_name, seed=seed)

    if runner_name == "single":
        runner = SinglePathRunner(model=model, model_name=resolved_model_id, provider=resolved_provider)
        return runner, task, config

    if runner_name == "react":
        runner = ReactRunner(model=model, model_name=resolved_model_id, provider=resolved_provider)
        return runner, task, config

    raise ValueError(f"Unsupported runner_name: {runner_name}")


def execute_and_record(
    runner_name: str,
    input_numbers: List[int],
    runs_dir: Path,
    run_log: Path,
    seed: int = 0,
    provider: str = "scripted",
    model_id: str | None = None,
    hf_token_env: str = "HF_TOKEN",
    hf_timeout_seconds: int = 120,
    hf_max_new_tokens: int = 192,
    hf_temperature: float = 0.0,
    hf_top_p: float = 1.0,
) -> Dict[str, Any]:
    """Run one baseline condition and persist its manifest artifacts."""
    runner, task, config = create_baseline_setup(
        runner_name=runner_name,
        seed=seed,
        provider=provider,
        model_id=model_id,
        hf_token_env=hf_token_env,
        hf_timeout_seconds=hf_timeout_seconds,
        hf_max_new_tokens=hf_max_new_tokens,
        hf_temperature=hf_temperature,
        hf_top_p=hf_top_p,
    )
    runner.prepare(task=task, config=config)
    manifest = runner.run(input_numbers)

    out_path = runs_dir / f"{manifest['run_id']}.json"
    manifest["artifact_paths"].append(str(out_path))
    write_manifest(manifest, out_path)
    append_run_log(run_log, manifest)

    return manifest
