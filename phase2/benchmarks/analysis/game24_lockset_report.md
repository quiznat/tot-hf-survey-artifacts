# Game24 Lockset Report

Generated UTC: 2026-02-20T05:23:03Z
Panel ID: game24-lockset-v1
Provider: hf
Model: Qwen/Qwen3-Coder-Next:novita
ToT evaluator mode: model_self_eval
Items evaluated: 50
Runs executed: 150

## Condition Summary

| Condition | Runs | Success Rate | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---:|---:|
| baseline-react | 50 | 0.400 | 21117.0 | 718.0 | 315.9 |
| baseline-single-path | 50 | 0.080 | 6040.7 | 21.0 | 18.6 |
| tot-prototype | 50 | 0.840 | 53823.3 | 765.9 | 90.8 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N |
|---|---|---:|---:|---:|---:|---:|
| baseline-react | baseline-single-path | 50 | 20 | 4 | 26 | 0.320 |
| baseline-react | tot-prototype | 50 | 3 | 25 | 22 | -0.440 |
| baseline-single-path | tot-prototype | 50 | 0 | 38 | 12 | -0.760 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Small item slices are for protocol validation; full locksets are the primary panel summary.
