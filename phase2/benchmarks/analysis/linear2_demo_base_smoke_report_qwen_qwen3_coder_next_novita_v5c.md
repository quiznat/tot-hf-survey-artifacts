# Structured Lockset Report

Generated UTC: 2026-02-23T02:12:49Z
Task ID: linear2-demo
Panel ID: linear2-lockset-v4
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
Task tools available: check_xy, solve2
Condition tools exposed: cot=[none]; cot_sc=[none]; react=[check_xy, solve2]; single=[none]
Items evaluated: 10
Runs executed: 40
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-cot | 10 | 0 | 0.000 | [0.000, 0.278] | 2955.9 | 43.0 | 83.8 |
| baseline-cot-sc | 10 | 1 | 0.100 | [0.018, 0.404] | 35114.9 | 250.0 | 396.0 |
| baseline-react | 10 | 9 | 0.900 | [0.596, 0.982] | 11040.4 | 366.8 | 219.1 |
| baseline-single-path | 10 | 2 | 0.200 | [0.057, 0.510] | 4950.2 | 30.0 | 77.4 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-cot | baseline-cot-sc | 10 | 0 | 1 | 9 | -0.100 | [-0.300, 0.000] | 1.000000 | 1.000000 |
| baseline-cot | baseline-react | 10 | 0 | 9 | 1 | -0.900 | [-1.000, -0.700] | 0.003906 | 0.023438 |
| baseline-cot | baseline-single-path | 10 | 0 | 2 | 8 | -0.200 | [-0.500, 0.000] | 0.500000 | 1.000000 |
| baseline-cot-sc | baseline-react | 10 | 0 | 8 | 2 | -0.800 | [-1.000, -0.500] | 0.007812 | 0.039062 |
| baseline-cot-sc | baseline-single-path | 10 | 0 | 1 | 9 | -0.100 | [-0.300, 0.000] | 1.000000 | 1.000000 |
| baseline-react | baseline-single-path | 10 | 7 | 0 | 3 | 0.700 | [0.400, 1.000] | 0.015625 | 0.062500 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
