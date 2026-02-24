# Structured Lockset Report

Generated UTC: 2026-02-23T02:30:11Z
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
| baseline-cot | 10 | 10 | 1.000 | [0.722, 1.000] | 10096.9 | 146.2 | 163.8 |
| baseline-cot-sc | 10 | 10 | 1.000 | [0.722, 1.000] | 40228.2 | 1156.0 | 1082.3 |
| baseline-react | 10 | 10 | 1.000 | [0.722, 1.000] | 5108.7 | 59.2 | 155.6 |
| baseline-single-path | 10 | 6 | 0.600 | [0.313, 0.832] | 11289.0 | 53.2 | 2.2 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-cot | baseline-cot-sc | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-cot | baseline-react | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-cot | baseline-single-path | 10 | 4 | 0 | 6 | 0.400 | [0.100, 0.700] | 0.125000 | 0.750000 |
| baseline-cot-sc | baseline-react | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-cot-sc | baseline-single-path | 10 | 4 | 0 | 6 | 0.400 | [0.100, 0.700] | 0.125000 | 0.750000 |
| baseline-react | baseline-single-path | 10 | 4 | 0 | 6 | 0.400 | [0.100, 0.700] | 0.125000 | 0.750000 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
