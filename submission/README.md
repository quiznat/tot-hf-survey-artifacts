# Submission Artifact Manifest

Date: 2026-02-19  
Source manuscript: `/Users/quiznat/Desktop/Tree_of_Thought/Tree of Thoughts Meets Hugging Face Agents — ClaudDib.html`

## Generated Artifacts
- Journal-friendly Word export:
  - `/Users/quiznat/Desktop/Tree_of_Thought/submission/tot_hf_agents_survey_2026-02-19.docx`
- arXiv conversion scaffolding:
  - `/Users/quiznat/Desktop/Tree_of_Thought/submission/convert_to_arxiv.sh`
  - `/Users/quiznat/Desktop/Tree_of_Thought/submission/ARXIV_CONVERSION_NOTES.md`
- Manuscript hardening features now included in source HTML:
  - Section 0.3 study-selection flow diagram (Mermaid),
  - Section 0.4 reproducibility subsection (frozen run ID),
  - Appendix F claim-evidence mapping,
  - Appendix G revision history,
  - version metadata set to `v1.1` with submission date `TBD`.

## Remaining Conversion Work
1. arXiv-preferred source format export (LaTeX or clean Markdown-to-LaTeX pipeline).
2. Publish/verify reproducibility artifact files in `https://github.com/quiznat/tot-hf-survey-artifacts`.
3. Bibliography style normalization for target venue template.

## Notes
- Word export was generated with `textutil -convert docx`.
- `pandoc` is not currently available in this environment, so direct HTML -> LaTeX conversion is pending tool availability.
