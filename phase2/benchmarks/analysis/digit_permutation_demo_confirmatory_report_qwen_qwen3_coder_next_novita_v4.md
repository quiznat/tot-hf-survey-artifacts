# Structured Lockset Report

Generated UTC: 2026-02-22T18:10:11Z
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
Items evaluated: 50
Runs executed: 150
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-react | 50 | 44 | 0.880 | [0.762, 0.944] | 20455.0 | 506.0 | 259.1 |
| baseline-single-path | 50 | 8 | 0.160 | [0.083, 0.285] | 6974.3 | 28.0 | 89.3 |
| tot-prototype | 50 | 49 | 0.980 | [0.895, 0.996] | 30028.7 | 306.8 | 9.3 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | baseline-single-path | 50 | 37 | 1 | 12 | 0.720 | [0.580, 0.840] | 2.84e-10 | 5.68e-10 |
| baseline-react | tot-prototype | 50 | 1 | 6 | 43 | -0.100 | [-0.200, 0.000] | 0.125000 | 0.125000 |
| baseline-single-path | tot-prototype | 50 | 0 | 41 | 9 | -0.820 | [-0.920, -0.700] | 9.09e-13 | 2.73e-12 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
