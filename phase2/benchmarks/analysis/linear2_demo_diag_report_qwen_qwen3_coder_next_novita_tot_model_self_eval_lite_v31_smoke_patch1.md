# Structured Lockset Report

Generated UTC: 2026-02-22T04:47:18Z
Task ID: linear2-demo
Panel ID: linear2-lockset-v1
Provider: hf
Model: Qwen/Qwen3-Coder-Next:novita
ToT evaluator mode: model_self_eval
ToT search settings: depth=2, branch_factor=2, frontier_width=2
Seed policy: item_hash
HF temperature: 0.0
HF top-p: 1.0
Items evaluated: 10
Runs executed: 20
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-react | 10 | 10 | 1.000 | [0.722, 1.000] | 3791.6 | 291.5 | 187.1 |
| tot-prototype | 10 | 5 | 0.500 | [0.237, 0.763] | 4675.9 | 319.1 | 6.9 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | tot-prototype | 10 | 5 | 0 | 5 | 0.500 | [0.200, 0.800] | 0.062500 | 0.062500 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
