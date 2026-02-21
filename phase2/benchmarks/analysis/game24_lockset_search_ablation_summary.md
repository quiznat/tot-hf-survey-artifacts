# Game24 Lockset Search Ablation Summary (Protocol v2)

Generated UTC: 2026-02-21T17:41:24Z  
Protocol ID: `TOT-HF-P2-EPV2-2026-02-20`  
Panel ID: `game24-lockset-v1`  
Provider: `hf`  
Model: `Qwen/Qwen3-Coder-Next:novita`

## Condition Success by Search Preset

| Preset | ToT Depth | ToT Branch | ToT Frontier | Single Success | ReAct Success | ToT Success | ToT - ReAct | ToT - Single |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| primary | 3 | 3 | 3 | 0.080 | 0.440 | 0.760 | +0.320 | +0.680 |
| A1 | 2 | 3 | 3 | 0.060 | 0.360 | 0.720 | +0.360 | +0.660 |
| A2 | 3 | 4 | 4 | 0.080 | 0.420 | 0.920 | +0.500 | +0.840 |

## Paired Significance (ToT vs ReAct)

| Preset | ReAct Better | ToT Better | Ties | McNemar p | Holm p | Delta CI (ReAct - ToT) |
|---|---:|---:|---:|---:|---:|---|
| primary | 3 | 19 | 28 | 0.000855 | 0.000855 | [-0.480, -0.160] |
| A1 | 2 | 20 | 28 | 0.000121 | 0.000242 | [-0.520, -0.200] |
| A2 | 0 | 25 | 25 | 5.96e-08 | 1.19e-07 | [-0.640, -0.360] |

## Cost/Latency Snapshot (ToT Condition)

| Preset | ToT Latency Mean (ms) | ToT Tokens In Mean | ToT Tokens Out Mean |
|---|---:|---:|---:|
| primary | 58213.6 | 978.3 | 107.0 |
| A1 | 9050.9 | 636.7 | 70.8 |
| A2 | 11262.8 | 955.9 | 121.9 |

## Interpretation
- Compare presets on both success and latency/cost; a higher-success preset is not automatically preferred if latency/token inflation is disproportionate.
- Claims should remain panel/model-specific under the frozen protocol and avoid cross-task generalization.
