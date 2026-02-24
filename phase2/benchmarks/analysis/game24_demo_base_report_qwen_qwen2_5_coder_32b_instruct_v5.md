# Structured Lockset Report

Generated UTC: 2026-02-22T19:24:30Z
Task ID: game24-demo
Panel ID: game24-lockset-v4
Provider: hf
Model: Qwen/Qwen2.5-Coder-32B-Instruct
ToT evaluator mode: model_self_eval
ToT search settings: depth=3, branch_factor=3, frontier_width=3
Seed policy: item_hash
HF temperature: 0.0
HF top-p: 1.0
Capability parity policy: equalize_react_to_tot
Task tools available: calc
Condition tools exposed: cot=[none]; cot_sc=[none]; react=[none]; single=[none]; tot=[none]
Items evaluated: 50
Runs executed: 250
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-cot | 50 | 4 | 0.080 | [0.032, 0.188] | 2761.5 | 34.0 | 118.7 |
| baseline-cot-sc | 50 | 3 | 0.060 | [0.021, 0.162] | 13482.2 | 205.0 | 597.9 |
| baseline-react | 50 | 0 | 0.000 | [0.000, 0.071] | 7071.1 | 613.7 | 343.9 |
| baseline-single-path | 50 | 6 | 0.120 | [0.056, 0.238] | 1622.1 | 21.0 | 54.4 |
| tot-prototype | 50 | 30 | 0.600 | [0.462, 0.724] | 8028.5 | 1336.0 | 149.9 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-cot | baseline-cot-sc | 50 | 4 | 3 | 43 | 0.020 | [-0.080, 0.120] | 1.000000 | 1.000000 |
| baseline-cot | baseline-react | 50 | 4 | 0 | 46 | 0.080 | [0.020, 0.160] | 0.125000 | 0.625000 |
| baseline-cot | baseline-single-path | 50 | 4 | 6 | 40 | -0.040 | [-0.160, 0.080] | 0.753906 | 1.000000 |
| baseline-cot | tot-prototype | 50 | 1 | 27 | 22 | -0.520 | [-0.660, -0.380] | 2.16e-07 | 1.51e-06 |
| baseline-cot-sc | baseline-react | 50 | 3 | 0 | 47 | 0.060 | [0.000, 0.140] | 0.250000 | 1.000000 |
| baseline-cot-sc | baseline-single-path | 50 | 2 | 5 | 43 | -0.060 | [-0.160, 0.040] | 0.453125 | 1.000000 |
| baseline-cot-sc | tot-prototype | 50 | 0 | 27 | 23 | -0.540 | [-0.680, -0.400] | 1.49e-08 | 1.34e-07 |
| baseline-react | baseline-single-path | 50 | 0 | 6 | 44 | -0.120 | [-0.220, -0.040] | 0.031250 | 0.187500 |
| baseline-react | tot-prototype | 50 | 0 | 30 | 20 | -0.600 | [-0.740, -0.460] | 1.86e-09 | 1.86e-08 |
| baseline-single-path | tot-prototype | 50 | 0 | 24 | 26 | -0.480 | [-0.620, -0.340] | 1.19e-07 | 9.54e-07 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
