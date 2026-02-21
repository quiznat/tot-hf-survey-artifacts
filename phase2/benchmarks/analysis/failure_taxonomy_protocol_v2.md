# Failure Taxonomy

Total failures summarized: 202
Condition filter: baseline-single-path, baseline-react, tot-prototype
Task filter: none
Provider filter: huggingface-inference

| Bucket | Count | Conditions | Sample Run IDs |
|---|---:|---|---|
| format_or_notation_mismatch | 109 | baseline-single-path, tot-prototype | BASELINE-SINGLE-PATH-20260220-025629-9649ee, BASELINE-SINGLE-PATH-20260220-030606-f5cac5, BASELINE-SINGLE-PATH-20260220-031315-12f4c5, BASELINE-SINGLE-PATH-20260220-031350-0e9956, BASELINE-SINGLE-PATH-20260220-031416-5a3ac6 |
| other_failure | 66 | baseline-react, baseline-single-path | BASELINE-REACT-20260220-031349-d8e4f3, BASELINE-REACT-20260220-031403-dbefeb, BASELINE-REACT-20260220-031456-a47550, BASELINE-REACT-20260220-031520-fa6cac, BASELINE-REACT-20260220-040630-ecc0e0 |
| depth_limit_no_solution | 24 | tot-prototype | TOT-PROTOTYPE-20260220-031623-d6e4bf, TOT-PROTOTYPE-20260220-031728-850d3c, TOT-PROTOTYPE-20260220-032050-01e6cb, TOT-PROTOTYPE-20260220-032458-010964, TOT-PROTOTYPE-20260220-040601-dcd520 |
| invalid_candidate_retained | 2 | tot-prototype | TOT-PROTOTYPE-20260220-042347-3a7853, TOT-PROTOTYPE-20260220-045553-fc6491 |
| unsafe_expression_filtered | 1 | baseline-react | BASELINE-REACT-20260220-174449-71aca4 |

## Notes
- Buckets are heuristic and intended for iterative debugging guidance.
- Keep all failed runs archived; taxonomy should evolve with evaluator/prompt updates.
