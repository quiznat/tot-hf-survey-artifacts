# Structured Lockset Report

Generated UTC: 2026-02-22T17:53:56Z
Task ID: subset-sum-demo
Panel ID: subset-sum-lockset-v4
Provider: hf
Model: Qwen/Qwen2.5-Coder-32B-Instruct
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
| baseline-react | 50 | 16 | 0.320 | [0.208, 0.458] | 7758.7 | 658.3 | 315.0 |
| baseline-single-path | 50 | 25 | 0.500 | [0.366, 0.634] | 605.6 | 52.6 | 7.5 |
| tot-prototype | 50 | 46 | 0.920 | [0.812, 0.968] | 2702.8 | 392.1 | 14.7 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | baseline-single-path | 50 | 8 | 17 | 25 | -0.180 | [-0.360, 0.020] | 0.107752 | 0.107752 |
| baseline-react | tot-prototype | 50 | 2 | 32 | 16 | -0.600 | [-0.760, -0.440] | 6.94e-08 | 2.08e-07 |
| baseline-single-path | tot-prototype | 50 | 0 | 21 | 29 | -0.420 | [-0.560, -0.280] | 9.54e-07 | 1.91e-06 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
