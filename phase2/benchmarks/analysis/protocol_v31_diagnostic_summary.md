# Protocol v3.1 Diagnostic Summary

Reports aggregated: 24

## Task x Model x Profile

| Task | Model | Profile | ReAct | ToT | Delta ToT-ReAct | Holm p | ReAct Lat (ms) | ToT Lat (ms) |
|---|---|---|---:|---:|---:|---:|---:|---:|
| digit-permutation-demo | Qwen/Qwen2.5-72B-Instruct | ToT self-eval (3/3/3) | 0.960 | 0.520 | -0.440 | 1.05e-05 | 7799.4 | 55906.7 |
| digit-permutation-demo | Qwen/Qwen2.5-72B-Instruct | ToT hybrid (3/3/3) | 0.960 | 0.500 | -0.460 | 2.38e-07 | 8369.4 | 61613.7 |
| digit-permutation-demo | Qwen/Qwen2.5-72B-Instruct | ToT rule-based (3/3/3) | 0.980 | 0.460 | -0.520 | 2.98e-08 | 6898.9 | 11017.4 |
| digit-permutation-demo | Qwen/Qwen2.5-72B-Instruct | ToT self-eval lite (2/2/2) | 0.980 | 0.420 | -0.560 | 7.45e-09 | 6957.1 | 17479.9 |
| digit-permutation-demo | Qwen/Qwen2.5-Coder-32B-Instruct | ToT self-eval (3/3/3) | 0.800 | 0.660 | -0.140 | 0.210040 | 6322.5 | 7564.7 |
| digit-permutation-demo | Qwen/Qwen2.5-Coder-32B-Instruct | ToT hybrid (3/3/3) | 0.780 | 0.640 | -0.140 | 0.229523 | 6618.2 | 8269.9 |
| digit-permutation-demo | Qwen/Qwen2.5-Coder-32B-Instruct | ToT rule-based (3/3/3) | 0.780 | 0.680 | -0.100 | 0.383310 | 7166.5 | 5068.0 |
| digit-permutation-demo | Qwen/Qwen2.5-Coder-32B-Instruct | ToT self-eval lite (2/2/2) | 0.840 | 0.540 | -0.300 | 0.001490 | 5842.0 | 4902.5 |
| digit-permutation-demo | Qwen/Qwen3-Coder-Next:novita | ToT self-eval (3/3/3) | 1.000 | 0.660 | -0.340 | 1.53e-05 | 3808.4 | 12677.7 |
| digit-permutation-demo | Qwen/Qwen3-Coder-Next:novita | ToT hybrid (3/3/3) | 0.960 | 0.680 | -0.280 | 0.000519 | 3869.8 | 12374.5 |
| digit-permutation-demo | Qwen/Qwen3-Coder-Next:novita | ToT rule-based (3/3/3) | 0.980 | 0.680 | -0.300 | 6.10e-05 | 3461.2 | 4507.1 |
| digit-permutation-demo | Qwen/Qwen3-Coder-Next:novita | ToT self-eval lite (2/2/2) | 0.960 | 0.600 | -0.360 | 4.01e-05 | 3770.0 | 5146.3 |
| linear2-demo | Qwen/Qwen2.5-72B-Instruct | ToT self-eval (3/3/3) | 0.980 | 0.300 | -0.680 | 1.16e-10 | 6806.6 | 75847.9 |
| linear2-demo | Qwen/Qwen2.5-72B-Instruct | ToT hybrid (3/3/3) | 1.000 | 0.360 | -0.640 | 4.66e-10 | 6492.5 | 68950.0 |
| linear2-demo | Qwen/Qwen2.5-72B-Instruct | ToT rule-based (3/3/3) | 1.000 | 0.360 | -0.640 | 4.66e-10 | 6213.8 | 19487.8 |
| linear2-demo | Qwen/Qwen2.5-72B-Instruct | ToT self-eval lite (2/2/2) | 1.000 | 0.260 | -0.740 | 1.46e-11 | 6133.2 | 22725.0 |
| linear2-demo | Qwen/Qwen2.5-Coder-32B-Instruct | ToT self-eval (3/3/3) | 0.860 | 0.340 | -0.520 | 2.16e-07 | 4322.5 | 11727.4 |
| linear2-demo | Qwen/Qwen2.5-Coder-32B-Instruct | ToT hybrid (3/3/3) | 0.880 | 0.360 | -0.520 | 2.16e-07 | 3493.5 | 11328.2 |
| linear2-demo | Qwen/Qwen2.5-Coder-32B-Instruct | ToT rule-based (3/3/3) | 0.900 | 0.300 | -0.600 | 6.94e-08 | 4593.3 | 7986.8 |
| linear2-demo | Qwen/Qwen2.5-Coder-32B-Instruct | ToT self-eval lite (2/2/2) | 0.880 | 0.320 | -0.560 | 5.77e-08 | 4325.8 | 4687.2 |
| linear2-demo | Qwen/Qwen3-Coder-Next:novita | ToT self-eval (3/3/3) | 0.940 | 0.300 | -0.640 | 4.07e-09 | 4822.4 | 17621.5 |
| linear2-demo | Qwen/Qwen3-Coder-Next:novita | ToT hybrid (3/3/3) | 0.940 | 0.360 | -0.580 | 2.98e-08 | 4862.1 | 17644.5 |
| linear2-demo | Qwen/Qwen3-Coder-Next:novita | ToT rule-based (3/3/3) | 0.980 | 0.340 | -0.640 | 4.66e-10 | 5360.7 | 10127.3 |
| linear2-demo | Qwen/Qwen3-Coder-Next:novita | ToT self-eval lite (2/2/2) | 1.000 | 0.000 | -1.000 | 1.000000 | 4085.0 | 9203.0 |

