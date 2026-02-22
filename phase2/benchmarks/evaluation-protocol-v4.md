# Evaluation Protocol v4 (Confirmatory Reset)

Status: active (frozen before confirmatory launch)
Freeze date: 2026-02-22
Protocol ID: `TOT-HF-P2-EPV4-2026-02-22`

## 1. Purpose
Reset Phase 2 to a publication-grade confirmatory track after pre-v4 exploratory evidence and capability-parity invalidation.

## 2. Exploratory vs Confirmatory Boundary
Exploratory (excluded from primary inference):
- all pre-v4 runs and reports, as declared in `phase2/benchmarks/evidence/series_registry.json`.

Confirmatory (allowed for primary inference):
- `protocol_v4_confirmatory_matrix` only.

Gate-only (not primary inference):
- `protocol_v4_smoke`.

## 3. Research Questions (Confirmatory Scope)
- RQ1: Under matched capability exposure, what is `ToT - ReAct` success delta by task and model?
- RQ2: Under the same controls, what is `ToT - Single` success delta by task and model?
- RQ3: What latency/token tradeoffs accompany those deltas?

## 4. Frozen Conditions
Required:
- `baseline-single-path`
- `baseline-react`
- `tot-prototype` with `tot_evaluator_mode=model_self_eval`

Capability parity lock (mandatory):
- Paired `react` vs `tot` comparisons must use matched tool exposure.
- Allowed policies: `equalize_react_to_tot` (default) or `strict`.
- `off` policy is prohibited for protocol-v4 confirmatory and smoke runs.

## 5. Frozen Tasks and Panels
- `game24-demo`: `phase2/benchmarks/panels/game24_lockset_v4.json`
- `subset-sum-demo`: `phase2/benchmarks/panels/subset_sum_lockset_v4.json`
- `linear2-demo`: `phase2/benchmarks/panels/linear2_lockset_v4.json`
- `digit-permutation-demo`: `phase2/benchmarks/panels/digit_permutation_lockset_v4.json`

Panel policy:
- 50 paired items per task.
- Panels are disjoint from v1 tuned panels (validated by disjointness report artifact).

## 6. Frozen Model Matrix
- `Qwen/Qwen3-Coder-Next:novita`
- `Qwen/Qwen2.5-72B-Instruct`
- `Qwen/Qwen2.5-Coder-32B-Instruct`

Lock rule:
- no substitutions during confirmatory run window.

## 7. Run Volume
Per task-model block:
- `3 conditions x 50 items = 150` runs.

Full matrix:
- `4 tasks x 3 models x 150 = 1800` runs.

## 8. Execution Controls
- Provider: Hugging Face Inference Router.
- Auth env: `HF_TOKEN`.
- Determinism: `seed_policy=item_hash`.
- Sampling: `hf_temperature=0.0`, `hf_top_p=1.0`.
- Parallelism target: `max_workers=8`.

Retry policy:
- infra/transport failure: bounded retries with exponential backoff
  (`max_attempts_per_task=3` in smoke, `max_attempts_per_block=3` in matrix; configurable via CLI).
- semantic/task failure: keep as failure (no rerun).
- if infra retries are exhausted for a task/model block: abort that block and rerun the full block later with unchanged frozen config; do not drop or replace failed items ad hoc.

Stop rules:
- Any model outage requiring substitution pauses protocol-v4 and requires protocol version bump.
- Any implementation or prompt change after freeze invalidates in-progress confirmatory run family.

## 9. Statistical Plan (Predeclared)
Per task-model block:
- condition success CIs: Wilson interval.
- paired delta CIs: bootstrap percentile (`bootstrap_samples=10000`).
- hypothesis tests: exact two-sided McNemar on paired contrasts.

Multiple comparisons:
- Holm correction across pairwise contrasts reported together in each block.

## 10. Mandatory Gates Before Matrix
1. Unit/integration tests pass.
2. Smoke execution complete on all four tasks (`n=10`, paired conditions).
3. Capability audit on smoke series reports zero findings.
4. `--report-only` replay parity on smoke reports is stable.

## 11. Artifact Policy
Primary inferential artifacts must come only from:
- runs: `phase2/benchmarks/runs/protocol_v4_confirmatory_matrix/`
- reports: `phase2/benchmarks/analysis/*_confirmatory_report_*_v4.{md,json}`
- summary: `phase2/benchmarks/analysis/protocol_v4_matrix_summary.{md,json}`

Gate artifacts:
- `phase2/benchmarks/analysis/protocol_v4_gate_report.{md,json}`
- `phase2/benchmarks/analysis/protocol_v4_smoke_capability_audit.{md,json}`

## 12. Claim Boundaries
Allowed:
- task- and model-scoped comparative claims under protocol-v4 controls.

Not allowed:
- universal claims across arbitrary tasks/models or pre-v4 exploratory evidence.
