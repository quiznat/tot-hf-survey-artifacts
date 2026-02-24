# Structured Lockset Report

Generated UTC: 2026-02-23T01:46:53Z
Task ID: linear2-demo
Panel ID: linear2-lockset-v4
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
Task tools available: check_xy, solve2
Condition tools exposed: react=[none]; tot=[none]
Items evaluated: 10
Runs executed: 20
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-react | 10 | 8 | 0.800 | [0.490, 0.943] | 15109.4 | 369.7 | 208.4 |
| tot-prototype | 10 | 10 | 1.000 | [0.722, 1.000] | 16741.1 | 706.2 | 131.6 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | tot-prototype | 10 | 0 | 2 | 8 | -0.200 | [-0.500, 0.000] | 0.500000 | 0.500000 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
