# Failure Taxonomy

Total failures summarized: 253
Condition filter: tot-prototype
Task filter: digit-permutation-demo
Provider filter: none

| Bucket | Count | Conditions | Sample Run IDs |
|---|---:|---|---|
| depth_limit_no_solution | 235 | tot-prototype | TOT-PROTOTYPE-20260222-040617-5dbc6d, TOT-PROTOTYPE-20260222-040617-ff0acd, TOT-PROTOTYPE-20260222-040638-40e45a, TOT-PROTOTYPE-20260222-040640-005599, TOT-PROTOTYPE-20260222-040701-ad2b1e |
| search_empty_frontier | 11 | tot-prototype | TOT-PROTOTYPE-20260222-041438-3348de, TOT-PROTOTYPE-20260222-041936-a35f5d, TOT-PROTOTYPE-20260222-042014-5d9d8e, TOT-PROTOTYPE-20260222-042014-a6f483, TOT-PROTOTYPE-20260222-042103-262344 |
| format_or_notation_mismatch | 7 | tot-prototype | TOT-PROTOTYPE-20260222-041825-679e66, TOT-PROTOTYPE-20260222-041858-3b3cf6, TOT-PROTOTYPE-20260222-041903-887581, TOT-PROTOTYPE-20260222-042126-890510, TOT-PROTOTYPE-20260222-042207-61c15e |

## Notes
- Buckets are heuristic and intended for iterative debugging guidance.
- Keep all failed runs archived; taxonomy should evolve with evaluator/prompt updates.
