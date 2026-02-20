# Phase 2 Code Workspace

This directory will contain the executable implementation for baseline and ToT-integrated agent runners.

## Current Layout
- `src/phase2_baselines/runners/`: baseline runner implementations.
  - includes `ToTRunner` prototype with search-state tracing.
- `src/phase2_baselines/adapters.py`: scripted and Hugging Face inference model adapters.
- `src/phase2_baselines/tasks/`: benchmark task adapters.
- `src/phase2_baselines/metrics.py`: unified metric and cost estimation helpers.
- `src/phase2_baselines/manifest.py`: run manifest generation/validation/writing.
- `src/phase2_baselines/pipeline.py`: shared baseline execution/recording pipeline.
- `src/phase2_baselines/reporting.py`: condition-level variance summary utilities.
- `configs/hf-default.json`: pinned default Hugging Face provider profile.
- `scripts/run_baseline.py`: local baseline execution entry point.
- `scripts/run_baseline_sweep.py`: repeated baseline execution + variance report generation.
- `scripts/run_tot_demo.py`: ToT prototype demo run with manifest output.
- `scripts/run_tot_sweep.py`: repeated ToT execution + variance report generation.
- `scripts/build_metrics_table.py`: aggregate manifest-driven evaluation metrics tables.
- `scripts/build_failure_taxonomy.py`: heuristic failure taxonomy from run manifests.
- `tests/`: smoke tests for runner scaffolding.

## Interface Contract
Each runner should support:
- `prepare(task, config)`
- `run()`
- `result()` -> standardized manifest-compatible output

## Output Contract
Runner output must map directly to the manifest fields defined in:
- `/Users/quiznat/Desktop/Tree_of_Thought/phase2/reproducibility/run-manifest-schema.md`

## Local Smoke Run
```bash
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_baseline.py --runner single
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

## Hugging Face Baseline Run
```bash
export HF_TOKEN=your_token_here
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_baseline.py \
  --runner single \
  --provider hf \
  --model-id Qwen/Qwen2.5-7B-Instruct
```

## Hugging Face Sweep
```bash
export HF_TOKEN=your_token_here
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_baseline_sweep.py \
  --provider hf \
  --model-id Qwen/Qwen2.5-7B-Instruct \
  --runs-per-condition 3
```

## ToT Prototype Demo
```bash
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_tot_demo.py \
  --evaluator-mode rule_based
```

## ToT Prototype With Hugging Face
```bash
export HF_TOKEN=your_token_here
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_tot_demo.py \
  --provider hf \
  --model-id Qwen/Qwen3-Coder-Next:novita \
  --evaluator-mode hybrid
```

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
  --provider huggingface-inference \
  --out-md /Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/evaluation_v1_metrics_hf.md \
  --out-json /Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/evaluation_v1_metrics_hf.json
```

## Build Failure Taxonomy
```bash
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/build_failure_taxonomy.py \
  --task-id game24-demo \
  --provider huggingface-inference \
  --out-md /Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/failure_taxonomy_hf.md \
  --out-json /Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/failure_taxonomy_hf.json
```
