# Game24 Lockset Report

Generated UTC: 2026-02-21T02:57:54Z
Panel ID: game24-lockset-v1
Provider: hf
Model: Qwen/Qwen3-Coder-Next:novita
ToT evaluator mode: hybrid
Seed policy: item_hash
HF temperature: 0.0
HF top-p: 1.0
Items evaluated: 50
Runs executed: 150
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-react | 50 | 21 | 0.420 | [0.294, 0.558] | 9828.7 | 689.2 | 307.3 |
| baseline-single-path | 50 | 4 | 0.080 | [0.032, 0.188] | 1837.5 | 21.0 | 22.8 |
| tot-prototype | 50 | 39 | 0.780 | [0.648, 0.872] | 14485.5 | 935.8 | 104.6 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | baseline-single-path | 50 | 20 | 3 | 27 | 0.340 | [0.180, 0.500] | 0.000488 | 0.000488 |
| baseline-react | tot-prototype | 50 | 1 | 19 | 30 | -0.360 | [-0.500, -0.220] | 4.01e-05 | 8.01e-05 |
| baseline-single-path | tot-prototype | 50 | 0 | 35 | 15 | -0.700 | [-0.820, -0.560] | 5.82e-11 | 1.75e-10 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Small item slices are for protocol validation; full locksets are the primary panel summary.
