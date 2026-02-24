# Structured Lockset Report

Generated UTC: 2026-02-23T02:44:04Z
Task ID: game24-demo
Panel ID: game24-lockset-v4
Provider: scripted
Model: default
ToT evaluator mode: model_self_eval
ToT mode: legacy_candidate_search
ToT-gen mode: model_decompose_search
ToT decomposition rounds: 1
ToT search settings: depth=3, branch_factor=3, frontier_width=3
Seed policy: item_hash
HF temperature: 0.0
HF top-p: 1.0
Capability parity policy: equalize_react_to_tot
Task tools available: calc
Condition tools exposed: single=[none]; tot=[none]; tot_gen=[none]
Items evaluated: 1
Runs executed: 3
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-single-path | 1 | 0 | 0.000 | [0.000, 0.793] | 0.0 | 21.0 | 1.0 |
| tot-gen | 1 | 0 | 0.000 | [0.000, 0.793] | 0.0 | 823.0 | 4.0 |
| tot-prototype | 1 | 0 | 0.000 | [0.000, 0.793] | 0.0 | 510.0 | 4.0 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-single-path | tot-gen | 1 | 0 | 0 | 1 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-single-path | tot-prototype | 1 | 0 | 0 | 1 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| tot-gen | tot-prototype | 1 | 0 | 0 | 1 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
