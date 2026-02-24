# Structured Lockset Report

Generated UTC: 2026-02-22T19:15:56Z
Task ID: game24-demo
Panel ID: game24-lockset-v4
Provider: hf
Model: Qwen/Qwen3-Coder-Next:novita
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
| baseline-cot | 50 | 0 | 0.000 | [0.000, 0.071] | 4749.1 | 34.0 | 109.5 |
| baseline-cot-sc | 50 | 2 | 0.040 | [0.011, 0.135] | 31748.1 | 205.0 | 545.3 |
| baseline-react | 50 | 3 | 0.060 | [0.021, 0.162] | 18395.6 | 622.5 | 274.9 |
| baseline-single-path | 50 | 8 | 0.160 | [0.083, 0.285] | 4701.5 | 21.0 | 23.4 |
| tot-prototype | 50 | 36 | 0.720 | [0.583, 0.825] | 59518.9 | 1051.8 | 143.5 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-cot | baseline-cot-sc | 50 | 0 | 2 | 48 | -0.040 | [-0.100, 0.000] | 0.500000 | 1.000000 |
| baseline-cot | baseline-react | 50 | 0 | 3 | 47 | -0.060 | [-0.140, 0.000] | 0.250000 | 0.906250 |
| baseline-cot | baseline-single-path | 50 | 0 | 8 | 42 | -0.160 | [-0.260, -0.060] | 0.007812 | 0.046875 |
| baseline-cot | tot-prototype | 50 | 0 | 36 | 14 | -0.720 | [-0.840, -0.600] | 2.91e-11 | 2.91e-10 |
| baseline-cot-sc | baseline-react | 50 | 2 | 3 | 45 | -0.020 | [-0.100, 0.060] | 1.000000 | 1.000000 |
| baseline-cot-sc | baseline-single-path | 50 | 1 | 7 | 42 | -0.120 | [-0.220, -0.020] | 0.070312 | 0.351562 |
| baseline-cot-sc | tot-prototype | 50 | 0 | 34 | 16 | -0.680 | [-0.800, -0.540] | 1.16e-10 | 1.05e-09 |
| baseline-react | baseline-single-path | 50 | 3 | 8 | 39 | -0.100 | [-0.240, 0.020] | 0.226562 | 0.906250 |
| baseline-react | tot-prototype | 50 | 0 | 33 | 17 | -0.660 | [-0.780, -0.520] | 2.33e-10 | 1.86e-09 |
| baseline-single-path | tot-prototype | 50 | 0 | 28 | 22 | -0.560 | [-0.700, -0.420] | 7.45e-09 | 5.22e-08 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
