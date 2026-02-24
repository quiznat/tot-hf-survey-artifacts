# Structured Lockset Report

Generated UTC: 2026-02-22T17:43:18Z
Task ID: game24-demo
Panel ID: game24-lockset-v4
Provider: hf
Model: Qwen/Qwen2.5-72B-Instruct
ToT evaluator mode: model_self_eval
ToT search settings: depth=3, branch_factor=3, frontier_width=3
Seed policy: item_hash
HF temperature: 0.0
HF top-p: 1.0
Capability parity policy: equalize_react_to_tot
Task tools available: calc
Condition tools exposed: react=[none]; single=[none]; tot=[none]
Items evaluated: 50
Runs executed: 150
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-react | 50 | 0 | 0.000 | [0.000, 0.071] | 8094.1 | 221.2 | 163.0 |
| baseline-single-path | 50 | 4 | 0.080 | [0.032, 0.188] | 1192.1 | 21.0 | 9.8 |
| tot-prototype | 50 | 29 | 0.580 | [0.442, 0.706] | 24685.3 | 1374.2 | 253.0 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | baseline-single-path | 50 | 0 | 4 | 46 | -0.080 | [-0.160, -0.020] | 0.125000 | 0.125000 |
| baseline-react | tot-prototype | 50 | 0 | 29 | 21 | -0.580 | [-0.720, -0.440] | 3.73e-09 | 1.12e-08 |
| baseline-single-path | tot-prototype | 50 | 0 | 25 | 25 | -0.500 | [-0.640, -0.360] | 5.96e-08 | 1.19e-07 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
