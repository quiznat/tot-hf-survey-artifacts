# Structured Lockset Report

Generated UTC: 2026-02-21T19:36:47Z
Task ID: linear2-demo
Panel ID: linear2-lockset-v1
Provider: hf
Model: Qwen/Qwen2.5-72B-Instruct
ToT evaluator mode: model_self_eval
ToT search settings: depth=3, branch_factor=3, frontier_width=3
Seed policy: item_hash
HF temperature: 0.0
HF top-p: 1.0
Items evaluated: 50
Runs executed: 150
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-react | 50 | 50 | 1.000 | [0.929, 1.000] | 5685.5 | 147.5 | 72.1 |
| baseline-single-path | 50 | 18 | 0.360 | [0.241, 0.499] | 1285.6 | 30.0 | 4.5 |
| tot-prototype | 50 | 19 | 0.380 | [0.259, 0.518] | 64887.9 | 1666.6 | 895.9 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | baseline-single-path | 50 | 32 | 0 | 18 | 0.640 | [0.500, 0.780] | 4.66e-10 | 1.40e-09 |
| baseline-react | tot-prototype | 50 | 31 | 0 | 19 | 0.620 | [0.480, 0.760] | 9.31e-10 | 1.86e-09 |
| baseline-single-path | tot-prototype | 50 | 3 | 4 | 43 | -0.020 | [-0.120, 0.080] | 1.000000 | 1.000000 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
