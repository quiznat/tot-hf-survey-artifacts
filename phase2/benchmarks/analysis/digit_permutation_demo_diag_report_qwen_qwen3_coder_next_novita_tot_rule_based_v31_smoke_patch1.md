# Structured Lockset Report

Generated UTC: 2026-02-22T04:48:13Z
Task ID: digit-permutation-demo
Panel ID: digit-permutation-lockset-v1
Provider: hf
Model: Qwen/Qwen3-Coder-Next:novita
ToT evaluator mode: rule_based
ToT search settings: depth=3, branch_factor=3, frontier_width=3
Seed policy: item_hash
HF temperature: 0.0
HF top-p: 1.0
Items evaluated: 10
Runs executed: 20
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-react | 10 | 10 | 1.000 | [0.722, 1.000] | 3028.7 | 195.3 | 164.6 |
| tot-prototype | 10 | 9 | 0.900 | [0.596, 0.982] | 2058.2 | 167.6 | 6.9 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | tot-prototype | 10 | 1 | 0 | 9 | 0.100 | [0.000, 0.300] | 1.000000 | 1.000000 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
