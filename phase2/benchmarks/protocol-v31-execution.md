# Protocol v3.1 Execution Guide

Status: active  
Protocol ID: `TOT-HF-P2-EPV31-2026-02-22`

## 1. Mandatory Smoke Gate (All Task Types)
Run this before any production/full matrix execution.
```bash
export HF_TOKEN=your_token_here
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_protocol_v31_diagnostics.py \
  --tasks linear2-demo,digit-permutation-demo \
  --models Qwen/Qwen3-Coder-Next:novita \
  --profiles tot_model_self_eval,tot_hybrid,tot_rule_based,tot_model_self_eval_lite \
  --limit 10 \
  --max-workers 8 \
  --capability-parity-policy equalize_react_to_tot \
  --hf-temperature 0.0 \
  --hf-top-p 1.0 \
  --seed-policy item_hash \
  --bootstrap-samples 10000 \
  --confidence-level 0.95
```

## 2. Execute Full Diagnostic Matrix
```bash
export HF_TOKEN=your_token_here
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_protocol_v31_diagnostics.py \
  --tasks linear2-demo,digit-permutation-demo \
  --models Qwen/Qwen3-Coder-Next:novita,Qwen/Qwen2.5-72B-Instruct,Qwen/Qwen2.5-Coder-32B-Instruct \
  --profiles tot_model_self_eval,tot_hybrid,tot_rule_based,tot_model_self_eval_lite \
  --limit 50 \
  --max-workers 8 \
  --capability-parity-policy equalize_react_to_tot \
  --hf-temperature 0.0 \
  --hf-top-p 1.0 \
  --seed-policy item_hash \
  --bootstrap-samples 10000 \
  --confidence-level 0.95
```

## 3. Rebuild Summary Outputs
```bash
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/build_protocol_v31_diagnostic_summary.py
```

## 4. Report-Only Rebuild
```bash
export HF_TOKEN=your_token_here
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_protocol_v31_diagnostics.py \
  --report-only
```

## 5. Notes
- No within-matrix model substitutions.
- Smoke-gate pass across all task types is mandatory before production/full runs.
- Keep paired-condition capability parity enabled (`--capability-parity-policy equalize_react_to_tot`) unless intentionally running a disclosed mismatch audit.
- Keep execution log in `phase2/reproducibility/run-log-protocol-v31.md`.
- Write run manifests to `phase2/benchmarks/runs/protocol_v31_diagnostic/`.
- Summary artifacts:
  - `phase2/benchmarks/analysis/protocol_v31_diagnostic_summary.md`
  - `phase2/benchmarks/analysis/protocol_v31_diagnostic_summary.json`
