# Protocol-v5 Execution Guide

## 1. Run Base-Pattern Smoke
```bash
export HF_TOKEN=your_token_here
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_protocol_v5_smoke.py \
  --conditions single,cot,cot_sc,react,tot \
  --limit 10 \
  --max-workers 12 \
  --cot-sc-samples 5 \
  --capability-parity-policy equalize_react_to_tot
```

Smoke outputs:
- `phase2/benchmarks/analysis/*_base_smoke_report_*_v5.md`
- `phase2/benchmarks/analysis/*_base_smoke_report_*_v5.json`

## 2. Execute Base-Pattern Matrix
```bash
export HF_TOKEN=your_token_here
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_protocol_v5_matrix.py \
  --models Qwen/Qwen3-Coder-Next:novita,Qwen/Qwen2.5-72B-Instruct,Qwen/Qwen2.5-Coder-32B-Instruct \
  --conditions single,cot,cot_sc,react,tot \
  --limit 50 \
  --max-workers 12 \
  --cot-sc-samples 5 \
  --tot-evaluator-mode model_self_eval \
  --capability-parity-policy equalize_react_to_tot
```

## 3. Build Base-Pattern Summary
```bash
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/build_protocol_v5_matrix_summary.py
```

Summary outputs:
- `phase2/benchmarks/analysis/protocol_v5_matrix_summary.md`
- `phase2/benchmarks/analysis/protocol_v5_matrix_summary.json`

## 4. Execute Hybrid Profile Matrix (v5.1)
```bash
export HF_TOKEN=your_token_here
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_protocol_v51_hybrid_matrix.py \
  --profiles tot_model_self_eval,tot_hybrid_eval,tot_rule_based_eval,tot_deep_search \
  --conditions single,cot,cot_sc,react,tot \
  --limit 50 \
  --max-workers 12 \
  --capability-parity-policy equalize_react_to_tot
```

## 5. Build Hybrid Summary (v5.1)
```bash
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/build_protocol_v51_hybrid_summary.py
```

Summary outputs:
- `phase2/benchmarks/analysis/protocol_v51_hybrid_summary.md`
- `phase2/benchmarks/analysis/protocol_v51_hybrid_summary.json`

## 6. Optional Report-Only Replay
Rebuild v5 reports from existing manifests:
```bash
export HF_TOKEN=your_token_here
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_protocol_v5_matrix.py \
  --report-only
```

## Guardrails
- Do not run with `--capability-parity-policy off`.
- Do not substitute models during active matrix runs.
- Do not change prompts/code/settings mid-run.
