# Structured Lockset Report

Generated UTC: 2026-02-21T19:26:18Z
Task ID: subset-sum-demo
Panel ID: subset-sum-lockset-v1
Provider: hf
Model: Qwen/Qwen2.5-Coder-32B-Instruct
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
| baseline-react | 50 | 40 | 0.800 | [0.670, 0.888] | 10469.8 | 658.0 | 336.4 |
| baseline-single-path | 50 | 18 | 0.360 | [0.241, 0.499] | 739.7 | 51.8 | 9.2 |
| tot-prototype | 50 | 32 | 0.640 | [0.501, 0.759] | 7933.3 | 1121.3 | 108.5 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | baseline-single-path | 50 | 24 | 2 | 24 | 0.440 | [0.280, 0.600] | 1.05e-05 | 3.15e-05 |
| baseline-react | tot-prototype | 50 | 13 | 5 | 32 | 0.160 | [0.000, 0.320] | 0.096252 | 0.096252 |
| baseline-single-path | tot-prototype | 50 | 4 | 18 | 28 | -0.280 | [-0.440, -0.120] | 0.004344 | 0.008687 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
