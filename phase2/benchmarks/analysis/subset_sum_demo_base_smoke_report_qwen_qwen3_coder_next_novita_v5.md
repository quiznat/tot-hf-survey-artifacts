# Structured Lockset Report

Generated UTC: 2026-02-23T03:25:17Z
Task ID: subset-sum-demo
Panel ID: subset-sum-lockset-v4
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
Task tools available: check_target, sum_list
Condition tools exposed: cot=[none]; cot_sc=[none]; react=[none]; single=[none]; tot=[none]; tot_gen=[none]
Items evaluated: 10
Runs executed: 60
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-cot | 10 | 8 | 0.800 | [0.490, 0.943] | 7404.5 | 66.2 | 175.4 |
| baseline-cot-sc | 10 | 9 | 0.900 | [0.596, 0.982] | 79124.3 | 732.0 | 2058.1 |
| baseline-react | 10 | 7 | 0.700 | [0.397, 0.892] | 6759.3 | 82.4 | 159.8 |
| baseline-single-path | 10 | 5 | 0.500 | [0.237, 0.763] | 2688.4 | 53.2 | 1.9 |
| tot-gen | 10 | 10 | 1.000 | [0.722, 1.000] | 19763.3 | 483.3 | 64.5 |
| tot-prototype | 10 | 10 | 1.000 | [0.722, 1.000] | 25476.7 | 382.8 | 61.8 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-cot | baseline-cot-sc | 10 | 0 | 1 | 9 | -0.100 | [-0.300, 0.000] | 1.000000 | 1.000000 |
| baseline-cot | baseline-react | 10 | 3 | 2 | 5 | 0.100 | [-0.300, 0.500] | 1.000000 | 1.000000 |
| baseline-cot | baseline-single-path | 10 | 4 | 1 | 5 | 0.300 | [-0.100, 0.700] | 0.375000 | 1.000000 |
| baseline-cot | tot-gen | 10 | 0 | 2 | 8 | -0.200 | [-0.500, 0.000] | 0.500000 | 1.000000 |
| baseline-cot | tot-prototype | 10 | 0 | 2 | 8 | -0.200 | [-0.500, 0.000] | 0.500000 | 1.000000 |
| baseline-cot-sc | baseline-react | 10 | 3 | 1 | 6 | 0.200 | [-0.200, 0.600] | 0.625000 | 1.000000 |
| baseline-cot-sc | baseline-single-path | 10 | 4 | 0 | 6 | 0.400 | [0.100, 0.700] | 0.125000 | 1.000000 |
| baseline-cot-sc | tot-gen | 10 | 0 | 1 | 9 | -0.100 | [-0.300, 0.000] | 1.000000 | 1.000000 |
| baseline-cot-sc | tot-prototype | 10 | 0 | 1 | 9 | -0.100 | [-0.300, 0.000] | 1.000000 | 1.000000 |
| baseline-react | baseline-single-path | 10 | 4 | 2 | 4 | 0.200 | [-0.300, 0.600] | 0.687500 | 1.000000 |
| baseline-react | tot-gen | 10 | 0 | 3 | 7 | -0.300 | [-0.600, 0.000] | 0.250000 | 1.000000 |
| baseline-react | tot-prototype | 10 | 0 | 3 | 7 | -0.300 | [-0.600, 0.000] | 0.250000 | 1.000000 |
| baseline-single-path | tot-gen | 10 | 0 | 5 | 5 | -0.500 | [-0.800, -0.200] | 0.062500 | 0.937500 |
| baseline-single-path | tot-prototype | 10 | 0 | 5 | 5 | -0.500 | [-0.800, -0.200] | 0.062500 | 0.937500 |
| tot-gen | tot-prototype | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
