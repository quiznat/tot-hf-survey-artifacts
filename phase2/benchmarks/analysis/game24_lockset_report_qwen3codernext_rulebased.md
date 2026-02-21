# Game24 Lockset Report

Generated UTC: 2026-02-21T01:36:28Z
Panel ID: game24-lockset-v1
Provider: hf
Model: Qwen/Qwen3-Coder-Next:novita
ToT evaluator mode: rule_based
Seed policy: item_hash
HF temperature: 0.0
HF top-p: 1.0
Items evaluated: 50
Runs executed: 150
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-react | 50 | 21 | 0.420 | [0.294, 0.558] | 8668.0 | 722.3 | 320.1 |
| baseline-single-path | 50 | 4 | 0.080 | [0.032, 0.188] | 1573.4 | 21.0 | 22.8 |
| tot-prototype | 50 | 43 | 0.860 | [0.738, 0.930] | 5374.7 | 516.7 | 89.7 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | baseline-single-path | 50 | 21 | 4 | 25 | 0.340 | [0.160, 0.500] | 0.000911 | 0.000911 |
| baseline-react | tot-prototype | 50 | 3 | 25 | 22 | -0.440 | [-0.600, -0.280] | 2.74e-05 | 5.49e-05 |
| baseline-single-path | tot-prototype | 50 | 0 | 39 | 11 | -0.780 | [-0.880, -0.660] | 3.64e-12 | 1.09e-11 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Small item slices are for protocol validation; full locksets are the primary panel summary.
