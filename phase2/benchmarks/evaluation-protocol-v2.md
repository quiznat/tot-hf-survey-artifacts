# Evaluation Protocol v2 (Frozen)

Status: approved (frozen)
Proposed date: 2026-02-20
Approved date: 2026-02-20
Protocol ID: TOT-HF-P2-EPV2-2026-02-20

## 1. Purpose
Freeze a publication-grade Phase 2 protocol before additional experiments. This protocol defines the exact comparison design, statistics, artifact outputs, and acceptance criteria for claims.

## 2. Research Questions
- RQ1: On fixed paired benchmark items, does `tot-prototype` with `model_self_eval` improve success rate over `baseline-single-path` and `baseline-react`?
- RQ2: What latency and token-cost tradeoff accompanies any success-rate improvement?
- RQ3: How sensitive outcomes are to evaluator mode and search settings on the same paired panel?

## 3. Primary Claim Scope (Locked)
Allowed claim scope after this protocol:
- "Under Protocol ID TOT-HF-P2-EPV2-2026-02-20 on paired Game24 lockset items, ToT improved success by X absolute points versus baseline Y with CI and corrected p-values."

Disallowed claim scope:
- Generalization to all tasks/models or production deployments from this protocol alone.

## 4. Conditions
Primary conditions (all required):
- `baseline-single-path`
- `baseline-react`
- `tot-prototype` with `tot_evaluator_mode=model_self_eval`

Control/ablation conditions (secondary):
- `tot-prototype` with `tot_evaluator_mode=rule_based`
- `tot-prototype` with `tot_evaluator_mode=hybrid`

## 5. Tasks and Panels
### 5.1 Locked Primary Task
- Task family: Arithmetic reasoning (Game24)
- Panel: `phase2/benchmarks/panels/game24_lockset_v1.json`
- Panel size: 50 fixed solvable items
- Pairing rule: each item ID must be run on every condition in the same experiment batch

### 5.2 Secondary Task Expansion (Optional in this protocol window)
- Only if implemented and validated under the same manifest schema.
- Must use fixed item list and paired execution identical to 5.1.

## 6. Model Matrix
Primary model matrix (required, locked):
- `Qwen/Qwen3-Coder-Next:novita`
- `Qwen/Qwen2.5-72B-Instruct`
- `Qwen/Qwen2.5-Coder-32B-Instruct`

Primary model for ablations and gate criteria: `Qwen/Qwen3-Coder-Next:novita` (chosen as the most capable openly-available coding/agent model at protocol freeze).

Lock rule:
- No model substitution is allowed within a matrix run window.
- If any locked model is unavailable, stop the matrix run, update protocol version, and restart that model row under the new protocol lock.

## 7. Sample Size and Run Plan
- Per model, per condition, per task panel: `n=50` paired items.
- Primary per-model run count (Game24): `3 conditions x 50 = 150` runs.
- Primary matrix total (3 models): `450` runs.

Ablation run count (per model, optional but recommended for P2-G4):
- evaluator ablations (`rule_based`, `hybrid`) at `n=50` each: +100/model.
- search ablations (depth/width presets below) at `n=50` each: +100/model.

### 7.1 Sample-Size Justification
`n=50` per condition was chosen because pilot data (50 runs) showed large net advantages (Δ = 32-76 percentage points). This yields >98% power for the primary McNemar contrast (Δ>=25%) at α=0.05 after Holm correction across three pairwise tests (calculated via exact binomial power for discordant pairs). For smaller future effects (Δ=10-15%) the protocol allows scaling to `n=100-150` in confirmation runs.

### 7.2 Expected Resource Use (Primary Matrix)
- Per model, per condition: ~1.5-4 hours wall-clock (4 workers)
- Total primary matrix (450 runs): 12-25 hours across 3 models
- Token cost: dominated by `tot-prototype` (~750 input tokens/run)

## 8. ToT Search Settings
Default (primary) ToT settings:
- `max_depth=3`
- `branch_factor=3`
- `frontier_width=3`
- pruning: `topk_cumulative_score`
- stop policy: `first_terminal_or_depth_limit`

