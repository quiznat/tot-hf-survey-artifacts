# Game24 Lockset Report

Generated UTC: 2026-02-20T20:16:55Z
Panel ID: game24-lockset-v1
Provider: hf
Model: Qwen/Qwen2.5-72B-Instruct
ToT evaluator mode: model_self_eval
Seed policy: item_hash
HF temperature: 0.0
HF top-p: 1.0
Items evaluated: 50
Runs executed: 150
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-react | 50 | 1 | 0.020 | [0.004, 0.105] | 12369.2 | 521.3 | 222.7 |
| baseline-single-path | 50 | 8 | 0.160 | [0.083, 0.285] | 1317.5 | 21.0 | 8.2 |
| tot-prototype | 50 | 29 | 0.580 | [0.442, 0.706] | 30015.1 | 1578.6 | 286.1 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | baseline-single-path | 50 | 1 | 8 | 41 | -0.140 | [-0.260, -0.040] | 0.039062 | 0.039062 |
| baseline-react | tot-prototype | 50 | 0 | 28 | 22 | -0.560 | [-0.700, -0.420] | 7.45e-09 | 2.24e-08 |
| baseline-single-path | tot-prototype | 50 | 2 | 23 | 25 | -0.420 | [-0.580, -0.260] | 1.94e-05 | 3.89e-05 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Small item slices are for protocol validation; full locksets are the primary panel summary.
