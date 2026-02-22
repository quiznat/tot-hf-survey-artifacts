# Phase 2 Prepaper (Living Source of Truth)

Status: active draft (build-as-we-go)
Last updated: 2026-02-22 (protocol-v3.1 diagnostics complete; deep analysis integrated)

## Working Title
Tree-of-Thought Search with Hugging Face Inference Models: Reproducible Evaluation with LLM-Based In-Chain Judging

## Scope
This prepaper is the canonical source for Phase 2 methodological decisions, frozen protocol settings, claim boundaries, and evolving manuscript text.

## Protocol Freeze v2 (Approved)
- Active protocol file: `phase2/benchmarks/evaluation-protocol-v2.md`
- Protocol ID: `TOT-HF-P2-EPV2-2026-02-20`
- Freeze date: 2026-02-20

## Protocol v3 Expansion Track (Active)
- Active protocol file: `phase2/benchmarks/evaluation-protocol-v3.md`
- Protocol ID: `TOT-HF-P2-EPV3-2026-02-21`
- Status: matrix execution complete; consolidation and manuscript integration active.
- Additional task panels prepared:
  - `phase2/benchmarks/panels/subset_sum_lockset_v1.json`
  - `phase2/benchmarks/panels/linear2_lockset_v1.json`
  - `phase2/benchmarks/panels/digit_permutation_lockset_v1.json`
- Canonical execution tooling:
  - `phase2/code/scripts/run_structured_lockset.py`
  - `phase2/code/scripts/run_protocol_v3_matrix.py`
  - `phase2/code/scripts/build_protocol_v3_matrix_summary.py`

## Protocol v3.1 Diagnostic Track (Completed)
- Active protocol file: `phase2/benchmarks/evaluation-protocol-v31.md`
- Protocol ID: `TOT-HF-P2-EPV31-2026-02-22`
- Status: matrix execution complete and postprocessing complete.
- Focus:
  - task subset where v3 showed ToT-vs-ReAct weakness (`linear2-demo`, `digit-permutation-demo`)
  - evaluator/search profile comparisons against paired ReAct baselines
- Canonical execution tooling:
  - `phase2/code/scripts/run_protocol_v31_diagnostics.py`
  - `phase2/code/scripts/build_protocol_v31_diagnostic_summary.py`
  - `phase2/code/scripts/build_protocol_v31_deep_analysis.py`
- Consolidated artifacts:
  - `phase2/benchmarks/analysis/protocol_v31_diagnostic_summary.md`
  - `phase2/benchmarks/analysis/protocol_v31_diagnostic_summary.json`
  - `phase2/benchmarks/analysis/protocol_v31_deep_analysis.md`
  - `phase2/benchmarks/analysis/protocol_v31_deep_analysis.json`
  - `phase2/benchmarks/analysis/protocol_v31_implementation_audit.md`

## Methodology Decision Freeze (2026-02-20)
- Primary ToT methodology uses LLM-based in-chain evaluation (`model_self_eval`).
- `rule_based` and `hybrid` evaluator modes are retained for ablations/controls only.
- For Game24, arithmetic correctness checks are used as an offline measurement oracle for reporting metrics, not as the primary in-chain decision mechanism.
- No performance claim is made without paired-condition evidence on the same benchmark item set.

## Research Questions
- RQ1: Does ToT with LLM in-chain evaluation improve success over single-path and ReAct baselines on matched item sets?
- RQ2: What are latency/token tradeoffs of ToT under fixed budget constraints?
- RQ3: How sensitive are outcomes to evaluator mode and search policy choices?

## Experimental Design (Current Evidence Baseline)
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

## Statistical Plan (Current Evidence Baseline)
- Fixed panel: 50 paired Game24 items per condition (150 total runs per model for primary 3-condition matrix).
- Primary success analysis:
  - paired condition comparisons on identical item IDs,
  - Wilson CIs for condition success rates,
  - paired bootstrap percentile CIs for success-rate deltas,
  - exact McNemar p-values with Holm correction.
- Interpretation guardrail:
  - claim scope is panel/model-specific unless replicated across additional tasks/models.

## Protocol-v3 Statistical Plan (Active Expansion)
- Fixed panel size remains `n=50` paired items per condition for every task/model block.
- Core matrix volume: `4 tasks x 3 models x 3 conditions x 50 = 1800` runs.
- Per block reporting:
  - Wilson confidence intervals for success rates,
  - paired bootstrap confidence intervals for deltas (`bootstrap_samples=10000`),
  - exact two-sided McNemar tests for paired contrasts.
