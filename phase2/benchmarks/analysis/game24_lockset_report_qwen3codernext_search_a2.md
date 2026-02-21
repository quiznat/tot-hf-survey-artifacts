# Game24 Lockset Report

Generated UTC: 2026-02-21T17:40:40Z
Panel ID: game24-lockset-v1
Provider: hf
Model: Qwen/Qwen3-Coder-Next:novita
ToT evaluator mode: model_self_eval
ToT search settings: depth=3, branch_factor=4, frontier_width=4
Seed policy: item_hash
HF temperature: 0.0
HF top-p: 1.0
Items evaluated: 50
Runs executed: 150
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-react | 50 | 21 | 0.420 | [0.294, 0.558] | 6031.5 | 699.0 | 307.9 |
| baseline-single-path | 50 | 4 | 0.080 | [0.032, 0.188] | 1099.3 | 21.0 | 22.2 |
| tot-prototype | 50 | 46 | 0.920 | [0.812, 0.968] | 11262.8 | 955.9 | 121.9 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | baseline-single-path | 50 | 20 | 3 | 27 | 0.340 | [0.180, 0.500] | 0.000488 | 0.000488 |
| baseline-react | tot-prototype | 50 | 0 | 25 | 25 | -0.500 | [-0.640, -0.360] | 5.96e-08 | 1.19e-07 |
| baseline-single-path | tot-prototype | 50 | 0 | 42 | 8 | -0.840 | [-0.940, -0.740] | 4.55e-13 | 1.36e-12 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Small item slices are for protocol validation; full locksets are the primary panel summary.
