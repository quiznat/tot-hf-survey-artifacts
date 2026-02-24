# Structured Lockset Report

Generated UTC: 2026-02-22T17:44:45Z
Task ID: game24-demo
Panel ID: game24-lockset-v4
Provider: hf
Model: Qwen/Qwen2.5-Coder-32B-Instruct
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
| baseline-react | 50 | 0 | 0.000 | [0.000, 0.071] | 7813.1 | 562.9 | 327.2 |
| baseline-single-path | 50 | 6 | 0.120 | [0.056, 0.238] | 1701.8 | 21.0 | 51.8 |
| tot-prototype | 50 | 29 | 0.580 | [0.442, 0.706] | 8668.6 | 1357.1 | 148.0 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | baseline-single-path | 50 | 0 | 6 | 44 | -0.120 | [-0.220, -0.040] | 0.031250 | 0.031250 |
| baseline-react | tot-prototype | 50 | 0 | 29 | 21 | -0.580 | [-0.720, -0.440] | 3.73e-09 | 1.12e-08 |
| baseline-single-path | tot-prototype | 50 | 0 | 23 | 27 | -0.460 | [-0.600, -0.320] | 2.38e-07 | 4.77e-07 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
