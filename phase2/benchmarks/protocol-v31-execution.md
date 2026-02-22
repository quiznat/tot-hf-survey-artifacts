# Protocol v3.1 Execution Guide

Status: active  
Protocol ID: `TOT-HF-P2-EPV31-2026-02-22`

## 1. Execute Full Diagnostic Matrix
```bash
export HF_TOKEN=your_token_here
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_protocol_v31_diagnostics.py \
  --tasks linear2-demo,digit-permutation-demo \
  --models Qwen/Qwen3-Coder-Next:novita,Qwen/Qwen2.5-72B-Instruct,Qwen/Qwen2.5-Coder-32B-Instruct \
  --profiles tot_model_self_eval,tot_hybrid,tot_rule_based,tot_model_self_eval_lite \
  --limit 50 \
  --max-workers 8 \
  --hf-temperature 0.0 \
  --hf-top-p 1.0 \
  --seed-policy item_hash \
  --bootstrap-samples 10000 \
  --confidence-level 0.95
```

## 2. Rebuild Summary Outputs
```bash
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/build_protocol_v31_diagnostic_summary.py
```

## 3. Report-Only Rebuild
```bash
export HF_TOKEN=your_token_here
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_protocol_v31_diagnostics.py \
  --report-only
```

## 4. Notes
- No within-matrix model substitutions.
- Keep execution log in `phase2/reproducibility/run-log-protocol-v31.md`.
- Write run manifests to `phase2/benchmarks/runs/protocol_v31_diagnostic/`.
- Summary artifacts:
  - `phase2/benchmarks/analysis/protocol_v31_diagnostic_summary.md`
  - `phase2/benchmarks/analysis/protocol_v31_diagnostic_summary.json`
