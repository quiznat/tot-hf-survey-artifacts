# Phase 2 Project State

Status date: 2026-02-20

## Current Phase
- Phase 1 (survey): submission-ready and awaiting external review process.
- Phase 2 (novel implementation): baseline harness and ToT prototype completed.
- Canonical manuscript source: `phase2/manuscript/PREPAPER.md`.

## Gate Status
- P2-G0 (Project Bootstrap): completed
- P2-G1 (Baseline Harness): completed
- P2-G2 (ToT Integration Prototype): completed
- P2-G3 (Evaluation v1): completed
- P2-G4 (Ablation and Error Analysis): in progress
- P2-G5 (Manuscript Draft): not started
- P2-G6 (Submission Package): not started

## Completed This Session
- Established Phase 2 planning and operating framework (`phase2/`).
- Drafted benchmark matrix and run manifest schema for evaluation protocol.
- Added reproducibility run log and first dry-run manifest artifact.
- Implemented Python baseline scaffold under `phase2/code/src/phase2_baselines/`:
  - single-path runner,
  - ReAct runner,
  - unified metrics and manifest utilities,
  - arithmetic task adapter and scripted model adapter.
- Added runner smoke tests and validated successful baseline runs with manifest outputs.
- Added repeated-run sweep driver and generated baseline variance reports:
  - `phase2/benchmarks/analysis/baseline_variance_report.md`
  - `phase2/benchmarks/analysis/baseline_variance_report.json`
- Added ToT prototype implementation under `phase2/code/src/phase2_baselines/runners/tot.py` with:
  - generation-evaluation-search loop,
  - configurable depth/breadth/frontier pruning,
  - failure handling and structured search trace summary.
- Added ToT demo run artifact:
  - `phase2/benchmarks/runs/TOT-PROTOTYPE-20260220-013700-a7df83.json`.
- Added Hugging Face provider integration:
  - adapter in `phase2/code/src/phase2_baselines/adapters.py`,
  - pinned config in `phase2/code/configs/hf-default.json`,
  - CLI support in baseline/toT run scripts (`--provider hf`).
- Completed first live HF executions via Router with archived manifests:
  - baseline: `phase2/benchmarks/runs/BASELINE-SINGLE-PATH-20260220-025629-9649ee.json`,
  - ToT: `phase2/benchmarks/runs/TOT-PROTOTYPE-20260220-025520-892eed.json`,
  - ToT: `phase2/benchmarks/runs/TOT-PROTOTYPE-20260220-025614-869706.json`.
- Implemented ToT evaluator strategy variants:
  - `task_binary`, `rule_based`, `model_self_eval`, `hybrid`.
- Completed first live HF ToT success artifact after evaluator upgrades:
  - `phase2/benchmarks/runs/TOT-PROTOTYPE-20260220-030557-6c91df.json`.
- Added Evaluation v1 protocol and metrics aggregation tooling:
  - `phase2/benchmarks/evaluation-protocol-v1.md`,
  - `phase2/code/scripts/build_metrics_table.py`,
  - `phase2/benchmarks/analysis/evaluation_v1_metrics.md`,
  - `phase2/benchmarks/analysis/evaluation_v1_metrics.json`.
- Added HF-filtered analysis outputs:
  - `phase2/benchmarks/analysis/evaluation_v1_metrics_hf.md`,
  - `phase2/benchmarks/analysis/evaluation_v1_metrics_hf.json`,
  - `phase2/benchmarks/analysis/failure_taxonomy_hf.md`,
  - `phase2/benchmarks/analysis/failure_taxonomy_hf.json`.
- Hardened `ReactRunner` parsing/recovery for mixed `ACTION` + underspecified `FINAL` outputs.
- Hardened `ToTRunner` generation with duplicate filtering and retry prompts for candidate diversity.
- Archived new live HF success artifacts:
  - `phase2/benchmarks/runs/BASELINE-REACT-20260220-032336-d65d87.json`,
  - `phase2/benchmarks/runs/TOT-PROTOTYPE-20260220-032653-617ab6.json`.
- Added paired lockset infrastructure for publication-style panel execution:
  - panel file: `phase2/benchmarks/panels/game24_lockset_v1.json` (50 fixed solvable items),
  - runner: `phase2/code/scripts/run_game24_lockset.py`,
  - paired pilot report: `phase2/benchmarks/analysis/game24_lockset_report_pilot.md` (3-item smoke panel).
- Added manifest panel metadata fields (`item_id`, `panel_id`, `input_data`) to preserve paired-evaluation traceability.
- Completed full paired lockset execution (50 items x 3 conditions = 150 runs):
  - report: `phase2/benchmarks/analysis/game24_lockset_report.md`,
  - machine-readable summary: `phase2/benchmarks/analysis/game24_lockset_report.json`,
  - archived run artifacts under `phase2/benchmarks/runs/` with panel-linked metadata.
- Full lockset summary on `Qwen/Qwen3-Coder-Next:novita`:
  - `baseline-single-path`: success 0.080,
  - `baseline-react`: success 0.400,
  - `tot-prototype (model_self_eval)`: success 0.840.

## Next 3 Tasks
1. Run ablations over evaluator mode and search parameters against the same fixed lockset.
2. Extend paired report with confidence intervals and significance tests.
3. Implement parallel lockset execution controls for faster future batch runs.

## Risks / Dependencies
- Benchmark selection scope creep.
- Model/API variability affecting reproducibility.
- Need consistent environment pinning before evaluation runs.

## Decision Log
- 2026-02-20: Adopted gate-based roadmap for Phase 2 execution.
- 2026-02-20: Set TMLR-quality reproducibility standard for this track.
- 2026-02-20: Completed Gate P2-G0 bootstrap with benchmark/reproducibility scaffolding.
- 2026-02-20: Chose Python-first implementation stack for baseline and evaluation harness.
- 2026-02-20: Completed Gate P2-G1 with repeated-run baseline variance report generation.
- 2026-02-20: Completed Gate P2-G2 with ToT prototype runner and traceable demo artifact.
- 2026-02-20: Added Hugging Face provider adapter path for baseline and ToT scripts (live token validation pending).
- 2026-02-20: Completed first live Hugging Face baseline/ToT runs; captured failure artifacts for taxonomy and evaluator-improvement work.
- 2026-02-20: Added evaluator variants and achieved first live HF ToT success artifact.
- 2026-02-20: Started P2-G3 with fixed protocol and aggregate metrics-table generation pipeline.
- 2026-02-20: Hardened ReAct parser/recovery path; converted live HF ReAct run to success on same benchmark.
- 2026-02-20: Added ToT duplicate-aware candidate generation and captured additional live HF ToT success artifact.
- 2026-02-20: Adopted LLM-based in-chain evaluation (`model_self_eval`) as primary Phase 2 methodology; relegated rule-based evaluation to ablation/control role.
- 2026-02-20: Created `phase2/manuscript/PREPAPER.md` as canonical living source of truth for protocol and manuscript decisions.
- 2026-02-20: Added fixed paired Game24 lockset panel and paired-condition runner/report pipeline; completed 3-item pilot execution.
- 2026-02-20: Completed full 50-item paired Game24 lockset run and marked Gate P2-G3 complete.
