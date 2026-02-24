#!/usr/bin/env zsh
set -euo pipefail
source "$HOME/.zprofile" >/dev/null 2>&1 || true
cd /Users/quiznat/Desktop/Tree_of_Thought
export PYTHONUNBUFFERED=1
export PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src

# Gate pass before confirmatory matrix launch.
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_protocol_v4_gates.py \
  --skip-tests \
  --model-id Qwen/Qwen3-Coder-Next:novita \
  --limit 10 \
  --max-workers 4 \
  --max-attempts-per-task 5 \
  --retry-backoff-seconds 30 \
  --capability-parity-policy equalize_react_to_tot

# Full frozen matrix execution (no model substitution).
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_protocol_v4_matrix.py \
  --models Qwen/Qwen3-Coder-Next:novita,Qwen/Qwen2.5-72B-Instruct,Qwen/Qwen2.5-Coder-32B-Instruct \
  --conditions single,react,tot \
  --limit 50 \
  --max-workers 4 \
  --max-attempts-per-block 5 \
  --retry-backoff-seconds 45 \
  --tot-evaluator-mode model_self_eval \
  --capability-parity-policy equalize_react_to_tot

# Build consolidated v4 summary from confirmatory reports.
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/build_protocol_v4_matrix_summary.py
