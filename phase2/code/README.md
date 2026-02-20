# Phase 2 Code Workspace

This directory will contain the executable implementation for baseline and ToT-integrated agent runners.

## Current Layout
- `src/phase2_baselines/runners/`: baseline runner implementations.
- `src/phase2_baselines/tasks/`: benchmark task adapters.
- `src/phase2_baselines/metrics.py`: unified metric and cost estimation helpers.
- `src/phase2_baselines/manifest.py`: run manifest generation/validation/writing.
- `src/phase2_baselines/pipeline.py`: shared baseline execution/recording pipeline.
- `src/phase2_baselines/reporting.py`: condition-level variance summary utilities.
- `scripts/run_baseline.py`: local baseline execution entry point.
- `scripts/run_baseline_sweep.py`: repeated baseline execution + variance report generation.
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

## Local Tests
```bash
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 -m unittest discover /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/tests
```
