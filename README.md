# Tree of Thoughts Meets Hugging Face Agents

Public-facing repository for the survey manuscript and supporting reproducibility artifacts.

## Live paper site
- GitHub Pages URL (after Pages is enabled):  
  `https://quiznat.github.io/tot-hf-survey-artifacts/`

Repository view (`github.com/...`) shows files/README.  
Rendered paper hosting is the Pages URL above.

## Read the paper
- Web manuscript: [`paper.html`](paper.html)
- Word export: [`submission/paper-v1.1.docx`](submission/paper-v1.1.docx)

## Automated publishing/build
- `.github/workflows/publish-site.yml`: deploys `index.html`, `paper.html`, and `assets/` to GitHub Pages.
- `.github/workflows/build-arxiv-artifacts.yml`: builds `submission/arxiv/main.tex` and uploads an `arxiv-bundle.tgz` artifact.

## One-time setup in GitHub
1. Open repository `Settings` -> `Pages`.
2. Set Source to `GitHub Actions`.
3. Push to `main` (or run workflow manually) to publish the site.

## Reproducibility anchor
- Frozen run ID: `TOT-HF-SURVEY-2026-02-19`
- Artifact index: [`artifacts/`](artifacts/)

## Repository layout
- `paper.html`: canonical survey manuscript (v1.1 pre-submission clean)
- `assets/`: diagrams and static assets used by the manuscript
- `artifacts/`: screening and reproducibility materials
- `submission/`: export and submission-conversion helpers

## License
This repository is released under the MIT License. Third-party publications and citation metadata remain under their original terms.
