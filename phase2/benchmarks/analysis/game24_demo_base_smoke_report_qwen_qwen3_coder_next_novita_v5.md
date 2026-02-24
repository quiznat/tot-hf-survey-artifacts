# Structured Lockset Report

Generated UTC: 2026-02-23T03:16:38Z
Task ID: game24-demo
Panel ID: game24-lockset-v4
Provider: hf
Model: Qwen/Qwen3-Coder-Next:novita
ToT evaluator mode: model_self_eval
ToT mode: legacy_candidate_search
ToT-gen mode: model_decompose_search
ToT decomposition rounds: 1
ToT search settings: depth=4, branch_factor=3, frontier_width=3
ToT per-condition depth overrides: legacy=base, gen=base
Seed policy: item_hash
HF temperature: 0.0
CoT temperature: 0.0
CoT-SC temperature: 0.7
ReAct temperature: 0.0
HF top-p: 1.0
Capability parity policy: equalize_react_to_tot
Task tools available: calc
Condition tools exposed: cot=[none]; cot_sc=[none]; react=[none]; single=[none]; tot=[none]; tot_gen=[none]
Items evaluated: 10
Runs executed: 60
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-cot | 10 | 2 | 0.200 | [0.057, 0.510] | 15723.4 | 34.0 | 238.4 |
| baseline-cot-sc | 10 | 0 | 0.000 | [0.000, 0.278] | 80533.0 | 410.0 | 2269.0 |
| baseline-react | 10 | 1 | 0.100 | [0.018, 0.404] | 8330.0 | 271.1 | 253.1 |
| baseline-single-path | 10 | 3 | 0.300 | [0.108, 0.603] | 15989.7 | 21.0 | 19.3 |
| tot-gen | 10 | 8 | 0.800 | [0.490, 0.943] | 91032.6 | 12606.4 | 571.3 |
| tot-prototype | 10 | 8 | 0.800 | [0.490, 0.943] | 65645.9 | 1198.7 | 140.4 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-cot | baseline-cot-sc | 10 | 2 | 0 | 8 | 0.200 | [0.000, 0.500] | 0.500000 | 1.000000 |
| baseline-cot | baseline-react | 10 | 2 | 1 | 7 | 0.100 | [-0.200, 0.400] | 1.000000 | 1.000000 |
| baseline-cot | baseline-single-path | 10 | 1 | 2 | 7 | -0.100 | [-0.400, 0.200] | 1.000000 | 1.000000 |
| baseline-cot | tot-gen | 10 | 0 | 6 | 4 | -0.600 | [-0.900, -0.300] | 0.031250 | 0.343750 |
| baseline-cot | tot-prototype | 10 | 0 | 6 | 4 | -0.600 | [-0.900, -0.300] | 0.031250 | 0.343750 |
| baseline-cot-sc | baseline-react | 10 | 0 | 1 | 9 | -0.100 | [-0.300, 0.000] | 1.000000 | 1.000000 |
| baseline-cot-sc | baseline-single-path | 10 | 0 | 3 | 7 | -0.300 | [-0.600, -0.100] | 0.250000 | 1.000000 |
| baseline-cot-sc | tot-gen | 10 | 0 | 8 | 2 | -0.800 | [-1.000, -0.500] | 0.007812 | 0.117188 |
| baseline-cot-sc | tot-prototype | 10 | 0 | 8 | 2 | -0.800 | [-1.000, -0.500] | 0.007812 | 0.117188 |
| baseline-react | baseline-single-path | 10 | 0 | 2 | 8 | -0.200 | [-0.500, 0.000] | 0.500000 | 1.000000 |
| baseline-react | tot-gen | 10 | 0 | 7 | 3 | -0.700 | [-0.900, -0.400] | 0.015625 | 0.203125 |
| baseline-react | tot-prototype | 10 | 0 | 7 | 3 | -0.700 | [-1.000, -0.400] | 0.015625 | 0.203125 |
| baseline-single-path | tot-gen | 10 | 1 | 6 | 3 | -0.500 | [-0.900, -0.100] | 0.125000 | 1.000000 |
| baseline-single-path | tot-prototype | 10 | 1 | 6 | 3 | -0.500 | [-0.900, -0.100] | 0.125000 | 1.000000 |
| tot-gen | tot-prototype | 10 | 1 | 1 | 8 | 0.000 | [-0.300, 0.300] | 1.000000 | 1.000000 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
