# Runnable Paper Roadmap

Goal: migrate all manuscript code listings to runnable, tested examples while preserving clear evidence boundaries.

## Success Criteria
- Every listing in `paper.html` is tagged `Runnable (tested)` and maps to a helper in `examples/paper_snippets/`.
- `tests/test_paper_snippets.py` covers each helper family with deterministic assertions.
- Pseudo-code is eliminated from main sections, or retained only with explicit de-scope rationale and an adjacent runnable equivalent.

## Phase A: High-ROI Conversions
Status: In progress

Scope:
- Convert narrative pseudo-code and walkthrough listings into deterministic runnable fixtures.
- Convert integration-pattern sketches into runnable stand-ins using local `CodeAgent` stubs.
- Convert basic ToT template snippets to tested helper classes.

Target blocks:
- Section 2 examples and formal ToT loop
- Section 3.4.1 JSON tool call
- Section 4.2.2, 4.3.1 text walkthrough, 4.3.3
- Section 4.4 case-study pseudo walkthroughs
- Section 5.1.2 basic ToT template
- Section 6.1.2, 6.1.3, 6.1.4
- Appendix B reference pseudo-code

Estimated effort:
- 6-10 hours including tests and manuscript updates.

## Phase B: Hardening and Reproducibility
Status: Pending

Scope:
- Add focused regression tests for edge cases in new ToT helpers.
- Validate snippet outputs against expected listing narratives.
- Add coverage report and snippet-to-test mapping table.

Estimated effort:
- 2-4 hours.

## Phase C: Pipeline Alignment
Status: Pending

Scope:
- Regenerate derivative formats (`tot-hf-agents-llm.md`, `submission/arxiv/main.tex`) and ensure code-language fidelity in conversion.
- Add CI guard that fails on unlabeled pseudo listings.

Estimated effort:
- 1-3 hours.

## Open Risks
- HTML-to-markdown/LaTeX conversion can strip language info when custom `<pre>` attributes are used.
- Fully runnable replacements should stay deterministic and avoid external network/API dependencies.
- Case-study conversion must remain clearly synthetic (not empirical claims).
