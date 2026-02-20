# Phase 2 Prepaper (Living Source of Truth)

Status: active draft (build-as-we-go)
Last updated: 2026-02-20

## Working Title
Tree-of-Thought Search with Hugging Face Inference Models: Reproducible Evaluation with LLM-Based In-Chain Judging

## Scope
This prepaper is the canonical source for Phase 2 methodological decisions, frozen protocol settings, claim boundaries, and evolving manuscript text.

## Methodology Decision Freeze (2026-02-20)
- Primary ToT methodology uses LLM-based in-chain evaluation (`model_self_eval`).
- `rule_based` and `hybrid` evaluator modes are retained for ablations/controls only.
- For Game24, arithmetic correctness checks are used as an offline measurement oracle for reporting metrics, not as the primary in-chain decision mechanism.
- No performance claim is made without paired-condition evidence on the same benchmark item set.

## Research Questions
- RQ1: Does ToT with LLM in-chain evaluation improve success over single-path and ReAct baselines on matched item sets?
- RQ2: What are latency/token tradeoffs of ToT under fixed budget constraints?
- RQ3: How sensitive are outcomes to evaluator mode and search policy choices?

## Experimental Design (Current)
- Conditions:
  - `baseline-single-path`
  - `baseline-react`
  - `tot-prototype` (default evaluator mode: `model_self_eval`)
- Provider/model:
  - Hugging Face Router
  - Primary model for current lock set: `Qwen/Qwen3-Coder-Next:novita`
- Task family:
  - Game24 arithmetic expression synthesis
- Pairing policy:
  - Identical item IDs evaluated across all conditions.

## Statistical Plan (Current)
- Pilot lock set: 50 paired Game24 items per condition (150 total runs).
- Primary success analysis:
  - paired condition comparisons on the same items,
  - effect size + confidence intervals,
  - p-values reported with multiple-comparison correction if >1 contrast.
- Interpretation guardrail:
  - 50 paired items is a pilot-scale panel; use for effect-size estimation and protocol validation.

## Claim Boundary
- Allowed claim pattern: "On fixed paired Game24 items, condition A outperformed condition B by X absolute success points under protocol Y."
- Disallowed claim pattern: broad generalization to arbitrary tasks or models from single-task pilot results.

## Prepaper Build Plan
1. Finalize protocol freeze block (task panel, budgets, thresholds, evaluator defaults).
2. Run pilot lock set and generate paired-condition analysis tables.
3. Draft Methods and Experimental Setup sections from executed protocol only.
4. Draft Results and Failure Analysis from archived artifacts.
5. Draft Limitations and Threats to Validity before any conclusion text.

## Required Tables/Figures (Planned)
- Table 1: Condition-level success/latency/token metrics (paired panel).
- Table 2: Ablation summary (evaluator mode, depth/width, duplicate filtering).
- Table 3: Failure taxonomy with representative run IDs.
- Figure 1: ToT search-state trace diagram with stop-policy points.

## Protocol Changes Log
- 2026-02-20: Set LLM-based in-chain evaluation as primary methodology; moved rule-based scoring to ablation/control role.
