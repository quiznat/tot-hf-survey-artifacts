# Submission Package

This directory contains manuscript export assets and conversion scripts used for archival submission workflows.

## Primary Outputs
- [`paper-v1.1.docx`](paper-v1.1.docx): Word-format manuscript export.
- [`arxiv/main.tex`](arxiv/main.tex): generated LaTeX source derived from `paper.html`.
- [`arxiv/main.pdf`](arxiv/main.pdf): rendered PDF compiled from `arxiv/main.tex`.

## Conversion Utilities
- [`convert_to_arxiv.sh`](convert_to_arxiv.sh): converts `paper.html` to LaTeX (`arxiv/main.tex`).
- [`build_llm_markdown.sh`](build_llm_markdown.sh): regenerates `tot-hf-agents-llm.md` from `paper.html`.
- [`ARXIV_CONVERSION_NOTES.md`](ARXIV_CONVERSION_NOTES.md): procedural notes and validation checklist.

## CI Build
`.github/workflows/build-arxiv-artifacts.yml` performs the same build path in GitHub Actions and uploads a bundled artifact (`arxiv-bundle.tgz`).

## Local Build Notes
- `pandoc` is required for HTML-to-LaTeX conversion.
- `latexmk` with XeLaTeX is recommended for Unicode-heavy manuscripts:
  - `latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex`