- Correction policy:
  - Holm correction within each task/model block report;
  - any pooled cross-task analysis must declare its own second-stage correction scope.
- Claim boundary remains task- and model-scoped unless replicated across blocks.

## Draft Manuscript Text: Methods and Experimental Setup (v0.1)

### 4. Methods
We evaluate Tree-of-Thought (ToT) search in a controlled agent harness with three conditions implemented under a shared execution stack: `baseline-single-path`, `baseline-react`, and `tot-prototype`. The single-path baseline performs one forward generation pass and is scored on the final extracted expression. The ReAct baseline runs an iterative loop (`max_steps=5`) with a `calc` tool and returns either a tagged `FINAL` answer or a recovered action expression when valid. The ToT prototype maintains an explicit frontier of thought nodes. At each depth, it generates candidate expressions, evaluates each candidate, accumulates scores along parent-child paths, prunes to a fixed frontier width by cumulative score, and stops on the first terminal solution or at depth limit.

The primary ToT evaluator is `model_self_eval`, where the same model assigns a scalar score in `[0,1]` to each candidate via an in-chain scoring prompt. `rule_based` and `hybrid` evaluators are retained as control/ablation modes only and are not used for primary claims. Default primary search settings are `max_depth=3`, `branch_factor=3`, and `frontier_width=3`, with frozen ablation presets A1 (`2/3/3`) and A2 (`3/4/4`).

All runs use the Hugging Face Inference Router with fixed execution controls from the frozen protocol (`TOT-HF-P2-EPV2-2026-02-20`): deterministic item-level seeding via `seed_policy=item_hash`, sampling controls logged per run (`hf_temperature=0.0`, `hf_top_p=1.0`), and no within-matrix model substitution. Each run emits a structured manifest with run metadata (`run_id`, timestamp, condition, provider/model, panel/item IDs, input), configuration fields (search and evaluator settings), and outcome/trace metrics (success, latency, tokens, notes, error type where applicable).

### 5. Experimental Setup
The primary task is Game24 expression synthesis on a fixed paired panel (`game24_lockset_v1`) containing 50 solvable items (`selection_seed=20260220`, number range 1-10). Each item is defined by four integers and an oracle solution string used for panel provenance; agent execution receives only the four-number input. Success is binary and requires an expression that uses each provided number exactly once and evaluates to 24 under the task validator.

The locked model matrix is:
- `Qwen/Qwen3-Coder-Next:novita`
- `Qwen/Qwen2.5-72B-Instruct`
- `Qwen/Qwen2.5-Coder-32B-Instruct`

For each model, we run all three primary conditions on the identical 50-item panel (`3 x 50 = 150` runs/model; `450` runs total for the matrix). Additional ablations are executed on the primary model (`Qwen/Qwen3-Coder-Next:novita`) using the same paired panel design: evaluator-mode ablations (`model_self_eval`, `rule_based`, `hybrid`) and search-policy ablations (primary, A1, A2). These executed batches contribute an additional `600` runs, yielding `1050` protocol-v2 matrix+ablation runs in total (excluding smoke prechecks).

Primary endpoint is success rate by condition. Secondary endpoints are latency (ms) and token usage (`tokens_in`, `tokens_out`). Statistical reporting is pre-registered in the protocol and implemented by the lockset report pipeline: Wilson confidence intervals for condition success rates, paired bootstrap percentile confidence intervals for success-rate deltas (`bootstrap_samples=10000`, fixed seed), and exact two-sided McNemar tests for paired contrasts with Holm correction across reported pairwise tests. All claims are restricted to panel/model-scoped observations under this protocol.

## Draft Manuscript Text: Results and Limitations (v0.1)

### 6. Results
Under the frozen protocol (`TOT-HF-P2-EPV2-2026-02-20`), ToT with `model_self_eval` outperformed both baseline conditions on all three locked models in paired 50-item Game24 evaluations. Success rates for `tot-prototype` were `0.760` (`Qwen3-Coder-Next`), `0.580` (`Qwen2.5-72B-Instruct`), and `0.680` (`Qwen2.5-Coder-32B-Instruct`). Corresponding absolute deltas versus ReAct were `+0.320`, `+0.560`, and `+0.620`, with Holm-corrected McNemar p-values `8.55e-04`, `2.24e-08`, and `2.79e-09`, respectively. Deltas versus single-path were `+0.680`, `+0.420`, and `+0.500`, each with corrected p-values below `1e-04`.