## Task x Profile (Mean Across Models)

| Task | Profile | Models | Mean ReAct | Mean ToT | Mean Delta ToT-ReAct | ToT Wins | ToT Losses |
|---|---|---:|---:|---:|---:|---:|---:|
| digit-permutation-demo | ToT hybrid (3/3/3) | 3 | 0.900 | 0.607 | -0.293 | 0 | 3 |
| digit-permutation-demo | ToT self-eval (3/3/3) | 3 | 0.920 | 0.613 | -0.307 | 0 | 3 |
| digit-permutation-demo | ToT self-eval lite (2/2/2) | 3 | 0.927 | 0.520 | -0.407 | 0 | 3 |
| digit-permutation-demo | ToT rule-based (3/3/3) | 3 | 0.913 | 0.607 | -0.307 | 0 | 3 |
| linear2-demo | ToT hybrid (3/3/3) | 3 | 0.940 | 0.360 | -0.580 | 0 | 3 |
| linear2-demo | ToT self-eval (3/3/3) | 3 | 0.927 | 0.313 | -0.613 | 0 | 3 |
| linear2-demo | ToT self-eval lite (2/2/2) | 3 | 0.960 | 0.193 | -0.767 | 0 | 3 |
| linear2-demo | ToT rule-based (3/3/3) | 3 | 0.960 | 0.333 | -0.627 | 0 | 3 |

## Best Profile Per Task x Model

| Task | Model | Best Profile | Best Delta ToT-ReAct | ToT Success | Holm p |
|---|---|---|---:|---:|---:|
| digit-permutation-demo | Qwen/Qwen2.5-72B-Instruct | ToT self-eval (3/3/3) | -0.440 | 0.520 | 1.05e-05 |
| digit-permutation-demo | Qwen/Qwen2.5-Coder-32B-Instruct | ToT rule-based (3/3/3) | -0.100 | 0.680 | 0.383310 |
| digit-permutation-demo | Qwen/Qwen3-Coder-Next:novita | ToT hybrid (3/3/3) | -0.280 | 0.680 | 0.000519 |
| linear2-demo | Qwen/Qwen2.5-72B-Instruct | ToT hybrid (3/3/3) | -0.640 | 0.360 | 4.66e-10 |
| linear2-demo | Qwen/Qwen2.5-Coder-32B-Instruct | ToT hybrid (3/3/3) | -0.520 | 0.360 | 2.16e-07 |
| linear2-demo | Qwen/Qwen3-Coder-Next:novita | ToT hybrid (3/3/3) | -0.580 | 0.360 | 2.98e-08 |
