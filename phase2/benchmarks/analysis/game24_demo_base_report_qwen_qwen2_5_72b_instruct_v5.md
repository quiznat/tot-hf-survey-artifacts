# Structured Lockset Report

Generated UTC: 2026-02-22T19:21:55Z
Task ID: game24-demo
Panel ID: game24-lockset-v4
Provider: hf
Model: Qwen/Qwen2.5-72B-Instruct
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
| baseline-cot | 50 | 3 | 0.060 | [0.021, 0.162] | 6348.9 | 34.0 | 112.1 |
| baseline-cot-sc | 50 | 2 | 0.040 | [0.011, 0.135] | 31551.8 | 205.0 | 572.3 |
| baseline-react | 50 | 0 | 0.000 | [0.000, 0.071] | 9089.0 | 258.6 | 174.8 |
| baseline-single-path | 50 | 5 | 0.100 | [0.043, 0.214] | 1374.7 | 21.0 | 10.6 |
| tot-prototype | 50 | 29 | 0.580 | [0.442, 0.706] | 26376.3 | 1369.7 | 248.0 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-cot | baseline-cot-sc | 50 | 3 | 2 | 45 | 0.020 | [-0.060, 0.100] | 1.000000 | 1.000000 |
| baseline-cot | baseline-react | 50 | 3 | 0 | 47 | 0.060 | [0.000, 0.140] | 0.250000 | 1.000000 |
| baseline-cot | baseline-single-path | 50 | 1 | 3 | 46 | -0.040 | [-0.120, 0.040] | 0.625000 | 1.000000 |
| baseline-cot | tot-prototype | 50 | 1 | 27 | 22 | -0.520 | [-0.660, -0.380] | 2.16e-07 | 1.51e-06 |
| baseline-cot-sc | baseline-react | 50 | 2 | 0 | 48 | 0.040 | [0.000, 0.100] | 0.500000 | 1.000000 |
| baseline-cot-sc | baseline-single-path | 50 | 2 | 5 | 43 | -0.060 | [-0.160, 0.040] | 0.453125 | 1.000000 |
| baseline-cot-sc | tot-prototype | 50 | 0 | 27 | 23 | -0.540 | [-0.680, -0.400] | 1.49e-08 | 1.34e-07 |
| baseline-react | baseline-single-path | 50 | 0 | 5 | 45 | -0.100 | [-0.200, -0.020] | 0.062500 | 0.375000 |
| baseline-react | tot-prototype | 50 | 0 | 29 | 21 | -0.580 | [-0.720, -0.440] | 3.73e-09 | 3.73e-08 |
| baseline-single-path | tot-prototype | 50 | 0 | 24 | 26 | -0.480 | [-0.620, -0.340] | 1.19e-07 | 9.54e-07 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
