# Capability Parity Audit

Generated UTC: 2026-02-22T17:15:57Z

## Task Tool Declarations

| Task | Declared Tools |
|---|---|
| `digit-permutation-demo` | `best_divisible, is_divisible` |
| `game24-demo` | `calc` |
| `linear2-demo` | `check_xy, solve2` |
| `subset-sum-demo` | `check_target, sum_list` |

## Code Guardrails

| Status | File | Line | Description |
|---|---|---:|---|
| `ok` | `/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src/phase2_baselines/runners/react.py` | 23 | React runner supports explicit tool enable/disable policy. |
| `ok` | `/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_structured_lockset.py` | 174 | Structured lockset runner enforces capability parity policy before execution. |
| `ok` | `/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_game24_lockset.py` | 164 | Legacy Game24 lockset runner enforces the same capability parity policy. |
| `ok` | `/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src/phase2_baselines/pipeline.py` | 32 | Baseline pipeline reflects task-accurate React tool exposure in manifests. |

## Series Audit

### protocol_v4_smoke

| Task | Condition | Runs | Action Rate | Tool Sets (runs) |
|---|---|---:|---:|---|
| `digit-permutation-demo` | `baseline-react` | 50 | 0.000 | (none) (50) |
| `digit-permutation-demo` | `baseline-single-path` | 50 | 0.000 | (none) (50) |
| `digit-permutation-demo` | `tot-prototype` | 50 | 0.000 | (none) (50) |
| `game24-demo` | `baseline-react` | 109 | 0.000 | (none) (109) |
| `game24-demo` | `baseline-single-path` | 110 | 0.000 | (none) (110) |
| `game24-demo` | `tot-prototype` | 109 | 0.000 | (none) (109) |
| `linear2-demo` | `baseline-react` | 50 | 0.000 | (none) (50) |
| `linear2-demo` | `baseline-single-path` | 50 | 0.000 | (none) (50) |
| `linear2-demo` | `tot-prototype` | 50 | 0.000 | (none) (50) |
| `subset-sum-demo` | `baseline-react` | 68 | 0.000 | (none) (68) |
| `subset-sum-demo` | `baseline-single-path` | 68 | 0.000 | (none) (68) |
| `subset-sum-demo` | `tot-prototype` | 68 | 0.000 | (none) (68) |

## Findings

No capability parity findings.
