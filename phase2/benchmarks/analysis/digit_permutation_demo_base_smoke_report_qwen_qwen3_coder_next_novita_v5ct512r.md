# Structured Lockset Report

Generated UTC: 2026-02-23T02:33:26Z
Task ID: digit-permutation-demo
Panel ID: digit-permutation-lockset-v4
Provider: hf
Model: Qwen/Qwen3-Coder-Next:novita
ToT evaluator mode: model_self_eval
ToT mode: model_decompose_search
ToT decomposition rounds: 1
ToT search settings: depth=3, branch_factor=3, frontier_width=3
Seed policy: item_hash
HF temperature: 0.0
HF top-p: 1.0
Capability parity policy: equalize_react_to_tot
Task tools available: best_divisible, is_divisible
Condition tools exposed: cot=[none]; cot_sc=[none]; react=[best_divisible, is_divisible]; single=[none]
Items evaluated: 10
Runs executed: 40
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-cot | 10 | 9 | 0.900 | [0.596, 0.982] | 8522.9 | 209.3 | 269.1 |
| baseline-cot-sc | 10 | 8 | 0.800 | [0.490, 0.943] | 42807.8 | 1072.0 | 1317.0 |
| baseline-react | 10 | 10 | 1.000 | [0.722, 1.000] | 8329.0 | 181.8 | 186.8 |
| baseline-single-path | 10 | 6 | 0.600 | [0.313, 0.832] | 6999.3 | 28.0 | 200.2 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-cot | baseline-cot-sc | 10 | 1 | 0 | 9 | 0.100 | [0.000, 0.300] | 1.000000 | 1.000000 |
| baseline-cot | baseline-react | 10 | 0 | 1 | 9 | -0.100 | [-0.300, 0.000] | 1.000000 | 1.000000 |
| baseline-cot | baseline-single-path | 10 | 3 | 0 | 7 | 0.300 | [0.000, 0.600] | 0.250000 | 1.000000 |
| baseline-cot-sc | baseline-react | 10 | 0 | 2 | 8 | -0.200 | [-0.500, 0.000] | 0.500000 | 1.000000 |
| baseline-cot-sc | baseline-single-path | 10 | 3 | 1 | 6 | 0.200 | [-0.200, 0.600] | 0.625000 | 1.000000 |
| baseline-react | baseline-single-path | 10 | 4 | 0 | 6 | 0.400 | [0.100, 0.700] | 0.125000 | 0.750000 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
