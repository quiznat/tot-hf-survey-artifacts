# Structured Lockset Report

Generated UTC: 2026-02-21T20:01:08Z
Task ID: subset-sum-demo
Panel ID: subset-sum-lockset-v1
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
| baseline-react | 50 | 47 | 0.940 | [0.838, 0.979] | 6078.2 | 391.8 | 221.8 |
| baseline-single-path | 50 | 26 | 0.520 | [0.385, 0.652] | 4072.9 | 51.8 | 4.6 |
| tot-prototype | 50 | 43 | 0.860 | [0.738, 0.930] | 9534.4 | 604.3 | 25.1 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | baseline-single-path | 50 | 22 | 1 | 27 | 0.420 | [0.260, 0.560] | 5.72e-06 | 1.72e-05 |
| baseline-react | tot-prototype | 50 | 5 | 1 | 44 | 0.080 | [0.000, 0.180] | 0.218750 | 0.218750 |
| baseline-single-path | tot-prototype | 50 | 1 | 18 | 31 | -0.340 | [-0.480, -0.200] | 7.63e-05 | 0.000153 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
