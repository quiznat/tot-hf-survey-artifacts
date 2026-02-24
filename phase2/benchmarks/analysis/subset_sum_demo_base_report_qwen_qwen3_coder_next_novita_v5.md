# Structured Lockset Report

Generated UTC: 2026-02-23T01:15:30Z
Task ID: subset-sum-demo
Panel ID: subset-sum-lockset-v4
Provider: hf
Model: Qwen/Qwen3-Coder-Next:novita
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
| baseline-cot | 50 | 5 | 0.100 | [0.043, 0.214] | 5684.2 | 65.6 | 96.3 |
| baseline-cot-sc | 50 | 5 | 0.100 | [0.043, 0.214] | 34309.7 | 363.0 | 503.8 |
| baseline-react | 50 | 20 | 0.400 | [0.276, 0.538] | 23917.9 | 746.1 | 301.9 |
| baseline-single-path | 50 | 26 | 0.520 | [0.385, 0.652] | 3321.4 | 52.6 | 2.0 |
| tot-prototype | 50 | 47 | 0.940 | [0.838, 0.979] | 24385.0 | 332.5 | 13.3 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-cot | baseline-cot-sc | 50 | 2 | 2 | 46 | 0.000 | [-0.080, 0.080] | 1.000000 | 1.000000 |
| baseline-cot | baseline-react | 50 | 4 | 19 | 27 | -0.300 | [-0.480, -0.140] | 0.002599 | 0.010398 |
| baseline-cot | baseline-single-path | 50 | 2 | 23 | 25 | -0.420 | [-0.580, -0.260] | 1.94e-05 | 9.72e-05 |
| baseline-cot | tot-prototype | 50 | 2 | 44 | 4 | -0.840 | [-0.960, -0.700] | 3.08e-11 | 3.08e-10 |
| baseline-cot-sc | baseline-react | 50 | 4 | 19 | 27 | -0.300 | [-0.460, -0.120] | 0.002599 | 0.010398 |
| baseline-cot-sc | baseline-single-path | 50 | 1 | 22 | 27 | -0.420 | [-0.560, -0.280] | 5.72e-06 | 4.01e-05 |
| baseline-cot-sc | tot-prototype | 50 | 2 | 44 | 4 | -0.840 | [-0.960, -0.700] | 3.08e-11 | 3.08e-10 |
| baseline-react | baseline-single-path | 50 | 8 | 14 | 28 | -0.120 | [-0.300, 0.060] | 0.286279 | 0.572557 |
| baseline-react | tot-prototype | 50 | 1 | 28 | 21 | -0.540 | [-0.680, -0.380] | 1.12e-07 | 8.94e-07 |
| baseline-single-path | tot-prototype | 50 | 1 | 22 | 27 | -0.420 | [-0.560, -0.280] | 5.72e-06 | 4.01e-05 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
