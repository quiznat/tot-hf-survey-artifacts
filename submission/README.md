# Submission Package

This directory contains manuscript export assets and venue-specific submission workflows.

## Primary Outputs
- [`paper-v1.1.docx`](paper-v1.1.docx): Word-format manuscript export.
- [`arxiv/main.tex`](arxiv/main.tex): generated LaTeX source derived from `paper.html`.
- [`arxiv/main.pdf`](arxiv/main.pdf): rendered PDF compiled from `arxiv/main.tex`.

## arXiv Conversion Utilities
- [`convert_to_arxiv.sh`](convert_to_arxiv.sh): converts `paper.html` to LaTeX (`arxiv/main.tex`).
- [`build_llm_markdown.sh`](build_llm_markdown.sh): regenerates `tot-hf-agents-llm.md` from `paper.html`.
- [`ARXIV_CONVERSION_NOTES.md`](ARXIV_CONVERSION_NOTES.md): procedural notes and validation checklist.

## TMLR Submission Utilities
- [`build_tmlr_submission.sh`](build_tmlr_submission.sh): generates an anonymous double-blind package from `paper.html`.
- [`tmlr/`](tmlr/): TMLR checklist, OpenReview metadata template, disclosure draft, and anonymous build outputs.

## CI Workflows
- `.github/workflows/build-arxiv-artifacts.yml`: builds arXiv-oriented artifacts.
- `.github/workflows/build-tmlr-submission.yml`: builds and uploads anonymous TMLR submission artifacts.

## Local Build Notes
- `pandoc` is required for HTML-to-LaTeX/Markdown conversion.
- `latexmk` with XeLaTeX is recommended for Unicode-heavy manuscripts:
  - `latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex`
