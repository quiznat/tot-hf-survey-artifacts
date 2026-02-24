# Structured Lockset Report

Generated UTC: 2026-02-23T01:18:26Z
Task ID: subset-sum-demo
Panel ID: subset-sum-lockset-v4
Provider: hf
Model: Qwen/Qwen2.5-72B-Instruct
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
| baseline-cot | 50 | 26 | 0.520 | [0.385, 0.652] | 1118.3 | 65.6 | 2.3 |
| baseline-cot-sc | 50 | 27 | 0.540 | [0.404, 0.670] | 5570.2 | 363.0 | 14.2 |
| baseline-react | 50 | 30 | 0.600 | [0.462, 0.724] | 19448.1 | 905.1 | 407.2 |
| baseline-single-path | 50 | 26 | 0.520 | [0.385, 0.652] | 1016.8 | 52.6 | 1.3 |
| tot-prototype | 50 | 47 | 0.940 | [0.838, 0.979] | 9622.4 | 322.5 | 118.9 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-cot | baseline-cot-sc | 50 | 4 | 5 | 41 | -0.020 | [-0.140, 0.100] | 1.000000 | 1.000000 |
| baseline-cot | baseline-react | 50 | 4 | 8 | 38 | -0.080 | [-0.220, 0.060] | 0.387695 | 1.000000 |
| baseline-cot | baseline-single-path | 50 | 3 | 3 | 44 | 0.000 | [-0.100, 0.100] | 1.000000 | 1.000000 |
| baseline-cot | tot-prototype | 50 | 1 | 22 | 27 | -0.420 | [-0.560, -0.280] | 5.72e-06 | 4.58e-05 |
| baseline-cot-sc | baseline-react | 50 | 4 | 7 | 39 | -0.060 | [-0.200, 0.060] | 0.548828 | 1.000000 |
| baseline-cot-sc | baseline-single-path | 50 | 4 | 3 | 43 | 0.020 | [-0.080, 0.120] | 1.000000 | 1.000000 |
| baseline-cot-sc | tot-prototype | 50 | 0 | 20 | 30 | -0.400 | [-0.540, -0.260] | 1.91e-06 | 1.72e-05 |
| baseline-react | baseline-single-path | 50 | 9 | 5 | 36 | 0.080 | [-0.060, 0.220] | 0.423950 | 1.000000 |
| baseline-react | tot-prototype | 50 | 0 | 17 | 33 | -0.340 | [-0.480, -0.220] | 1.53e-05 | 0.000107 |
| baseline-single-path | tot-prototype | 50 | 0 | 21 | 29 | -0.420 | [-0.560, -0.280] | 9.54e-07 | 9.54e-06 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
