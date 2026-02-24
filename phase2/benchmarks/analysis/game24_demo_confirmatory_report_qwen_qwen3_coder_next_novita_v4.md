# Structured Lockset Report

Generated UTC: 2026-02-22T17:40:39Z
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
Items evaluated: 50
Runs executed: 150
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-react | 50 | 5 | 0.100 | [0.043, 0.214] | 21585.8 | 646.7 | 273.8 |
| baseline-single-path | 50 | 7 | 0.140 | [0.070, 0.262] | 5743.8 | 21.0 | 23.8 |
| tot-prototype | 50 | 41 | 0.820 | [0.692, 0.902] | 58696.7 | 916.4 | 116.6 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | baseline-single-path | 50 | 5 | 7 | 38 | -0.040 | [-0.180, 0.100] | 0.774414 | 0.774414 |
| baseline-react | tot-prototype | 50 | 0 | 36 | 14 | -0.720 | [-0.840, -0.600] | 2.91e-11 | 8.73e-11 |
| baseline-single-path | tot-prototype | 50 | 0 | 34 | 16 | -0.680 | [-0.800, -0.540] | 1.16e-10 | 2.33e-10 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
