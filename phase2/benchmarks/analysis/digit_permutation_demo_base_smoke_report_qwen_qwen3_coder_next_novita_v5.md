# Structured Lockset Report

Generated UTC: 2026-02-23T03:38:07Z
Task ID: digit-permutation-demo
Panel ID: digit-permutation-lockset-v4
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
Task tools available: best_divisible, is_divisible
Condition tools exposed: cot=[none]; cot_sc=[none]; react=[none]; single=[none]; tot=[none]; tot_gen=[none]
Items evaluated: 10
Runs executed: 60
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-cot | 10 | 6 | 0.600 | [0.313, 0.832] | 7021.2 | 41.0 | 266.2 |
| baseline-cot-sc | 10 | 6 | 0.600 | [0.313, 0.832] | 79578.7 | 480.0 | 2603.3 |
| baseline-react | 10 | 10 | 1.000 | [0.722, 1.000] | 7274.7 | 52.0 | 152.7 |
| baseline-single-path | 10 | 7 | 0.700 | [0.397, 0.892] | 9872.3 | 28.0 | 188.7 |
| tot-gen | 10 | 10 | 1.000 | [0.722, 1.000] | 25430.1 | 374.3 | 57.8 |
| tot-prototype | 10 | 10 | 1.000 | [0.722, 1.000] | 15513.3 | 202.0 | 6.6 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-cot | baseline-cot-sc | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-cot | baseline-react | 10 | 0 | 4 | 6 | -0.400 | [-0.700, -0.100] | 0.125000 | 1.000000 |
| baseline-cot | baseline-single-path | 10 | 1 | 2 | 7 | -0.100 | [-0.400, 0.200] | 1.000000 | 1.000000 |
| baseline-cot | tot-gen | 10 | 0 | 4 | 6 | -0.400 | [-0.700, -0.100] | 0.125000 | 1.000000 |
| baseline-cot | tot-prototype | 10 | 0 | 4 | 6 | -0.400 | [-0.700, -0.100] | 0.125000 | 1.000000 |
| baseline-cot-sc | baseline-react | 10 | 0 | 4 | 6 | -0.400 | [-0.700, -0.100] | 0.125000 | 1.000000 |
| baseline-cot-sc | baseline-single-path | 10 | 1 | 2 | 7 | -0.100 | [-0.400, 0.200] | 1.000000 | 1.000000 |
| baseline-cot-sc | tot-gen | 10 | 0 | 4 | 6 | -0.400 | [-0.700, -0.100] | 0.125000 | 1.000000 |
| baseline-cot-sc | tot-prototype | 10 | 0 | 4 | 6 | -0.400 | [-0.700, -0.100] | 0.125000 | 1.000000 |
| baseline-react | baseline-single-path | 10 | 3 | 0 | 7 | 0.300 | [0.000, 0.600] | 0.250000 | 1.000000 |
| baseline-react | tot-gen | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-react | tot-prototype | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-single-path | tot-gen | 10 | 0 | 3 | 7 | -0.300 | [-0.600, -0.100] | 0.250000 | 1.000000 |
| baseline-single-path | tot-prototype | 10 | 0 | 3 | 7 | -0.300 | [-0.600, 0.000] | 0.250000 | 1.000000 |
| tot-gen | tot-prototype | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
