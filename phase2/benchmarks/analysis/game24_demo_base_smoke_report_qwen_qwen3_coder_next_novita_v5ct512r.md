# Structured Lockset Report

Generated UTC: 2026-02-23T02:28:37Z
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
| baseline-cot | 10 | 8 | 0.800 | [0.490, 0.943] | 10937.9 | 276.3 | 251.5 |
| baseline-cot-sc | 10 | 8 | 0.800 | [0.490, 0.943] | 59767.9 | 1289.7 | 1232.4 |
| baseline-react | 10 | 4 | 0.400 | [0.168, 0.687] | 10651.7 | 415.3 | 253.5 |
| baseline-single-path | 10 | 2 | 0.200 | [0.057, 0.510] | 7484.3 | 21.0 | 20.0 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-cot | baseline-cot-sc | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-cot | baseline-react | 10 | 4 | 0 | 6 | 0.400 | [0.100, 0.700] | 0.125000 | 0.500000 |
| baseline-cot | baseline-single-path | 10 | 7 | 1 | 2 | 0.600 | [0.200, 1.000] | 0.070312 | 0.421875 |
| baseline-cot-sc | baseline-react | 10 | 4 | 0 | 6 | 0.400 | [0.100, 0.700] | 0.125000 | 0.500000 |
| baseline-cot-sc | baseline-single-path | 10 | 7 | 1 | 2 | 0.600 | [0.100, 1.000] | 0.070312 | 0.421875 |
| baseline-react | baseline-single-path | 10 | 4 | 2 | 4 | 0.200 | [-0.300, 0.700] | 0.687500 | 1.000000 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
