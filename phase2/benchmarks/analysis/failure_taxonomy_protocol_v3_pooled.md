# Failure Taxonomy

Total failures summarized: 943
Condition filter: baseline-single-path, baseline-react, tot-prototype
Task filter: none
Provider filter: huggingface-inference

| Bucket | Count | Conditions | Sample Run IDs |
|---|---:|---|---|
| other_failure | 443 | baseline-react, baseline-single-path | BASELINE-REACT-20260221-194853-88da9c, BASELINE-REACT-20260221-195222-b7cc5d, BASELINE-SINGLE-PATH-20260221-194847-eb26f2, BASELINE-SINGLE-PATH-20260221-194848-4a23c6, BASELINE-SINGLE-PATH-20260221-194848-64c64c |
| format_or_notation_mismatch | 240 | baseline-single-path, tot-prototype | BASELINE-SINGLE-PATH-20260221-195644-0cf86e, BASELINE-SINGLE-PATH-20260221-195644-2c94b5, BASELINE-SINGLE-PATH-20260221-195644-474b06, BASELINE-SINGLE-PATH-20260221-195644-6b7c8a, BASELINE-SINGLE-PATH-20260221-195644-9a804e |
| depth_limit_no_solution | 205 | tot-prototype | TOT-PROTOTYPE-20260221-194955-facf86, TOT-PROTOTYPE-20260221-195023-ab9d4d, TOT-PROTOTYPE-20260221-195024-b07894, TOT-PROTOTYPE-20260221-195029-b809c2, TOT-PROTOTYPE-20260221-195030-33e02b |
| unsafe_expression_filtered | 38 | baseline-react | BASELINE-REACT-20260221-190710-3c7ff3, BASELINE-REACT-20260221-190717-69a6da, BASELINE-REACT-20260221-190717-780519, BASELINE-REACT-20260221-190717-fb09b5, BASELINE-REACT-20260221-190722-34634a |
| search_empty_frontier | 17 | tot-prototype | TOT-PROTOTYPE-20260221-195659-929374, TOT-PROTOTYPE-20260221-195759-b30e52, TOT-PROTOTYPE-20260221-195901-1c12a8, TOT-PROTOTYPE-20260221-195906-b5cc8c, TOT-PROTOTYPE-20260221-195916-34995b |

## Notes
- Buckets are heuristic and intended for iterative debugging guidance.
- Keep all failed runs archived; taxonomy should evolve with evaluator/prompt updates.