Latency and token footprints indicate a cost-performance tradeoff rather than uniform dominance. In the matrix reports, ToT latency exceeds single-path latency on all models and usually exceeds ReAct latency; however, magnitude varies by model and run window (for example, near parity between ToT and ReAct on `Qwen2.5-Coder-32B-Instruct`). This supports a scoped claim: paired success gains are robust on the fixed panel, while compute overhead is model- and configuration-dependent.

Evaluator ablations on the primary model (`Qwen3-Coder-Next`) show that ToT remains superior to ReAct across all tested evaluator modes: `model_self_eval` (`0.760`), `rule_based` (`0.860`), and `hybrid` (`0.780`) ToT success rates, each with corrected paired significance. Because `rule_based` uses task-structured heuristics, it is treated as a diagnostic control and not the primary claim path. Search-policy ablations further show sensitivity to depth/width settings: A1 (`2/3/3`) achieved `0.720` ToT success, primary (`3/3/3`) `0.760`, and A2 (`3/4/4`) `0.920`, with ToT-vs-ReAct paired significance preserved in all presets.

Failure taxonomy analysis across archived protocol runs (`n=202` failures) identifies dominant error classes: `format_or_notation_mismatch` (`109`), `other_failure` (`66`), and `depth_limit_no_solution` (`24`), plus infrequent `invalid_candidate_retained` (`2`) and `unsafe_expression_filtered` (`1`). These patterns are consistent with parser/normalization fragility and residual search termination failures, and motivate targeted robustness work in output normalization and candidate filtering.

### 7. Limitations
First, the current evidence is task-specific: all primary claims are derived from a fixed Game24 panel and do not establish generalization to broader tool-use or open-domain planning tasks. Second, the model set is intentionally locked and relatively narrow; conclusions are limited to the three evaluated models and the execution windows in which they were run. Third, provider-side effects (routing, transient latency variance, serving updates) may influence latency comparisons across batches even when protocol controls are held fixed.

Fourth, the primary in-chain evaluator (`model_self_eval`) uses the same model family for generation and scoring, which may introduce correlated biases in branch selection. The offline arithmetic validator provides an external correctness check for reporting, but does not remove all possible in-chain evaluator biases. Fifth, some ablation outcomes (for example, strong `rule_based` performance) may reflect task-structured advantages and should not be interpreted as a general recommendation for unconstrained domains.

Finally, this phase emphasizes internal reproducibility and controlled paired inference rather than deployment realism: no external human preference judgments, end-to-end agent productivity tasks, or production cost audits are included yet. These omissions are intentional and define the boundary of current claims.

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

## Executed Evaluator Ablation Evidence (Primary Model)
- Primary model: `Qwen/Qwen3-Coder-Next:novita`
- Evaluator modes executed on identical 50-item paired panel:
  - `model_self_eval`: single 0.080, react 0.440, tot 0.760
  - `rule_based`: single 0.080, react 0.420, tot 0.860
  - `hybrid`: single 0.080, react 0.420, tot 0.780
- Consolidated artifacts:
  - `phase2/benchmarks/analysis/game24_lockset_evaluator_ablation_summary.md`
  - `phase2/benchmarks/analysis/game24_lockset_evaluator_ablation_summary.json`
- Significance snapshot (ToT vs ReAct, paired McNemar):
  - `model_self_eval`: p=8.55e-04
  - `rule_based`: p=2.74e-05
  - `hybrid`: p=4.01e-05
- Interpretation:
  - ToT remains superior to both baselines under all evaluator modes on this fixed panel.
  - `model_self_eval` remains the primary methodology; `rule_based`/`hybrid` remain ablation/control conditions.

## Executed Search Ablation Evidence (Primary Model)
- Primary model: `Qwen/Qwen3-Coder-Next:novita`
- Search presets executed on identical 50-item paired panel:
  - `primary` (`depth=3, branch=3, frontier=3`): single 0.080, react 0.440, tot 0.760
  - `A1` (`depth=2, branch=3, frontier=3`): single 0.060, react 0.360, tot 0.720
  - `A2` (`depth=3, branch=4, frontier=4`): single 0.080, react 0.420, tot 0.920
- Consolidated artifacts:
  - `phase2/benchmarks/analysis/game24_lockset_search_ablation_summary.md`
  - `phase2/benchmarks/analysis/game24_lockset_search_ablation_summary.json`
- Significance snapshot (ToT vs ReAct, paired McNemar):
  - `primary`: p=8.55e-04 (Holm 8.55e-04)
  - `A1`: p=1.21e-04 (Holm 2.42e-04)
  - `A2`: p=5.96e-08 (Holm 1.19e-07)
