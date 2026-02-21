# Structured Lockset Report

Generated UTC: 2026-02-21T20:01:07Z
Task ID: game24-demo
Panel ID: game24-lockset-v1
Provider: hf
Model: Qwen/Qwen3-Coder-Next:novita
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
| baseline-react | 50 | 20 | 0.400 | [0.276, 0.538] | 7794.5 | 822.7 | 353.0 |
| baseline-single-path | 50 | 3 | 0.060 | [0.021, 0.162] | 1219.9 | 21.0 | 20.7 |
| tot-prototype | 50 | 44 | 0.880 | [0.762, 0.944] | 9661.7 | 780.9 | 85.4 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | baseline-single-path | 50 | 19 | 2 | 29 | 0.340 | [0.180, 0.480] | 0.000221 | 0.000221 |
| baseline-react | tot-prototype | 50 | 0 | 24 | 26 | -0.480 | [-0.620, -0.340] | 1.19e-07 | 2.38e-07 |
| baseline-single-path | tot-prototype | 50 | 0 | 41 | 9 | -0.820 | [-0.920, -0.700] | 9.09e-13 | 2.73e-12 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
