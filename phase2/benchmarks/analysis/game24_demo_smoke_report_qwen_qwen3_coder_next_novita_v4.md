# Structured Lockset Report

Generated UTC: 2026-02-22T17:15:57Z
Task ID: game24-demo
Panel ID: game24-lockset-v4
Provider: hf
Model: Qwen/Qwen3-Coder-Next:novita
ToT evaluator mode: model_self_eval
ToT search settings: depth=3, branch_factor=3, frontier_width=3
Seed policy: item_hash
HF temperature: 0.0
HF top-p: 1.0
Capability parity policy: equalize_react_to_tot
Task tools available: calc
Condition tools exposed: react=[none]; single=[none]; tot=[none]
Items evaluated: 10
Runs executed: 30
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-react | 10 | 0 | 0.000 | [0.000, 0.278] | 21257.7 | 800.2 | 315.1 |
| baseline-single-path | 10 | 2 | 0.200 | [0.057, 0.510] | 6328.7 | 21.0 | 19.2 |
| tot-prototype | 10 | 8 | 0.800 | [0.490, 0.943] | 49141.1 | 816.2 | 97.5 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | baseline-single-path | 10 | 0 | 2 | 8 | -0.200 | [-0.500, 0.000] | 0.500000 | 0.500000 |
| baseline-react | tot-prototype | 10 | 0 | 8 | 2 | -0.800 | [-1.000, -0.500] | 0.007812 | 0.023438 |
| baseline-single-path | tot-prototype | 10 | 0 | 6 | 4 | -0.600 | [-0.900, -0.300] | 0.031250 | 0.062500 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
