# Capability Parity Audit

Generated UTC: 2026-02-22T05:45:00Z

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

### tmp_capability_equalized

| Task | Condition | Runs | Action Rate | Tool Sets (runs) |
|---|---|---:|---:|---|
| `linear2-demo` | `baseline-react` | 1 | 1.000 | (none) (1) |
| `linear2-demo` | `tot-prototype` | 1 | 0.000 | (none) (1) |

### tmp_capability_equalized_game24

| Task | Condition | Runs | Action Rate | Tool Sets (runs) |
|---|---|---:|---:|---|
| `game24-demo` | `baseline-react` | 1 | 1.000 | (none) (1) |
| `game24-demo` | `tot-prototype` | 1 | 0.000 | (none) (1) |

## Findings

No capability parity findings.
