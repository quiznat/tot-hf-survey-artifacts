# Structured Lockset Report

Generated UTC: 2026-02-23T01:59:08Z
Task ID: linear2-demo
Panel ID: linear2-lockset-v4
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
Task tools available: check_xy, solve2
Condition tools exposed: cot=[none]; cot_sc=[none]; react=[none]; single=[none]; tot=[none]
Items evaluated: 10
Runs executed: 50
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-cot | 10 | 0 | 0.000 | [0.000, 0.278] | 4897.0 | 43.0 | 83.9 |
| baseline-cot-sc | 10 | 0 | 0.000 | [0.000, 0.278] | 22032.4 | 250.0 | 392.7 |
| baseline-react | 10 | 8 | 0.800 | [0.490, 0.943] | 15765.7 | 477.8 | 225.1 |
| baseline-single-path | 10 | 0 | 0.000 | [0.000, 0.278] | 4203.0 | 30.0 | 79.1 |
| tot-prototype | 10 | 9 | 0.900 | [0.596, 0.982] | 16116.4 | 1089.3 | 173.1 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-cot | baseline-cot-sc | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-cot | baseline-react | 10 | 0 | 8 | 2 | -0.800 | [-1.000, -0.500] | 0.007812 | 0.054688 |
| baseline-cot | baseline-single-path | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-cot | tot-prototype | 10 | 0 | 9 | 1 | -0.900 | [-1.000, -0.700] | 0.003906 | 0.039062 |
| baseline-cot-sc | baseline-react | 10 | 0 | 8 | 2 | -0.800 | [-1.000, -0.500] | 0.007812 | 0.054688 |
| baseline-cot-sc | baseline-single-path | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-cot-sc | tot-prototype | 10 | 0 | 9 | 1 | -0.900 | [-1.000, -0.700] | 0.003906 | 0.039062 |
| baseline-react | baseline-single-path | 10 | 8 | 0 | 2 | 0.800 | [0.500, 1.000] | 0.007812 | 0.054688 |
| baseline-react | tot-prototype | 10 | 1 | 2 | 7 | -0.100 | [-0.400, 0.200] | 1.000000 | 1.000000 |
| baseline-single-path | tot-prototype | 10 | 0 | 9 | 1 | -0.900 | [-1.000, -0.700] | 0.003906 | 0.039062 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
