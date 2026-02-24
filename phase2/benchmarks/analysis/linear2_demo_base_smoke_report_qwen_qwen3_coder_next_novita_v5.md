# Structured Lockset Report

Generated UTC: 2026-02-23T03:33:03Z
Task ID: linear2-demo
Panel ID: linear2-lockset-v4
Provider: hf
Model: Qwen/Qwen3-Coder-Next:novita
ToT evaluator mode: model_self_eval
ToT mode: legacy_candidate_search
ToT-gen mode: model_decompose_search
ToT decomposition rounds: 1
ToT search settings: depth=4, branch_factor=3, frontier_width=3
ToT per-condition depth overrides: legacy=base, gen=base
Seed policy: item_hash
HF temperature: 0.0
CoT temperature: 0.0
CoT-SC temperature: 0.7
ReAct temperature: 0.0
HF top-p: 1.0
Capability parity policy: equalize_react_to_tot
Task tools available: check_xy, solve2
Condition tools exposed: cot=[none]; cot_sc=[none]; react=[none]; single=[none]; tot=[none]; tot_gen=[none]
Items evaluated: 10
Runs executed: 60
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-cot | 10 | 10 | 1.000 | [0.722, 1.000] | 10459.2 | 43.0 | 145.3 |
| baseline-cot-sc | 10 | 10 | 1.000 | [0.722, 1.000] | 95173.2 | 500.0 | 1514.6 |
| baseline-react | 10 | 10 | 1.000 | [0.722, 1.000] | 5524.7 | 50.0 | 133.9 |
| baseline-single-path | 10 | 10 | 1.000 | [0.722, 1.000] | 5391.2 | 30.0 | 121.0 |
| tot-gen | 10 | 10 | 1.000 | [0.722, 1.000] | 32531.5 | 844.4 | 95.1 |
| tot-prototype | 10 | 6 | 0.600 | [0.313, 0.832] | 79618.4 | 798.1 | 21.5 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-cot | baseline-cot-sc | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-cot | baseline-react | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-cot | baseline-single-path | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-cot | tot-gen | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-cot | tot-prototype | 10 | 4 | 0 | 6 | 0.400 | [0.100, 0.700] | 0.125000 | 1.000000 |
| baseline-cot-sc | baseline-react | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-cot-sc | baseline-single-path | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-cot-sc | tot-gen | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-cot-sc | tot-prototype | 10 | 4 | 0 | 6 | 0.400 | [0.100, 0.700] | 0.125000 | 1.000000 |
| baseline-react | baseline-single-path | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-react | tot-gen | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-react | tot-prototype | 10 | 4 | 0 | 6 | 0.400 | [0.100, 0.700] | 0.125000 | 1.000000 |
| baseline-single-path | tot-gen | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-single-path | tot-prototype | 10 | 4 | 0 | 6 | 0.400 | [0.100, 0.700] | 0.125000 | 1.000000 |
| tot-gen | tot-prototype | 10 | 4 | 0 | 6 | 0.400 | [0.100, 0.700] | 0.125000 | 1.000000 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
