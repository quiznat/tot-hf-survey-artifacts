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
