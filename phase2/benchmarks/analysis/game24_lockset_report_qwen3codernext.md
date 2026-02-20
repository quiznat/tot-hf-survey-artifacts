# Game24 Lockset Report

Generated UTC: 2026-02-20T17:49:01Z
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
| baseline-react | 50 | 22 | 0.440 | [0.312, 0.577] | 20854.2 | 714.7 | 314.8 |
| baseline-single-path | 50 | 4 | 0.080 | [0.032, 0.188] | 5430.3 | 21.0 | 18.5 |
| tot-prototype | 50 | 38 | 0.760 | [0.626, 0.857] | 58213.6 | 978.3 | 107.0 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | baseline-single-path | 50 | 21 | 3 | 26 | 0.360 | [0.200, 0.520] | 0.000277 | 0.000554 |
| baseline-react | tot-prototype | 50 | 3 | 19 | 28 | -0.320 | [-0.480, -0.160] | 0.000855 | 0.000855 |
| baseline-single-path | tot-prototype | 50 | 0 | 34 | 16 | -0.680 | [-0.800, -0.540] | 1.16e-10 | 3.49e-10 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Small item slices are for protocol validation; full locksets are the primary panel summary.
