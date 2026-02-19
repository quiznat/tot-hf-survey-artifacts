# PROJECT_STATE

Last updated: 2026-02-19

## Current Focus
Track 1 (scholarly survey publication standard).

## Current Status
Split architecture completed:
1. Survey draft created.
2. Novel-work research spec created.
3. HTML manuscript received a framing/clarity edit pass (survey scope, claim boundaries, pseudo-code labeling, and citation typo fixes).
4. Appendix C rewritten to report source-attributed benchmark evidence only, with explicit evidence boundaries.
5. Unsourced quantitative comparative table removed and replaced with qualitative non-benchmark analysis.
6. Survey methodology section added (RQs, search strategy, inclusion/exclusion, extraction protocol).
7. Appendix D/E added as publication artifacts (selection-flow counts + exclusion ledger + row-level extraction matrix).
8. Frozen core-corpus selection run completed with fixed counts and exclusion ledger (`TOT-HF-SURVEY-2026-02-19`).
9. Appendix E expanded to full row-level extraction for all 22 included records.
10. First-pass citation hardening completed for key factual sections (intro/background/frameworks/threats/appendices).
11. API-facing smolagents snippets updated to doc-aligned patterns (model class, tools, executor configuration, and error-handling examples).
12. Added publication artifacts: `CLAIM_EVIDENCE_AUDIT.md` and `SUBMISSION_PACKAGE_CHECKLIST.md`.
13. Completed final claim-to-citation sweep across Sections 0-7; remaining uncited narrative text is explicitly framed as synthesis, hypothesis, or pseudo-code context.
14. Performed format-quality cleanup pass in main HTML manuscript:
   - removed duplicated pre-abstract lead paragraphs,
   - added keywords line,
   - replaced `TBD` placeholders in illustrative case study text with explicit non-estimation wording.
15. Generated journal-friendly Word export:
   - `/Users/quiznat/Desktop/Tree_of_Thought/submission/tot_hf_agents_survey_2026-02-19.docx`
16. Added arXiv conversion scaffold scripts/notes in `submission/` (execution pending local `pandoc` availability).
17. Updated front matter metadata for preprint readiness:
   - authors/affiliation block finalized,
   - version set to `v1.1 – Final pre-submission clean (19 February 2026)`,
   - submission date set to `TBD`,
   - arXiv categories set to `cs.AI` primary with `cs.CL` cross-list (`cs.LG` optional).
18. Completed tone-neutralization and scholarly-language hardening pass:
   - promotional wording normalized to neutral survey language,
   - subtitle softened to survey framing.
19. Added Section 0.3 PRISMA-style study-selection flow diagram (Mermaid) with frozen-run counts.
20. Added Section 0.4 reproducibility subsection with frozen protocol run ID and public repository URL.
21. Added Appendix F (Claim-Evidence Mapping) and Appendix G (Revision History).
22. Added inline citations to all Appendix C benchmark method rows.
23. Added explicit snippet labels across all code blocks (`Runnable` vs `Illustrative / pseudo-code`).
24. Reproducibility section now points to the configured public artifacts repository:
   - `https://github.com/quiznat/tot-hf-survey-artifacts`
25. GitHub remote configured and pushed:
   - repository now hosts the manuscript package as an alternate public paper endpoint.

## Next Action
Harden the manuscript to peer-review survey standards:
1. Populate and verify the public artifacts repository contents (screening log, extraction matrix, raw search exports, and counts manifest).
2. Complete arXiv-friendly source conversion (LaTeX or markdown-to-LaTeX pipeline).
3. Run final freeze checks (bibliography style normalization and submission bundle assembly).

## Active Blockers
1. `pandoc` not available locally for automated HTML -> LaTeX conversion.
2. Public artifact repository contents are not yet verified against Section 0.4 claims.

## Notes for Next Session
1. Primary Track 1 source is now `/Users/quiznat/Desktop/Tree_of_Thought/Tree of Thoughts Meets Hugging Face Agents — ClaudDib.html`.
2. Use `/Users/quiznat/Desktop/Tree_of_Thought/drafts/tot_hf_agents_novel_work_spec.md` as Track 2 source plan.
3. Keep Track 2 in planning mode until benchmark harness starts.
