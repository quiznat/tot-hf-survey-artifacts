# Phase 2 Roadmap: Novel ToT-HF Contribution

Last updated: 2026-02-21

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

## Protocol Freeze (Approved)
- Active protocol: `phase2/benchmarks/evaluation-protocol-v2.md`
- Protocol ID: `TOT-HF-P2-EPV2-2026-02-20`
- Primary gate/ablation model: `Qwen/Qwen3-Coder-Next:novita`

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
- [ ] Methods, experiments, and limitations sections drafted.
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

## Immediate Next Actions (Sprint 4)
1. Draft Results/Limitations with explicit panel/model scope and cost-latency tradeoff reporting.
2. Build first anonymous submission package and reproducibility artifact index.
3. Generate submission-ready tables/figures from archived matrix and ablation artifacts.
