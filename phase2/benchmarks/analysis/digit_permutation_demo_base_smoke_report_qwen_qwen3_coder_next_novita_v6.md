# Structured Lockset Report

Generated UTC: 2026-02-23T19:17:56Z
Task ID: digit-permutation-demo
Panel ID: digit-permutation-lockset-v4
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
Task tools available: best_divisible, is_divisible
Condition tools exposed: cot=[none]; cot_sc=[none]; react=[none]; single=[none]; tot=[none]; tot_gen=[none]
Items evaluated: 10
Runs executed: 60
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-cot | 10 | 6 | 0.600 | [0.313, 0.832] | 5892.6 | 41.0 | 267.4 |
| baseline-cot-sc | 10 | 6 | 0.600 | [0.313, 0.832] | 8614.8 | 480.0 | 2667.4 |
| baseline-react | 10 | 10 | 1.000 | [0.722, 1.000] | 6833.5 | 3050.0 | 393.8 |
| baseline-single-path | 10 | 6 | 0.600 | [0.313, 0.832] | 6476.9 | 28.0 | 203.7 |
| tot-gen | 10 | 10 | 1.000 | [0.722, 1.000] | 5909.0 | 455.5 | 79.5 |
| tot-prototype | 10 | 10 | 1.000 | [0.722, 1.000] | 7338.7 | 376.9 | 60.1 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-cot | baseline-cot-sc | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-cot | baseline-react | 10 | 0 | 4 | 6 | -0.400 | [-0.700, -0.100] | 0.125000 | 1.000000 |
| baseline-cot | baseline-single-path | 10 | 1 | 1 | 8 | 0.000 | [-0.300, 0.300] | 1.000000 | 1.000000 |
| baseline-cot | tot-gen | 10 | 0 | 4 | 6 | -0.400 | [-0.700, -0.100] | 0.125000 | 1.000000 |
| baseline-cot | tot-prototype | 10 | 0 | 4 | 6 | -0.400 | [-0.700, -0.100] | 0.125000 | 1.000000 |
| baseline-cot-sc | baseline-react | 10 | 0 | 4 | 6 | -0.400 | [-0.700, -0.100] | 0.125000 | 1.000000 |
| baseline-cot-sc | baseline-single-path | 10 | 1 | 1 | 8 | 0.000 | [-0.300, 0.300] | 1.000000 | 1.000000 |
| baseline-cot-sc | tot-gen | 10 | 0 | 4 | 6 | -0.400 | [-0.700, -0.100] | 0.125000 | 1.000000 |
| baseline-cot-sc | tot-prototype | 10 | 0 | 4 | 6 | -0.400 | [-0.700, -0.100] | 0.125000 | 1.000000 |
| baseline-react | baseline-single-path | 10 | 4 | 0 | 6 | 0.400 | [0.100, 0.700] | 0.125000 | 1.000000 |
| baseline-react | tot-gen | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-react | tot-prototype | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-single-path | tot-gen | 10 | 0 | 4 | 6 | -0.400 | [-0.700, -0.100] | 0.125000 | 1.000000 |
| baseline-single-path | tot-prototype | 10 | 0 | 4 | 6 | -0.400 | [-0.700, -0.100] | 0.125000 | 1.000000 |
| tot-gen | tot-prototype | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
