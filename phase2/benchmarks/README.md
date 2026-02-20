# Benchmarks Workspace

Use this directory for benchmark definitions, run results, and analysis summaries.

## Planned Files
- `benchmark-matrix.md`: task panel, baselines, and primary metrics.
- `evaluation-protocol-v1.md`: fixed protocol settings for Evaluation v1 runs.
- `runs/`: run-level output artifacts.
  - includes baseline and `tot-prototype` demo manifests.
- `analysis/`: aggregate tables and plots.
  - `analysis/baseline_variance_report.md`: repeated baseline-run stability summary.
  - `analysis/baseline_variance_report.json`: machine-readable summary.
  - `analysis/tot_variance_report.md`: repeated ToT-run stability summary.
  - `analysis/tot_variance_report.json`: machine-readable ToT summary.
  - `analysis/evaluation_v1_metrics.md`: condition-level metrics table for fixed protocol.
  - `analysis/evaluation_v1_metrics.json`: machine-readable evaluation summary.
  - `analysis/evaluation_v1_metrics_hf.md`: HF-filtered condition-level metrics table.
  - `analysis/evaluation_v1_metrics_hf.json`: machine-readable HF-filtered summary.
  - `analysis/failure_taxonomy.md`: heuristic failure-category summary.
  - `analysis/failure_taxonomy.json`: machine-readable failure taxonomy.
  - `analysis/failure_taxonomy_hf.md`: HF-filtered failure-category summary.
  - `analysis/failure_taxonomy_hf.json`: machine-readable HF-filtered failure taxonomy.

All benchmark claims in manuscript drafts must trace back to files in this directory.
