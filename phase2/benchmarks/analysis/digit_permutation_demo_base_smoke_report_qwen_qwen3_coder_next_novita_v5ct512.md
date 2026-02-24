# Structured Lockset Report

Generated UTC: 2026-02-23T02:23:39Z
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
| baseline-cot | 10 | 5 | 0.500 | [0.237, 0.763] | 10783.2 | 41.0 | 267.4 |
| baseline-cot-sc | 10 | 5 | 0.500 | [0.237, 0.763] | 48572.3 | 240.0 | 1303.9 |
| baseline-react | 10 | 10 | 1.000 | [0.722, 1.000] | 9349.5 | 202.6 | 217.7 |
| baseline-single-path | 10 | 8 | 0.800 | [0.490, 0.943] | 7663.0 | 28.0 | 204.1 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-cot | baseline-cot-sc | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-cot | baseline-react | 10 | 0 | 5 | 5 | -0.500 | [-0.800, -0.200] | 0.062500 | 0.375000 |
| baseline-cot | baseline-single-path | 10 | 0 | 3 | 7 | -0.300 | [-0.600, 0.000] | 0.250000 | 1.000000 |
| baseline-cot-sc | baseline-react | 10 | 0 | 5 | 5 | -0.500 | [-0.800, -0.200] | 0.062500 | 0.375000 |
| baseline-cot-sc | baseline-single-path | 10 | 0 | 3 | 7 | -0.300 | [-0.600, 0.000] | 0.250000 | 1.000000 |
| baseline-react | baseline-single-path | 10 | 2 | 0 | 8 | 0.200 | [0.000, 0.500] | 0.500000 | 1.000000 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
