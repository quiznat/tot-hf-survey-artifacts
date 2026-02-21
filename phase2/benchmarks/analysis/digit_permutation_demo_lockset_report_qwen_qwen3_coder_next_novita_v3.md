# Structured Lockset Report

Generated UTC: 2026-02-21T20:01:09Z
Task ID: digit-permutation-demo
Panel ID: digit-permutation-lockset-v1
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
| baseline-react | 50 | 49 | 0.980 | [0.895, 0.996] | 3579.4 | 241.8 | 180.3 |
| baseline-single-path | 50 | 3 | 0.060 | [0.021, 0.162] | 1960.2 | 28.0 | 101.0 |
| tot-prototype | 50 | 36 | 0.720 | [0.583, 0.825] | 11055.2 | 1007.7 | 74.7 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | baseline-single-path | 50 | 47 | 1 | 2 | 0.920 | [0.820, 1.000] | 3.48e-13 | 1.04e-12 |
| baseline-react | tot-prototype | 50 | 14 | 1 | 35 | 0.260 | [0.120, 0.400] | 0.000977 | 0.000977 |
| baseline-single-path | tot-prototype | 50 | 0 | 33 | 17 | -0.660 | [-0.780, -0.520] | 2.33e-10 | 4.66e-10 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
