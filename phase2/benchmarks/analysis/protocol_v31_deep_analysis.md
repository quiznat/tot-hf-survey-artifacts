# Protocol v3.1 Deep Analysis

Series analyzed: 24

## Executive Signals
- Across completed v3.1 series, mean ToT-ReAct delta is negative, indicating net regression relative to ReAct.
- Most ToT failures are depth-limit terminations, consistent with search budget/pruning constraints rather than random noise.
- 21 series show statistically significant ToT underperformance (Holm-adjusted p < 0.05).

## Series Ranking (ToT - ReAct Delta)

| Task | Model | Profile | ReAct | ToT | Delta | Holm p | ToT better | ReAct better | Latency x |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| linear2-demo | Qwen/Qwen2.5-72B-Instruct | ToT self-eval lite (2/2/2) | 1.000 | 0.260 | -0.740 | 1.46e-11 | 0 | 37 | 3.705 |
| linear2-demo | Qwen/Qwen2.5-72B-Instruct | ToT self-eval (3/3/3) | 0.980 | 0.300 | -0.680 | 1.16e-10 | 0 | 34 | 11.143 |
| linear2-demo | Qwen/Qwen2.5-72B-Instruct | ToT hybrid (3/3/3) | 1.000 | 0.360 | -0.640 | 4.66e-10 | 0 | 32 | 10.620 |
| linear2-demo | Qwen/Qwen2.5-72B-Instruct | ToT rule-based (3/3/3) | 1.000 | 0.360 | -0.640 | 4.66e-10 | 0 | 32 | 3.136 |
| linear2-demo | Qwen/Qwen3-Coder-Next:novita | ToT self-eval (3/3/3) | 0.940 | 0.300 | -0.640 | 4.07e-09 | 1 | 33 | 3.654 |
| linear2-demo | Qwen/Qwen3-Coder-Next:novita | ToT rule-based (3/3/3) | 0.980 | 0.340 | -0.640 | 4.66e-10 | 0 | 32 | 1.889 |
| linear2-demo | Qwen/Qwen2.5-Coder-32B-Instruct | ToT rule-based (3/3/3) | 0.900 | 0.300 | -0.600 | 6.94e-08 | 2 | 32 | 1.739 |
| linear2-demo | Qwen/Qwen3-Coder-Next:novita | ToT self-eval lite (2/2/2) | 0.920 | 0.320 | -0.600 | 1.54e-08 | 1 | 31 | 1.260 |
| linear2-demo | Qwen/Qwen3-Coder-Next:novita | ToT hybrid (3/3/3) | 0.940 | 0.360 | -0.580 | 2.98e-08 | 1 | 30 | 3.629 |
| digit-permutation-demo | Qwen/Qwen2.5-72B-Instruct | ToT self-eval lite (2/2/2) | 0.980 | 0.420 | -0.560 | 7.45e-09 | 0 | 28 | 2.513 |
| linear2-demo | Qwen/Qwen2.5-Coder-32B-Instruct | ToT self-eval lite (2/2/2) | 0.880 | 0.320 | -0.560 | 5.77e-08 | 1 | 29 | 1.084 |
| digit-permutation-demo | Qwen/Qwen2.5-72B-Instruct | ToT rule-based (3/3/3) | 0.980 | 0.460 | -0.520 | 2.98e-08 | 0 | 26 | 1.597 |
| linear2-demo | Qwen/Qwen2.5-Coder-32B-Instruct | ToT hybrid (3/3/3) | 0.880 | 0.360 | -0.520 | 2.16e-07 | 1 | 27 | 3.243 |
| linear2-demo | Qwen/Qwen2.5-Coder-32B-Instruct | ToT self-eval (3/3/3) | 0.860 | 0.340 | -0.520 | 2.16e-07 | 1 | 27 | 2.713 |
| digit-permutation-demo | Qwen/Qwen2.5-72B-Instruct | ToT hybrid (3/3/3) | 0.960 | 0.500 | -0.460 | 2.38e-07 | 0 | 23 | 7.362 |
| digit-permutation-demo | Qwen/Qwen2.5-72B-Instruct | ToT self-eval (3/3/3) | 0.960 | 0.520 | -0.440 | 1.05e-05 | 2 | 24 | 7.168 |
| digit-permutation-demo | Qwen/Qwen3-Coder-Next:novita | ToT self-eval lite (2/2/2) | 0.960 | 0.600 | -0.360 | 4.01e-05 | 1 | 19 | 1.365 |
| digit-permutation-demo | Qwen/Qwen3-Coder-Next:novita | ToT self-eval (3/3/3) | 1.000 | 0.660 | -0.340 | 1.53e-05 | 0 | 17 | 3.329 |
| digit-permutation-demo | Qwen/Qwen2.5-Coder-32B-Instruct | ToT self-eval lite (2/2/2) | 0.840 | 0.540 | -0.300 | 0.001490 | 3 | 18 | 0.839 |
| digit-permutation-demo | Qwen/Qwen3-Coder-Next:novita | ToT rule-based (3/3/3) | 0.980 | 0.680 | -0.300 | 6.10e-05 | 0 | 15 | 1.302 |
| digit-permutation-demo | Qwen/Qwen3-Coder-Next:novita | ToT hybrid (3/3/3) | 0.960 | 0.680 | -0.280 | 0.000519 | 1 | 15 | 3.198 |
| digit-permutation-demo | Qwen/Qwen2.5-Coder-32B-Instruct | ToT hybrid (3/3/3) | 0.780 | 0.640 | -0.140 | 0.229523 | 9 | 16 | 1.250 |
| digit-permutation-demo | Qwen/Qwen2.5-Coder-32B-Instruct | ToT self-eval (3/3/3) | 0.800 | 0.660 | -0.140 | 0.210040 | 8 | 15 | 1.196 |
| digit-permutation-demo | Qwen/Qwen2.5-Coder-32B-Instruct | ToT rule-based (3/3/3) | 0.780 | 0.680 | -0.100 | 0.383310 | 8 | 13 | 0.707 |

