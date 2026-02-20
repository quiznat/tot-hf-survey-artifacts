# Game24 Lockset Report

Generated UTC: 2026-02-20T04:11:06Z
Panel ID: game24-lockset-v1
Provider: hf
Model: Qwen/Qwen3-Coder-Next:novita
ToT evaluator mode: model_self_eval
Items evaluated: 3
Runs executed: 9

## Condition Summary

| Condition | Runs | Success Rate | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---:|---:|
| baseline-react | 3 | 0.333 | 3391.3 | 193.7 | 195.0 |
| baseline-single-path | 3 | 0.000 | 11684.0 | 21.0 | 9.0 |
| tot-prototype | 3 | 0.667 | 48073.3 | 1039.3 | 98.7 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N |
|---|---|---:|---:|---:|---:|---:|
| baseline-react | baseline-single-path | 3 | 1 | 0 | 2 | 0.333 |
| baseline-react | tot-prototype | 3 | 0 | 1 | 2 | -0.333 |
| baseline-single-path | tot-prototype | 3 | 0 | 2 | 1 | -0.667 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Use this pilot report for protocol validation and effect-size estimation before larger panels.
