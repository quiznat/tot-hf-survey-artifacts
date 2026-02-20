# Changelog

## Unreleased

### Phase 2 Workspace
- Added `phase2/` execution scaffold for the novel ToT-HF integration track.
- Added long-term multi-session coordination files: `AGENT_CONTEXT.md`, `ROADMAP.md`, `PROJECT_STATE.md`, and `TASK_BACKLOG.md`.
- Added benchmark and reproducibility templates (`benchmark-matrix.md`, `run-manifest-schema.md`, `templates/experiment_record.md`).
- Added Python baseline harness scaffold (`phase2/code/src/phase2_baselines/`) with:
  - single-path and ReAct baseline runners,
  - unified metrics and manifest utilities,
  - arithmetic task adapter and scripted model adapter,
  - smoke tests and runnable baseline script.
- Added repeated baseline sweep tooling and reporting:
  - `phase2/code/scripts/run_baseline_sweep.py`,
  - `phase2/benchmarks/analysis/baseline_variance_report.md`,
  - `phase2/benchmarks/analysis/baseline_variance_report.json`.
- Added ToT integration prototype components:
  - `phase2/code/src/phase2_baselines/runners/tot.py`,
  - `phase2/code/scripts/run_tot_demo.py`,
  - search-state dataclasses and trace summary integration in run manifests.
- Added Hugging Face model integration path:
  - HTTP-based HF inference adapter in `phase2/code/src/phase2_baselines/adapters.py`,
  - pinned provider config in `phase2/code/configs/hf-default.json`,
  - `--provider hf` support in baseline and ToT run scripts.
- Updated HF adapter to Router chat-completions endpoint and improved arithmetic-expression normalization for live-model outputs.
- Archived first live HF run artifacts (baseline + ToT) for error-analysis traceability.
- Added ToT evaluator strategy variants (`task_binary`, `rule_based`, `model_self_eval`, `hybrid`) and candidate parsing hardening.
- Added Evaluation v1 protocol/aggregation tooling:
  - `phase2/benchmarks/evaluation-protocol-v1.md`
  - `phase2/code/scripts/build_metrics_table.py`
  - `phase2/benchmarks/analysis/evaluation_v1_metrics.md`
  - `phase2/benchmarks/analysis/evaluation_v1_metrics.json`
- Archived first live HF ToT success artifact (`TOT-PROTOTYPE-20260220-030557-6c91df.json`).
- Added HF-filtered analysis outputs:
  - `phase2/benchmarks/analysis/evaluation_v1_metrics_hf.md/.json`,
  - `phase2/benchmarks/analysis/failure_taxonomy_hf.md/.json`.
- Hardened ReAct parsing and recovery:
  - fixed `ACTION`/`FINAL` tag regex extraction,
  - added fallback recovery path when model emits `ACTION` with underspecified `FINAL` value.
- Hardened ToT candidate generation with duplicate filtering and retry prompts to reduce repeated-node stagnation.
- Archived additional live HF success artifacts:
  - `BASELINE-REACT-20260220-032336-d65d87`,
  - `TOT-PROTOTYPE-20260220-032653-617ab6`.
- Updated variance-report writer to support configurable report titles and context-specific notes.
- Set ToT CLI defaults to `model_self_eval` for in-chain evaluation:
  - `phase2/code/scripts/run_tot_demo.py`
  - `phase2/code/scripts/run_tot_sweep.py`
- Added canonical Phase 2 living manuscript source:
  - `phase2/manuscript/PREPAPER.md`
- Updated Phase 2 governance docs to freeze methodology stance:
  - LLM in-chain evaluation as primary condition,
  - rule-based evaluation as control/ablation only.

## v1.1 - 2026-02-19

### Manuscript and Claims
- Aligned authorship and evidence-language in `paper.html` with the validated claim boundary.
- Added Appendix I (`Evidence Scope and Validation`) to distinguish frozen server evidence from local collaboration evidence.

### Reproducibility and Evidence
- Added publication evidence indexing and validation records under `artifacts/publication-evidence/`.
- Finalized claim-evidence mapping and submission-readiness records.

### Build and Distribution
- Regenerated `tot-hf-agents-llm.md` from canonical `paper.html`.
- Regenerated `submission/arxiv/main.tex` and enabled CI PDF compilation/output publication.
- Standardized public-facing repository structure and naming for publication readiness.
