# Evaluation v1 Metrics Summary

Total runs summarized: 20
Condition filter: baseline-single-path, baseline-react, tot-prototype
Task filter: game24-demo
Provider filter: huggingface-inference

| Condition | Runs | Success Rate | Latency Mean (ms) | Latency Std (ms) | Tokens In Mean | Tokens Out Mean | Cost Mean (USD) |
|---|---:|---:|---:|---:|---:|---:|---:|
| baseline-react | 5 | 0.200 | 22835.400 | 9292.743 | 965.600 | 334.000 | 0.00000000 |
| baseline-single-path | 7 | 0.000 | 4182.000 | 5321.020 | 21.000 | 7.857 | 0.00000000 |
| tot-prototype | 8 | 0.250 | 39767.125 | 17729.089 | 340.000 | 147.750 | 0.00000000 |

## Notes
- This table is generated from run manifests only.
- Include both successes and failures to avoid survivorship bias.
