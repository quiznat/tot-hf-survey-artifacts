# Failure Taxonomy

Total failures summarized: 165
Condition filter: baseline-single-path, baseline-react, tot-prototype
Task filter: subset-sum-demo
Provider filter: huggingface-inference

| Bucket | Count | Conditions | Sample Run IDs |
|---|---:|---|---|
| other_failure | 126 | baseline-react, baseline-single-path | BASELINE-REACT-20260221-191741-f7002b, BASELINE-REACT-20260221-191742-39274b, BASELINE-REACT-20260221-191742-c01102, BASELINE-REACT-20260221-191748-c7c4bc, BASELINE-REACT-20260221-191750-f6a75f |
| depth_limit_no_solution | 36 | tot-prototype | TOT-PROTOTYPE-20260221-191834-454dc7, TOT-PROTOTYPE-20260221-191840-6955f4, TOT-PROTOTYPE-20260221-191858-6c7901, TOT-PROTOTYPE-20260221-191910-b88b16, TOT-PROTOTYPE-20260221-191913-d1230a |
| search_empty_frontier | 3 | tot-prototype | TOT-PROTOTYPE-20260221-192429-efd1d6, TOT-PROTOTYPE-20260221-192443-ded68d, TOT-PROTOTYPE-20260221-192445-58bd1b |

## Notes
- Buckets are heuristic and intended for iterative debugging guidance.
- Keep all failed runs archived; taxonomy should evolve with evaluator/prompt updates.
