# Phase 2 Task Backlog

Status date: 2026-02-22

## P0 (Locked Foundations)
- [x] Build deterministic baseline + ToT harness with manifested run outputs.
- [x] Freeze protocol-v2 and complete 3-model paired Game24 matrix.
- [x] Complete evaluator/search ablations and failure taxonomy on the primary model.
- [x] Draft manuscript-ready Methods/Results/Limitations text from frozen v2 artifacts.

## P1 (Protocol-v3 Scaffolding)
- [x] Add multi-task adapters (`subset-sum`, `linear2`, `digit-permutation`) with objective validators.
- [x] Add task registry and pipeline task-selection support.
- [x] Add deterministic panel generator for protocol-v3 locksets (50 items each).
- [x] Add generic paired lockset runner (`run_structured_lockset.py`) for registered tasks.
- [x] Add protocol-v3 matrix orchestrator and summary builder scripts.
- [x] Add protocol-v3 benchmark/protocol/execution documentation.
- [x] Add protocol-v3 run-log scaffold and unit coverage for new tasks.

## P2 (Active Execution Queue)
- [x] Execute protocol-v3 block 1: `game24-demo` x `Qwen/Qwen3-Coder-Next:novita` (50 paired items x 3 conditions).
- [x] Execute remaining protocol-v3 matrix blocks without substitutions (4 tasks x 3 models total).
- [x] Rebuild consolidated v3 matrix summary from generated `*_v3.json` reports.
- [x] Refresh failure taxonomy artifacts from protocol-v3 manifests (task-scoped + pooled views).
- [x] Validate rerun determinism on a sampled subset using `--report-only` parity checks.

## P3 (Manuscript and Packaging)
- [x] Update `phase2/manuscript/PREPAPER.md` with protocol-v3 design, status, and evidence-bound claim scope.
- [x] Generate v3-backed submission tables/figures directly from matrix summary JSON.
- [x] Draft reproducibility appendix text for v3 commands, panels, and artifact map.
- [ ] Prepare anonymous vs camera-ready package variants once v3 evidence is complete.

## P4 (Protocol-v3.1 Diagnostics)
- [x] Define diagnostic protocol-v3.1 for failure tasks (`linear2`, `digit-permutation`) and lock profile matrix.
- [x] Scaffold diagnostic execution and summary scripts.
- [x] Execute full v3.1 diagnostic matrix (`2 tasks x 3 models x 4 profiles`, paired `react,tot`).
- [x] Build consolidated v3.1 diagnostic summary and deep-analysis artifacts.
- [x] Validate v3.1 report determinism with full-matrix `--report-only` parity on canonical metrics.
- [ ] Decide adaptive routing policy (`ReAct` vs `ToT` by task/profile) from v3.1 evidence.
