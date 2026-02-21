# Structured Lockset Report

Generated UTC: 2026-02-21T19:59:16Z
Task ID: digit-permutation-demo
Panel ID: digit-permutation-lockset-v1
Provider: hf
Model: Qwen/Qwen2.5-Coder-32B-Instruct
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
| baseline-react | 50 | 39 | 0.780 | [0.648, 0.872] | 9059.8 | 749.7 | 352.0 |
| baseline-single-path | 50 | 0 | 0.000 | [0.000, 0.071] | 3014.2 | 28.0 | 113.9 |
| tot-prototype | 50 | 33 | 0.660 | [0.522, 0.776] | 10124.4 | 1251.1 | 225.8 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | baseline-single-path | 50 | 39 | 0 | 11 | 0.780 | [0.660, 0.880] | 3.64e-12 | 1.09e-11 |
| baseline-react | tot-prototype | 50 | 15 | 9 | 26 | 0.120 | [-0.080, 0.300] | 0.307456 | 0.307456 |
| baseline-single-path | tot-prototype | 50 | 0 | 33 | 17 | -0.660 | [-0.780, -0.520] | 2.33e-10 | 4.66e-10 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
