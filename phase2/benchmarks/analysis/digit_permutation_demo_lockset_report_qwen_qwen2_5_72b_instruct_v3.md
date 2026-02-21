# Structured Lockset Report

Generated UTC: 2026-02-21T19:56:34Z
Task ID: digit-permutation-demo
Panel ID: digit-permutation-lockset-v1
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
| baseline-react | 50 | 48 | 0.960 | [0.865, 0.989] | 6917.7 | 148.8 | 102.7 |
| baseline-single-path | 50 | 20 | 0.400 | [0.276, 0.538] | 964.5 | 28.0 | 1.0 |
| tot-prototype | 50 | 24 | 0.480 | [0.348, 0.615] | 56404.9 | 1377.2 | 824.3 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | baseline-single-path | 50 | 28 | 0 | 22 | 0.560 | [0.420, 0.700] | 7.45e-09 | 2.24e-08 |
| baseline-react | tot-prototype | 50 | 25 | 1 | 24 | 0.480 | [0.340, 0.620] | 8.05e-07 | 1.61e-06 |
| baseline-single-path | tot-prototype | 50 | 2 | 6 | 42 | -0.080 | [-0.180, 0.020] | 0.289062 | 0.289062 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
