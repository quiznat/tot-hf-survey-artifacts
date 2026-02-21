# Evaluation Protocol v3 (Expanded Multi-Task Matrix)

Status: active (frozen for execution)  
Freeze date: 2026-02-21  
Protocol ID: `TOT-HF-P2-EPV3-2026-02-21`

## 1. Purpose
Extend Phase 2 from narrow single-task evidence to a broader, publication-strength multi-task matrix while retaining the same reproducibility and paired-comparison discipline established in protocol v2.

## 2. Research Questions
- RQ1: Across multiple objective reasoning tasks, does ToT (`model_self_eval`) improve success over single-path and ReAct baselines?
- RQ2: How consistent are success gains across model families and task families?
- RQ3: What latency/token tradeoffs accompany any observed gains per task/model block?

## 3. Claim Scope (Locked)
Allowed:
- "Under protocol `TOT-HF-P2-EPV3-2026-02-21`, ToT improved success by X on task T and model M with paired CIs and corrected p-values."

Disallowed:
- Generalized claims about arbitrary tasks, production environments, or all model families.

## 4. Conditions
Primary conditions (required):
- `baseline-single-path`
- `baseline-react`
- `tot-prototype` with `tot_evaluator_mode=model_self_eval`

Secondary conditions (optional post-matrix):
- `tot-prototype` with `rule_based`
- `tot-prototype` with `hybrid`
- search presets A1/A2 or task-specific equivalents

## 5. Tasks and Panels (Locked)
- `game24-demo`: `phase2/benchmarks/panels/game24_lockset_v1.json`
- `subset-sum-demo`: `phase2/benchmarks/panels/subset_sum_lockset_v1.json`
- `linear2-demo`: `phase2/benchmarks/panels/linear2_lockset_v1.json`
- `digit-permutation-demo`: `phase2/benchmarks/panels/digit_permutation_lockset_v1.json`

Each panel contains 50 fixed items and must be run in paired condition mode.

## 6. Model Matrix (Locked)
- `Qwen/Qwen3-Coder-Next:novita`
- `Qwen/Qwen2.5-72B-Instruct`
- `Qwen/Qwen2.5-Coder-32B-Instruct`

Lock rules:
- No substitutions within a matrix window.
- If any locked model becomes unavailable, pause matrix execution and version protocol forward before resuming.

## 7. Run Volume
- Per task-model block: `3 x 50 = 150` runs.
- Full matrix: `4 tasks x 3 models x 150 = 1800` runs.

Optional ablations after core matrix:
- Primary model only (`Qwen/Qwen3-Coder-Next:novita`), task-by-task evaluator/search sensitivity.

## 8. Execution Controls
- Provider: Hugging Face Inference Router.
- Auth token env: `HF_TOKEN`.
- Determinism: `--seed-policy item_hash`.
- Randomness policy: `--hf-temperature 0.0` (or provider minimum when not supported), `--hf-top-p 1.0`.
- Parallelism: `--max-workers 8` target.
- Retries:
  - infra/transport failure: retry once,
  - semantic/task failure: keep as failure (no rerun).

## 9. Statistical Plan
Per task-model block:
- success-rate CIs: Wilson interval,
- paired delta CIs: bootstrap percentile (`bootstrap_samples=10000`, fixed bootstrap seed),
- hypothesis tests: exact two-sided McNemar per paired contrast.

Multiple comparisons:
- Holm correction over pairwise contrasts reported together in a task/model report.
- For pooled cross-task summaries, apply a second-stage correction policy explicitly in the pooled report.

## 10. Artifact Requirements
Per task-model block:
- manifests in task/model-scoped runs directory,
- markdown report (`*_v3.md`),
- json report (`*_v3.json`),
- run-log append in `phase2/reproducibility/run-log-protocol-v3.md`.

Consolidated:
- matrix summary markdown/json from `build_protocol_v3_matrix_summary.py`.

## 11. Canonical Tooling
- Panel generator: `phase2/code/scripts/build_protocol_v3_panels.py`
- Generic lockset runner: `phase2/code/scripts/run_structured_lockset.py`
- Matrix orchestrator: `phase2/code/scripts/run_protocol_v3_matrix.py`
- Matrix summary builder: `phase2/code/scripts/build_protocol_v3_matrix_summary.py`

## 12. Gate Mapping
Protocol v3 completion criteria (for deepening claims):
- Core matrix (`1800` runs) complete with archived reports.
- Task-wise failure taxonomy updated from v3 artifacts.
- Manuscript claims updated to task/model-scoped multi-task evidence.
