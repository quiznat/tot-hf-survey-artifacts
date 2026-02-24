# Protocol v7 Execution Guide

Date: 2026-02-24  
Protocol ID: `TOT-HF-P2-EPV7-2026-02-24`

## 1. Prerequisites

1. `HF_TOKEN` set in environment.
2. Matrix-specific runner paths implemented and tested.
3. Capability manifest checker available and wired as pre-run gate.

Example environment:

```bash
export HF_TOKEN=your_token_here
```

## 2. Matrix A Launch (Reasoning-Only)

## 2.1 Mandatory prelaunch checks

1. All conditions run without tools and without code execution.
2. `baseline-react-text` path exists and is selected (not CodeAgent path).
3. Unit tests pass for single/cot/cot-sc/react-text/tot runners.
4. Capability manifest equality report passes for all five conditions.

Stop rule:
if any check fails, do not launch smoke.

## 2.2 Smoke run (`n=10`)

Run smoke after gate pass. Use existing orchestration with Matrix-A condition set once `baseline-react-text` is available.

Canonical command:

```bash
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_protocol_v7_smoke.py
```

Notes:
1. The smoke orchestrator now runs all locked Matrix-A models by default (`Qwen/Qwen3-Coder-Next:novita`, `Qwen/Qwen2.5-72B-Instruct`, `Qwen/Qwen2.5-Coder-32B-Instruct`).
2. Use `--model-id <model>` only for a bounded single-model probe.

Required output artifacts:

1. Matrix A smoke report per task/model.
2. Consolidated Matrix A capability parity audit:
   - `phase2/benchmarks/analysis/protocol_v7_matrix_a_smoke_capability_audit_<report_tag>.md`
   - `phase2/benchmarks/analysis/protocol_v7_matrix_a_smoke_capability_audit_<report_tag>.json`
3. Matrix A determinism sample parity report.

## 2.3 Confirmatory run (`n=50`)

Launch only after smoke is green for all tasks/models.

Required output artifacts:

1. Matrix A confirmatory reports per task/model.
2. Matrix A consolidated summary (`.md` + `.json`).
3. Matrix A failure taxonomy views.

Canonical command:

```bash
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_protocol_v7_matrix.py
```

## 3. Matrix B Launch (Tool-Calling Parity)

Entry gate:
Matrix A complete and frozen.

Additional checks:

1. Shared tool registry hash is identical for all conditions.
2. Shared tool-calling budget/timeout/retry policy is identical for all conditions.
3. No hidden tool access by condition.

Run sequence:

1. Smoke `n=10`.
2. Confirmatory `n=50`.
3. Build Matrix B summary and keep claims separate from Matrix A.

## 4. Matrix C Launch (Code-Execution Extension)

Entry gate:
Matrix B complete and frozen.

Additional checks:

1. Shared executor type and sandbox policy across all conditions.
2. Shared import allowlist and execution budget across all conditions.

Run sequence:

1. Smoke `n=10`.
2. Confirmatory `n=50`.
3. Build Matrix C summary and report as extension-only evidence.

## 5. Publication Reporting Rule

1. Primary causal claims come from Matrix A.
2. Matrix B and Matrix C are separate claim families.
3. Do not pool A/B/C outcomes into one effect-size table.
