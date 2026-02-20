# Phase 2 Code Workspace

This directory will contain the executable implementation for baseline and ToT-integrated agent runners.

## Planned Layout
- `runners/`: baseline and ToT runner implementations.
- `tasks/`: benchmark task adapters.
- `metrics/`: result collection and aggregation.
- `configs/`: experiment configs.
- `scripts/`: run orchestration entry points.

## Interface Contract (Initial)
Each runner should support:
- `prepare(task, config)`
- `run()`
- `result()` -> standardized manifest-compatible output

## Output Contract
Runner output must map directly to the manifest fields defined in:
- `/Users/quiznat/Desktop/Tree_of_Thought/phase2/reproducibility/run-manifest-schema.md`
