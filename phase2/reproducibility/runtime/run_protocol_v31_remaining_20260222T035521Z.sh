#!/usr/bin/env zsh
set -euo pipefail
source "$HOME/.zprofile" >/dev/null 2>&1 || true
cd /Users/quiznat/Desktop/Tree_of_Thought
export PYTHONUNBUFFERED=1
export PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_protocol_v31_diagnostics.py \
  --tasks digit-permutation-demo \
  --models Qwen/Qwen2.5-72B-Instruct,Qwen/Qwen2.5-Coder-32B-Instruct \
  --profiles tot_model_self_eval,tot_hybrid,tot_rule_based,tot_model_self_eval_lite \
  --limit 50 \
  --max-workers 8 \
  --hf-temperature 0.0 \
  --hf-top-p 1.0 \
  --seed-policy item_hash \
  --bootstrap-samples 10000 \
  --confidence-level 0.95 \
  --continue-on-error
