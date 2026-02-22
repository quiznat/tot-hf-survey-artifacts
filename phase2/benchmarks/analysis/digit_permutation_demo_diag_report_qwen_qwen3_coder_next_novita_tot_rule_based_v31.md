# Structured Lockset Report

Generated UTC: 2026-02-22T04:25:17Z
Task ID: digit-permutation-demo
Panel ID: digit-permutation-lockset-v1
Provider: hf
Model: Qwen/Qwen3-Coder-Next:novita
ToT evaluator mode: rule_based
ToT search settings: depth=3, branch_factor=3, frontier_width=3
Seed policy: item_hash
HF temperature: 0.0
HF top-p: 1.0
Items evaluated: 50
Runs executed: 100
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-react | 50 | 49 | 0.980 | [0.895, 0.996] | 3461.2 | 223.9 | 185.4 |
| tot-prototype | 50 | 34 | 0.680 | [0.542, 0.792] | 4507.1 | 613.9 | 64.8 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | tot-prototype | 50 | 15 | 0 | 35 | 0.300 | [0.180, 0.420] | 6.10e-05 | 6.10e-05 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
