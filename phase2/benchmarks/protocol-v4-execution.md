# Protocol-v4 Execution Guide

## 0. Build Disjoint Panels
```bash
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/build_protocol_v4_panels.py
```

Expected artifacts:
- `phase2/benchmarks/panels/game24_lockset_v4.json`
- `phase2/benchmarks/panels/subset_sum_lockset_v4.json`
- `phase2/benchmarks/panels/linear2_lockset_v4.json`
- `phase2/benchmarks/panels/digit_permutation_lockset_v4.json`
- `phase2/benchmarks/analysis/protocol_v4_panel_disjointness.md`
- `phase2/benchmarks/analysis/protocol_v4_panel_disjointness.json`

## 1. Run Pre-Launch Gates
```bash
export HF_TOKEN=your_token_here
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_protocol_v4_gates.py \
  --model-id Qwen/Qwen3-Coder-Next:novita \
  --limit 10 \
  --max-workers 8 \
  --max-attempts-per-task 3 \
  --retry-backoff-seconds 20 \
  --capability-parity-policy equalize_react_to_tot
```

Gate outputs:
- `phase2/benchmarks/analysis/protocol_v4_gate_report.md`
- `phase2/benchmarks/analysis/protocol_v4_gate_report.json`
- `phase2/benchmarks/analysis/protocol_v4_smoke_capability_audit.md`
- `phase2/benchmarks/analysis/protocol_v4_smoke_capability_audit.json`

## 2. Execute Confirmatory Matrix (Frozen)
```bash
export HF_TOKEN=your_token_here
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_protocol_v4_matrix.py \
  --models Qwen/Qwen3-Coder-Next:novita,Qwen/Qwen2.5-72B-Instruct,Qwen/Qwen2.5-Coder-32B-Instruct \
  --conditions single,react,tot \
  --limit 50 \
  --max-workers 8 \
  --max-attempts-per-block 3 \
  --retry-backoff-seconds 30 \
  --tot-evaluator-mode model_self_eval \
  --capability-parity-policy equalize_react_to_tot
```

## 3. Build Confirmatory Summary
```bash
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/build_protocol_v4_matrix_summary.py
```

Summary outputs:
- `phase2/benchmarks/analysis/protocol_v4_matrix_summary.md`
- `phase2/benchmarks/analysis/protocol_v4_matrix_summary.json`

## 4. Optional Report-Only Replay
Rebuild reports from existing manifests without generating new runs:
```bash
export HF_TOKEN=your_token_here
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_protocol_v4_matrix.py \
  --report-only
```

## Guardrails
- Do not run protocol-v4 with `--capability-parity-policy off`.
- Do not substitute models during matrix execution.
- Do not modify prompts/code/settings mid-run.
