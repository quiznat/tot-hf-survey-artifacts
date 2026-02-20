# Game24 Lockset Report

Generated UTC: 2026-02-20T17:08:47Z
Panel ID: game24-lockset-v1
Provider: hf
Model: Qwen/Qwen3-Coder-Next:novita
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
| baseline-react | 50 | 20 | 0.400 | [0.276, 0.538] | 21117.0 | 718.0 | 315.9 |
| baseline-single-path | 50 | 4 | 0.080 | [0.032, 0.188] | 6040.7 | 21.0 | 18.6 |
| tot-prototype | 50 | 42 | 0.840 | [0.715, 0.917] | 53823.3 | 765.9 | 90.8 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | baseline-single-path | 50 | 20 | 4 | 26 | 0.320 | [0.160, 0.480] | 0.001544 | 0.001544 |
| baseline-react | tot-prototype | 50 | 3 | 25 | 22 | -0.440 | [-0.600, -0.260] | 2.74e-05 | 5.49e-05 |
| baseline-single-path | tot-prototype | 50 | 0 | 38 | 12 | -0.760 | [-0.880, -0.640] | 7.28e-12 | 2.18e-11 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Small item slices are for protocol validation; full locksets are the primary panel summary.
