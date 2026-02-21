# Structured Lockset Report

Generated UTC: 2026-02-21T19:39:15Z
Task ID: linear2-demo
Panel ID: linear2-lockset-v1
Provider: hf
Model: Qwen/Qwen2.5-Coder-32B-Instruct
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
| baseline-react | 50 | 43 | 0.860 | [0.738, 0.930] | 5393.9 | 447.8 | 199.6 |
| baseline-single-path | 50 | 7 | 0.140 | [0.070, 0.262] | 2043.3 | 30.0 | 56.4 |
| tot-prototype | 50 | 16 | 0.320 | [0.208, 0.458] | 14588.3 | 1586.4 | 209.8 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | baseline-single-path | 50 | 37 | 1 | 12 | 0.720 | [0.580, 0.840] | 2.84e-10 | 8.51e-10 |
| baseline-react | tot-prototype | 50 | 29 | 2 | 19 | 0.540 | [0.380, 0.700] | 4.63e-07 | 9.26e-07 |
| baseline-single-path | tot-prototype | 50 | 1 | 10 | 39 | -0.180 | [-0.300, -0.060] | 0.011719 | 0.011719 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
