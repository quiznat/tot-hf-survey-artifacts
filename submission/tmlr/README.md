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

## Submission Metadata and Policy Docs
- `submission/tmlr/TMLR_SUBMISSION_CHECKLIST.md`
- `submission/tmlr/OPENREVIEW_METADATA_TEMPLATE.md`
- `submission/tmlr/OPENREVIEW_ACCOUNT_SETUP.md`
- `submission/tmlr/AI_USE_DISCLOSURE_TMLR.md`

## Important Constraint
TMLR requires use of the official LaTeX stylefile/template for final submission formatting. The anonymous preflight build here is intended to accelerate review-readiness checks and anonymization, but final upload should still pass through the official template workflow.
