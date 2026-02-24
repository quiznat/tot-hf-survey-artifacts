# Structured Lockset Report

Generated UTC: 2026-02-22T17:50:04Z
Task ID: subset-sum-demo
Panel ID: subset-sum-lockset-v4
Provider: hf
Model: Qwen/Qwen3-Coder-Next:novita
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
| baseline-react | 50 | 17 | 0.340 | [0.224, 0.478] | 21690.2 | 623.1 | 274.4 |
| baseline-single-path | 50 | 25 | 0.500 | [0.366, 0.634] | 6407.9 | 52.6 | 2.0 |
| tot-prototype | 50 | 44 | 0.880 | [0.762, 0.944] | 25720.9 | 384.4 | 18.9 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | baseline-single-path | 50 | 9 | 17 | 24 | -0.160 | [-0.360, 0.040] | 0.168638 | 0.168638 |
| baseline-react | tot-prototype | 50 | 1 | 28 | 21 | -0.540 | [-0.680, -0.380] | 1.12e-07 | 3.35e-07 |
| baseline-single-path | tot-prototype | 50 | 1 | 20 | 29 | -0.380 | [-0.520, -0.240] | 2.10e-05 | 4.20e-05 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
