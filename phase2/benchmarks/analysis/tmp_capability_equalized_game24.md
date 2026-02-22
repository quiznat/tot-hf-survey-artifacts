# Game24 Lockset Report

Generated UTC: 2026-02-22T05:44:56Z
Panel ID: game24-lockset-v1
Provider: scripted
Model: default
ToT evaluator mode: model_self_eval
ToT search settings: depth=3, branch_factor=3, frontier_width=3
Seed policy: item_hash
HF temperature: 0.0
HF top-p: 1.0
Capability parity policy: equalize_react_to_tot
Task tools available: calc
Condition tools exposed: react=[none]; tot=[none]
Items evaluated: 1
Runs executed: 2
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-react | 1 | 0 | 0.000 | [0.000, 0.793] | 0.0 | 147.0 | 14.0 |
| tot-prototype | 1 | 0 | 0.000 | [0.000, 0.793] | 0.0 | 510.0 | 4.0 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-react | tot-prototype | 1 | 0 | 0 | 1 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Small item slices are for protocol validation; full locksets are the primary panel summary.
