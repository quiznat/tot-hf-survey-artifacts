# Structured Lockset Report

Generated UTC: 2026-02-22T17:15:58Z
Task ID: linear2-demo
Panel ID: linear2-lockset-v4
Provider: hf
Model: Qwen/Qwen3-Coder-Next:novita
ToT evaluator mode: model_self_eval
ToT search settings: depth=3, branch_factor=3, frontier_width=3
Seed policy: item_hash
HF temperature: 0.0
HF top-p: 1.0
Capability parity policy: equalize_react_to_tot
Task tools available: check_xy, solve2
Condition tools exposed: react=[none]; single=[none]; tot=[none]
Items evaluated: 10
Runs executed: 30
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-react | 10 | 8 | 0.800 | [0.490, 0.943] | 11451.5 | 370.4 | 196.3 |
| baseline-single-path | 10 | 0 | 0.000 | [0.000, 0.278] | 3419.6 | 30.0 | 79.2 |
| tot-prototype | 10 | 7 | 0.700 | [0.397, 0.892] | 34390.2 | 450.7 | 11.5 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | baseline-single-path | 10 | 8 | 0 | 2 | 0.800 | [0.500, 1.000] | 0.007812 | 0.023438 |
| baseline-react | tot-prototype | 10 | 3 | 2 | 5 | 0.100 | [-0.300, 0.500] | 1.000000 | 1.000000 |
| baseline-single-path | tot-prototype | 10 | 0 | 7 | 3 | -0.700 | [-1.000, -0.400] | 0.015625 | 0.031250 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
