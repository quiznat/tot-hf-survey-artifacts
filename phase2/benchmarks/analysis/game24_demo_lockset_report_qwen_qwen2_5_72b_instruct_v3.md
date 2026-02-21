# Structured Lockset Report

Generated UTC: 2026-02-21T19:12:08Z
Task ID: game24-demo
Panel ID: game24-lockset-v1
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
| baseline-react | 50 | 2 | 0.040 | [0.011, 0.135] | 13072.1 | 439.2 | 205.5 |
| baseline-single-path | 50 | 8 | 0.160 | [0.083, 0.285] | 1388.4 | 21.0 | 8.3 |
| tot-prototype | 50 | 33 | 0.660 | [0.522, 0.776] | 27282.9 | 1364.6 | 246.5 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | baseline-single-path | 50 | 2 | 8 | 40 | -0.120 | [-0.240, 0.000] | 0.109375 | 0.109375 |
| baseline-react | tot-prototype | 50 | 1 | 32 | 17 | -0.620 | [-0.760, -0.480] | 7.92e-09 | 2.37e-08 |
| baseline-single-path | tot-prototype | 50 | 0 | 25 | 25 | -0.500 | [-0.640, -0.360] | 5.96e-08 | 1.19e-07 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
