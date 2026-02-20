# Evaluation Protocol v1 (Draft)

Last updated: 2026-02-20

Status: superseded by `phase2/benchmarks/evaluation-protocol-v2.md` (approved freeze on 2026-02-20).

## Goal
Establish a fixed, reproducible protocol for comparing baseline and ToT conditions in Phase 2.

## Conditions
- `baseline-single-path`
- `baseline-react`
- `tot-prototype`

## Default Model Route
- Provider: Hugging Face Router
- Default model ID: `Qwen/Qwen3-Coder-Next:novita`
- Credential: `HF_TOKEN`

## Task Panel (Current)
- `game24-demo` (Arithmetic24Task)

## Fixed Settings
- Repetitions per condition: 5 (minimum)
- Prompt template version: `v1`
- Token budget: condition-specific (as defined in runner configs)
- Time budget: condition-specific (as defined in runner configs)
- Seed policy: deterministic seed sweep from `0..N-1`

## ToT Settings (Current v1)
- `max_depth=3`
- `branch_factor=3`
- `frontier_width=3`
- Pruning: `topk_cumulative_score`
- Stop policy: `first_terminal_or_depth_limit`
- Evaluator mode: `rule_based` (default), optional: `hybrid`, `model_self_eval`

## Metrics
- `success` (binary)
- `latency_ms`
- `tokens_in`
- `tokens_out`
- `cost_usd` (estimated)

## Required Artifacts
- Run manifests in `phase2/benchmarks/runs/`
- Updated run log in `phase2/reproducibility/run-log.md`
- Aggregated metrics table in `phase2/benchmarks/analysis/evaluation_v1_metrics.md`

## Execution Notes
- Keep failed runs; do not delete.
- Record model/provider route explicitly in each manifest.
- Any protocol change requires version bump and note in project state.
