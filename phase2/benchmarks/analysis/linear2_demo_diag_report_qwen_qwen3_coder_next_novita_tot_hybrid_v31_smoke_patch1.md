# Structured Lockset Report

Generated UTC: 2026-02-22T04:46:46Z
Task ID: linear2-demo
Panel ID: linear2-lockset-v1
Provider: hf
Model: Qwen/Qwen3-Coder-Next:novita
ToT evaluator mode: hybrid
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
| baseline-react | 10 | 10 | 1.000 | [0.722, 1.000] | 4213.3 | 334.3 | 214.6 |
| tot-prototype | 10 | 6 | 0.600 | [0.313, 0.832] | 6894.1 | 452.4 | 12.2 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | tot-prototype | 10 | 4 | 0 | 6 | 0.400 | [0.100, 0.700] | 0.125000 | 0.125000 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
