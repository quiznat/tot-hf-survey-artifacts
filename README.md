# Tree of Thoughts Meets Hugging Face Agents

**Subtitle:** A Survey of Tree of Thoughts and Hugging Face Agent Frameworks

This repository contains the canonical manuscript and reproducibility materials for a scholarly survey on Tree of Thoughts (ToT) reasoning and Hugging Face agent frameworks.

## Manuscript (Canonical HTML)
- [https://quiznat.github.io/tot-hf-survey-artifacts/paper.html](https://quiznat.github.io/tot-hf-survey-artifacts/paper.html)

## Version and Status
- Version: `v1.1 – Final pre-submission clean (19 February 2026)`
- Status: `submission preparation`

## Scope
- Systematic survey of ToT methodology and agent framework design patterns.
- Comparative synthesis of architectural choices, execution models, and evaluation practices.
- Explicit separation of evidence-backed findings from illustrative examples.

## Reproducibility and Evidence
- Frozen protocol run ID: `TOT-HF-SURVEY-2026-02-19`
- Artifact index: [`artifacts/`](artifacts/)
- Evidence scaffold: [`artifacts/Paper Inception/`](artifacts/Paper%20Inception/)
- Claim-evidence index: [`artifacts/Paper Inception/EVIDENCE_INDEX.md`](artifacts/Paper%20Inception/EVIDENCE_INDEX.md)

## Build and Release
- Workflow: `.github/workflows/publish-site.yml` publishes the HTML manuscript and assets to GitHub Pages.
- Workflow: `.github/workflows/build-arxiv-artifacts.yml` generates submission artifacts (`main.tex`, `main.pdf`, `tot-hf-agents-llm.md`, `arxiv-bundle.tgz`).

## Repository Structure
- `paper.html`: canonical survey manuscript source.
- `assets/`: figures and static assets used in the manuscript.
- `artifacts/`: evidence bundles, validation records, and reproducibility documentation.
- `submission/`: export scripts and submission-focused build helpers.

## License
Released under the MIT License. Third-party referenced works remain under their original licenses and terms.
