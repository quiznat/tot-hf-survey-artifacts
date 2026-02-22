# Capability Parity Audit

Generated UTC: 2026-02-22T05:39:48Z

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
| `ok` | `/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src/phase2_baselines/pipeline.py` | 32 | Baseline pipeline reflects task-accurate React tool exposure in manifests. |

## Series Audit

### protocol_v3_matrix

| Task | Condition | Runs | Action Rate | Tool Sets (runs) |
|---|---|---:|---:|---|
| `digit-permutation-demo` | `baseline-react` | 193 | 0.746 | calc (193) |
| `digit-permutation-demo` | `baseline-single-path` | 193 | 0.000 | (none) (193) |
| `digit-permutation-demo` | `tot-prototype` | 193 | 0.000 | (none) (193) |
| `game24-demo` | `baseline-react` | 150 | 0.940 | calc (150) |
| `game24-demo` | `baseline-single-path` | 150 | 0.000 | (none) (150) |
| `game24-demo` | `tot-prototype` | 150 | 0.000 | (none) (150) |
| `linear2-demo` | `baseline-react` | 150 | 0.953 | calc (150) |
| `linear2-demo` | `baseline-single-path` | 150 | 0.000 | (none) (150) |
| `linear2-demo` | `tot-prototype` | 150 | 0.000 | (none) (150) |
| `subset-sum-demo` | `baseline-react` | 150 | 0.980 | calc (150) |
| `subset-sum-demo` | `baseline-single-path` | 150 | 0.000 | (none) (150) |
| `subset-sum-demo` | `tot-prototype` | 150 | 0.000 | (none) (150) |

### protocol_v31_diagnostic

| Task | Condition | Runs | Action Rate | Tool Sets (runs) |
|---|---|---:|---:|---|
| `digit-permutation-demo` | `baseline-react` | 615 | 0.810 | calc (615) |
| `digit-permutation-demo` | `tot-prototype` | 615 | 0.000 | (none) (615) |
| `linear2-demo` | `baseline-react` | 640 | 0.963 | calc (640) |
| `linear2-demo` | `tot-prototype` | 640 | 0.000 | (none) (640) |

### protocol_v31_smoke_patch1

| Task | Condition | Runs | Action Rate | Tool Sets (runs) |
|---|---|---:|---:|---|
| `digit-permutation-demo` | `baseline-react` | 40 | 0.575 | calc (40) |
| `digit-permutation-demo` | `tot-prototype` | 40 | 0.000 | (none) (40) |
| `linear2-demo` | `baseline-react` | 40 | 0.975 | calc (40) |
| `linear2-demo` | `tot-prototype` | 40 | 0.000 | (none) (40) |

### protocol_v32_diagnostic

| Task | Condition | Runs | Action Rate | Tool Sets (runs) |
|---|---|---:|---:|---|
| `digit-permutation-demo` | `baseline-react` | 293 | 0.713 | calc (293) |
| `digit-permutation-demo` | `tot-prototype` | 293 | 0.000 | (none) (293) |
| `linear2-demo` | `baseline-react` | 600 | 0.970 | calc (600) |
| `linear2-demo` | `tot-prototype` | 600 | 0.000 | (none) (600) |

## Findings

| Severity | Type | Series | Task | Message |
|---|---|---|---|---|
| `high` | `paired_condition_tool_mismatch` | `protocol_v3_matrix` | `digit-permutation-demo` | React and ToT tool exposure differ within paired comparisons. |
| `medium` | `react_manifest_tool_declaration_mismatch` | `protocol_v3_matrix` | `digit-permutation-demo` | React manifest tool_config differs from task.available_tools() declaration. |
| `high` | `paired_condition_tool_mismatch` | `protocol_v3_matrix` | `game24-demo` | React and ToT tool exposure differ within paired comparisons. |
| `high` | `paired_condition_tool_mismatch` | `protocol_v3_matrix` | `linear2-demo` | React and ToT tool exposure differ within paired comparisons. |
| `medium` | `react_manifest_tool_declaration_mismatch` | `protocol_v3_matrix` | `linear2-demo` | React manifest tool_config differs from task.available_tools() declaration. |
| `high` | `paired_condition_tool_mismatch` | `protocol_v3_matrix` | `subset-sum-demo` | React and ToT tool exposure differ within paired comparisons. |
| `medium` | `react_manifest_tool_declaration_mismatch` | `protocol_v3_matrix` | `subset-sum-demo` | React manifest tool_config differs from task.available_tools() declaration. |
| `high` | `paired_condition_tool_mismatch` | `protocol_v31_diagnostic` | `digit-permutation-demo` | React and ToT tool exposure differ within paired comparisons. |
| `medium` | `react_manifest_tool_declaration_mismatch` | `protocol_v31_diagnostic` | `digit-permutation-demo` | React manifest tool_config differs from task.available_tools() declaration. |
| `high` | `paired_condition_tool_mismatch` | `protocol_v31_diagnostic` | `linear2-demo` | React and ToT tool exposure differ within paired comparisons. |
| `medium` | `react_manifest_tool_declaration_mismatch` | `protocol_v31_diagnostic` | `linear2-demo` | React manifest tool_config differs from task.available_tools() declaration. |
| `high` | `paired_condition_tool_mismatch` | `protocol_v31_smoke_patch1` | `digit-permutation-demo` | React and ToT tool exposure differ within paired comparisons. |
| `medium` | `react_manifest_tool_declaration_mismatch` | `protocol_v31_smoke_patch1` | `digit-permutation-demo` | React manifest tool_config differs from task.available_tools() declaration. |
| `high` | `paired_condition_tool_mismatch` | `protocol_v31_smoke_patch1` | `linear2-demo` | React and ToT tool exposure differ within paired comparisons. |
| `medium` | `react_manifest_tool_declaration_mismatch` | `protocol_v31_smoke_patch1` | `linear2-demo` | React manifest tool_config differs from task.available_tools() declaration. |
| `high` | `paired_condition_tool_mismatch` | `protocol_v32_diagnostic` | `digit-permutation-demo` | React and ToT tool exposure differ within paired comparisons. |
| `medium` | `react_manifest_tool_declaration_mismatch` | `protocol_v32_diagnostic` | `digit-permutation-demo` | React manifest tool_config differs from task.available_tools() declaration. |
| `high` | `paired_condition_tool_mismatch` | `protocol_v32_diagnostic` | `linear2-demo` | React and ToT tool exposure differ within paired comparisons. |
| `medium` | `react_manifest_tool_declaration_mismatch` | `protocol_v32_diagnostic` | `linear2-demo` | React manifest tool_config differs from task.available_tools() declaration. |
