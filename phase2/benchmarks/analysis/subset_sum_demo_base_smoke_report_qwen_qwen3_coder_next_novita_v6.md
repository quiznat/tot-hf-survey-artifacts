# Structured Lockset Report

Generated UTC: 2026-02-23T19:15:32Z
Task ID: subset-sum-demo
Panel ID: subset-sum-lockset-v4
Provider: smolagents
Model: Qwen/Qwen3-Coder-Next:novita
ToT evaluator mode: model_self_eval
ToT mode: model_decompose_search
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
| baseline-cot | 10 | 7 | 0.700 | [0.397, 0.892] | 6498.1 | 66.2 | 178.9 |
| baseline-cot-sc | 10 | 10 | 1.000 | [0.722, 1.000] | 15355.5 | 732.0 | 2082.3 |
| baseline-react | 10 | 10 | 1.000 | [0.722, 1.000] | 5711.1 | 4878.4 | 369.0 |
| baseline-single-path | 10 | 6 | 0.600 | [0.313, 0.832] | 5198.1 | 53.2 | 2.2 |
| tot-gen | 10 | 10 | 1.000 | [0.722, 1.000] | 9419.8 | 814.7 | 105.6 |
| tot-prototype | 10 | 10 | 1.000 | [0.722, 1.000] | 10765.5 | 558.9 | 77.0 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-cot | baseline-cot-sc | 10 | 0 | 3 | 7 | -0.300 | [-0.600, 0.000] | 0.250000 | 1.000000 |
| baseline-cot | baseline-react | 10 | 0 | 3 | 7 | -0.300 | [-0.600, 0.000] | 0.250000 | 1.000000 |
| baseline-cot | baseline-single-path | 10 | 2 | 1 | 7 | 0.100 | [-0.200, 0.400] | 1.000000 | 1.000000 |
| baseline-cot | tot-gen | 10 | 0 | 3 | 7 | -0.300 | [-0.600, 0.000] | 0.250000 | 1.000000 |
| baseline-cot | tot-prototype | 10 | 0 | 3 | 7 | -0.300 | [-0.600, 0.000] | 0.250000 | 1.000000 |
| baseline-cot-sc | baseline-react | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-cot-sc | baseline-single-path | 10 | 4 | 0 | 6 | 0.400 | [0.100, 0.700] | 0.125000 | 1.000000 |
| baseline-cot-sc | tot-gen | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-cot-sc | tot-prototype | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-react | baseline-single-path | 10 | 4 | 0 | 6 | 0.400 | [0.100, 0.700] | 0.125000 | 1.000000 |
| baseline-react | tot-gen | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-react | tot-prototype | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-single-path | tot-gen | 10 | 0 | 4 | 6 | -0.400 | [-0.700, -0.100] | 0.125000 | 1.000000 |
| baseline-single-path | tot-prototype | 10 | 0 | 4 | 6 | -0.400 | [-0.700, -0.100] | 0.125000 | 1.000000 |
| tot-gen | tot-prototype | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
