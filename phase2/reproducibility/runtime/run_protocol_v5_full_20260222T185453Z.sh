#!/usr/bin/env bash
set -euo pipefail
ROOT="/Users/quiznat/Desktop/Tree_of_Thought/phase2"
export PYTHONPATH="$ROOT/code/src"
export PYTHONUNBUFFERED=1
cd "$ROOT"

echo "protocol_v5_full_start=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "hf_token_len=${#HF_TOKEN}"

echo "stage=v5_smoke start=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
python3 -u "$ROOT/code/scripts/run_protocol_v5_smoke.py" \
  --conditions single,cot,cot_sc,react,tot \
  --limit 10 \
  --max-workers 12 \
  --cot-sc-samples 5 \
  --tot-evaluator-mode model_self_eval \
  --capability-parity-policy equalize_react_to_tot

echo "stage=v5_matrix start=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
python3 -u "$ROOT/code/scripts/run_protocol_v5_matrix.py" \
  --conditions single,cot,cot_sc,react,tot \
  --limit 50 \
  --max-workers 12 \
  --cot-sc-samples 5 \
  --tot-evaluator-mode model_self_eval \
  --capability-parity-policy equalize_react_to_tot

echo "stage=v5_summary start=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
python3 -u "$ROOT/code/scripts/build_protocol_v5_matrix_summary.py"

echo "protocol_v5_full_done=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
