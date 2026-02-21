# Protocol v3 Submission Tables and Figure Data

Generated from `protocol_v3_matrix_summary.json`.

## Table S1: Task x Model Matrix

| Task | Model | Single | ReAct | ToT | Delta ToT-ReAct | Holm p | Delta ToT-Single | Holm p | ToT Latency (ms) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| digit-permutation-demo | Qwen/Qwen2.5-72B-Instruct | 0.400 | 0.960 | 0.480 | -0.480 | 1.61e-06 | 0.080 | 0.289062 | 56404.9 |
| digit-permutation-demo | Qwen/Qwen2.5-Coder-32B-Instruct | 0.000 | 0.780 | 0.660 | -0.120 | 0.307456 | 0.660 | 4.66e-10 | 10124.4 |
| digit-permutation-demo | Qwen/Qwen3-Coder-Next:novita | 0.060 | 0.980 | 0.720 | -0.260 | 0.000977 | 0.660 | 4.66e-10 | 11055.2 |
| game24-demo | Qwen/Qwen2.5-72B-Instruct | 0.160 | 0.040 | 0.660 | 0.620 | 2.37e-08 | 0.500 | 1.19e-07 | 27282.9 |
| game24-demo | Qwen/Qwen2.5-Coder-32B-Instruct | 0.200 | 0.060 | 0.680 | 0.620 | 2.79e-09 | 0.480 | 6.06e-06 | 7475.9 |
| game24-demo | Qwen/Qwen3-Coder-Next:novita | 0.060 | 0.400 | 0.880 | 0.480 | 2.38e-07 | 0.820 | 2.73e-12 | 9661.7 |
| linear2-demo | Qwen/Qwen2.5-72B-Instruct | 0.360 | 1.000 | 0.380 | -0.620 | 1.86e-09 | 0.020 | 1.000000 | 64887.9 |
| linear2-demo | Qwen/Qwen2.5-Coder-32B-Instruct | 0.140 | 0.860 | 0.320 | -0.540 | 9.26e-07 | 0.180 | 0.011719 | 14588.3 |
| linear2-demo | Qwen/Qwen3-Coder-Next:novita | 0.020 | 0.940 | 0.340 | -0.600 | 3.07e-08 | 0.320 | 3.05e-05 | 16053.2 |
| subset-sum-demo | Qwen/Qwen2.5-72B-Instruct | 0.460 | 0.400 | 0.720 | 0.320 | 0.007482 | 0.260 | 0.021244 | 29233.6 |
| subset-sum-demo | Qwen/Qwen2.5-Coder-32B-Instruct | 0.360 | 0.800 | 0.640 | -0.160 | 0.096252 | 0.280 | 0.008687 | 7933.3 |
| subset-sum-demo | Qwen/Qwen3-Coder-Next:novita | 0.520 | 0.940 | 0.860 | -0.080 | 0.218750 | 0.340 | 0.000153 | 9534.4 |

## Table S2: Task-Aggregated Means Across Models

| Task | Models | Mean Single | Mean ReAct | Mean ToT | Mean Delta ToT-ReAct | Mean Delta ToT-Single | ToT Wins vs ReAct | ToT Losses vs ReAct |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| digit-permutation-demo | 3 | 0.153 | 0.907 | 0.620 | -0.287 | 0.467 | 0 | 3 |
| game24-demo | 3 | 0.140 | 0.167 | 0.740 | 0.573 | 0.600 | 3 | 0 |
| linear2-demo | 3 | 0.173 | 0.933 | 0.347 | -0.587 | 0.173 | 0 | 3 |
| subset-sum-demo | 3 | 0.447 | 0.713 | 0.740 | 0.027 | 0.293 | 1 | 2 |

## Figure Data Exports
- ToT vs ReAct effect-size points: `/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/protocol_v3_figure_effect_tot_vs_react.csv`
- ToT vs Single-path effect-size points: `/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/protocol_v3_figure_effect_tot_vs_single.csv`

## Table Data Exports
- Matrix table CSV: `/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/protocol_v3_table_matrix.csv`
- Task-aggregate table CSV: `/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/protocol_v3_table_task_aggregate.csv`
