# Forensics Ingest Checklist

Use this after the VM evidence collector finishes.

## Source Bundle
- Bundle absolute path:
- Collection start UTC:
- Collection end UTC:
- Collector identity:
- Hostname:
- SHA256 manifest path:

## Required Inputs
- `reports/EVIDENCE_SUMMARY.md` present.
- `reports/chain_of_custody.md` present.
- `reports/claim_evidence_matrix.csv` present.
- Runtime/service logs present (`raw_logs/`).
- Config snapshots present (`configs/`).
- Timeline/git provenance present (`timelines/`).
- Web captures for leaderboard/profile present.
- Screenshot evidence present (`screenshots/`), including TUI capture.

## Validation
- Verify all timestamps are UTC or explicitly converted.
- Verify all claims in manuscript have at least one evidence pointer.
- Verify no secrets remain in copied logs/configs.
- Verify all referenced files exist and match manifest hashes.

## Import Record
- Imported by:
- Imported UTC:
- Imported commit:
- Notes:
