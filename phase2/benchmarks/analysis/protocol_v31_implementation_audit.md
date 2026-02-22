# Protocol v3.1 Implementation Audit

Date: 2026-02-22

## Summary
- The v3.1 diagnostic regressions are not only a modeling effect; there is a concrete task-mismatch defect in ToT candidate generation.
- `tot-prototype` candidate prompts are hardcoded for arithmetic-expression search, even when the active task is not arithmetic (for example `linear2-demo`, `digit-permutation-demo`).

## Primary Defect
- File: `phase2/code/src/phase2_baselines/runners/tot.py`
- Evidence:
  - `_generate_candidates(...)` injects task-agnostic hardcoded instructions:
    - "Generate candidate arithmetic expressions that use each provided number exactly once."
    - "Output only raw expressions using + - * / and parentheses."
  - These instructions are valid for `game24-demo`, but misaligned for:
    - `linear2-demo` (expected answer format: `x=<value>,y=<value>`)
    - `digit-permutation-demo` (expected answer format: integer)

## Quantitative Signals (v3.1, latest-manifest slice)
- ToT underperformed ReAct in 24/24 task-model-profile series (21/24 Holm-adjusted p<0.05).
- Paired outcome asymmetry across all 1200 item-profile pairs:
  - ReAct success + ToT failure: 605
  - ToT success + ReAct failure: 40
- ToT failure buckets:
  - `depth_limit`: 625/652
  - `empty_frontier`: 27/652
- Profile-level ToT failure rates:
  - `tot_model_self_eval`: 0.537
  - `tot_hybrid`: 0.517
  - `tot_rule_based`: 0.530
  - `tot_model_self_eval_lite`: 0.590
- Task-level ToT failure rates:
  - `linear2-demo`: 0.673
  - `digit-permutation-demo`: 0.413

## Interpretation
- Evaluator mode changes do not remove the core issue; all profiles remain negative against ReAct.
- Dominant `depth_limit` with cross-profile consistency is compatible with branch-generation mismatch (invalid/low-yield candidates), not just evaluator calibration.

## Corrective Action (next execution cycle)
1. Replace hardcoded arithmetic candidate instructions with task-specific candidate formatting guidance.
2. Add a task-level `build_tot_candidate_prompt(...)` hook (default fallback in `BaseTask`) and implement explicit overrides for `linear2-demo` and `digit-permutation-demo`.
3. Re-run v3.1 on a 10-item smoke subset first, then full 50-item panels after format/terminal hit-rate sanity checks.
