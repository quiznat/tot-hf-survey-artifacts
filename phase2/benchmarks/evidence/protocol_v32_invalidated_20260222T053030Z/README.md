# protocol_v32 invalidated (aborted)

- Series ID: `protocol_v32_diagnostic`
- Status: `invalidated`
- Aborted UTC: `2026-02-22T05:30:30Z`
- Trigger: user-requested abort after identifying method mismatch in linear2 evaluation fairness.

## Invalidation reason
ReAct baseline was tool-augmented while ToT remained tool-free candidate search on linear2-style tasks. This confounds interpretation of ToT-vs-ReAct deltas as a pure reasoning/search comparison.

## Exclusion rule
Do not use protocol-v32 outputs from this run as decision-grade comparative evidence.

## Frozen counts at abort
- Diagnostic reports (`*_v32.json`): `17`
- Manifest files under run tree: `1786`

## Notes
Artifacts remain in place for forensic reference only.
