# Phase 2 Roadmap: Novel ToT-HF Contribution

Last updated: 2026-02-24

## Objective
Deliver a reproducible implementation and empirical evaluation of Tree-of-Thought-style reasoning integrated with Hugging Face agent frameworks.

## Research Questions
- RQ1: Does ToT-style search improve task success over strong single-path and ReAct-style baselines in selected agentic tasks?
- RQ2: What are the compute, latency, and cost tradeoffs of ToT integration under controlled settings?
- RQ3: Which ToT components (generator, evaluator, search policy, pruning) drive gains in this integration?

## Methodology Baseline (Frozen)
- Primary ToT methodology uses LLM-based in-chain evaluation (`model_self_eval`).
- `rule_based` evaluator mode is diagnostic/control only and must not be treated as the main claim condition.
- Arithmetic correctness checks for Game24 are offline verification metrics, not the primary in-chain decision mechanism.
- All condition comparisons must be paired on identical item IDs.

## Protocol Status
- Frozen baseline protocol: `phase2/benchmarks/evaluation-protocol-v2.md`
- Protocol ID: `TOT-HF-P2-EPV2-2026-02-20`
- Primary gate/ablation model: `Qwen/Qwen3-Coder-Next:novita`
- Active expansion protocol: `phase2/benchmarks/evaluation-protocol-v3.md`
- Expansion protocol ID: `TOT-HF-P2-EPV3-2026-02-21`
- Active confirmatory reset protocol: `phase2/benchmarks/evaluation-protocol-v4.md`
- Confirmatory protocol ID: `TOT-HF-P2-EPV4-2026-02-22`
- Active base-pattern protocol: `phase2/benchmarks/evaluation-protocol-v5.md`
- Base-pattern protocol ID: `TOT-HF-P2-EPV5-2026-02-22`
- Active hybrid profile protocol: `phase2/benchmarks/evaluation-protocol-v51.md`
- Hybrid protocol ID: `TOT-HF-P2-EPV51-2026-02-22`
- Active refreshed smoke/matrix protocol: `protocol-v6` execution scripts under `phase2/code/scripts/`
- Pre-v6 freeze archive: `phase2/benchmarks/runs/_frozen/pre_v6_20260223T185128Z`
- Active reset protocol: `phase2/benchmarks/evaluation-protocol-v7.md`
- Reset protocol ID: `TOT-HF-P2-EPV7-2026-02-24`
- Locked sequence for publication-grade causal clarity:
  - Matrix A (reasoning-only) first and canonical for baseline claims.
  - Matrix B (tool-calling parity) second after Matrix A passes launch gates.
  - Matrix C (code-execution engineering extension) only after A/B stability.

## Gate Model

### Gate P2-G0: Project Bootstrap
Acceptance criteria:
- [x] `phase2` workspace initialized.
- [x] Phase 2 context, roadmap, project state, and backlog in place.
- [x] Baseline benchmark task matrix drafted.

### Gate P2-G1: Baseline Harness
Acceptance criteria:
- [x] Deterministic benchmark harness implemented.
- [x] At least two baseline agents runnable end-to-end.
- [x] Repeated baseline runs show stable variance bands.

### Gate P2-G2: ToT Integration Prototype
Acceptance criteria:
- [x] ToT loop integrated (generation, evaluation, search, stop policy).
- [x] Configurable branching depth/width and pruning.
- [x] Failure handling and trace logging implemented.

### Gate P2-G3: Evaluation v1
Acceptance criteria:
- [x] Minimum benchmark panel executed with fixed protocol.
- [x] Metrics table produced: success, latency, token/cost footprint.
- [x] All run artifacts archived with reproducibility metadata.

### Gate P2-G4: Ablation and Error Analysis
Acceptance criteria:
- [x] Evaluator ablations complete (`model_self_eval`, `rule_based`, `hybrid`) on primary model.
- [x] Search/policy ablations complete (depth, breadth, pruning presets).
- [x] Error taxonomy and representative failure cases documented.
- [x] Claims updated to match observed evidence only.

### Gate P2-G5: Manuscript Draft (Novel Work)
Acceptance criteria:
- [x] Methods, experiments, and limitations sections drafted from protocol-v2 evidence.
- [ ] Protocol-v3 core matrix evidence integrated into manuscript claims.
- [ ] Figures/tables generated from source data.
- [ ] Reproducibility appendix complete.
- [ ] `phase2/manuscript/PREPAPER.md` updated as the canonical source before manuscript export.

### Gate P2-G6: Submission Package
Acceptance criteria:
- [ ] Venue-compliant anonymous package built.
- [ ] Disclosure and authorship policy checks complete.
- [ ] Final quality scan: claims, citations, reproducibility.

## Workstreams
1. Implementation: ToT-agent integration in code.
2. Evaluation: benchmark harness, metrics, ablations.
3. Reproducibility: protocol freeze, run logging, artifact packaging.
4. Writing: manuscript updates grounded in measured results.

## Immediate Next Actions (Sprint 6)
1. Execute Matrix A smoke (`n=10`) across all tasks/models with parity profile `matrix_a_reasoning_only`.
2. Launch full Matrix A confirmatory run (`4 tasks x 3 models x 5 conditions x 50`) only if smoke passes.
3. Build Matrix A consolidated summary and freeze manuscript claim scope to Matrix A evidence.
