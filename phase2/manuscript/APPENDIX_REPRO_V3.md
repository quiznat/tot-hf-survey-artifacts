# Appendix: Protocol-v3 Reproducibility

Protocol ID: `TOT-HF-P2-EPV3-2026-02-21`  
Execution status: completed (4 tasks x 3 models x 3 conditions x 50 items = 1800 runs)

## A. Locked Configuration
- Tasks: `game24-demo,subset-sum-demo,linear2-demo,digit-permutation-demo`
- Models (fixed, no substitutions):
  - `Qwen/Qwen3-Coder-Next:novita`
  - `Qwen/Qwen2.5-72B-Instruct`
  - `Qwen/Qwen2.5-Coder-32B-Instruct`
- Conditions: `single,react,tot`
- ToT evaluator mode: `model_self_eval`
- ToT search: `max_depth=3`, `branch_factor=3`, `frontier_width=3`
- Sampling controls: `hf_temperature=0.0`, `hf_top_p=1.0`
- Deterministic seeding: `seed_policy=item_hash`
- Inference matrix scale: `limit=50`, `max_workers=8`
- Statistical settings: `bootstrap_samples=10000`, `confidence_level=0.95`

## B. Canonical Commands

### B.1 Build Deterministic Panels
```bash
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/build_protocol_v3_panels.py
```

### B.2 Execute Full Protocol-v3 Matrix
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

### B.3 Rebuild Matrix Summary
```bash
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/build_protocol_v3_matrix_summary.py
```

### B.4 Refresh Failure Taxonomies (Pooled + Task-Scoped)
```bash
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/build_failure_taxonomy.py \
  --runs-dir /Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/runs/protocol_v3_matrix \
  --recursive \
  --provider huggingface-inference \
  --out-md /Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/failure_taxonomy_protocol_v3_pooled.md \
  --out-json /Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/analysis/failure_taxonomy_protocol_v3_pooled.json
```

### B.5 Generate Submission Tables/Figure Data
```bash
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/build_protocol_v3_submission_tables.py
```

## C. Panel Files
- `phase2/benchmarks/panels/game24_lockset_v1.json`
- `phase2/benchmarks/panels/subset_sum_lockset_v1.json`
- `phase2/benchmarks/panels/linear2_lockset_v1.json`
- `phase2/benchmarks/panels/digit_permutation_lockset_v1.json`

## D. Artifact Map

### D.1 Per-Block Reports (12 JSON + 12 Markdown)
- Pattern: `phase2/benchmarks/analysis/*_lockset_report_*_v3.{json,md}`

### D.2 Consolidated Matrix Outputs
- `phase2/benchmarks/analysis/protocol_v3_matrix_summary.md`
- `phase2/benchmarks/analysis/protocol_v3_matrix_summary.json`

### D.3 Failure Taxonomy Outputs
- Pooled:
  - `phase2/benchmarks/analysis/failure_taxonomy_protocol_v3_pooled.md`
  - `phase2/benchmarks/analysis/failure_taxonomy_protocol_v3_pooled.json`
- Task-scoped:
  - `phase2/benchmarks/analysis/failure_taxonomy_protocol_v3_game24_demo.md`
  - `phase2/benchmarks/analysis/failure_taxonomy_protocol_v3_game24_demo.json`
  - `phase2/benchmarks/analysis/failure_taxonomy_protocol_v3_subset_sum_demo.md`
  - `phase2/benchmarks/analysis/failure_taxonomy_protocol_v3_subset_sum_demo.json`
  - `phase2/benchmarks/analysis/failure_taxonomy_protocol_v3_linear2_demo.md`
  - `phase2/benchmarks/analysis/failure_taxonomy_protocol_v3_linear2_demo.json`
  - `phase2/benchmarks/analysis/failure_taxonomy_protocol_v3_digit_permutation_demo.md`
  - `phase2/benchmarks/analysis/failure_taxonomy_protocol_v3_digit_permutation_demo.json`

### D.4 Determinism Parity Check
- `phase2/benchmarks/analysis/protocol_v3_report_only_parity_check.md`
- `phase2/benchmarks/analysis/protocol_v3_report_only_parity_check.json`

### D.5 Submission Table/Figure Data
- `phase2/benchmarks/analysis/protocol_v3_submission_tables.md`
- `phase2/benchmarks/analysis/protocol_v3_table_matrix.csv`
- `phase2/benchmarks/analysis/protocol_v3_table_task_aggregate.csv`
- `phase2/benchmarks/analysis/protocol_v3_figure_effect_tot_vs_react.csv`
- `phase2/benchmarks/analysis/protocol_v3_figure_effect_tot_vs_single.csv`

## E. Rebuild-Only Determinism
- Determinism validation used two sequential `--report-only` rebuilds on sampled blocks.
- Parity criterion: normalized report JSON hash equality after excluding `generated_utc`.
- Current parity result: all sampled checks passed.
