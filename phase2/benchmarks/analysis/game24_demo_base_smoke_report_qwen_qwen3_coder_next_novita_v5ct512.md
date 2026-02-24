# Structured Lockset Report

Generated UTC: 2026-02-23T02:18:34Z
Task ID: game24-demo
Panel ID: game24-lockset-v4
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
Task tools available: calc
Condition tools exposed: cot=[none]; cot_sc=[none]; react=[calc]; single=[none]
Items evaluated: 10
Runs executed: 40
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-cot | 10 | 1 | 0.100 | [0.018, 0.404] | 4490.6 | 34.0 | 220.5 |
| baseline-cot-sc | 10 | 2 | 0.200 | [0.057, 0.510] | 37195.9 | 205.0 | 1128.1 |
| baseline-react | 10 | 5 | 0.500 | [0.237, 0.763] | 7942.1 | 154.7 | 214.8 |
| baseline-single-path | 10 | 3 | 0.300 | [0.108, 0.603] | 2126.7 | 21.0 | 18.5 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-cot | baseline-cot-sc | 10 | 0 | 1 | 9 | -0.100 | [-0.300, 0.000] | 1.000000 | 1.000000 |
| baseline-cot | baseline-react | 10 | 0 | 4 | 6 | -0.400 | [-0.700, -0.100] | 0.125000 | 0.750000 |
| baseline-cot | baseline-single-path | 10 | 1 | 3 | 6 | -0.200 | [-0.600, 0.200] | 0.625000 | 1.000000 |
| baseline-cot-sc | baseline-react | 10 | 0 | 3 | 7 | -0.300 | [-0.600, 0.000] | 0.250000 | 1.000000 |
| baseline-cot-sc | baseline-single-path | 10 | 1 | 2 | 7 | -0.100 | [-0.400, 0.200] | 1.000000 | 1.000000 |
| baseline-react | baseline-single-path | 10 | 4 | 2 | 4 | 0.200 | [-0.300, 0.600] | 0.687500 | 1.000000 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
