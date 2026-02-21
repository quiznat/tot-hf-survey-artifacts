# Benchmark Matrix v3 (Expanded Scope)

Last updated: 2026-02-21  
Status: active plan (pre-execution)

## Objective
Expand Phase 2 from single-task evidence (Game24) to a multi-task matrix with preserved paired-design rigor.

## Task Families (Locked for v3)

| Task ID | Family | Panel File | Items | Output Type | Objective Scoring | Why Included |
|---|---|---|---:|---|---|---|
| `game24-demo` | Arithmetic expression synthesis | `phase2/benchmarks/panels/game24_lockset_v1.json` | 50 | expression | exact-equality + number-usage | continuity with v2 evidence |
| `subset-sum-demo` | Combinatorial subset selection | `phase2/benchmarks/panels/subset_sum_lockset_v1.json` | 50 | comma-separated integers | subset usage + exact target sum | branch-search utility on constrained selection |
| `linear2-demo` | Symbolic equation solving | `phase2/benchmarks/panels/linear2_lockset_v1.json` | 50 | `x=<v>,y=<v>` | residual threshold on both equations | multi-step algebraic reasoning |
| `digit-permutation-demo` | Constrained optimization | `phase2/benchmarks/panels/digit_permutation_lockset_v1.json` | 50 | integer | digit multiset + divisibility + optimality | search under discrete constraints |

## Conditions
- `baseline-single-path`
- `baseline-react`
- `tot-prototype` (`model_self_eval` as primary evaluator mode)

## Locked Model Matrix
- `Qwen/Qwen3-Coder-Next:novita`
- `Qwen/Qwen2.5-72B-Instruct`
- `Qwen/Qwen2.5-Coder-32B-Instruct`

## Planned Run Volume
- Per task-model block: `3 conditions x 50 = 150` runs.
- Full primary matrix: `4 tasks x 3 models x 150 = 1800` runs.
- Optional post-matrix ablations (primary model only): evaluator/search sweeps per task.

## Statistical Reporting (Task-Scoped)
- Wilson CIs for condition success rates.
- Paired bootstrap percentile CIs for success deltas.
- Exact McNemar tests for paired contrasts with Holm correction.
- Report primary contrast per task/model: `ToT vs ReAct`.

## Guardrails
- No model substitution within the same matrix window.
- Paired item IDs across all conditions.
- Deterministic seed policy (`item_hash`) and fixed temperature logging.
- No broad generalization beyond evaluated task/model panels.
