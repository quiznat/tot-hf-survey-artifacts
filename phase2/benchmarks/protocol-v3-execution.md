# Protocol v3 Execution Guide

Status: ready  
Protocol ID: `TOT-HF-P2-EPV3-2026-02-21`

## 1. Build Panels
```bash
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/build_protocol_v3_panels.py
```

## 2. Dry-Run the Full Matrix (Command Validation)
```bash
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_protocol_v3_matrix.py \
  --dry-run
```

## 3. Execute the Full Matrix
```bash
export HF_TOKEN=your_token_here
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_protocol_v3_matrix.py \
  --tasks game24-demo,subset-sum-demo,linear2-demo,digit-permutation-demo \
  --models Qwen/Qwen3-Coder-Next:novita,Qwen/Qwen2.5-72B-Instruct,Qwen/Qwen2.5-Coder-32B-Instruct \
  --conditions single,react,tot \
  --limit 50 \
  --max-workers 8 \
  --tot-evaluator-mode model_self_eval \
  --tot-max-depth 3 \
  --tot-branch-factor 3 \
  --tot-frontier-width 3 \
  --hf-temperature 0.0 \
  --hf-top-p 1.0 \
  --seed-policy item_hash \
  --bootstrap-samples 10000 \
  --confidence-level 0.95
```

## 4. Build Consolidated Matrix Summary
```bash
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/build_protocol_v3_matrix_summary.py \
  --reports-glob '/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/*_lockset_report_*_v3.json' \
  --out-md /Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/protocol_v3_matrix_summary.md \
  --out-json /Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/protocol_v3_matrix_summary.json
```

## 5. Report-Only Rebuild (No New Runs)
Use when manifests already exist and only reports need regeneration.
```bash
export HF_TOKEN=your_token_here
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_protocol_v3_matrix.py \
  --report-only
```

## 6. Notes
- Do not mix fallback models within a locked matrix run.
- Keep run-log updates in `phase2/reproducibility/run-log-protocol-v3.md`.
- If provider/model availability changes mid-run, stop and version protocol before resuming.
