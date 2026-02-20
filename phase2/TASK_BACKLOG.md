# Phase 2 Task Backlog

Status date: 2026-02-20

## P0 (Do Now)
- [x] Create `phase2/benchmarks/benchmark-matrix.md` with tasks, datasets, metrics, and baseline mapping.
- [x] Create `phase2/reproducibility/run-manifest-schema.md` for mandatory run metadata.
- [x] Create `phase2/code/README.md` with interface contract for baseline and ToT runners.
- [x] Create `phase2/reproducibility/run-log.md` for chronological run tracking.
- [x] Add first dry-run manifest example under `phase2/benchmarks/runs/`.
- [x] Create `phase2/reproducibility/environment.md` for dependency pinning policy.
- [x] Finalize implementation stack decision for `phase2/code/` (Python-first vs mixed stack).

## P1 (Next)
- [x] Implement baseline runner A (single-path reasoning).
- [x] Implement baseline runner B (ReAct-style tool loop).
- [x] Add unified metrics collector (success, latency, token usage, cost estimate).
- [x] Add repeated-run driver to generate baseline variance bands.
- [x] Add real model/provider adapter with pinned configuration profile (Hugging Face).
- [x] Add manifest validation test for required-field/schema compliance.
- [ ] Validate Hugging Face baseline runs with live token and archive first non-scripted manifests.

## P2 (After Baselines)
- [x] Implement ToT runner with configurable breadth/depth.
- [ ] Add evaluator strategy variants (self-eval and rule-based checks).
- [x] Add pruning and early-stop policies.
- [x] Integrate ToT runner with at least one non-scripted model/provider adapter (Hugging Face path).
- [ ] Validate ToT Hugging Face run and capture failure taxonomy notes.

## P3 (Analysis and Writing)
- [ ] Build ablation report template.
- [ ] Build failure taxonomy template with examples.
- [ ] Draft Methods + Experiments sections for novel manuscript track.
