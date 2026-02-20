# Failure Taxonomy

Total failures summarized: 17
Condition filter: baseline-single-path, baseline-react, tot-prototype
Task filter: game24-demo
Provider filter: huggingface-inference

| Bucket | Count | Conditions | Sample Run IDs |
|---|---:|---|---|
| format_or_notation_mismatch | 9 | baseline-single-path, tot-prototype | BASELINE-SINGLE-PATH-20260220-025629-9649ee, BASELINE-SINGLE-PATH-20260220-030606-f5cac5, BASELINE-SINGLE-PATH-20260220-031315-12f4c5, BASELINE-SINGLE-PATH-20260220-031350-0e9956, BASELINE-SINGLE-PATH-20260220-031416-5a3ac6 |
| other_failure | 4 | baseline-react | BASELINE-REACT-20260220-031349-d8e4f3, BASELINE-REACT-20260220-031403-dbefeb, BASELINE-REACT-20260220-031456-a47550, BASELINE-REACT-20260220-031520-fa6cac |
| depth_limit_no_solution | 4 | tot-prototype | TOT-PROTOTYPE-20260220-031623-d6e4bf, TOT-PROTOTYPE-20260220-031728-850d3c, TOT-PROTOTYPE-20260220-032050-01e6cb, TOT-PROTOTYPE-20260220-032458-010964 |

## Notes
- Buckets are heuristic and intended for iterative debugging guidance.
- Keep all failed runs archived; taxonomy should evolve with evaluator/prompt updates.
