# Structured Lockset Report

Generated UTC: 2026-02-23T02:14:31Z
Task ID: digit-permutation-demo
Panel ID: digit-permutation-lockset-v4
Provider: hf
Model: Qwen/Qwen3-Coder-Next:novita
ToT evaluator mode: model_self_eval
ToT mode: model_decompose_search
ToT decomposition rounds: 1
ToT search settings: depth=3, branch_factor=3, frontier_width=3
Seed policy: item_hash
HF temperature: 0.0
HF top-p: 1.0
Capability parity policy: equalize_react_to_tot
Task tools available: best_divisible, is_divisible
Condition tools exposed: cot=[none]; cot_sc=[none]; react=[best_divisible, is_divisible]; single=[none]
Items evaluated: 10
Runs executed: 40
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-cot | 10 | 0 | 0.000 | [0.000, 0.278] | 10572.9 | 41.0 | 118.1 |
| baseline-cot-sc | 10 | 0 | 0.000 | [0.000, 0.278] | 37920.5 | 240.0 | 597.6 |
| baseline-react | 10 | 9 | 0.900 | [0.596, 0.982] | 13332.2 | 286.4 | 192.9 |
| baseline-single-path | 10 | 2 | 0.200 | [0.057, 0.510] | 9239.1 | 28.0 | 106.7 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-cot | baseline-cot-sc | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-cot | baseline-react | 10 | 0 | 9 | 1 | -0.900 | [-1.000, -0.700] | 0.003906 | 0.023438 |
| baseline-cot | baseline-single-path | 10 | 0 | 2 | 8 | -0.200 | [-0.500, 0.000] | 0.500000 | 1.000000 |
| baseline-cot-sc | baseline-react | 10 | 0 | 9 | 1 | -0.900 | [-1.000, -0.700] | 0.003906 | 0.023438 |
| baseline-cot-sc | baseline-single-path | 10 | 0 | 2 | 8 | -0.200 | [-0.500, 0.000] | 0.500000 | 1.000000 |
| baseline-react | baseline-single-path | 10 | 7 | 0 | 3 | 0.700 | [0.400, 1.000] | 0.015625 | 0.062500 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
