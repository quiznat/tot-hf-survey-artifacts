# arXiv Conversion Notes

## Objective
Generate archival LaTeX submission material from the canonical HTML manuscript.

## Canonical Input
- `../paper.html`

## Conversion Script
- `./convert_to_arxiv.sh`

## Requirements
1. `pandoc`

## Procedure
```bash
bash submission/convert_to_arxiv.sh
```

## Output
- `./arxiv/main.tex`

## Validation Checklist
1. Verify all figure paths resolve from `submission/arxiv/`.
2. Verify citation formatting and bibliography rendering.
3. Verify author/title/abstract metadata satisfy target venue requirements.
4. Compile PDF with XeLaTeX and confirm no fatal font or Unicode errors.
