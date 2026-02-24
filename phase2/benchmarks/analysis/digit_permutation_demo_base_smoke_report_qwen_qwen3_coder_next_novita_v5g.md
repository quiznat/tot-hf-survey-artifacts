# Structured Lockset Report

Generated UTC: 2026-02-23T02:00:30Z
Task ID: digit-permutation-demo
Panel ID: digit-permutation-lockset-v4
Provider: hf
Model: Qwen/Qwen3-Coder-Next:novita
ToT evaluator mode: rule_based
ToT mode: model_decompose_search
ToT decomposition rounds: 1
ToT search settings: depth=3, branch_factor=3, frontier_width=3
Seed policy: item_hash
HF temperature: 0.0
HF top-p: 1.0
Capability parity policy: equalize_react_to_tot
Task tools available: best_divisible, is_divisible
Condition tools exposed: cot=[none]; cot_sc=[none]; react=[none]; single=[none]; tot=[none]
Items evaluated: 10
Runs executed: 50
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-cot | 10 | 0 | 0.000 | [0.000, 0.278] | 2201.2 | 41.0 | 117.8 |
| baseline-cot-sc | 10 | 0 | 0.000 | [0.000, 0.278] | 16977.3 | 240.0 | 594.8 |
| baseline-react | 10 | 10 | 1.000 | [0.722, 1.000] | 13915.4 | 396.3 | 218.2 |
| baseline-single-path | 10 | 2 | 0.200 | [0.057, 0.510] | 2327.5 | 28.0 | 96.4 |
| tot-prototype | 10 | 10 | 1.000 | [0.722, 1.000] | 10642.2 | 330.7 | 111.2 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-cot | baseline-cot-sc | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-cot | baseline-react | 10 | 0 | 10 | 0 | -1.000 | [-1.000, -1.000] | 0.001953 | 0.019531 |
| baseline-cot | baseline-single-path | 10 | 0 | 2 | 8 | -0.200 | [-0.500, 0.000] | 0.500000 | 1.000000 |
| baseline-cot | tot-prototype | 10 | 0 | 10 | 0 | -1.000 | [-1.000, -1.000] | 0.001953 | 0.019531 |
| baseline-cot-sc | baseline-react | 10 | 0 | 10 | 0 | -1.000 | [-1.000, -1.000] | 0.001953 | 0.019531 |
| baseline-cot-sc | baseline-single-path | 10 | 0 | 2 | 8 | -0.200 | [-0.500, 0.000] | 0.500000 | 1.000000 |
| baseline-cot-sc | tot-prototype | 10 | 0 | 10 | 0 | -1.000 | [-1.000, -1.000] | 0.001953 | 0.019531 |
| baseline-react | baseline-single-path | 10 | 8 | 0 | 2 | 0.800 | [0.500, 1.000] | 0.007812 | 0.046875 |
| baseline-react | tot-prototype | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-single-path | tot-prototype | 10 | 0 | 8 | 2 | -0.800 | [-1.000, -0.500] | 0.007812 | 0.046875 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
