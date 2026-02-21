# Game24 Lockset Report

Generated UTC: 2026-02-21T17:38:19Z
Panel ID: game24-lockset-v1
Provider: hf
Model: Qwen/Qwen3-Coder-Next:novita
ToT evaluator mode: model_self_eval
ToT search settings: depth=2, branch_factor=3, frontier_width=3
Seed policy: item_hash
HF temperature: 0.0
HF top-p: 1.0
Items evaluated: 50
Runs executed: 150
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-react | 50 | 18 | 0.360 | [0.241, 0.499] | 6094.5 | 675.7 | 300.0 |
| baseline-single-path | 50 | 3 | 0.060 | [0.021, 0.162] | 1204.0 | 21.0 | 21.6 |
| tot-prototype | 50 | 36 | 0.720 | [0.583, 0.825] | 9050.9 | 636.7 | 70.8 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | baseline-single-path | 50 | 18 | 3 | 29 | 0.300 | [0.140, 0.460] | 0.001490 | 0.001490 |
| baseline-react | tot-prototype | 50 | 2 | 20 | 28 | -0.360 | [-0.520, -0.200] | 0.000121 | 0.000242 |
| baseline-single-path | tot-prototype | 50 | 0 | 33 | 17 | -0.660 | [-0.780, -0.520] | 2.33e-10 | 6.98e-10 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Small item slices are for protocol validation; full locksets are the primary panel summary.
