# Phase 2 Prepaper (Living Source of Truth)

Status: active draft (build-as-we-go)
Last updated: 2026-02-20

## Working Title
Tree-of-Thought Search with Hugging Face Inference Models: Reproducible Evaluation with LLM-Based In-Chain Judging

## Scope
This prepaper is the canonical source for Phase 2 methodological decisions, frozen protocol settings, claim boundaries, and evolving manuscript text.

## Protocol Freeze v2 (Approved)
- Active protocol file: `phase2/benchmarks/evaluation-protocol-v2.md`
- Protocol ID: `TOT-HF-P2-EPV2-2026-02-20`
- Freeze date: 2026-02-20

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
- Fixed panel: 50 paired Game24 items per condition (150 total runs per model for primary 3-condition matrix).
- Primary success analysis:
  - paired condition comparisons on identical item IDs,
  - Wilson CIs for condition success rates,
  - paired bootstrap percentile CIs for success-rate deltas,
  - exact McNemar p-values with Holm correction.
- Interpretation guardrail:
  - claim scope is panel/model-specific unless replicated across additional tasks/models.

## Executed Pilot Evidence (Current)
- Paired 3-item smoke panel executed across `baseline-single-path`, `baseline-react`, and `tot-prototype`.
- Run settings:
  - provider/model: Hugging Face Router, `Qwen/Qwen3-Coder-Next:novita`
  - ToT evaluator mode: `model_self_eval`
- Pilot artifact:
  - `phase2/benchmarks/analysis/game24_lockset_report_pilot.md`
- Pilot summary (exploratory only, not for final claims):
  - `baseline-single-path`: 0/3
  - `baseline-react`: 1/3
  - `tot-prototype`: 2/3
- Interpretation:
  - confirms paired-run pipeline and reporting integrity,
  - insufficient sample for significance; full 50-item panel required.

## Executed Lockset Evidence (50 Paired Items)
- Full paired panel executed: 50 items x 3 conditions = 150 runs.
- Full report artifacts:
  - `phase2/benchmarks/analysis/game24_lockset_report.md`
  - `phase2/benchmarks/analysis/game24_lockset_report.json`
- Condition-level outcomes on `Qwen/Qwen3-Coder-Next:novita`:
  - `baseline-single-path`: success 0.080, mean latency 6040.7 ms
  - `baseline-react`: success 0.400, mean latency 21117.0 ms
  - `tot-prototype (model_self_eval)`: success 0.840, mean latency 53823.3 ms
- Paired deltas (A-B)/N:
  - `baseline-react` vs `baseline-single-path`: +0.320
  - `tot-prototype` vs `baseline-react`: +0.440 (reported as -0.440 in reverse direction)
  - `tot-prototype` vs `baseline-single-path`: +0.760 (reported as -0.760 in reverse direction)
- Paired significance highlights:
  - `baseline-react` vs `baseline-single-path`: p=0.00154 (Holm 0.00154)
  - `tot-prototype` vs `baseline-react`: p=2.74e-05 (Holm 5.49e-05)
  - `tot-prototype` vs `baseline-single-path`: p=7.28e-12 (Holm 2.18e-11)
- Interpretation:
  - lockset execution confirms strong performance separation under this fixed model/panel,
  - ToT gains are accompanied by higher latency/token usage and must be discussed as an explicit tradeoff.

## Executed Protocol-v2 Matrix Evidence (3 Locked Models)
- Locked models:
  - `Qwen/Qwen3-Coder-Next:novita`
  - `Qwen/Qwen2.5-72B-Instruct`
  - `Qwen/Qwen2.5-Coder-32B-Instruct`
- Matrix summary artifacts:
  - `phase2/benchmarks/analysis/game24_lockset_matrix_summary_protocol_v2.md`
  - `phase2/benchmarks/analysis/game24_lockset_matrix_summary_protocol_v2.json`
- Success-rate snapshot across conditions:
  - `Qwen/Qwen3-Coder-Next:novita`: single 0.080, react 0.440, tot 0.760
  - `Qwen/Qwen2.5-72B-Instruct`: single 0.160, react 0.020, tot 0.580
  - `Qwen/Qwen2.5-Coder-32B-Instruct`: single 0.180, react 0.060, tot 0.680
- Interpretation:
  - ToT outperforms ReAct and single-path on all three locked models under paired evaluation.
  - ReAct underperforms markedly on two locked models, suggesting strong model-format sensitivity in the baseline condition.

## Claim Boundary
- Allowed claim pattern: "On fixed paired Game24 items, condition A outperformed condition B by X absolute success points under protocol Y."
- Disallowed claim pattern: broad generalization to arbitrary tasks or models from single-task pilot results.

## Prepaper Build Plan
1. Execute the full protocol-v2 primary matrix across the 3-model set.
2. Run evaluator/search ablations on the primary model and merge into unified analysis tables.
3. Draft Methods and Experimental Setup directly from frozen protocol and executed manifests.
4. Draft Results, Failure Analysis, and Tradeoff analysis from archived artifacts only.
5. Draft Limitations and Threats to Validity before conclusion text.

## Required Tables/Figures (Planned)
- Table 1: Condition-level success/latency/token metrics (paired panel).
- Table 2: Ablation summary (evaluator mode, depth/width, duplicate filtering).
- Table 3: Failure taxonomy with representative run IDs.
- Figure 1: ToT search-state trace diagram with stop-policy points.

## Protocol Changes Log
- 2026-02-20: Set LLM-based in-chain evaluation as primary methodology; moved rule-based scoring to ablation/control role.
- 2026-02-20: Added fixed 50-item Game24 paired panel (`game24_lockset_v1`) and lockset runner script.
- 2026-02-20: Completed 3-item paired smoke pilot; validated end-to-end artifact/report pipeline.
- 2026-02-20: Completed full 50-item paired lockset execution and archived final report artifacts.
- 2026-02-20: Added inferential statistics to lockset reporting (CI + exact McNemar + Holm correction).
- 2026-02-20: Approved protocol freeze `TOT-HF-P2-EPV2-2026-02-20` and promoted `evaluation-protocol-v2.md` as active protocol.
- 2026-02-20: Locked protocol-v2 matrix to fixed available model set with no within-matrix substitutions.
- 2026-02-20: Completed full 3-model protocol-v2 matrix execution and added matrix-level summary artifacts.
