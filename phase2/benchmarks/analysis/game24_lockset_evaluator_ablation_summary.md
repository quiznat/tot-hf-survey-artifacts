# Game24 Lockset Evaluator Ablation Summary (Protocol v2)

Generated UTC: 2026-02-21T02:59:06Z  
Protocol ID: `TOT-HF-P2-EPV2-2026-02-20`  
Panel ID: `game24-lockset-v1`  
Provider: `hf`  
Model: `Qwen/Qwen3-Coder-Next:novita`  
Items per condition: 50

## Condition Success by Evaluator Mode

| Evaluator Mode | Single Success | ReAct Success | ToT Success | ToT - ReAct | ToT - Single |
|---|---:|---:|---:|---:|---:|
| `model_self_eval` | 0.080 | 0.440 | 0.760 | +0.320 | +0.680 |
| `rule_based` | 0.080 | 0.420 | 0.860 | +0.440 | +0.780 |
| `hybrid` | 0.080 | 0.420 | 0.780 | +0.360 | +0.700 |

## Paired Significance (ToT vs ReAct)

| Evaluator Mode | A Better (ReAct) | B Better (ToT) | Ties | McNemar p | Holm p | Delta CI (ReAct - ToT) |
|---|---:|---:|---:|---:|---:|---|
| `model_self_eval` | 3 | 19 | 28 | 8.55e-04 | 8.55e-04 | [-0.480, -0.160] |
| `rule_based` | 3 | 25 | 22 | 2.74e-05 | 5.49e-05 | [-0.600, -0.280] |
| `hybrid` | 1 | 19 | 30 | 4.01e-05 | 8.01e-05 | [-0.500, -0.220] |

## Cost/Latency Snapshot (ToT Condition)

| Evaluator Mode | ToT Latency Mean (ms) | ToT Tokens In Mean | ToT Tokens Out Mean |
|---|---:|---:|---:|
| `model_self_eval` | 58213.6 | 978.3 | 107.0 |
| `rule_based` | 5374.7 | 516.7 | 89.7 |
| `hybrid` | 14485.5 | 935.8 | 104.6 |

## Interpretation
- ToT outperforms both baselines under all three evaluator modes on the fixed paired panel.
- The strongest absolute ToT success rate appears in `rule_based`, but this mode remains a control/diagnostic condition and is not the primary methodology claim path.
- `model_self_eval` remains the primary in-chain methodology for Phase 2, with ablations reported as robustness checks.
