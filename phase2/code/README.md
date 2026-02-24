# Phase 2 Code Workspace

This directory will contain the executable implementation for baseline and ToT-integrated agent runners.

## Current Layout
- `src/phase2_baselines/runners/`: baseline runner implementations.
  - includes `CoTRunner`, `CoTSelfConsistencyRunner`, and `ToTRunner`.
- `src/phase2_baselines/catalog/`: atomic condition catalog (algorithm IDs + capability surfaces).
  - `catalog/condition_registry.py` composes canonical condition specs from one-file atomic modules.
  - each atomic element has its own file, e.g. `condition_baseline_*`, `algorithm_*`, `runner_adapter_*`, `execution_surface_*`, `tool_surface_*`, `memory_surface_*`.
- `src/phase2_baselines/adapters.py`: smolagents inference model adapter.
- `src/phase2_baselines/tasks/`: benchmark task adapters.
  - includes `subset-sum`, `linear2`, and `digit-permutation` tasks for protocol-v3.
- `src/phase2_baselines/metrics.py`: unified metric and cost estimation helpers.
- `src/phase2_baselines/manifest.py`: run manifest generation/validation/writing.
- `src/phase2_baselines/pipeline.py`: shared baseline execution/recording pipeline.
- `src/phase2_baselines/reporting.py`: condition-level variance summary utilities.
- `configs/hf-default.json`: pinned default generation profile shared by smolagents/HF inference.
- `scripts/run_baseline.py`: local baseline execution entry point.
- `scripts/run_baseline_sweep.py`: repeated baseline execution + variance report generation.
- `scripts/run_tot_demo.py`: ToT prototype demo run with manifest output.
- `scripts/run_tot_sweep.py`: repeated ToT execution + variance report generation.
- `scripts/run_game24_lockset.py`: paired Game24 panel runner across `single`, `react`, and `tot` conditions.
- `scripts/run_structured_lockset.py`: generic paired lockset runner for registered tasks.
- `scripts/build_protocol_v3_panels.py`: deterministic panel generator for protocol-v3 tasks.
- `scripts/build_protocol_v4_panels.py`: disjoint panel generator for protocol-v4 confirmatory track.
- `scripts/run_protocol_v3_matrix.py`: task x model matrix orchestrator for protocol-v3.
- `scripts/build_protocol_v3_matrix_summary.py`: consolidated summary across protocol-v3 reports.
- `scripts/run_protocol_v4_smoke.py`: protocol-v4 smoke execution across all tasks.
- `scripts/run_protocol_v4_gates.py`: protocol-v4 pre-launch gate runner (tests, smoke, parity audit, report-only parity).
- `scripts/run_protocol_v4_matrix.py`: frozen confirmatory matrix orchestrator for protocol-v4.
- `scripts/build_protocol_v4_matrix_summary.py`: consolidated summary across protocol-v4 confirmatory reports.
- `scripts/run_protocol_v5_smoke.py`: protocol-v5 smoke execution for `single,cot,cot_sc,react,tot`.
- `scripts/run_protocol_v5_matrix.py`: protocol-v5 base-pattern matrix orchestrator.
- `scripts/build_protocol_v5_matrix_summary.py`: consolidated summary across protocol-v5 base reports.
- `scripts/run_protocol_v51_hybrid_matrix.py`: protocol-v5.1 hybrid profile matrix orchestrator.
- `scripts/build_protocol_v51_hybrid_summary.py`: consolidated summary across protocol-v5.1 hybrid reports.
- `scripts/run_protocol_v7_smoke.py`: protocol-v7 Matrix A smoke launcher (`single,cot,cot_sc,react_text,tot`).
- `scripts/run_protocol_v7_matrix.py`: protocol-v7 Matrix A full launcher with hard parity profile gates.
- `scripts/build_metrics_table.py`: aggregate manifest-driven evaluation metrics tables.
- `scripts/build_failure_taxonomy.py`: heuristic failure taxonomy from run manifests.
- `scripts/build_search_ablation_summary.py`: consolidate primary + A1 + A2 lockset reports into one search-ablation summary.
- `tests/`: smoke tests for runner scaffolding.

