# Structured Lockset Report

Generated UTC: 2026-02-21T19:24:05Z
Task ID: subset-sum-demo
Panel ID: subset-sum-lockset-v1
Provider: hf
Model: Qwen/Qwen2.5-72B-Instruct
ToT evaluator mode: model_self_eval
ToT search settings: depth=3, branch_factor=3, frontier_width=3
Seed policy: item_hash
HF temperature: 0.0
HF top-p: 1.0
Items evaluated: 50
Runs executed: 150
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-react | 50 | 20 | 0.400 | [0.276, 0.538] | 23239.8 | 793.8 | 344.5 |
| baseline-single-path | 50 | 23 | 0.460 | [0.330, 0.596] | 1223.4 | 51.8 | 1.5 |
| tot-prototype | 50 | 36 | 0.720 | [0.583, 0.825] | 29233.6 | 789.0 | 271.5 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | baseline-single-path | 50 | 9 | 12 | 29 | -0.060 | [-0.240, 0.120] | 0.663624 | 0.663624 |
| baseline-react | tot-prototype | 50 | 5 | 21 | 24 | -0.320 | [-0.500, -0.140] | 0.002494 | 0.007482 |
| baseline-single-path | tot-prototype | 50 | 5 | 18 | 27 | -0.260 | [-0.440, -0.080] | 0.010622 | 0.021244 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
