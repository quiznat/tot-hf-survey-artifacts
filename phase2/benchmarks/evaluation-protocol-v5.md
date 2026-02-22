# Evaluation Protocol v5 (Base Pattern Expansion)

Status: active (frozen for v5 base-pattern matrix)
Freeze date: 2026-02-22
Protocol ID: `TOT-HF-P2-EPV5-2026-02-22`

## 1. Purpose
Extend Phase 2 benchmarking beyond `single,react,tot` by adding direct Chain-of-Thought comparators:
- `baseline-cot`
- `baseline-cot-sc` (self-consistency majority vote)

The v5 objective is comparative mapping across base reasoning patterns before hybrid-profile studies.

## 2. Confirmatory Scope
Primary matrix series:
- `protocol_v5_base_matrix`

Gate/smoke series:
- `protocol_v5_base_smoke`

Hybrid follow-on series (separate protocol family):
- `protocol_v51_hybrid_matrix` (see `evaluation-protocol-v51.md`)

## 3. Frozen Conditions
Required:
- `baseline-single-path`
- `baseline-cot`
- `baseline-cot-sc`
- `baseline-react`
- `tot-prototype` with `tot_evaluator_mode=model_self_eval`

Condition aliases in CLI:
- `single,cot,cot_sc,react,tot`

Capability parity lock:
- Paired `react` vs `tot` comparisons must use matched tool exposure.
- Allowed policies: `equalize_react_to_tot` (default) or `strict`.
- `off` policy is prohibited for v5 primary/gate runs.

## 4. Frozen Tasks and Panels
- `game24-demo`: `phase2/benchmarks/panels/game24_lockset_v4.json`
- `subset-sum-demo`: `phase2/benchmarks/panels/subset_sum_lockset_v4.json`
- `linear2-demo`: `phase2/benchmarks/panels/linear2_lockset_v4.json`
- `digit-permutation-demo`: `phase2/benchmarks/panels/digit_permutation_lockset_v4.json`

Panel policy:
- 50 paired items per task for matrix.
- 10 paired items per task for smoke.
- Disjoint from pre-v4 tuned panels.

## 5. Frozen Model Matrix
- `Qwen/Qwen3-Coder-Next:novita`
- `Qwen/Qwen2.5-72B-Instruct`
- `Qwen/Qwen2.5-Coder-32B-Instruct`

Lock rule:
- no substitutions during v5 execution.

## 6. Run Volume
Per task-model block:
- `5 conditions x 50 items = 250` runs.

Full v5 matrix:
- `4 tasks x 3 models x 250 = 3000` runs.

## 7. Execution Controls
- Provider: Hugging Face Inference Router.
- Auth env: `HF_TOKEN`.
- Determinism controls: `seed_policy=item_hash`, `hf_temperature=0.0`, `hf_top_p=1.0`.
- Parallelism target: `max_workers=12`.
- `cot_sc_samples=5` in frozen base protocol.
- ToT default search: depth/breadth/frontier = `3/3/3`.

Retry policy:
- infrastructure failures: bounded retries with exponential backoff.
- semantic failures: recorded as failures (no ad hoc reruns).

Stop rules:
- model availability issue requiring substitution pauses v5 and requires protocol version bump.
- prompt/code/config change during active run family invalidates that family.

## 8. Statistical Plan (Predeclared)
Per task-model block:
- Wilson CIs for condition success rates.
- paired bootstrap percentile CIs (`bootstrap_samples=10000`) for deltas.
- exact two-sided McNemar for paired contrasts.

Primary pairwise contrasts:
- `ToT - ReAct`
- `ToT - CoT`
- `ToT - CoT-SC`
- `ToT - Single`
- `CoT-SC - CoT`

Multiple comparisons:
- Holm correction across all pairwise contrasts reported in the same block.

## 9. Mandatory Gates Before Matrix
1. Unit tests pass.
2. Smoke coverage complete on all four tasks (`n=10`, all five conditions).
3. Smoke `--report-only` replay is stable.
4. Capability parity policy set to `equalize_react_to_tot` or `strict`.

## 10. Artifact Policy
Primary inferential artifacts:
- runs: `phase2/benchmarks/runs/protocol_v5_base_matrix/`
- reports: `phase2/benchmarks/analysis/*_base_report_*_v5.{md,json}`
- summary: `phase2/benchmarks/analysis/protocol_v5_matrix_summary.{md,json}`

Gate artifacts:
- runs: `phase2/benchmarks/runs/protocol_v5_base_smoke/`
- reports: `phase2/benchmarks/analysis/*_base_smoke_report_*_v5.{md,json}`

## 11. Claim Boundaries
Allowed:
- task/model-scoped comparative claims under v5 controls.

Not allowed:
- universal ordering claims across arbitrary tasks/models/providers.
- mixing exploratory pre-v5 series into v5 inferential tables.