Search ablation presets:
- A1 (shallower): `max_depth=2, branch_factor=3, frontier_width=3`
- A2 (wider): `max_depth=3, branch_factor=4, frontier_width=4`

## 9. Execution Controls
- Provider: Hugging Face Inference Router
- Auth env var: `HF_TOKEN`
- Prompt template version: `v1`
- Determinism policy: identical fixed item IDs with deterministic seed assignment from the first 32 bits of `SHA-256(item_id)` (CLI: `--seed-policy item_hash`).
- Randomness policy: `--hf-temperature 0.0` wherever supported by the model; otherwise the minimum temperature that the provider allows. Full seed and temperature are logged in every manifest.
- Parallelism: `--max-workers` allowed and recorded; default target 4 unless rate-limited.
- Retry policy:
  - transport/API failure: retry once, then mark infrastructure failure.
  - invalid reasoning/incorrect answer: retain as task failure (no rerun).

## 10. Statistical Plan (Pre-Registered)
Primary endpoint:
- Binary task success.

Primary contrast:
- `tot-prototype (model_self_eval)` vs `baseline-react` (paired on same item IDs).

Secondary contrasts:
- `tot-prototype` vs `baseline-single-path`
- `baseline-react` vs `baseline-single-path`

Inferential methods:
- Condition success CIs: Wilson interval.
- Paired delta CI: bootstrap percentile CI on item-level differences.
- Significance: exact McNemar test (two-sided) per paired contrast.

Reporting policy:
- Report absolute deltas, CI bounds, p-values, and Holm-adjusted p-values.
- Multiple comparisons: Holm-Bonferroni correction applied across all pairwise contrasts reported in a single final report (typically 3 primary + any ablations included).
- No "significant improvement" language without corrected p-value and compatible CI.

## 11. Artifact and Reproducibility Requirements
Required outputs per executed batch:
- manifests: `phase2/benchmarks/runs/*.json`
- report markdown: `phase2/benchmarks/analysis/game24_lockset_report.md`
- report json: `phase2/benchmarks/analysis/game24_lockset_report.json`
- run log updates: `phase2/reproducibility/run-log.md`
- project state update: `phase2/PROJECT_STATE.md`
- prepaper update: `phase2/manuscript/PREPAPER.md`

All manifests must include:
- `run_id`, `timestamp_utc`, `condition_id`, `model.name`, `provider.name`, `item_id`, `panel_id`, `input_data`, metrics block, and config block.

## 12. Gate Criteria for P2-G4 Completion
P2-G4 is complete when all are true:
- Primary matrix complete for 3 models on Game24 lockset (`450` runs total).
- At least evaluator ablation complete on the primary model.
- Failure taxonomy updated with representative run IDs.
- Claim language in manuscript constrained to observed evidence.

## 13. Canonical Commands
Primary run (single model):
```bash
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_game24_lockset.py \
  --provider hf \
  --model-id Qwen/Qwen3-Coder-Next:novita \
  --conditions single,react,tot \
  --tot-evaluator-mode model_self_eval \
  --hf-temperature 0.0 \
  --seed-policy item_hash \
  --limit 50 \
  --max-workers 4 \
  --confidence-level 0.95 \
  --bootstrap-samples 10000
```

Report-only rebuild:
```bash
PYTHONPATH=/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src \
python3 /Users/quiznat/Desktop/Tree_of_Thought/phase2/code/scripts/run_game24_lockset.py \
  --report-only \
  --provider hf \
  --model-id Qwen/Qwen3-Coder-Next:novita \
  --conditions single,react,tot \
  --tot-evaluator-mode model_self_eval \
  --hf-temperature 0.0 \
  --seed-policy item_hash \
  --limit 50 \
  --confidence-level 0.95 \
  --bootstrap-samples 10000
```

## 14. Approval Record
This protocol is approved and frozen; all subsequent claims/runs must conform unless a new version is created.

- [x] Approved as written (2026-02-20)
