# Structured Lockset Report

Generated UTC: 2026-02-22T04:25:15Z
Task ID: linear2-demo
Panel ID: linear2-lockset-v1
Provider: hf
Model: Qwen/Qwen3-Coder-Next:novita
ToT evaluator mode: model_self_eval
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
| baseline-react | 50 | 47 | 0.940 | [0.838, 0.979] | 4822.4 | 380.1 | 230.2 |
| tot-prototype | 50 | 15 | 0.300 | [0.191, 0.438] | 17621.5 | 1571.2 | 85.2 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | tot-prototype | 50 | 33 | 1 | 16 | 0.640 | [0.500, 0.780] | 4.07e-09 | 4.07e-09 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
