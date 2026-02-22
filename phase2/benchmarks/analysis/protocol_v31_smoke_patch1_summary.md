# Protocol v3.1 Diagnostic Summary

Reports aggregated: 8

## Task x Model x Profile

| Task | Model | Profile | ReAct | ToT | Delta ToT-ReAct | Holm p | ReAct Lat (ms) | ToT Lat (ms) |
|---|---|---|---:|---:|---:|---:|---:|---:|
| digit-permutation-demo | Qwen/Qwen3-Coder-Next:novita | unknown | 0.900 | 0.900 | -0.000 | 1.000000 | 3723.9 | 4040.9 |
| digit-permutation-demo | Qwen/Qwen3-Coder-Next:novita | unknown | 0.900 | 0.800 | -0.100 | 1.000000 | 3803.0 | 3560.1 |
| digit-permutation-demo | Qwen/Qwen3-Coder-Next:novita | unknown | 1.000 | 0.900 | -0.100 | 1.000000 | 2749.7 | 3923.7 |
| digit-permutation-demo | Qwen/Qwen3-Coder-Next:novita | unknown | 1.000 | 0.900 | -0.100 | 1.000000 | 3028.7 | 2058.2 |
| linear2-demo | Qwen/Qwen3-Coder-Next:novita | unknown | 1.000 | 0.600 | -0.400 | 0.125000 | 4213.3 | 6894.1 |
| linear2-demo | Qwen/Qwen3-Coder-Next:novita | unknown | 1.000 | 0.500 | -0.500 | 0.062500 | 3791.6 | 4675.9 |
| linear2-demo | Qwen/Qwen3-Coder-Next:novita | unknown | 0.900 | 0.600 | -0.300 | 0.250000 | 4645.1 | 6632.2 |
| linear2-demo | Qwen/Qwen3-Coder-Next:novita | unknown | 0.900 | 0.500 | -0.400 | 0.125000 | 4470.0 | 4310.0 |

## Task x Profile (Mean Across Models)

| Task | Profile | Models | Mean ReAct | Mean ToT | Mean Delta ToT-ReAct | ToT Wins | ToT Losses |
|---|---|---:|---:|---:|---:|---:|---:|
| digit-permutation-demo | unknown | 4 | 0.950 | 0.875 | -0.075 | 0 | 3 |
| linear2-demo | unknown | 4 | 0.950 | 0.550 | -0.400 | 0 | 4 |

## Best Profile Per Task x Model

| Task | Model | Best Profile | Best Delta ToT-ReAct | ToT Success | Holm p |
|---|---|---|---:|---:|---:|
| digit-permutation-demo | Qwen/Qwen3-Coder-Next:novita | unknown | -0.000 | 0.900 | 1.000000 |
| linear2-demo | Qwen/Qwen3-Coder-Next:novita | unknown | -0.300 | 0.600 | 0.250000 |
