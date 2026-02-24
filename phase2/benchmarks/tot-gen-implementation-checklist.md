# ToT-Gen Recursive Implementation Checklist

Status: Ready for execution  
Owner lane: `tot_gen_recursive` (new condition, no replacement of legacy `tot_gen`)

## 0) Freeze Scope
- [ ] Freeze v1 recursive scope: `decompose`, `solve`, `chain` only.
- [ ] Freeze search budgets: `max_depth`, `branch_factor`, `frontier_width`, `max_nodes`, `max_tokens`.
- [ ] Freeze claim boundary: exploratory until parity + determinism gates pass.

## 1) Action Model (Core Behavior)
- [ ] Define action enum in node state: `DECOMPOSE`, `SOLVE`, `CHAIN`.
- [ ] Define transition rules:
- `DECOMPOSE -> child goals + recomposition contract`
- `SOLVE -> typed result or failure`
- `CHAIN -> next-step goal/state without child split`
- [ ] Enforce that every expanded node picks exactly one action.

Target files:
- `phase2/code/src/phase2_baselines/models.py`
- `phase2/code/src/phase2_baselines/runners/tot.py`

## 2) Node + Contract Schema
- [ ] Extend node model with:
- `goal_id`, `goal_text`, `action`, `parent_goal_id`
- `children_goal_ids`
- `contract_id`, `contract`
- `result`, `result_type`, `verification`
- [ ] Add recomposition contract schema:
- `child_specs`
- `combine_instruction`
- `verify_instruction`
- `failure_policy`
- [ ] Reject decomposition nodes with missing/invalid contracts.

Target files:
- `phase2/code/src/phase2_baselines/models.py`
- `phase2/code/src/phase2_baselines/runners/tot.py`

## 3) Prompt/Parse Layer for 3 Actions
- [ ] Add planner prompt that can emit one of three action records.
- [ ] Add strict parser for structured action output (JSON-first, text fallback).
- [ ] Add task helpers for action-specific prompts:
- decomposition prompt
- direct solve prompt
- chain-step prompt

Target files:
- `phase2/code/src/phase2_baselines/tasks/base.py`
- `phase2/code/src/phase2_baselines/runners/tot.py`

## 4) Recursive Solver Engine
- [ ] Implement `solve_goal(goal, context)` as explicit recursion.
- [ ] Base case: `SOLVE` returns typed result + verification.
- [ ] Recursive case: `DECOMPOSE` creates children, recursively solves each child.
- [ ] Chain case: `CHAIN` advances one step and re-enters solve loop.
- [ ] Parent recomposition uses contract and child results.
- [ ] Parent verification runs after recomposition; fail triggers backtrack.

Target files:
- `phase2/code/src/phase2_baselines/runners/tot.py`

## 5) Search/Ranking Policy
- [ ] Keep multi-branch frontier over active goals/plans.
- [ ] Score branch from:
- decomposition quality
- child completion status
- recomposition verification confidence
- [ ] Prune to frontier width each expansion round.
- [ ] Keep global dedupe for equivalent goal states.

Target files:
- `phase2/code/src/phase2_baselines/runners/tot.py`

## 6) Runtime Safety + Determinism
- [ ] Add recursion guards: depth, node count, cycle detection.
- [ ] Add retry limits for parse/contract failures.
- [ ] Record deterministic seed path per node expansion.
- [ ] Keep manifest replay capability for identical runs.

Target files:
- `phase2/code/src/phase2_baselines/runners/tot.py`
- `phase2/code/src/phase2_baselines/runners/base.py`
- `phase2/code/scripts/run_structured_lockset.py`

## 7) Trace + Manifest Artifacts
- [ ] Log per node:
- selected action
- produced children
- contract summary
- recomposition output
- verification result
- [ ] Add aggregate fields:
- action counts (`decompose/solve/chain`)
- recomposition failures
- backtrack count
- [ ] Persist compact and full traces.

Target files:
- `phase2/code/src/phase2_baselines/runners/base.py`
- `phase2/code/src/phase2_baselines/runners/tot.py`

## 8) Condition Wiring
- [ ] Add new condition `tot_gen_recursive` in lockset runner.
- [ ] Keep current `tot` and `tot_gen` unchanged for historical comparability.
- [ ] Add explicit mode flags:
- `--tot-gen-recursive-enabled`
- `--tot-gen-recursive-max-depth`
- `--tot-gen-recursive-frontier-width`

Target files:
- `phase2/code/scripts/run_structured_lockset.py`
- `phase2/code/scripts/run_protocol_v5_smoke.py`
- `phase2/code/scripts/run_protocol_v5_matrix.py`

## 9) Tests (Must Pass Before Any Matrix)
- [ ] Unit: parser roundtrip for all action types.
- [ ] Unit: contract validation fail/pass paths.
- [ ] Unit: recomposition with missing child output fails hard.
- [ ] Unit: recursion guard halts loops/cycles.
- [ ] Integration: deterministic replay on fixed seed panel.
- [ ] Integration: parity check confirms no extra tools leaked.

Target files:
- `phase2/code/tests/test_tot_recursive_actions.py` (new)
- `phase2/code/tests/test_tot_recursive_contracts.py` (new)
- `phase2/code/tests/test_runner_smoke.py`

## 10) Launch Gates
- [ ] Gate A: all unit/integration tests green.
- [ ] Gate B: 10-item smoke on all tasks completes with full traces.
- [ ] Gate C: deterministic rerun parity (report-only + manifest hash checks).
- [ ] Gate D: capability parity audit passes for paired comparisons.
- [ ] Gate E: only then run full matrix.

## 11) First Execution Order
- [ ] Implement sections 1-4.
- [ ] Add tests in section 9.
- [ ] Run smoke gates A-D.
- [ ] Run v5 matrix with `tot_gen_recursive` included.
- [ ] Generate comparative summary against `tot_gen` and `tot`.

