# Structured Lockset Report

Generated UTC: 2026-02-22T18:13:22Z
Task ID: digit-permutation-demo
Panel ID: digit-permutation-lockset-v4
Provider: hf
Model: Qwen/Qwen2.5-72B-Instruct
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
| baseline-react | 50 | 26 | 0.520 | [0.385, 0.652] | 19332.3 | 717.9 | 351.1 |
| baseline-single-path | 50 | 20 | 0.400 | [0.276, 0.538] | 938.5 | 28.0 | 1.0 |
| tot-prototype | 50 | 49 | 0.980 | [0.895, 0.996] | 17395.6 | 531.1 | 234.1 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | baseline-single-path | 50 | 15 | 9 | 26 | 0.120 | [-0.060, 0.300] | 0.307456 | 0.307456 |
| baseline-react | tot-prototype | 50 | 1 | 24 | 25 | -0.460 | [-0.600, -0.300] | 1.55e-06 | 3.10e-06 |
| baseline-single-path | tot-prototype | 50 | 0 | 29 | 21 | -0.580 | [-0.720, -0.440] | 3.73e-09 | 1.12e-08 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