## Interface Contract
Each runner should support:
- `prepare(task, config)`
- `run()`
- `result()` -> standardized manifest-compatible output

## Output Contract
Runner output must map directly to the manifest fields defined in:
- `/Users/quiznat/Desktop/Tree_of_Thought/phase2/reproducibility/run-manifest-schema.md`

## smolagents Runtime (Recommended)
`smolagents` requires Python >= 3.10. This repo includes a local 3.11 venv path:

```bash
cd /Users/quiznat/Desktop/Tree_of_Thought
uv python install 3.11
uv venv phase2/.venv311 --python 3.11
source phase2/.venv311/bin/activate
python -m ensurepip --upgrade
python -m pip install --upgrade pip
python -m pip install smolagents huggingface-hub
```

When `--provider smolagents` is selected:
- `baseline_react_code_agent_with_task_tools_v1` runs through `smolagents.CodeAgent`.
- `baseline_react_reasoning_text_loop_only_v1` runs through reasoning-only text-loop ReAct mode with no code execution surface.
- Atomic condition identity and capability surfaces are cataloged in `src/phase2_baselines/catalog/condition_registry.py`.

## Canonical Condition Keys
- `baseline_single_path_reasoning_only_v1`
- `baseline_chain_of_thought_reasoning_only_v1`
- `baseline_chain_of_thought_self_consistency_reasoning_only_v1`
- `baseline_react_code_agent_with_task_tools_v1`
- `baseline_react_reasoning_text_loop_only_v1`
- `baseline_tree_of_thoughts_search_reasoning_only_v1`
- `baseline_tree_of_thoughts_generalized_recursive_reasoning_only_v1`

Legacy aliases (`single`, `cot`, `cot_sc`, `react`, `react_text`, `tot`, `tot_gen`) are still accepted, but canonical keys are recommended.

## Local Smoke Run
```bash
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_baseline.py \
  --condition baseline_single_path_reasoning_only_v1
```

## Repeated-Run Sweep
```bash
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_baseline_sweep.py --runs-per-condition 5
```

## Repeated ToT Sweep
```bash
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_tot_sweep.py \
  --runs-per-condition 5 \
  --evaluator-mode rule_based
```

## smolagents Baseline Run
```bash
export HF_TOKEN=your_token_here
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_baseline.py \
  --condition baseline_single_path_reasoning_only_v1 \
  --provider smolagents \
  --model-id Qwen/Qwen2.5-7B-Instruct
```

## smolagents Sweep
```bash
export HF_TOKEN=your_token_here
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_baseline_sweep.py \
  --provider smolagents \
  --model-id Qwen/Qwen2.5-7B-Instruct \
  --runs-per-condition 3
```

## ToT Prototype Demo
```bash
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_tot_demo.py \
  --evaluator-mode rule_based
```

## ToT Prototype With smolagents
```bash
export HF_TOKEN=your_token_here
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_tot_demo.py \
  --provider smolagents \
  --model-id Qwen/Qwen3-Coder-Next:novita \
  --evaluator-mode model_self_eval
```

## Paired Game24 Lockset Pilot (3 Items)
```bash
export HF_TOKEN=your_token_here
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_game24_lockset.py \
  --provider smolagents \
  --model-id Qwen/Qwen3-Coder-Next:novita \
  --conditions baseline_single_path_reasoning_only_v1,baseline_react_code_agent_with_task_tools_v1,baseline_tree_of_thoughts_search_reasoning_only_v1 \
  --tot-evaluator-mode model_self_eval \
  --hf-temperature 0.0 \
  --seed-policy item_hash \
  --limit 3 \
  --report-md /Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/game24_lockset_report_pilot.md \
  --report-json /Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/game24_lockset_report_pilot.json
```

