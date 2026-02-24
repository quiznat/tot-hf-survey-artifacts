# Structured Lockset Report

Generated UTC: 2026-02-23T01:20:35Z
Task ID: subset-sum-demo
Panel ID: subset-sum-lockset-v4
Provider: hf
Model: Qwen/Qwen2.5-Coder-32B-Instruct
ToT evaluator mode: model_self_eval
ToT search settings: depth=3, branch_factor=3, frontier_width=3
Seed policy: item_hash
HF temperature: 0.0
HF top-p: 1.0
Capability parity policy: equalize_react_to_tot
Task tools available: check_target, sum_list
Condition tools exposed: cot=[none]; cot_sc=[none]; react=[none]; single=[none]; tot=[none]
Items evaluated: 50
Runs executed: 250
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-cot | 50 | 7 | 0.140 | [0.070, 0.262] | 2543.9 | 65.6 | 109.6 |
| baseline-cot-sc | 50 | 6 | 0.120 | [0.056, 0.238] | 12678.0 | 363.0 | 549.9 |
| baseline-react | 50 | 15 | 0.300 | [0.191, 0.438] | 8016.0 | 756.7 | 342.0 |
| baseline-single-path | 50 | 23 | 0.460 | [0.330, 0.596] | 602.5 | 52.6 | 6.3 |
| tot-prototype | 50 | 44 | 0.880 | [0.762, 0.944] | 3504.1 | 442.5 | 18.7 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-cot | baseline-cot-sc | 50 | 4 | 3 | 43 | 0.020 | [-0.080, 0.120] | 1.000000 | 1.000000 |
| baseline-cot | baseline-react | 50 | 5 | 13 | 32 | -0.160 | [-0.320, 0.000] | 0.096252 | 0.313416 |
| baseline-cot | baseline-single-path | 50 | 2 | 18 | 30 | -0.320 | [-0.480, -0.160] | 0.000402 | 0.002012 |
| baseline-cot | tot-prototype | 50 | 0 | 37 | 13 | -0.740 | [-0.860, -0.620] | 1.46e-11 | 1.31e-10 |
| baseline-cot-sc | baseline-react | 50 | 6 | 15 | 29 | -0.180 | [-0.360, 0.000] | 0.078354 | 0.313416 |
| baseline-cot-sc | baseline-single-path | 50 | 2 | 19 | 29 | -0.340 | [-0.500, -0.180] | 0.000221 | 0.001328 |
| baseline-cot-sc | tot-prototype | 50 | 0 | 38 | 12 | -0.760 | [-0.880, -0.640] | 7.28e-12 | 7.28e-11 |
| baseline-react | baseline-single-path | 50 | 6 | 14 | 30 | -0.160 | [-0.320, 0.000] | 0.115318 | 0.313416 |
| baseline-react | tot-prototype | 50 | 0 | 29 | 21 | -0.580 | [-0.720, -0.440] | 3.73e-09 | 2.98e-08 |
| baseline-single-path | tot-prototype | 50 | 0 | 21 | 29 | -0.420 | [-0.560, -0.280] | 9.54e-07 | 6.68e-06 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
