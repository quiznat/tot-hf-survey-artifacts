# Structured Lockset Report

Generated UTC: 2026-02-22T18:05:00Z
Task ID: linear2-demo
Panel ID: linear2-lockset-v4
Provider: hf
Model: Qwen/Qwen2.5-Coder-32B-Instruct
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
| baseline-react | 50 | 40 | 0.800 | [0.670, 0.888] | 7720.3 | 434.3 | 267.7 |
| baseline-single-path | 50 | 4 | 0.080 | [0.032, 0.188] | 2509.5 | 30.0 | 56.8 |
| tot-prototype | 50 | 25 | 0.500 | [0.366, 0.634] | 10092.8 | 808.8 | 99.8 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | baseline-single-path | 50 | 38 | 2 | 10 | 0.720 | [0.560, 0.860] | 1.49e-09 | 4.48e-09 |
| baseline-react | tot-prototype | 50 | 21 | 6 | 23 | 0.300 | [0.120, 0.480] | 0.005925 | 0.005925 |
| baseline-single-path | tot-prototype | 50 | 0 | 21 | 29 | -0.420 | [-0.560, -0.280] | 9.54e-07 | 1.91e-06 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