## Paired Game24 Lockset Full Run (50 Items)
```bash
export HF_TOKEN=your_token_here
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_game24_lockset.py \
  --provider smolagents \
  --model-id Qwen/Qwen3-Coder-Next:novita \
  --conditions baseline_single_path_reasoning_only_v1,baseline_react_code_agent_with_task_tools_v1,baseline_tree_of_thoughts_search_reasoning_only_v1 \
  --tot-evaluator-mode model_self_eval \
  --hf-temperature 0.0 \
  --seed-policy item_hash \
  --max-workers 4 \
  --limit 50 \
  --report-md /Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/game24_lockset_report.md \
  --report-json /Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/game24_lockset_report.json
```

`--max-workers` controls parallel item execution. Use `1` for strict sequential execution.

## Rebuild Lockset Report (No Reruns)
```bash
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_game24_lockset.py \
  --report-only \
  --provider smolagents \
  --model-id Qwen/Qwen3-Coder-Next:novita \
  --conditions baseline_single_path_reasoning_only_v1,baseline_react_code_agent_with_task_tools_v1,baseline_tree_of_thoughts_search_reasoning_only_v1 \
  --tot-evaluator-mode model_self_eval \
  --hf-temperature 0.0 \
  --seed-policy item_hash \
  --limit 50 \
  --confidence-level 0.95 \
  --bootstrap-samples 10000 \
  --report-md /Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/game24_lockset_report.md \
  --report-json /Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/game24_lockset_report.json
```

Active protocol reference:
- `/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/evaluation-protocol-v7.md`
- `/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/benchmark-matrix-v7.md`
- `/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/protocol-v7-execution.md`

## Local Tests
```bash
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 -m unittest discover /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/tests
```

## Build Evaluation Table
```bash
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/build_metrics_table.py \
  --task-id game24-demo \
  --provider smolagents-inference \
  --out-md /Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/evaluation_v1_metrics_hf.md \
  --out-json /Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/evaluation_v1_metrics_hf.json
```

## Build Failure Taxonomy
```bash
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/build_failure_taxonomy.py \
  --task-id game24-demo \
  --provider smolagents-inference \
  --out-md /Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/failure_taxonomy_hf.md \
  --out-json /Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/failure_taxonomy_hf.json
```

## Build Search Ablation Summary
```bash
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/build_search_ablation_summary.py \
  --primary-report-json /Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/game24_lockset_report_qwen3codernext.json \
  --a1-report-json /Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/game24_lockset_report_qwen3codernext_search_a1.json \
  --a2-report-json /Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/game24_lockset_report_qwen3codernext_search_a2.json \
  --out-md /Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/game24_lockset_search_ablation_summary.md \
  --out-json /Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/game24_lockset_search_ablation_summary.json
```

## Build Protocol-v3 Panels
```bash
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/build_protocol_v3_panels.py
```

## Run Generic Structured Lockset (Any Registered Task)
```bash
export HF_TOKEN=your_token_here
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_structured_lockset.py \
  --task-id subset-sum-demo \
  --panel-file /Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/panels/subset_sum_lockset_v1.json \
  --provider smolagents \
  --model-id Qwen/Qwen3-Coder-Next:novita \
  --conditions baseline_single_path_reasoning_only_v1,baseline_chain_of_thought_reasoning_only_v1,baseline_chain_of_thought_self_consistency_reasoning_only_v1,baseline_react_code_agent_with_task_tools_v1,baseline_tree_of_thoughts_search_reasoning_only_v1 \
  --limit 50 \
  --max-workers 8
```

## Run Protocol-v3 Matrix
```bash
export HF_TOKEN=your_token_here
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_protocol_v3_matrix.py
```

## Build Protocol-v3 Matrix Summary
```bash
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/build_protocol_v3_matrix_summary.py
```

## Build Protocol-v4 Panels
```bash
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/build_protocol_v4_panels.py
```

## Run Protocol-v4 Gates
```bash
export HF_TOKEN=your_token_here
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_protocol_v4_gates.py
```

## Run Protocol-v4 Confirmatory Matrix
```bash
export HF_TOKEN=your_token_here
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_protocol_v4_matrix.py
```

## Build Protocol-v4 Matrix Summary
```bash
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/build_protocol_v4_matrix_summary.py
```
