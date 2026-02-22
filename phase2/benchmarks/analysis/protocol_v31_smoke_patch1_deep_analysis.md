# Protocol v3.1 Deep Analysis

Series analyzed: 8

## Executive Signals
- Across completed v3.1 series, mean ToT-ReAct delta is negative, indicating net regression relative to ReAct.
- Most ToT failures are depth-limit terminations, consistent with search budget/pruning constraints rather than random noise.

## Series Ranking (ToT - ReAct Delta)

| Task | Model | Profile | ReAct | ToT | Delta | Holm p | ToT better | ReAct better | Latency x |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| linear2-demo | Qwen/Qwen3-Coder-Next:novita | unknown | 1.000 | 0.500 | -0.500 | 0.062500 | 0 | 5 | 1.233 |
| linear2-demo | Qwen/Qwen3-Coder-Next:novita | unknown | 1.000 | 0.600 | -0.400 | 0.125000 | 0 | 4 | 1.636 |
| linear2-demo | Qwen/Qwen3-Coder-Next:novita | unknown | 0.900 | 0.500 | -0.400 | 0.125000 | 0 | 4 | 0.964 |
| linear2-demo | Qwen/Qwen3-Coder-Next:novita | unknown | 0.900 | 0.600 | -0.300 | 0.250000 | 0 | 3 | 1.428 |
| digit-permutation-demo | Qwen/Qwen3-Coder-Next:novita | unknown | 0.900 | 0.800 | -0.100 | 1.000000 | 0 | 1 | 0.936 |
| digit-permutation-demo | Qwen/Qwen3-Coder-Next:novita | unknown | 1.000 | 0.900 | -0.100 | 1.000000 | 0 | 1 | 1.427 |
| digit-permutation-demo | Qwen/Qwen3-Coder-Next:novita | unknown | 1.000 | 0.900 | -0.100 | 1.000000 | 0 | 1 | 0.680 |
| digit-permutation-demo | Qwen/Qwen3-Coder-Next:novita | unknown | 0.900 | 0.900 | -0.000 | 1.000000 | 1 | 1 | 1.085 |

## Aggregate by Task

| Task | Series | Mean Delta | Mean ReAct | Mean ToT | ToT wins | ToT losses | Sig. losses | Mean Latency x |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| digit-permutation-demo | 4 | -0.075 | 0.950 | 0.875 | 0 | 3 | 0 | 1.032 |
| linear2-demo | 4 | -0.400 | 0.950 | 0.550 | 0 | 4 | 0 | 1.315 |

## Aggregate by Model

| Model | Series | Mean Delta | Mean ReAct | Mean ToT | ToT wins | ToT losses | Sig. losses | Mean Latency x |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Qwen/Qwen3-Coder-Next:novita | 8 | -0.238 | 0.950 | 0.713 | 0 | 7 | 0 | 1.174 |

## Aggregate by Profile

| Profile | Series | Mean Delta | Mean ReAct | Mean ToT | ToT wins | ToT losses | Sig. losses | Mean Latency x |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| unknown | 8 | -0.238 | 0.950 | 0.713 | 0 | 7 | 0 | 1.174 |

## Aggregate by Task x Profile

| Task | Profile | Series | Mean Delta | ToT wins | ToT losses | Sig. losses |
|---|---|---:|---:|---:|---:|---:|
| digit-permutation-demo | unknown | 4 | -0.075 | 0 | 3 | 0 |
| linear2-demo | unknown | 4 | -0.400 | 0 | 4 | 0 |

## ToT Failure Buckets (Latest Item-Condition Manifests)

ToT successes: 57
ToT failures: 23

| Bucket | Count | Share |
|---|---:|---:|
| depth_limit | 17 | 0.739 |
| empty_frontier | 6 | 0.261 |

## ToT Failure Rate by Model

| Model | ToT runs | ToT failures | Failure rate |
|---|---:|---:|---:|
| Qwen/Qwen3-Coder-Next:novita | 80 | 23 | 0.287 |

## ToT Failure Rate by Profile

| Profile | ToT runs | ToT failures | Failure rate |
|---|---:|---:|---:|
| tot_hybrid | 20 | 5 | 0.250 |
| tot_model_self_eval | 20 | 5 | 0.250 |
| tot_model_self_eval_lite | 20 | 7 | 0.350 |
| tot_rule_based | 20 | 6 | 0.300 |

## ToT Failure Rate by Task

| Task | ToT runs | ToT failures | Failure rate |
|---|---:|---:|---:|
| digit-permutation-demo | 40 | 5 | 0.125 |
| linear2-demo | 40 | 18 | 0.450 |

## Interpretation Guardrails
- This report is diagnostic, not causal proof.
- A negative ToT delta can result from evaluator pruning, depth/branch budget, prompt mismatch, or task/tool interface effects.
- Depth-limit concentration specifically suggests search-budget pressure and/or weak candidate scoring calibration.
