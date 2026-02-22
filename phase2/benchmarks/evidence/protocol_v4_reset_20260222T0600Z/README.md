# Protocol v4 Reset and Inference Quarantine

- Snapshot ID: `protocol_v4_reset_20260222T0600Z`
- Effective UTC: `2026-02-22T06:00:00Z`
- Decision: all pre-v4 Phase 2 runs are retained for engineering diagnostics only and excluded from confirmatory inference.

## Quarantine Rule
All Phase 2 evidence generated before protocol-v4 is classified as:
- `exploratory_invalid_for_primary_claim`

This includes legacy root-level manifests and the following run series:
- `protocol_v2_locked`
- `protocol_v2_locked_ablations`
- `protocol_v2_locked_search_ablations`
- `protocol_v3_matrix`
- `protocol_v31_diagnostic`
- `protocol_v31_smoke_patch1`
- `protocol_v32_diagnostic`
- `tmp_capability_equalized`
- `tmp_capability_equalized_game24`

## Allowed Use
- engineering diagnostics
- implementation debugging
- failure taxonomy development
- exploratory hypothesis generation

## Disallowed Use
- primary effect-size reporting
- confirmatory p-value tables
- final manuscript claims framed as confirmatory evidence

## Forward Rule
Only protocol-v4 series labeled `confirmatory_primary` in `phase2/benchmarks/evidence/series_registry.json` may feed final effect-size and inferential tables.
