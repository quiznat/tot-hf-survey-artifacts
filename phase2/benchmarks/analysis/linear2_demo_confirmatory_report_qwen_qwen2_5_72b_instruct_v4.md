# Structured Lockset Report

Generated UTC: 2026-02-22T18:03:25Z
Task ID: linear2-demo
Panel ID: linear2-lockset-v4
Provider: hf
Model: Qwen/Qwen2.5-72B-Instruct
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
| baseline-react | 50 | 41 | 0.820 | [0.692, 0.902] | 15872.8 | 487.9 | 311.1 |
| baseline-single-path | 50 | 14 | 0.280 | [0.175, 0.417] | 1122.8 | 30.0 | 1.0 |
| tot-prototype | 50 | 28 | 0.560 | [0.423, 0.688] | 37316.4 | 988.0 | 363.5 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | baseline-single-path | 50 | 28 | 1 | 21 | 0.540 | [0.380, 0.680] | 1.12e-07 | 3.35e-07 |
| baseline-react | tot-prototype | 50 | 18 | 5 | 27 | 0.260 | [0.080, 0.440] | 0.010622 | 0.010622 |
| baseline-single-path | tot-prototype | 50 | 3 | 17 | 30 | -0.280 | [-0.440, -0.120] | 0.002577 | 0.005154 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
