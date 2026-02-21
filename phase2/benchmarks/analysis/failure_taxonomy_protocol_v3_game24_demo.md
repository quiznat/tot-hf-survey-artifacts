# Failure Taxonomy

Total failures summarized: 293
Condition filter: baseline-single-path, baseline-react, tot-prototype
Task filter: game24-demo
Provider filter: huggingface-inference

| Bucket | Count | Conditions | Sample Run IDs |
|---|---:|---|---|
| other_failure | 126 | baseline-react, baseline-single-path | BASELINE-REACT-20260221-190706-7e0eaf, BASELINE-REACT-20260221-190708-1dc753, BASELINE-REACT-20260221-190744-6c0e83, BASELINE-REACT-20260221-190821-e63a53, BASELINE-REACT-20260221-190848-40f50d |
| format_or_notation_mismatch | 92 | baseline-single-path, tot-prototype | BASELINE-SINGLE-PATH-20260221-190702-62e69c, BASELINE-SINGLE-PATH-20260221-190900-fdb54b, BASELINE-SINGLE-PATH-20260221-191005-752a77, BASELINE-SINGLE-PATH-20260221-191209-34868d, BASELINE-SINGLE-PATH-20260221-191209-6c2bd6 |
| unsafe_expression_filtered | 38 | baseline-react | BASELINE-REACT-20260221-190710-3c7ff3, BASELINE-REACT-20260221-190717-69a6da, BASELINE-REACT-20260221-190717-780519, BASELINE-REACT-20260221-190717-fb09b5, BASELINE-REACT-20260221-190722-34634a |
| depth_limit_no_solution | 37 | tot-prototype | TOT-PROTOTYPE-20260221-190748-521446, TOT-PROTOTYPE-20260221-190755-ba8e48, TOT-PROTOTYPE-20260221-190814-00353a, TOT-PROTOTYPE-20260221-190816-2b6019, TOT-PROTOTYPE-20260221-190842-016161 |

## Notes
- Buckets are heuristic and intended for iterative debugging guidance.
- Keep all failed runs archived; taxonomy should evolve with evaluator/prompt updates.
