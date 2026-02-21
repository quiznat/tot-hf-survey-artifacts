# Structured Lockset Report

Generated UTC: 2026-02-21T19:14:14Z
Task ID: game24-demo
Panel ID: game24-lockset-v1
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
| baseline-react | 50 | 3 | 0.060 | [0.021, 0.162] | 8540.8 | 688.8 | 312.8 |
| baseline-single-path | 50 | 10 | 0.200 | [0.112, 0.330] | 1754.3 | 21.0 | 48.6 |
| tot-prototype | 50 | 34 | 0.680 | [0.542, 0.792] | 7475.9 | 1195.4 | 122.1 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | baseline-single-path | 50 | 3 | 10 | 37 | -0.140 | [-0.280, 0.000] | 0.092285 | 0.092285 |
| baseline-react | tot-prototype | 50 | 0 | 31 | 19 | -0.620 | [-0.760, -0.480] | 9.31e-10 | 2.79e-09 |
| baseline-single-path | tot-prototype | 50 | 2 | 26 | 22 | -0.480 | [-0.640, -0.320] | 3.03e-06 | 6.06e-06 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
