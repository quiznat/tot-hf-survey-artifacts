# Structured Lockset Report

Generated UTC: 2026-02-22T18:14:50Z
Task ID: digit-permutation-demo
Panel ID: digit-permutation-lockset-v4
Provider: hf
Model: Qwen/Qwen2.5-Coder-32B-Instruct
ToT evaluator mode: model_self_eval
ToT search settings: depth=3, branch_factor=3, frontier_width=3
Seed policy: item_hash
HF temperature: 0.0
HF top-p: 1.0
Capability parity policy: equalize_react_to_tot
Task tools available: best_divisible, is_divisible
Condition tools exposed: react=[none]; single=[none]; tot=[none]
Items evaluated: 50
Runs executed: 150
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-react | 50 | 31 | 0.620 | [0.482, 0.741] | 11745.0 | 960.7 | 405.4 |
| baseline-single-path | 50 | 0 | 0.000 | [0.000, 0.071] | 3091.8 | 28.0 | 112.0 |
| tot-prototype | 50 | 44 | 0.880 | [0.762, 0.944] | 3177.7 | 433.8 | 14.7 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | baseline-single-path | 50 | 31 | 0 | 19 | 0.620 | [0.480, 0.760] | 9.31e-10 | 1.86e-09 |
| baseline-react | tot-prototype | 50 | 5 | 18 | 27 | -0.260 | [-0.420, -0.080] | 0.010622 | 0.010622 |
| baseline-single-path | tot-prototype | 50 | 0 | 44 | 6 | -0.880 | [-0.960, -0.780] | 1.14e-13 | 3.41e-13 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
