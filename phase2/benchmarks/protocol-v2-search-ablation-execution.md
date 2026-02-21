# Protocol v2 Search Ablation Execution

Status: executed (2026-02-21)  
Protocol ID: `TOT-HF-P2-EPV2-2026-02-20`  
Primary model: `Qwen/Qwen3-Coder-Next:novita`

## Scope
Run the two frozen search-policy presets on the fixed 50-item paired Game24 panel:
- A1 (shallower): `max_depth=2, branch_factor=3, frontier_width=3`
- A2 (wider): `max_depth=3, branch_factor=4, frontier_width=4`

Each preset runs all paired conditions (`single,react,tot`) to preserve within-batch paired comparisons.

## Prerequisites
- `HF_TOKEN` must be set in the environment running these commands.
- Use `--max-workers 8` for protocol-consistent parallel execution.

## Run Log Initialization
```bash
cat > /Users/quiznat/Desktop/Tree_of_Thought/phase2/reproducibility/run-log-protocol-v2-search-ablations.md << 'EOF'
# Phase 2 Run Log (Protocol v2 Search Ablations)

All timestamps are UTC. This log is isolated to search-policy ablation runs under protocol `TOT-HF-P2-EPV2-2026-02-20`.

| Run ID | Timestamp (UTC) | Task | Condition | Outcome | Notes |
|---|---|---|---|---|---|
EOF
```

## A1 Run Command
```bash
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_game24_lockset.py \
  --provider hf \
  --model-id Qwen/Qwen3-Coder-Next:novita \
  --conditions single,react,tot \
  --tot-evaluator-mode model_self_eval \
  --tot-max-depth 2 \
  --tot-branch-factor 3 \
  --tot-frontier-width 3 \
  --hf-temperature 0.0 \
  --seed-policy item_hash \
  --limit 50 \
  --max-workers 8 \
  --confidence-level 0.95 \
  --bootstrap-samples 10000 \
  --runs-dir /Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/runs/protocol_v2_locked_search_ablations/A1 \
  --run-log /Users/quiznat/Desktop/Tree_of_Thought/phase2/reproducibility/run-log-protocol-v2-search-ablations.md \
  --report-md /Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/game24_lockset_report_qwen3codernext_search_a1.md \
  --report-json /Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/game24_lockset_report_qwen3codernext_search_a1.json
```

## A2 Run Command
```bash
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_game24_lockset.py \
  --provider hf \
  --model-id Qwen/Qwen3-Coder-Next:novita \
  --conditions single,react,tot \
  --tot-evaluator-mode model_self_eval \
  --tot-max-depth 3 \
  --tot-branch-factor 4 \
  --tot-frontier-width 4 \
  --hf-temperature 0.0 \
  --seed-policy item_hash \
  --limit 50 \
  --max-workers 8 \
  --confidence-level 0.95 \
  --bootstrap-samples 10000 \
  --runs-dir /Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/runs/protocol_v2_locked_search_ablations/A2 \
  --run-log /Users/quiznat/Desktop/Tree_of_Thought/phase2/reproducibility/run-log-protocol-v2-search-ablations.md \
  --report-md /Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/game24_lockset_report_qwen3codernext_search_a2.md \
  --report-json /Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/game24_lockset_report_qwen3codernext_search_a2.json
```

## Consolidated Search-Ablation Summary
```bash
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/build_search_ablation_summary.py \
  --primary-report-json /Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/game24_lockset_report_qwen3codernext.json \
  --a1-report-json /Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/game24_lockset_report_qwen3codernext_search_a1.json \
  --a2-report-json /Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/game24_lockset_report_qwen3codernext_search_a2.json \
  --out-md /Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/game24_lockset_search_ablation_summary.md \
  --out-json /Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/game24_lockset_search_ablation_summary.json
```

## Post-Run Updates
- Update `phase2/PROJECT_STATE.md` Gate P2-G4 status and completed-items list.
- Update `phase2/manuscript/PREPAPER.md` with search-ablation outcomes and revised claim boundaries.
- Rebuild failure taxonomy using the new ablation manifests.

## Completed Outputs (2026-02-21)
- Run artifacts:
  - `phase2/benchmarks/runs/protocol_v2_locked_search_ablations/A1` (150 paired-condition manifests)
  - `phase2/benchmarks/runs/protocol_v2_locked_search_ablations/A2` (150 paired-condition manifests)
  - `phase2/benchmarks/runs/protocol_v2_locked_search_ablations/A1_smoke` (3-run smoke precheck retained separately)
- A1 report:
  - `phase2/benchmarks/analysis/game24_lockset_report_qwen3codernext_search_a1.md`
  - `phase2/benchmarks/analysis/game24_lockset_report_qwen3codernext_search_a1.json`
- A2 report:
  - `phase2/benchmarks/analysis/game24_lockset_report_qwen3codernext_search_a2.md`
  - `phase2/benchmarks/analysis/game24_lockset_report_qwen3codernext_search_a2.json`
- Consolidated summary:
  - `phase2/benchmarks/analysis/game24_lockset_search_ablation_summary.md`
  - `phase2/benchmarks/analysis/game24_lockset_search_ablation_summary.json`
