# Benchmark Matrix v7 (Causal-Clarity Sequence)

Date: 2026-02-24  
Protocol: `TOT-HF-P2-EPV7-2026-02-24`

## Matrix A (Reasoning-Only Canonical Baseline)

Purpose:
estimate reasoning-policy effects without tool/execution confounds.

| Field | Value |
|---|---|
| Tasks | `game24-demo`, `subset-sum-demo`, `linear2-demo`, `digit-permutation-demo` |
| Models | `Qwen/Qwen3-Coder-Next:novita`, `Qwen/Qwen2.5-72B-Instruct`, `Qwen/Qwen2.5-Coder-32B-Instruct` |
| Conditions | `baseline-single-path`, `baseline-cot`, `baseline-cot-sc`, `baseline-react-text`, `tot-prototype` |
| Panel sizes | smoke `n=10`, confirmatory `n=50` |
| Capability policy | no tools, no code execution, no persistent memory across items |
| Inferential status | primary claim source |

## Matrix B (Tool-Calling Parity)

Purpose:
measure planning/search effects under equal tool-calling access.

| Field | Value |
|---|---|
| Tasks | same as Matrix A |
| Models | same as Matrix A |
| Conditions | same logical five-condition family as Matrix A |
| Panel sizes | smoke `n=10`, confirmatory `n=50` |
| Capability policy | identical tool registry, schema, call budget, timeout, and retry policy |
| Inferential status | secondary claim family, reported separately |

## Matrix C (Code-Execution Extension)

Purpose:
engineering-forward evaluation in code-executing agent regime.

| Field | Value |
|---|---|
| Tasks | same as Matrix A |
| Models | same as Matrix A |
| Conditions | same logical five-condition family as Matrix A |
| Panel sizes | smoke `n=10`, confirmatory `n=50` |
| Capability policy | identical executor type, sandbox policy, import allowlist, and execution budget |
| Inferential status | extension-only, not substitute for Matrix A baseline |

## Progression Rules

1. Do not run Matrix B before Matrix A completion + gate pass.
2. Do not run Matrix C before Matrix B completion + gate pass.
3. Do not pool results across A/B/C for a single causal effect estimate.