- ToT latency/token snapshot by preset:
  - `primary`: 58213.6 ms, tokens_in 978.3, tokens_out 107.0
  - `A1`: 9050.9 ms, tokens_in 636.7, tokens_out 70.8
  - `A2`: 11262.8 ms, tokens_in 955.9, tokens_out 121.9
- Interpretation:
  - ToT remains superior to ReAct under all three search presets on this panel/model.
  - A2 currently yields the strongest accuracy (0.920) with markedly lower observed latency than the earlier `primary` execution window; this should be treated as observed run behavior under provider conditions, not a universal latency law.
  - Search policy materially affects both outcome quality and compute profile, and must remain explicitly reported in all claims.

## Executed Protocol-v3 Matrix Evidence (4 Tasks x 3 Models)
- Matrix completion:
  - 4 tasks x 3 models x 3 conditions x 50 paired items = 1800 runs.
  - Consolidated outputs:
    - `phase2/benchmarks/analysis/protocol_v3_matrix_summary.md`
    - `phase2/benchmarks/analysis/protocol_v3_matrix_summary.json`
- Directionality snapshot:
  - ToT vs ReAct: positive delta in 4/12 task-model blocks; negative delta in 8/12 blocks.
  - ToT vs Single-path: positive delta in 12/12 task-model blocks.
  - Holm-adjusted significance counts:
    - ToT vs ReAct: 9/12 blocks with p<0.05.
    - ToT vs Single-path: 10/12 blocks with p<0.05.
- Task-level mean delta (ToT minus ReAct):
  - `game24-demo`: +0.573
  - `subset-sum-demo`: +0.027
  - `digit-permutation-demo`: -0.287
  - `linear2-demo`: -0.587
- Interpretation:
  - The protocol-v2 Game24 finding (ToT > ReAct) replicates in `game24-demo` across all three locked models.
  - Under this v3 configuration, ReAct is stronger than ToT on `linear2-demo` and `digit-permutation-demo` across all three locked models.
  - Under this v3 configuration, ToT remains consistently stronger than single-path across all tasks/models.
  - Claim scope remains task- and model-scoped; v3 evidence does not support a universal "ToT > ReAct" statement.

## Executed Protocol-v3.1 Diagnostic Evidence (Failure Tasks x Profile Sweep)
- Matrix completion:
  - 2 tasks x 3 models x 4 profiles x 50 paired items = 1200 paired comparisons (`2400` total manifests).
  - Consolidated outputs:
    - `phase2/benchmarks/analysis/protocol_v31_diagnostic_summary.md`
    - `phase2/benchmarks/analysis/protocol_v31_diagnostic_summary.json`
    - `phase2/benchmarks/analysis/protocol_v31_deep_analysis.md`
    - `phase2/benchmarks/analysis/protocol_v31_deep_analysis.json`
- Profile/model summary:
  - ToT underperformed ReAct in 24/24 task-model-profile series (21/24 with Holm-adjusted p<0.05).
  - Mean ToT-minus-ReAct deltas by task:
    - `linear2-demo`: -0.647
    - `digit-permutation-demo`: -0.328
  - Mean latency multiplier (ToT/ReAct):
    - `linear2-demo`: 4.067x
    - `digit-permutation-demo`: 2.652x
- Deep-analysis failure signal:
  - Latest-manifest ToT failures are dominated by depth-limit termination (625/652 in the v3.1 deep-analysis latest-manifest slice).
  - Task-level ToT failure rates in latest-manifest slice:
    - `linear2-demo`: 0.673
    - `digit-permutation-demo`: 0.413
- Determinism and replay check:
  - Full-matrix `--report-only` replay completed.
  - Canonical statistical fields were stable across replay (0/24 changed after normalizing away regenerated metadata fields).
- Interpretation:
  - On these failure-task panels, current ToT implementation/prompt-budget policy is not competitive with ReAct.
  - Immediate claim posture: task-conditional routing and implementation refinement, not general ToT superiority.

## Claim Boundary
- Allowed claim pattern: "On fixed paired item sets for task T and model M, condition A outperformed condition B by X absolute success points under protocol Y."
- Allowed claim pattern: "Across this protocol-v3 matrix, ToT outperformed single-path in all evaluated blocks while ToT-vs-ReAct direction varied by task/model."
- Allowed claim pattern: "Under protocol-v3.1 diagnostic settings on failure-task panels, ToT underperformed ReAct across all profile variants."
- Disallowed claim pattern: universal ordering claims (for example, "ToT always outperforms ReAct") without additional cross-task replication and sensitivity analysis.

