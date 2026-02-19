# arXiv Conversion Notes

## Goal
Produce arXiv source output (`main.tex`) from the canonical HTML manuscript.

## Canonical Source
- `../paper.html`

## Script
- `./convert_to_arxiv.sh`

## Requirements
1. `pandoc` installed locally.

## Run
```bash
bash submission/convert_to_arxiv.sh
```

## Output
- `./arxiv/main.tex`

## Post-Conversion Checklist
1. Verify figure paths and captions in generated LaTeX.
2. Confirm citation rendering and reference formatting.
3. Normalize title/author/abstract metadata to arXiv template expectations.
