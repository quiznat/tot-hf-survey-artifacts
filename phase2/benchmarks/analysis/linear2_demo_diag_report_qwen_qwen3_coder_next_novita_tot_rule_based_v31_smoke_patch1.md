# Structured Lockset Report

Generated UTC: 2026-02-22T04:47:04Z
Task ID: linear2-demo
Panel ID: linear2-lockset-v1
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
| baseline-react | 10 | 9 | 0.900 | [0.596, 0.982] | 4470.0 | 461.5 | 237.7 |
| tot-prototype | 10 | 5 | 0.500 | [0.237, 0.763] | 4310.0 | 328.6 | 9.4 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | tot-prototype | 10 | 4 | 0 | 6 | 0.400 | [0.100, 0.700] | 0.125000 | 0.125000 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
