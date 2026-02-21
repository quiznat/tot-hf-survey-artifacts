# Forensics Ingest Checklist

Use this checklist to register and validate a newly collected forensic bundle.

## Source Bundle Metadata
- Bundle absolute path:
- Collection start (UTC):
- Collection end (UTC):
- Collector identity:
- Hostname:
- SHA256 manifest path:

## Required Components
- `reports/EVIDENCE_SUMMARY.md`
- `reports/chain_of_custody.md`
- `reports/claim_evidence_matrix.csv`
- `raw_logs/`
- `configs/`
- `timelines/`
- `manifests/`
- `screenshots/` (including TUI capture when applicable)

## Validation Controls
- Confirm timestamps are UTC or explicitly normalized.
- Confirm each manuscript claim has at least one evidence pointer.
- Confirm secret material has been redacted.
- Confirm referenced files match manifest hashes.

## Import Record
- Imported by:
- Imported at (UTC):
- Imported commit:
- Notes:
