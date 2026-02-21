# Structured Lockset Report

Generated UTC: 2026-02-21T20:01:09Z
Task ID: linear2-demo
Panel ID: linear2-lockset-v1
Provider: hf
Model: Qwen/Qwen3-Coder-Next:novita
ToT evaluator mode: model_self_eval
ToT search settings: depth=3, branch_factor=3, frontier_width=3
Seed policy: item_hash
HF temperature: 0.0
HF top-p: 1.0
Items evaluated: 50
Runs executed: 150
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-react | 50 | 47 | 0.940 | [0.838, 0.979] | 4595.5 | 350.6 | 223.1 |
| baseline-single-path | 50 | 1 | 0.020 | [0.004, 0.105] | 1919.9 | 30.0 | 79.4 |
| tot-prototype | 50 | 17 | 0.340 | [0.224, 0.478] | 16053.2 | 1424.4 | 70.3 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | baseline-single-path | 50 | 46 | 0 | 4 | 0.920 | [0.840, 0.980] | 2.84e-14 | 8.53e-14 |
| baseline-react | tot-prototype | 50 | 31 | 1 | 18 | 0.600 | [0.440, 0.740] | 1.54e-08 | 3.07e-08 |
| baseline-single-path | tot-prototype | 50 | 0 | 16 | 34 | -0.320 | [-0.460, -0.200] | 3.05e-05 | 3.05e-05 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
