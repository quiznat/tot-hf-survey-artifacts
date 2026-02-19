# TMLR Submission Package

This directory contains the venue-specific assets and workflow for a TMLR submission based on the canonical manuscript.

## Scope
- Prepare a double-blind anonymous preflight variant from `paper.html`.
- Generate synchronized Markdown/LaTeX derivatives for reviewer-facing upload checks.
- Provide metadata/disclosure/checklist templates for OpenReview submission.

## Build Command
```bash
bash submission/build_tmlr_submission.sh
```

## Outputs
- `submission/tmlr/anonymous/paper-anonymous.html`
- `submission/tmlr/anonymous/paper-anonymous.md`
- `submission/tmlr/anonymous/main.tex`
- `submission/tmlr/anonymous/main.pdf` (if `latexmk` is available)
- `submission/tmlr/tmlr-submission-anonymous.tgz`
- `submission/tmlr/official-anonymous/main-tmlr.tex` (if `tmlr.sty` is available)
- `submission/tmlr/official-anonymous/main-tmlr.pdf` (if `tmlr.sty` + `latexmk` are available)

## Submission Metadata and Policy Docs
- `submission/tmlr/TMLR_SUBMISSION_CHECKLIST.md`
- `submission/tmlr/OPENREVIEW_METADATA_TEMPLATE.md`
- `submission/tmlr/OPENREVIEW_ACCOUNT_SETUP.md`
- `submission/tmlr/AI_USE_DISCLOSURE_TMLR.md`
- `submission/tmlr/SUPPLEMENT_STRATEGY.md`
- `submission/tmlr/REVIEWER_SUGGESTION_GUIDE.md`

## Important Constraint
TMLR requires use of the official LaTeX stylefile/template for final submission formatting. This build supports:
- preflight anonymous conversion from `paper.html`, and
- optional official-style compile when `submission/tmlr/template/tmlr.sty` is present.
