# Structured Lockset Report

Generated UTC: 2026-02-23T02:11:25Z
Task ID: subset-sum-demo
Panel ID: subset-sum-lockset-v4
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
Task tools available: check_target, sum_list
Condition tools exposed: cot=[none]; cot_sc=[none]; react=[check_target, sum_list]; single=[none]
Items evaluated: 10
Runs executed: 40
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-cot | 10 | 2 | 0.200 | [0.057, 0.510] | 9811.6 | 66.2 | 99.2 |
| baseline-cot-sc | 10 | 5 | 0.500 | [0.237, 0.763] | 23059.3 | 366.0 | 506.7 |
| baseline-react | 10 | 10 | 1.000 | [0.722, 1.000] | 10616.3 | 175.8 | 141.7 |
| baseline-single-path | 10 | 5 | 0.500 | [0.237, 0.763] | 3920.0 | 53.2 | 1.9 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-cot | baseline-cot-sc | 10 | 1 | 4 | 5 | -0.300 | [-0.700, 0.100] | 0.375000 | 1.000000 |
| baseline-cot | baseline-react | 10 | 0 | 8 | 2 | -0.800 | [-1.000, -0.500] | 0.007812 | 0.046875 |
| baseline-cot | baseline-single-path | 10 | 2 | 5 | 3 | -0.300 | [-0.800, 0.200] | 0.453125 | 1.000000 |
| baseline-cot-sc | baseline-react | 10 | 0 | 5 | 5 | -0.500 | [-0.800, -0.200] | 0.062500 | 0.312500 |
| baseline-cot-sc | baseline-single-path | 10 | 2 | 2 | 6 | 0.000 | [-0.400, 0.400] | 1.000000 | 1.000000 |
| baseline-react | baseline-single-path | 10 | 5 | 0 | 5 | 0.500 | [0.200, 0.800] | 0.062500 | 0.312500 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
