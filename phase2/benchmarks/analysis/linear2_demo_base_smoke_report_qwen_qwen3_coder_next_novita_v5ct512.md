# Structured Lockset Report

Generated UTC: 2026-02-23T02:22:00Z
Task ID: linear2-demo
Panel ID: linear2-lockset-v4
Provider: hf
Model: Qwen/Qwen3-Coder-Next:novita
ToT evaluator mode: model_self_eval
ToT mode: model_decompose_search
ToT decomposition rounds: 1
ToT search settings: depth=3, branch_factor=3, frontier_width=3
Seed policy: item_hash
HF temperature: 0.0
HF top-p: 1.0
Capability parity policy: equalize_react_to_tot
Task tools available: check_xy, solve2
Condition tools exposed: cot=[none]; cot_sc=[none]; react=[check_xy, solve2]; single=[none]
Items evaluated: 10
Runs executed: 40
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-cot | 10 | 10 | 1.000 | [0.722, 1.000] | 8205.8 | 43.0 | 143.0 |
| baseline-cot-sc | 10 | 10 | 1.000 | [0.722, 1.000] | 35359.0 | 250.0 | 713.7 |
| baseline-react | 10 | 10 | 1.000 | [0.722, 1.000] | 14326.5 | 229.4 | 228.5 |
| baseline-single-path | 10 | 10 | 1.000 | [0.722, 1.000] | 7589.3 | 30.0 | 116.5 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-cot | baseline-cot-sc | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-cot | baseline-react | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-cot | baseline-single-path | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-cot-sc | baseline-react | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-cot-sc | baseline-single-path | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-react | baseline-single-path | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
