# Release Notes: Publication Snapshot

Date: 19 February 2026  
Version tag in manuscript: `v1.1 - Final pre-submission clean`

## Summary

This snapshot aligns the manuscript narrative with validated evidence and finalizes publication-facing artifact layering.

## Included Changes

1. Paper claim alignment
- Updated authorship wording in `paper.html` to match validated evidence boundaries:
  - autonomous initiation,
  - first incomplete draft identified in-session,
  - completion after degraded/stalled period,
  - Codex-led hardening with human approval,
  - Grok input treated as advisory.
- Added `Appendix I: Evidence Scope and Validation` to document frozen server scope vs local collaboration scope.

2. Evidence-first repository layering
- Added `artifacts/Paper Inception/EVIDENCE_INDEX.md`.
- Updated top-level artifact pointers in `README.md` and `artifacts/README.md`.
- Confirmed local validation and claim files:
  - `artifacts/Paper Inception/LOCAL_PUBLICATION_READINESS_VALIDATION.md`
  - `artifacts/Paper Inception/claim_evidence_matrix.csv`
  - `artifacts/Paper Inception/agent_human_contributions.md`
  - `artifacts/Paper Inception/submission_readiness_checklist.md`

3. Build and packaging snapshot
- Regenerated LLM markdown from `paper.html` via `submission/build_llm_markdown.sh`.
- Regenerated arXiv source via `submission/convert_to_arxiv.sh`.

## Output Artifacts
- `paper.html`
- `tot-hf-agents-llm.md`
- `submission/arxiv/main.tex`
