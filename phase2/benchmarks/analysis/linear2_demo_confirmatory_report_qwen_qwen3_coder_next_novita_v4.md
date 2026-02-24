# Structured Lockset Report

Generated UTC: 2026-02-22T17:59:13Z
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
Items evaluated: 50
Runs executed: 150
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-react | 50 | 45 | 0.900 | [0.786, 0.957] | 16082.6 | 388.6 | 207.9 |
| baseline-single-path | 50 | 0 | 0.000 | [0.000, 0.071] | 6507.1 | 30.0 | 81.1 |
| tot-prototype | 50 | 28 | 0.560 | [0.423, 0.688] | 37868.5 | 565.6 | 15.6 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | baseline-single-path | 50 | 45 | 0 | 5 | 0.900 | [0.820, 0.980] | 5.68e-14 | 1.71e-13 |
| baseline-react | tot-prototype | 50 | 19 | 2 | 29 | 0.340 | [0.200, 0.500] | 0.000221 | 0.000221 |
| baseline-single-path | tot-prototype | 50 | 0 | 28 | 22 | -0.560 | [-0.700, -0.420] | 7.45e-09 | 1.49e-08 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
