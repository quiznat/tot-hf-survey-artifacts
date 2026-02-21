# Failure Taxonomy

Total failures summarized: 232
Condition filter: baseline-single-path, baseline-react, tot-prototype
Task filter: linear2-demo
Provider filter: huggingface-inference

| Bucket | Count | Conditions | Sample Run IDs |
|---|---:|---|---|
| format_or_notation_mismatch | 80 | baseline-single-path, tot-prototype | TOT-PROTOTYPE-20260221-193008-d65c90, TOT-PROTOTYPE-20260221-193226-3454b9, TOT-PROTOTYPE-20260221-193459-44a7f2, TOT-PROTOTYPE-20260221-193607-022e1e, BASELINE-SINGLE-PATH-20260221-193651-77d28f |
| other_failure | 74 | baseline-react, baseline-single-path | BASELINE-SINGLE-PATH-20260221-192850-9b7e16, BASELINE-SINGLE-PATH-20260221-192850-da868f, BASELINE-SINGLE-PATH-20260221-192851-05a814, BASELINE-SINGLE-PATH-20260221-192851-15011d, BASELINE-SINGLE-PATH-20260221-192851-ba7692 |
| depth_limit_no_solution | 70 | tot-prototype | TOT-PROTOTYPE-20260221-193023-883e8f, TOT-PROTOTYPE-20260221-193032-9bdd05, TOT-PROTOTYPE-20260221-193041-362dae, TOT-PROTOTYPE-20260221-193044-5fdbfc, TOT-PROTOTYPE-20260221-193058-c09a62 |
| search_empty_frontier | 8 | tot-prototype | TOT-PROTOTYPE-20260221-192640-e5f77e, TOT-PROTOTYPE-20260221-192720-85f568, TOT-PROTOTYPE-20260221-192752-c0c1a5, TOT-PROTOTYPE-20260221-192818-c254ee, TOT-PROTOTYPE-20260221-192819-3326c2 |

## Notes
- Buckets are heuristic and intended for iterative debugging guidance.
- Keep all failed runs archived; taxonomy should evolve with evaluator/prompt updates.