## Prepaper Build Plan
1. Keep v2 Methods/Results text as frozen baseline evidence. (completed in v0.1 section above)
2. Execute protocol-v3 core matrix and generate consolidated v3 summary artifacts. (completed)
3. Add a dedicated v3 results section with task-scoped contrasts and correction policy details. (completed)
4. Execute protocol-v3.1 diagnostics and integrate negative/conditional evidence boundaries. (completed)
5. Draft reproducibility appendix with v3 command blocks, panel manifests, and artifact index. (completed: `phase2/manuscript/APPENDIX_REPRO_V3.md`)
6. Build anonymous manuscript package after v3 + v3.1 evidence integration.

Canonical execution commands for search ablations are archived in:
- `phase2/benchmarks/protocol-v2-search-ablation-execution.md`

## Required Tables/Figures
- Table 1: Condition-level success/latency/token metrics (paired panel).
- Table 2: Multi-task matrix summary (task x model x condition).
- Table 3: Ablation summary (evaluator mode and search presets).
- Table 4: Failure taxonomy with representative run IDs.
- Figure 1: ToT search-state trace diagram with stop-policy points.
- Figure 2: Protocol-v3 effect-size forest plot (ToT vs ReAct by task/model).
- Generated v3 table/figure-data artifacts:
  - `phase2/benchmarks/analysis/protocol_v3_submission_tables.md`
  - `phase2/benchmarks/analysis/protocol_v3_table_matrix.csv`
  - `phase2/benchmarks/analysis/protocol_v3_table_task_aggregate.csv`
  - `phase2/benchmarks/analysis/protocol_v3_figure_effect_tot_vs_react.csv`
  - `phase2/benchmarks/analysis/protocol_v3_figure_effect_tot_vs_single.csv`

## Protocol Changes Log
- 2026-02-20: Set LLM-based in-chain evaluation as primary methodology; moved rule-based scoring to ablation/control role.
- 2026-02-20: Added fixed 50-item Game24 paired panel (`game24_lockset_v1`) and lockset runner script.
- 2026-02-20: Completed 3-item paired smoke pilot; validated end-to-end artifact/report pipeline.
- 2026-02-20: Completed full 50-item paired lockset execution and archived final report artifacts.
- 2026-02-20: Added inferential statistics to lockset reporting (CI + exact McNemar + Holm correction).
- 2026-02-20: Approved protocol freeze `TOT-HF-P2-EPV2-2026-02-20` and promoted `evaluation-protocol-v2.md` as active protocol.
- 2026-02-20: Locked protocol-v2 matrix to fixed available model set with no within-matrix substitutions.
- 2026-02-20: Completed full 3-model protocol-v2 matrix execution and added matrix-level summary artifacts.
- 2026-02-21: Completed evaluator ablation runs (`rule_based`, `hybrid`) on primary model and added consolidated evaluator-ablation summary artifacts.
- 2026-02-21: Added search-ablation execution playbook and summary tooling (`build_search_ablation_summary.py`).
- 2026-02-21: Completed A1/A2 search-policy ablation runs on primary model and archived consolidated search-ablation summary artifacts.
- 2026-02-21: Refreshed protocol-v2 failure taxonomy artifacts from archived Hugging Face manifests.
- 2026-02-21: Drafted manuscript-ready Methods and Experimental Setup text from frozen protocol artifacts.
- 2026-02-21: Drafted manuscript-ready Results and Limitations text from frozen matrix, ablation, and taxonomy artifacts.
- 2026-02-21: Added protocol-v3 multi-task scaffold (new task adapters, deterministic panels, generic lockset runner, matrix orchestration, and matrix summary tooling).
- 2026-02-21: Activated protocol-v3 as the current deepening track while preserving v2 as frozen baseline evidence.
- 2026-02-21: Completed full locked protocol-v3 matrix execution (1800 runs) across 4 tasks and 3 models.
- 2026-02-21: Generated consolidated v3 matrix summary, task-scoped and pooled v3 failure taxonomies, and report-only determinism parity checks.
- 2026-02-21: Added v3 submission table/figure-data generator and reproducibility appendix draft (`APPENDIX_REPRO_V3.md`).
- 2026-02-22: Completed full protocol-v3.1 diagnostic matrix (1200 paired comparisons; 2400 total manifests) across failure tasks and profile variants.
- 2026-02-22: Added consolidated protocol-v3.1 summary/deep-analysis artifacts and completed full-matrix canonical parity replay checks.
- 2026-02-22: Logged implementation-audit finding that v3.1 ToT candidate prompting is hardcoded to arithmetic-expression output across non-arithmetic tasks.
