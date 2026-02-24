# Structured Lockset Report

Generated UTC: 2026-02-23T19:11:24Z
Task ID: game24-demo
Panel ID: game24-lockset-v4
Provider: smolagents
Model: Qwen/Qwen3-Coder-Next:novita
ToT evaluator mode: model_self_eval
ToT mode: model_decompose_search
ToT-gen mode: model_decompose_search
ToT decomposition rounds: 1
ToT search settings: depth=4, branch_factor=3, frontier_width=3
ToT per-condition depth overrides: legacy=base, gen=base
Seed policy: item_hash
HF temperature: 0.0
CoT temperature: 0.0
CoT-SC temperature: 0.7
ReAct temperature: 0.0
HF top-p: 1.0
Capability parity policy: equalize_react_to_tot
Task tools available: calc
Condition tools exposed: cot=[none]; cot_sc=[none]; react=[none]; single=[none]; tot=[none]; tot_gen=[none]
Items evaluated: 10
Runs executed: 60
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-cot | 10 | 1 | 0.100 | [0.018, 0.404] | 167073.3 | 34.0 | 220.3 |
| baseline-cot-sc | 10 | 1 | 0.100 | [0.018, 0.404] | 32036.4 | 410.0 | 2284.5 |
| baseline-react | 10 | 10 | 1.000 | [0.722, 1.000] | 5088.3 | 2741.8 | 348.9 |
| baseline-single-path | 10 | 4 | 0.400 | [0.168, 0.687] | 1817.6 | 21.0 | 17.9 |
| tot-gen | 10 | 8 | 0.800 | [0.490, 0.943] | 23859.5 | 14559.6 | 469.0 |
| tot-prototype | 10 | 9 | 0.900 | [0.596, 0.982] | 52072.6 | 13107.9 | 402.9 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-cot | baseline-cot-sc | 10 | 1 | 1 | 8 | 0.000 | [-0.300, 0.300] | 1.000000 | 1.000000 |
| baseline-cot | baseline-react | 10 | 0 | 9 | 1 | -0.900 | [-1.000, -0.700] | 0.003906 | 0.058594 |
| baseline-cot | baseline-single-path | 10 | 1 | 4 | 5 | -0.300 | [-0.700, 0.100] | 0.375000 | 1.000000 |
| baseline-cot | tot-gen | 10 | 0 | 7 | 3 | -0.700 | [-1.000, -0.400] | 0.015625 | 0.171875 |
| baseline-cot | tot-prototype | 10 | 0 | 8 | 2 | -0.800 | [-1.000, -0.500] | 0.007812 | 0.101562 |
| baseline-cot-sc | baseline-react | 10 | 0 | 9 | 1 | -0.900 | [-1.000, -0.700] | 0.003906 | 0.058594 |
| baseline-cot-sc | baseline-single-path | 10 | 1 | 4 | 5 | -0.300 | [-0.700, 0.100] | 0.375000 | 1.000000 |
| baseline-cot-sc | tot-gen | 10 | 0 | 7 | 3 | -0.700 | [-1.000, -0.400] | 0.015625 | 0.171875 |
| baseline-cot-sc | tot-prototype | 10 | 0 | 8 | 2 | -0.800 | [-1.000, -0.500] | 0.007812 | 0.101562 |
| baseline-react | baseline-single-path | 10 | 6 | 0 | 4 | 0.600 | [0.300, 0.900] | 0.031250 | 0.281250 |
| baseline-react | tot-gen | 10 | 2 | 0 | 8 | 0.200 | [0.000, 0.500] | 0.500000 | 1.000000 |
| baseline-react | tot-prototype | 10 | 1 | 0 | 9 | 0.100 | [0.000, 0.300] | 1.000000 | 1.000000 |
| baseline-single-path | tot-gen | 10 | 1 | 5 | 4 | -0.400 | [-0.800, 0.000] | 0.218750 | 1.000000 |
| baseline-single-path | tot-prototype | 10 | 0 | 5 | 5 | -0.500 | [-0.800, -0.200] | 0.062500 | 0.500000 |
| tot-gen | tot-prototype | 10 | 0 | 1 | 9 | -0.100 | [-0.300, 0.000] | 1.000000 | 1.000000 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
