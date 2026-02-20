# Game24 Lockset Matrix Summary (Protocol v2)

Models are fixed and evaluated on paired 50-item locksets (`single`, `react`, `tot model_self_eval`).

| Model | Single | ReAct | ToT | Δ ToT-ReAct | Holm p (ToT-ReAct) | Δ ToT-Single | Holm p (ToT-Single) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Qwen/Qwen3-Coder-Next:novita | 0.080 | 0.440 | 0.760 | +0.320 | 8.55e-04 | +0.680 | 3.49e-10 |
| Qwen/Qwen2.5-72B-Instruct | 0.160 | 0.020 | 0.580 | +0.560 | 2.24e-08 | +0.420 | 3.89e-05 |
| Qwen/Qwen2.5-Coder-32B-Instruct | 0.180 | 0.060 | 0.680 | +0.620 | 2.79e-09 | +0.500 | 9.30e-06 |

| Model | Mean Latency Single (ms) | Mean Latency ReAct (ms) | Mean Latency ToT (ms) |
|---|---:|---:|---:|
| Qwen/Qwen3-Coder-Next:novita | 5430.3 | 20854.2 | 58213.6 |
| Qwen/Qwen2.5-72B-Instruct | 1317.5 | 12369.2 | 30015.1 |
| Qwen/Qwen2.5-Coder-32B-Instruct | 1412.9 | 6618.3 | 6527.7 |
