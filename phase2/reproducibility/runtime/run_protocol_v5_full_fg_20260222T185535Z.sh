#!/usr/bin/env bash
set -euo pipefail
ROOT="/Users/quiznat/Desktop/Tree_of_Thought/phase2"
RUNTIME_DIR="/Users/quiznat/Desktop/Tree_of_Thought/phase2/reproducibility/runtime"
LOG="/Users/quiznat/Desktop/Tree_of_Thought/phase2/reproducibility/runtime/run_protocol_v5_full_20260222T185535Z.log"
ERR="/Users/quiznat/Desktop/Tree_of_Thought/phase2/reproducibility/runtime/run_protocol_v5_full_20260222T185535Z.err.log"

mkdir -p "$RUNTIME_DIR"
exec > >(tee -a "$LOG") 2> >(tee -a "$ERR" >&2)

echo $$ > "$RUNTIME_DIR/protocol_v5_active.pid"
echo "/Users/quiznat/Desktop/Tree_of_Thought/phase2/reproducibility/runtime/run_protocol_v5_full_fg_20260222T185535Z.sh" > "$RUNTIME_DIR/protocol_v5_active.script"
ln -sfn "run_protocol_v5_full_20260222T185535Z.log" "$RUNTIME_DIR/protocol_v5_active.log"
ln -sfn "run_protocol_v5_full_20260222T185535Z.err.log" "$RUNTIME_DIR/protocol_v5_active.err.log"

export PYTHONPATH="$ROOT/code/src"
export PYTHONUNBUFFERED=1
cd "$ROOT"

echo "protocol_v5_full_start=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "runner_pid=$$"
echo "hf_token_len=${#HF_TOKEN}"

echo "stage=v5_smoke start=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
python3 -u "$ROOT/code/scripts/run_protocol_v5_smoke.py"   --conditions single,cot,cot_sc,react,tot   --limit 10   --max-workers 12   --cot-sc-samples 5   --tot-evaluator-mode model_self_eval   --capability-parity-policy equalize_react_to_tot

echo "stage=v5_matrix start=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
python3 -u "$ROOT/code/scripts/run_protocol_v5_matrix.py"   --conditions single,cot,cot_sc,react,tot   --limit 50   --max-workers 12   --cot-sc-samples 5   --tot-evaluator-mode model_self_eval   --capability-parity-policy equalize_react_to_tot

echo "stage=v5_summary start=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
python3 -u "$ROOT/code/scripts/build_protocol_v5_matrix_summary.py"

echo "protocol_v5_full_done=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
