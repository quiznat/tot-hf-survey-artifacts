# Structured Lockset Report

Generated UTC: 2026-02-22T17:15:58Z
Task ID: digit-permutation-demo
Panel ID: digit-permutation-lockset-v4
Provider: hf
Model: Qwen/Qwen3-Coder-Next:novita
ToT evaluator mode: model_self_eval
ToT search settings: depth=3, branch_factor=3, frontier_width=3
Seed policy: item_hash
HF temperature: 0.0
HF top-p: 1.0
Capability parity policy: equalize_react_to_tot
Task tools available: best_divisible, is_divisible
Condition tools exposed: react=[none]; single=[none]; tot=[none]
Items evaluated: 10
Runs executed: 30
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-react | 10 | 8 | 0.800 | [0.490, 0.943] | 17301.5 | 654.4 | 279.8 |
| baseline-single-path | 10 | 1 | 0.100 | [0.018, 0.404] | 3657.9 | 28.0 | 105.9 |
| tot-prototype | 10 | 10 | 1.000 | [0.722, 1.000] | 10309.8 | 179.3 | 5.8 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | baseline-single-path | 10 | 7 | 0 | 3 | 0.700 | [0.400, 1.000] | 0.015625 | 0.031250 |
| baseline-react | tot-prototype | 10 | 0 | 2 | 8 | -0.200 | [-0.500, 0.000] | 0.500000 | 0.500000 |
| baseline-single-path | tot-prototype | 10 | 0 | 9 | 1 | -0.900 | [-1.000, -0.700] | 0.003906 | 0.011719 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
