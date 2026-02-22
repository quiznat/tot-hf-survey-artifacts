# Structured Lockset Report

Generated UTC: 2026-02-22T04:25:16Z
Task ID: linear2-demo
Panel ID: linear2-lockset-v1
Provider: hf
Model: Qwen/Qwen2.5-Coder-32B-Instruct
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
| baseline-react | 50 | 45 | 0.900 | [0.786, 0.957] | 4593.3 | 393.8 | 187.9 |
| tot-prototype | 50 | 15 | 0.300 | [0.191, 0.438] | 7986.8 | 908.9 | 102.0 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | tot-prototype | 50 | 32 | 2 | 16 | 0.600 | [0.440, 0.740] | 6.94e-08 | 6.94e-08 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
