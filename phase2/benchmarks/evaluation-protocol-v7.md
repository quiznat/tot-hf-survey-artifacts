# Evaluation Protocol v7 (Causal-Clarity Reset)

Protocol ID: `TOT-HF-P2-EPV7-2026-02-24`  
Status: active (frozen sequencing decision)  
Date frozen: 2026-02-24

## 1. Objective

Establish publication-grade causal clarity by separating algorithmic reasoning effects from tool/execution capability effects.

Locked sequence:

1. Matrix A first: reasoning-only canonical baseline.
2. Matrix B second: tool-calling parity.
3. Matrix C third: engineering-forward extension after A/B stability.

## 2. Claim Scope

Primary causal claims must be derived from Matrix A only unless Matrix B or Matrix C explicitly satisfies capability parity and is reported as a separate claim family.

## 3. Global Non-Negotiables

1. No model substitution within a matrix run.
2. No prompt/parser/runtime changes after confirmatory launch.
3. Paired item IDs for all cross-condition comparisons.
4. Fixed seeds and temperature policy recorded in manifests.
5. Hard-fail launch gates on capability mismatch.
6. Exploratory and confirmatory panels remain disjoint.

## 4. Matrix Definitions

## 4.1 Matrix A (Reasoning-Only, Canonical)

Purpose:
isolate reasoning-policy effects under matched capability.

Conditions:

1. `baseline-single-path`
2. `baseline-cot`
3. `baseline-cot-sc`
4. `baseline-react-text` (text-only ReAct loop; no tool execution)
5. `tot-prototype` (reasoning-only ToT; no external tools/executors)

Capability policy:

1. No CodeAgent execution.
2. No external tool calls.
3. No memory persistence across items.
4. Shared model interface and generation controls across all conditions.

## 4.2 Matrix B (Tool-Calling Parity)

Purpose:
measure planning/search effect when all conditions use equal tool-calling surfaces.

Conditions:

1. Same five logical reasoning conditions as Matrix A.
2. Shared tool-calling agent path and identical tool registry hash.

Capability policy:

1. Identical tools, schemas, and call budget.
2. Identical timeout, step budget, and retry policy.
3. No condition-specific hidden tools.

## 4.3 Matrix C (Code-Execution Engineering Extension)

Purpose:
evaluate planning/search policies in code-executing agent environments.

Conditions:

1. Same five logical reasoning conditions as Matrix A/B.
2. Shared code-execution path for all conditions.

Capability policy:

1. Identical executor type and sandbox policy.
2. Identical import allowlist and execution budget.
3. Treated as extension claims, not replacements for Matrix A causal baseline.

## 5. Tasks and Panels

Core tasks:

1. `game24-demo`
2. `subset-sum-demo`
3. `linear2-demo`
4. `digit-permutation-demo`

Panel policy:

1. Smoke: `n=10` paired items per task/model/condition.
2. Confirmatory: `n=50` paired items per task/model/condition.
3. Disjoint panel sets between exploratory tuning and confirmatory reporting.

## 6. Models

Locked model set:

1. `Qwen/Qwen3-Coder-Next:novita`
2. `Qwen/Qwen2.5-72B-Instruct`
3. `Qwen/Qwen2.5-Coder-32B-Instruct`

## 7. Launch Gates

Matrix-entry gates (must pass before execution):

1. Capability manifest equality check across all conditions for the matrix.
2. Unit/integration tests pass for matrix-specific runner paths.
3. Smoke run passes for every task/model block.
4. Determinism/report-only parity checks pass on sampled subset.

Matrix progression gates:

1. Matrix B cannot start until Matrix A is complete and stable.
2. Matrix C cannot start until Matrix B is complete and stable.

## 8. Statistics and Reporting

Per condition:

1. Success rate.
2. Latency.
3. Token input/output.

Pairwise:

1. Paired delta with confidence intervals.
2. Exact McNemar test.
3. Holm-Bonferroni correction across family-wise contrasts.

Reporting rule:
negative or mixed results are reported directly; no directional claim without corresponding inferential support in the frozen matrix.
