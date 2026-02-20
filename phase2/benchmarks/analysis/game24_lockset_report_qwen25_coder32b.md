# Game24 Lockset Report

Generated UTC: 2026-02-20T20:21:52Z
Panel ID: game24-lockset-v1
Provider: hf
Model: Qwen/Qwen2.5-Coder-32B-Instruct
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
| baseline-react | 50 | 3 | 0.060 | [0.021, 0.162] | 6618.3 | 664.6 | 298.2 |
| baseline-single-path | 50 | 9 | 0.180 | [0.098, 0.308] | 1412.9 | 21.0 | 43.8 |
| tot-prototype | 50 | 34 | 0.680 | [0.542, 0.792] | 6527.7 | 1191.5 | 119.1 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | baseline-single-path | 50 | 3 | 9 | 38 | -0.120 | [-0.260, 0.000] | 0.145996 | 0.145996 |
| baseline-react | tot-prototype | 50 | 0 | 31 | 19 | -0.620 | [-0.760, -0.480] | 9.31e-10 | 2.79e-09 |
| baseline-single-path | tot-prototype | 50 | 3 | 28 | 19 | -0.500 | [-0.660, -0.320] | 4.65e-06 | 9.30e-06 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Small item slices are for protocol validation; full locksets are the primary panel summary.
