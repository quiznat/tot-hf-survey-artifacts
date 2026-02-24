# Benchmarks Workspace

Use this directory for benchmark definitions, run results, and analysis summaries.

## Planned Files
- `benchmark-matrix.md`: task panel, baselines, and primary metrics.
- `benchmark-matrix-v3.md`: expanded multi-task matrix (protocol-v3 scope).
- `benchmark-matrix-v4.md`: confirmatory multi-task matrix (protocol-v4 scope).
- `benchmark-matrix-v5.md`: base reasoning-pattern matrix (protocol-v5 scope).
- `benchmark-matrix-v7.md`: causal-clarity reset matrix sequence (`A -> B -> C`) with claim-scope boundaries.
- `evaluation-protocol-v1.md`: fixed protocol settings for Evaluation v1 runs.
- `evaluation-protocol-v2.md`: frozen protocol for v2 matrix and ablations.
- `evaluation-protocol-v3.md`: expanded multi-task protocol for deeper pre-publication evidence.
- `evaluation-protocol-v4.md`: pre-registered confirmatory reset protocol after exploratory invalidation.
- `evaluation-protocol-v5.md`: base-pattern expansion protocol (`single,cot,cot_sc,react,tot`).
- `evaluation-protocol-v51.md`: hybrid profile protocol layered on v5 base conditions.
- `evaluation-protocol-v7.md`: frozen reset protocol with mandatory capability-parity gates and staged matrix progression.
- `protocol-v3-execution.md`: canonical matrix execution and summary commands.
- `protocol-v4-execution.md`: canonical confirmatory-gate + matrix execution commands.
- `protocol-v5-execution.md`: canonical v5 smoke/matrix and v5.1 hybrid execution commands.
- `protocol-v7-execution.md`: canonical Matrix A/B/C execution plan with stage-entry gate checks.
- `panels/game24_lockset_v1.json`: fixed 50-item paired Game24 panel for lockset evaluation.
- `panels/subset_sum_lockset_v1.json`: fixed 50-item paired subset-sum panel.
- `panels/linear2_lockset_v1.json`: fixed 50-item paired 2x2 linear-system panel.
- `panels/digit_permutation_lockset_v1.json`: fixed 50-item paired digit-permutation optimization panel.
- `panels/game24_lockset_v4.json`: confirmatory disjoint Game24 panel.
- `panels/subset_sum_lockset_v4.json`: confirmatory disjoint subset-sum panel.
- `panels/linear2_lockset_v4.json`: confirmatory disjoint linear2 panel.
- `panels/digit_permutation_lockset_v4.json`: confirmatory disjoint digit-permutation panel.
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
  - `analysis/game24_lockset_report.md`: paired lockset run summary for publication-style panel reporting.
  - `analysis/game24_lockset_report.json`: machine-readable paired lockset summary.
  - `analysis/game24_lockset_report_pilot.md`: paired pilot smoke report (small-N pipeline validation).
  - `analysis/game24_lockset_report_pilot.json`: machine-readable paired pilot report.
  - `analysis/protocol_v4_panel_disjointness.md`: v4 panel disjointness validation report.
  - `analysis/protocol_v4_panel_disjointness.json`: machine-readable disjointness report.
  - `analysis/protocol_v4_gate_report.md`: v4 pre-launch gate status report.
  - `analysis/protocol_v4_gate_report.json`: machine-readable gate report.

All benchmark claims in manuscript drafts must trace back to files in this directory.

Protocol-v7 governance rule:
- Primary causal claims must come from Matrix A (reasoning-only) unless a later matrix explicitly demonstrates matched capability parity.
