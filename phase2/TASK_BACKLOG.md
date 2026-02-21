# Phase 2 Task Backlog

Status date: 2026-02-21

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
- [ ] Execute protocol-v3 block 1: `game24-demo` x `Qwen/Qwen3-Coder-Next:novita` (50 paired items x 3 conditions).
- [ ] Execute remaining protocol-v3 matrix blocks without substitutions (4 tasks x 3 models total).
- [ ] Rebuild consolidated v3 matrix summary from generated `*_v3.json` reports.
- [ ] Refresh failure taxonomy artifacts from protocol-v3 manifests (task-scoped + pooled views).
- [ ] Validate rerun determinism on a sampled subset using `--report-only` parity checks.

## P3 (Manuscript and Packaging)
- [ ] Update `phase2/manuscript/PREPAPER.md` with protocol-v3 design, status, and evidence-bound claim scope.
- [ ] Generate v3-backed submission tables/figures directly from matrix summary JSON.
- [ ] Draft reproducibility appendix text for v3 commands, panels, and artifact map.
- [ ] Prepare anonymous vs camera-ready package variants once v3 evidence is complete.
