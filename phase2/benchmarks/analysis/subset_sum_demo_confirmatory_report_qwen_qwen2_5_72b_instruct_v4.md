# Structured Lockset Report

Generated UTC: 2026-02-22T17:53:01Z
Task ID: subset-sum-demo
Panel ID: subset-sum-lockset-v4
Provider: hf
Model: Qwen/Qwen2.5-72B-Instruct
ToT evaluator mode: model_self_eval
ToT search settings: depth=3, branch_factor=3, frontier_width=3
Seed policy: item_hash
HF temperature: 0.0
HF top-p: 1.0
Capability parity policy: equalize_react_to_tot
Task tools available: check_target, sum_list
Condition tools exposed: react=[none]; single=[none]; tot=[none]
Items evaluated: 50
Runs executed: 150
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-react | 50 | 22 | 0.440 | [0.312, 0.577] | 20122.5 | 755.0 | 374.8 |
| baseline-single-path | 50 | 29 | 0.580 | [0.442, 0.706] | 1045.8 | 52.6 | 1.4 |
| tot-prototype | 50 | 48 | 0.960 | [0.865, 0.989] | 9663.4 | 362.4 | 106.4 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | baseline-single-path | 50 | 4 | 11 | 35 | -0.140 | [-0.300, 0.000] | 0.118469 | 0.118469 |
| baseline-react | tot-prototype | 50 | 0 | 26 | 24 | -0.520 | [-0.660, -0.380] | 2.98e-08 | 8.94e-08 |
| baseline-single-path | tot-prototype | 50 | 0 | 19 | 31 | -0.380 | [-0.520, -0.240] | 3.81e-06 | 7.63e-06 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