## Aggregate by Task

| Task | Series | Mean Delta | Mean ReAct | Mean ToT | ToT wins | ToT losses | Sig. losses | Mean Latency x |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| digit-permutation-demo | 12 | -0.328 | 0.915 | 0.587 | 0 | 12 | 9 | 2.652 |
| linear2-demo | 12 | -0.613 | 0.940 | 0.327 | 0 | 12 | 12 | 3.985 |

## Aggregate by Model

| Model | Series | Mean Delta | Mean ReAct | Mean ToT | ToT wins | ToT losses | Sig. losses | Mean Latency x |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Qwen/Qwen2.5-72B-Instruct | 8 | -0.585 | 0.982 | 0.398 | 0 | 8 | 8 | 5.905 |
| Qwen/Qwen2.5-Coder-32B-Instruct | 8 | -0.360 | 0.840 | 0.480 | 0 | 8 | 5 | 1.596 |
| Qwen/Qwen3-Coder-Next:novita | 8 | -0.468 | 0.960 | 0.492 | 0 | 8 | 8 | 2.453 |

## Aggregate by Profile

| Profile | Series | Mean Delta | Mean ReAct | Mean ToT | ToT wins | ToT losses | Sig. losses | Mean Latency x |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ToT hybrid (3/3/3) | 6 | -0.437 | 0.920 | 0.483 | 0 | 6 | 5 | 4.883 |
| ToT self-eval (3/3/3) | 6 | -0.460 | 0.923 | 0.463 | 0 | 6 | 5 | 4.867 |
| ToT self-eval lite (2/2/2) | 6 | -0.520 | 0.930 | 0.410 | 0 | 6 | 6 | 1.794 |
| ToT rule-based (3/3/3) | 6 | -0.467 | 0.937 | 0.470 | 0 | 6 | 5 | 1.728 |

## Aggregate by Task x Profile

| Task | Profile | Series | Mean Delta | ToT wins | ToT losses | Sig. losses |
|---|---|---:|---:|---:|---:|---:|
| digit-permutation-demo | ToT hybrid (3/3/3) | 3 | -0.293 | 0 | 3 | 2 |
| digit-permutation-demo | ToT self-eval (3/3/3) | 3 | -0.307 | 0 | 3 | 2 |
| digit-permutation-demo | ToT self-eval lite (2/2/2) | 3 | -0.407 | 0 | 3 | 3 |
| digit-permutation-demo | ToT rule-based (3/3/3) | 3 | -0.307 | 0 | 3 | 2 |
| linear2-demo | ToT hybrid (3/3/3) | 3 | -0.580 | 0 | 3 | 3 |
| linear2-demo | ToT self-eval (3/3/3) | 3 | -0.613 | 0 | 3 | 3 |
| linear2-demo | ToT self-eval lite (2/2/2) | 3 | -0.633 | 0 | 3 | 3 |
| linear2-demo | ToT rule-based (3/3/3) | 3 | -0.627 | 0 | 3 | 3 |

## ToT Failure Buckets (Latest Item-Condition Manifests)

ToT successes: 548
ToT failures: 652

| Bucket | Count | Share |
|---|---:|---:|
| depth_limit | 625 | 0.959 |
| empty_frontier | 27 | 0.041 |

## ToT Failure Rate by Model

| Model | ToT runs | ToT failures | Failure rate |
|---|---:|---:|---:|
| Qwen/Qwen2.5-72B-Instruct | 400 | 241 | 0.603 |
| Qwen/Qwen2.5-Coder-32B-Instruct | 400 | 208 | 0.520 |
| Qwen/Qwen3-Coder-Next:novita | 400 | 203 | 0.507 |

## ToT Failure Rate by Profile

| Profile | ToT runs | ToT failures | Failure rate |
|---|---:|---:|---:|
| tot_hybrid | 300 | 155 | 0.517 |
| tot_model_self_eval | 300 | 161 | 0.537 |
| tot_model_self_eval_lite | 300 | 177 | 0.590 |
| tot_rule_based | 300 | 159 | 0.530 |

## ToT Failure Rate by Task

| Task | ToT runs | ToT failures | Failure rate |
|---|---:|---:|---:|
| digit-permutation-demo | 600 | 248 | 0.413 |
| linear2-demo | 600 | 404 | 0.673 |

## Interpretation Guardrails
- This report is diagnostic, not causal proof.
- A negative ToT delta can result from evaluator pruning, depth/branch budget, prompt mismatch, or task/tool interface effects.
- Depth-limit concentration specifically suggests search-budget pressure and/or weak candidate scoring calibration.
