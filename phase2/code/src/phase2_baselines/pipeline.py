"""Reusable baseline execution pipeline utilities."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List, Tuple

from .adapters import SmolagentsInferenceModel
from .catalog.condition_key_baseline_chain_of_thought_reasoning_only_v1 import (
    CONDITION_KEY_BASELINE_CHAIN_OF_THOUGHT_REASONING_ONLY_V1,
)
from .catalog.condition_key_baseline_chain_of_thought_self_consistency_reasoning_only_v1 import (
    CONDITION_KEY_BASELINE_CHAIN_OF_THOUGHT_SELF_CONSISTENCY_REASONING_ONLY_V1,
)
from .catalog.condition_key_baseline_react_code_agent_with_task_tools_v1 import (
    CONDITION_KEY_BASELINE_REACT_CODE_AGENT_WITH_TASK_TOOLS_V1,
)
from .catalog.condition_key_baseline_react_reasoning_text_loop_only_v1 import (
    CONDITION_KEY_BASELINE_REACT_REASONING_TEXT_LOOP_ONLY_V1,
)
from .catalog.condition_key_baseline_single_path_reasoning_only_v1 import (
    CONDITION_KEY_BASELINE_SINGLE_PATH_REASONING_ONLY_V1,
)
from .catalog.condition_registry import get_condition_spec
from .catalog.react_execution_mode_normalize import normalize_react_execution_mode
from .catalog.react_execution_mode_reasoning_text_loop_no_tools_v1 import (
    REACT_EXECUTION_MODE_REASONING_TEXT_LOOP_NO_TOOLS_V1,
)
from .catalog.react_execution_mode_smolagents_code_agent_with_task_tools_v1 import (
    REACT_EXECUTION_MODE_SMOLAGENTS_CODE_AGENT_WITH_TASK_TOOLS_V1,
)
from .catalog.runner_adapter_chain_of_thought_reasoning_v1 import (
    RUNNER_ADAPTER_CHAIN_OF_THOUGHT_REASONING_V1,
)
from .catalog.runner_adapter_chain_of_thought_self_consistency_reasoning_v1 import (
    RUNNER_ADAPTER_CHAIN_OF_THOUGHT_SELF_CONSISTENCY_REASONING_V1,
)
from .catalog.runner_adapter_normalize import normalize_runner_adapter_id
from .catalog.runner_adapter_react_code_agent_with_task_tools_v1 import (
    RUNNER_ADAPTER_REACT_CODE_AGENT_WITH_TASK_TOOLS_V1,
)
from .catalog.runner_adapter_react_reasoning_text_loop_no_tools_v1 import (
    RUNNER_ADAPTER_REACT_REASONING_TEXT_LOOP_NO_TOOLS_V1,
)
from .catalog.runner_adapter_single_path_reasoning_v1 import (
    RUNNER_ADAPTER_SINGLE_PATH_REASONING_V1,
)
from .manifest import append_run_log, write_manifest
from .runners import CoTRunner, CoTSelfConsistencyRunner, ReactRunner, SinglePathRunner
from .tasks import create_task, resolve_task_id


def _build_baseline_config(
    runner_adapter_id: str,
    seed: int,
    task_tool_names: List[str],
    react_enable_tools: bool,
    react_execution_mode: str | None,
    cot_sc_samples: int,
    cot_sc_parallel_workers: int,
    cot_answer_recovery: bool,
    react_strict_mode: bool,
) -> Dict[str, Any]:
    if runner_adapter_id == RUNNER_ADAPTER_SINGLE_PATH_REASONING_V1:
        return {
            "condition_id": get_condition_spec(CONDITION_KEY_BASELINE_SINGLE_PATH_REASONING_ONLY_V1).condition_id,
            "prompt_template_version": "v1",
            "search_config": {"depth": 0, "breadth": 0, "pruning": "none", "stop_policy": "single-pass"},
            "tool_config": [],
            "budget": {"token_budget": 2000, "time_budget_ms": 10000, "cost_budget_usd": 0.0},
            "seed": seed,
        }

    if runner_adapter_id == RUNNER_ADAPTER_CHAIN_OF_THOUGHT_REASONING_V1:
        return {
            "condition_id": get_condition_spec(
                CONDITION_KEY_BASELINE_CHAIN_OF_THOUGHT_REASONING_ONLY_V1
            ).condition_id,
            "prompt_template_version": "v1",
            "search_config": {"depth": 1, "breadth": 1, "pruning": "none", "stop_policy": "single-cot-pass"},
            "tool_config": [],
            "budget": {"token_budget": 3000, "time_budget_ms": 12000, "cost_budget_usd": 0.0},
            "seed": seed,
            "cot_answer_recovery": cot_answer_recovery,
        }

    if runner_adapter_id == RUNNER_ADAPTER_CHAIN_OF_THOUGHT_SELF_CONSISTENCY_REASONING_V1:
        samples = max(1, int(cot_sc_samples))
        parallel_workers = max(1, int(cot_sc_parallel_workers))
        return {
            "condition_id": get_condition_spec(
                CONDITION_KEY_BASELINE_CHAIN_OF_THOUGHT_SELF_CONSISTENCY_REASONING_ONLY_V1
            ).condition_id,
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
            "cot_sc_parallel_workers": parallel_workers,
            "cot_answer_recovery": cot_answer_recovery,
        }

    if runner_adapter_id in {
        RUNNER_ADAPTER_REACT_CODE_AGENT_WITH_TASK_TOOLS_V1,
        RUNNER_ADAPTER_REACT_REASONING_TEXT_LOOP_NO_TOOLS_V1,
    }:
        mode = react_execution_mode
        if not str(mode or "").strip():
            if runner_adapter_id == RUNNER_ADAPTER_REACT_REASONING_TEXT_LOOP_NO_TOOLS_V1:
                mode = REACT_EXECUTION_MODE_REASONING_TEXT_LOOP_NO_TOOLS_V1
            else:
                mode = REACT_EXECUTION_MODE_SMOLAGENTS_CODE_AGENT_WITH_TASK_TOOLS_V1
        mode = normalize_react_execution_mode(mode)

        if (
            runner_adapter_id == RUNNER_ADAPTER_REACT_REASONING_TEXT_LOOP_NO_TOOLS_V1
            and mode != REACT_EXECUTION_MODE_REASONING_TEXT_LOOP_NO_TOOLS_V1
        ):
            raise ValueError(
                "runner_adapter.react_reasoning_text_loop_no_tools.v1 requires "
                "react_execution_mode.reasoning_text_loop_no_tools.v1"
            )
        if (
            runner_adapter_id == RUNNER_ADAPTER_REACT_CODE_AGENT_WITH_TASK_TOOLS_V1
            and mode != REACT_EXECUTION_MODE_SMOLAGENTS_CODE_AGENT_WITH_TASK_TOOLS_V1
        ):
            raise ValueError(
                "runner_adapter.react_code_agent_with_task_tools.v1 requires "
                "react_execution_mode.smolagents_code_agent_with_task_tools.v1"
            )

        condition_key = (
            CONDITION_KEY_BASELINE_REACT_REASONING_TEXT_LOOP_ONLY_V1
            if mode == REACT_EXECUTION_MODE_REASONING_TEXT_LOOP_NO_TOOLS_V1
            else CONDITION_KEY_BASELINE_REACT_CODE_AGENT_WITH_TASK_TOOLS_V1
        )
        condition_id = get_condition_spec(condition_key).condition_id
        effective_react_enable_tools = bool(react_enable_tools) and (
            mode == REACT_EXECUTION_MODE_SMOLAGENTS_CODE_AGENT_WITH_TASK_TOOLS_V1
        )
        tool_config = list(task_tool_names) if effective_react_enable_tools else []
        return {
            "condition_id": condition_id,
            "prompt_template_version": "v1",
            "search_config": {"depth": 1, "breadth": 1, "pruning": "none", "stop_policy": "max_steps_or_final"},
            "tool_config": tool_config,
            "budget": {"token_budget": 3000, "time_budget_ms": 12000, "cost_budget_usd": 0.0},
            "seed": seed,
            "max_steps": 5,
            "react_enable_tools": effective_react_enable_tools,
            "react_strict_mode": react_strict_mode,
            "react_execution_mode": mode,
        }

    raise ValueError(f"Unsupported runner_adapter_id: {runner_adapter_id}")


def _resolve_model(
    provider: str,
    runner_adapter_id: str,
    model_id: str | None,
    hf_token_env: str,
    hf_timeout_seconds: int,
    hf_max_new_tokens: int,
    hf_temperature: float,
    hf_top_p: float,
) -> Tuple[Any, str, str]:
    del runner_adapter_id
    if provider != "smolagents":
        raise ValueError(
            f"Unsupported provider: {provider}. This repo is locked to --provider smolagents."
        )
    resolved_model_id = model_id or "Qwen/Qwen3-Coder-Next:novita"
    token = os.getenv(hf_token_env, "").strip()
    if not token:
        raise RuntimeError(
            f"smolagents provider requires ${hf_token_env} with a valid API token."
        )
    model = SmolagentsInferenceModel(
        model_id=resolved_model_id,
        api_token=token,
        timeout_seconds=hf_timeout_seconds,
        max_new_tokens=hf_max_new_tokens,
        temperature=hf_temperature,
        top_p=hf_top_p,
    )
    return model, resolved_model_id, "smolagents-inference"


def create_baseline_setup(
    runner_name: str,
    seed: int = 0,
    provider: str = "smolagents",
    task_name: str = "game24",
    model_id: str | None = None,
    hf_token_env: str = "HF_TOKEN",
    hf_timeout_seconds: int = 120,
    hf_max_new_tokens: int = 192,
    hf_temperature: float = 0.0,
    hf_top_p: float = 1.0,
    react_enable_tools: bool = True,
    react_execution_mode: str | None = None,
    cot_sc_samples: int = 10,
    cot_sc_parallel_workers: int = 0,
    cot_answer_recovery: bool = False,
    react_strict_mode: bool = True,
) -> Tuple[Any, Any, Dict[str, Any]]:
    """Create runner, task, and config for a named baseline condition."""
    normalized_runner_adapter_id = normalize_runner_adapter_id(runner_name)
    task = create_task(task_name)
    task_id = resolve_task_id(task_name)
    model, resolved_model_id, resolved_provider = _resolve_model(
        provider=provider,
        runner_adapter_id=normalized_runner_adapter_id,
        model_id=model_id,
        hf_token_env=hf_token_env,
        hf_timeout_seconds=hf_timeout_seconds,
        hf_max_new_tokens=hf_max_new_tokens,
        hf_temperature=hf_temperature,
        hf_top_p=hf_top_p,
    )
    task_tool_names = sorted(task.available_tools().keys())
    effective_cot_sc_parallel_workers = int(cot_sc_parallel_workers)
    if (
        normalized_runner_adapter_id == RUNNER_ADAPTER_CHAIN_OF_THOUGHT_SELF_CONSISTENCY_REASONING_V1
        and effective_cot_sc_parallel_workers <= 0
    ):
        # Self-consistency should sample in parallel for fair latency accounting.
        effective_cot_sc_parallel_workers = max(1, int(cot_sc_samples))

    config = _build_baseline_config(
        runner_adapter_id=normalized_runner_adapter_id,
        seed=seed,
        task_tool_names=task_tool_names,
        react_enable_tools=react_enable_tools,
        react_execution_mode=react_execution_mode,
        cot_sc_samples=cot_sc_samples,
        cot_sc_parallel_workers=effective_cot_sc_parallel_workers,
        cot_answer_recovery=cot_answer_recovery,
        react_strict_mode=react_strict_mode,
    )
    config["task_id"] = task_id

    if normalized_runner_adapter_id == RUNNER_ADAPTER_SINGLE_PATH_REASONING_V1:
        runner = SinglePathRunner(model=model, model_name=resolved_model_id, provider=resolved_provider)
        return runner, task, config

    if normalized_runner_adapter_id == RUNNER_ADAPTER_CHAIN_OF_THOUGHT_REASONING_V1:
        runner = CoTRunner(model=model, model_name=resolved_model_id, provider=resolved_provider)
        return runner, task, config

    if normalized_runner_adapter_id == RUNNER_ADAPTER_CHAIN_OF_THOUGHT_SELF_CONSISTENCY_REASONING_V1:
        runner = CoTSelfConsistencyRunner(model=model, model_name=resolved_model_id, provider=resolved_provider)
        return runner, task, config

    if normalized_runner_adapter_id in {
        RUNNER_ADAPTER_REACT_CODE_AGENT_WITH_TASK_TOOLS_V1,
        RUNNER_ADAPTER_REACT_REASONING_TEXT_LOOP_NO_TOOLS_V1,
    }:
        react_mode = normalize_react_execution_mode(
            str(
                config.get(
                    "react_execution_mode",
                    REACT_EXECUTION_MODE_SMOLAGENTS_CODE_AGENT_WITH_TASK_TOOLS_V1,
                )
            )
        )
        if react_mode == REACT_EXECUTION_MODE_REASONING_TEXT_LOOP_NO_TOOLS_V1:
            framework = "phase2-react-reasoning-text-loop-no-tools@0.1"
        else:
            framework = (
                "smolagents-code-agent-with-task-tools@hf"
                if resolved_provider == "smolagents-inference"
                else "phase2-baselines@0.1"
            )
        runner = ReactRunner(
            model=model,
            model_name=resolved_model_id,
            provider=resolved_provider,
            framework=framework,
        )
        return runner, task, config

    raise ValueError(
        "create_baseline_setup supports baseline runners only "
        f"(got runner_adapter_id={normalized_runner_adapter_id})"
    )


def execute_and_record(
    runner_name: str,
    runs_dir: Path,
    run_log: Path,
    input_data: Any | None = None,
    input_numbers: Any | None = None,
    seed: int = 0,
    provider: str = "smolagents",
    task_name: str = "game24",
    model_id: str | None = None,
    hf_token_env: str = "HF_TOKEN",
    hf_timeout_seconds: int = 120,
    hf_max_new_tokens: int = 192,
    hf_temperature: float = 0.0,
    hf_top_p: float = 1.0,
    cot_sc_samples: int = 10,
    cot_sc_parallel_workers: int = 0,
    cot_answer_recovery: bool = False,
    react_strict_mode: bool = True,
    react_execution_mode: str | None = None,
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
        cot_sc_parallel_workers=cot_sc_parallel_workers,
        cot_answer_recovery=cot_answer_recovery,
        react_strict_mode=react_strict_mode,
        react_execution_mode=react_execution_mode,
    )
    runner.prepare(task=task, config=config)
    manifest = runner.run(payload)

    out_path = runs_dir / f"{manifest['run_id']}.json"
    manifest["artifact_paths"].append(str(out_path))
    write_manifest(manifest, out_path)
    append_run_log(run_log, manifest)

    return manifest
