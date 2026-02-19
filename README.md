# Tree of Thoughts Meets Hugging Face Agents

Public-facing repository for the survey manuscript and supporting reproducibility artifacts.

## Live paper site
- GitHub Pages URL (after Pages is enabled):  
  `https://quiznat.github.io/tot-hf-survey-artifacts/`

Repository view (`github.com/...`) shows files/README.  
Rendered paper hosting is the Pages URL above.

## Read the paper
- Web manuscript: [`paper.html`](paper.html)
- LLM-friendly Markdown (auto-generated in CI / Pages): [`tot-hf-agents-llm.md`](https://quiznat.github.io/tot-hf-survey-artifacts/tot-hf-agents-llm.md)
- Word export: [`submission/paper-v1.1.docx`](submission/paper-v1.1.docx)

## Automated publishing/build
- `.github/workflows/publish-site.yml`: deploys `index.html`, `paper.html`, and `assets/` to GitHub Pages.
- `.github/workflows/build-arxiv-artifacts.yml`: builds `submission/arxiv/main.tex`, compiles `submission/arxiv/main.pdf`, generates `tot-hf-agents-llm.md`, and uploads an `arxiv-bundle.tgz` artifact.

## One-time setup in GitHub
1. Open repository `Settings` -> `Pages`.
2. Set Source to `GitHub Actions`.
3. Push to `main` (or run workflow manually) to publish the site.

## Reproducibility anchor
- Frozen run ID: `TOT-HF-SURVEY-2026-02-19`
- Artifact index: [`artifacts/`](artifacts/)
- Evidence scaffold and validation docs: [`artifacts/Paper Inception/`](artifacts/Paper%20Inception/)
- Evidence index: [`artifacts/Paper Inception/EVIDENCE_INDEX.md`](artifacts/Paper%20Inception/EVIDENCE_INDEX.md)

## Repository layout
- `paper.html`: canonical survey manuscript (v1.1 pre-submission clean)
- `assets/`: diagrams and static assets used by the manuscript
- `artifacts/`: screening and reproducibility materials
- `submission/`: export and submission-conversion helpers

## License
This repository is released under the MIT License. Third-party publications and citation metadata remain under their original terms.
