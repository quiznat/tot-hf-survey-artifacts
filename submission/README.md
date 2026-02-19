# Submission Files

## Available outputs
- [`paper-v1.1.docx`](paper-v1.1.docx): journal-friendly Word export.

## arXiv conversion helper
- [`convert_to_arxiv.sh`](convert_to_arxiv.sh)
- [`ARXIV_CONVERSION_NOTES.md`](ARXIV_CONVERSION_NOTES.md)
- [`build_llm_markdown.sh`](build_llm_markdown.sh)

The conversion helper expects `pandoc` to be installed locally.

CI alternative:
- The GitHub Actions workflow `build-arxiv-artifacts.yml` generates `main.tex`, compiles `main.pdf`, generates `tot-hf-agents-llm.md`, and uploads an `arxiv-bundle.tgz` artifact on `main` pushes.
