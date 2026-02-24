# Structured Lockset Report

Generated UTC: 2026-02-22T17:15:57Z
Task ID: subset-sum-demo
Panel ID: subset-sum-lockset-v4
Provider: hf
Model: Qwen/Qwen3-Coder-Next:novita
ToT evaluator mode: model_self_eval
ToT search settings: depth=3, branch_factor=3, frontier_width=3
Seed policy: item_hash
HF temperature: 0.0
HF top-p: 1.0
Capability parity policy: equalize_react_to_tot
Task tools available: check_target, sum_list
Condition tools exposed: react=[none]; single=[none]; tot=[none]
Items evaluated: 10
Runs executed: 30
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-react | 10 | 5 | 0.500 | [0.237, 0.763] | 26551.5 | 717.8 | 287.4 |
| baseline-single-path | 10 | 5 | 0.500 | [0.237, 0.763] | 5241.4 | 53.2 | 1.9 |
| tot-prototype | 10 | 10 | 1.000 | [0.722, 1.000] | 26409.2 | 353.2 | 18.6 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | baseline-single-path | 10 | 3 | 3 | 4 | 0.000 | [-0.500, 0.500] | 1.000000 | 1.000000 |
| baseline-react | tot-prototype | 10 | 0 | 5 | 5 | -0.500 | [-0.800, -0.200] | 0.062500 | 0.187500 |
| baseline-single-path | tot-prototype | 10 | 0 | 5 | 5 | -0.500 | [-0.800, -0.200] | 0.062500 | 0.187500 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
