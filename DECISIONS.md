# DECISIONS

## 2026-02-19

### D-001: Two-track execution strategy
- Decision: Execute work in two phases:
  1. Survey publication version first.
  2. Original research project second.
- Why: Produce a citable scholarly artifact first while preserving a rigorous research path.
- Consequence: Writing and research claims must be clearly separated.

### D-002: Split into two concrete documents now
- Decision: Create two separate drafts immediately:
  1. `drafts/tot_hf_agents_survey.md`
  2. `drafts/tot_hf_agents_novel_work_spec.md`
- Why: Reduce scope collision and enforce claim discipline early.
- Consequence: Survey and research tracks can now evolve independently.

### D-003: Use dropped HTML manuscript as Track 1 primary source
- Decision: Perform first framing and clarity pass directly in `Tree of Thoughts Meets Hugging Face Agents — ClaudDib.html`.
- Why: User requested HTML-first editing, and this is the canonical draft intended for publication flow.
- Consequence: Next Track 1 edits should continue on HTML unless intentionally backported to markdown.

### D-004: Enforce publication-grade survey standards (not blog standards)
- Decision: Track 1 quality bar is now peer-review survey readiness, with explicit methodology and claim-evidence traceability.
- Why: User priority is scholarly merit and substantiated claims over platform publication speed.
- Consequence: Any unsourced quantitative/comparative claims must be removed or cited; survey-method and evidence artifacts are mandatory before submission.

### D-005: Appendix evidence policy
- Decision: Appendix benchmark tables must contain source-attributed reported results only.
- Why: Prevent illustrative numbers from being interpreted as empirical findings.
- Consequence: Comparative intuition tables in main text must be qualitative unless backed by explicit extracted studies.

### D-006: Pre-submission tone policy
- Decision: Enforce neutral, non-promotional survey tone across abstract/body/conclusion.
- Why: Scholarly survey acceptance depends on conservative claim language and evidence-first framing.
- Consequence: Promotional wording and unsupported impact language are systematically replaced with source-grounded phrasing.

### D-007: Reproducibility and traceability appendices
- Decision: Add explicit PRISMA-style flow + reproducibility subsection and dedicated claim-evidence/revision appendices.
- Why: Improve auditability and reviewer confidence in methods/claims evolution.
- Consequence: Section 0.3/0.4 and Appendix F/G are now part of baseline submission package.

### D-008: Preprint metadata and category default
- Decision: Use preprint-style front matter with `cs.AI` primary category, `cs.CL` cross-list, and `cs.LG` optional.
- Why: The manuscript focuses on agentic reasoning systems with language-model integration.
- Consequence: Front matter now carries version/date/category fields with submission date set to `TBD` pending final post date.

### D-009: Public artifact repository endpoint
- Decision: Use `https://github.com/quiznat/tot-hf-survey-artifacts` as the canonical public reproducibility repository endpoint.
- Why: Section 0.4 requires a stable public link for screening, extraction, and raw-search artifacts.
- Consequence: Remaining work shifts from URL selection to artifact-file publication/verification in that repository.
