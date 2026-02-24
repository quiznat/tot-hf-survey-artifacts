# Structured Lockset Report

Generated UTC: 2026-02-23T01:57:32Z
Task ID: subset-sum-demo
Panel ID: subset-sum-lockset-v4
Provider: hf
Model: Qwen/Qwen3-Coder-Next:novita
ToT evaluator mode: rule_based
ToT mode: model_decompose_search
ToT decomposition rounds: 1
ToT search settings: depth=3, branch_factor=3, frontier_width=3
Seed policy: item_hash
HF temperature: 0.0
HF top-p: 1.0
Capability parity policy: equalize_react_to_tot
Task tools available: check_target, sum_list
Condition tools exposed: cot=[none]; cot_sc=[none]; react=[none]; single=[none]; tot=[none]
Items evaluated: 10
Runs executed: 50
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-cot | 10 | 1 | 0.100 | [0.018, 0.404] | 8092.3 | 66.2 | 99.9 |
| baseline-cot-sc | 10 | 1 | 0.100 | [0.018, 0.404] | 39522.1 | 366.0 | 511.2 |
| baseline-react | 10 | 3 | 0.300 | [0.108, 0.603] | 17043.9 | 562.6 | 242.4 |
| baseline-single-path | 10 | 5 | 0.500 | [0.237, 0.763] | 3492.0 | 53.2 | 1.9 |
| tot-prototype | 10 | 10 | 1.000 | [0.722, 1.000] | 10867.7 | 930.9 | 129.2 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-cot | baseline-cot-sc | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-cot | baseline-react | 10 | 1 | 3 | 6 | -0.200 | [-0.600, 0.200] | 0.625000 | 1.000000 |
| baseline-cot | baseline-single-path | 10 | 0 | 4 | 6 | -0.400 | [-0.700, -0.100] | 0.125000 | 0.750000 |
| baseline-cot | tot-prototype | 10 | 0 | 9 | 1 | -0.900 | [-1.000, -0.700] | 0.003906 | 0.039062 |
| baseline-cot-sc | baseline-react | 10 | 1 | 3 | 6 | -0.200 | [-0.600, 0.200] | 0.625000 | 1.000000 |
| baseline-cot-sc | baseline-single-path | 10 | 0 | 4 | 6 | -0.400 | [-0.700, -0.100] | 0.125000 | 0.750000 |
| baseline-cot-sc | tot-prototype | 10 | 0 | 9 | 1 | -0.900 | [-1.000, -0.700] | 0.003906 | 0.039062 |
| baseline-react | baseline-single-path | 10 | 2 | 4 | 4 | -0.200 | [-0.700, 0.300] | 0.687500 | 1.000000 |
| baseline-react | tot-prototype | 10 | 0 | 7 | 3 | -0.700 | [-1.000, -0.400] | 0.015625 | 0.125000 |
| baseline-single-path | tot-prototype | 10 | 0 | 5 | 5 | -0.500 | [-0.800, -0.200] | 0.062500 | 0.437500 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
