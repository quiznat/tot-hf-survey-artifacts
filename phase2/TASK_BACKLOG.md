# Phase 2 Task Backlog

Status date: 2026-02-24

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

## P5 (Protocol-v4 Confirmatory Reset)
- [x] Publish pre-v4 quarantine/invalidation ledger and series registry classification.
- [x] Freeze protocol-v4 and execution guide with mandatory capability-parity lock.
- [x] Implement disjoint panel generator for all tasks and generate v4 panel/disjointness artifacts.
- [x] Add protocol-v4 smoke, gate, and confirmatory matrix orchestrators.
- [x] Run protocol-v4 gate suite on live provider (`HF_TOKEN`) and archive gate report artifacts.
- [x] Execute full protocol-v4 confirmatory matrix (`4 tasks x 3 models x 3 conditions x 50`).
- [x] Build protocol-v4 confirmatory matrix summary and scope manuscript claims to v4 evidence only.

## P6 (Protocol-v5 Base Patterns)
- [x] Add `cot` and `cot_sc` baseline runners to the shared lockset pipeline.
- [x] Extend `run_structured_lockset.py` and tests for five-condition execution.
- [x] Add protocol-v5 smoke/matrix orchestration and summary scripts.
- [ ] Run protocol-v5 smoke (`n=10`) on all tasks with locked controls.
- [ ] Execute full protocol-v5 base-pattern matrix (`4 tasks x 3 models x 5 conditions x 50`).
- [ ] Build protocol-v5 matrix summary and publish task/model-scoped comparator table.

## P7 (Protocol-v5.1 Hybrid Profiles)
- [x] Freeze v5.1 profile grid and add execution + summary tooling.
- [ ] Execute v5.1 hybrid matrix (`4 tasks x 3 models x 4 profiles x 5 conditions x 50`).
- [ ] Build hybrid summary and choose profile policy for publication claims.

## P8 (Protocol-v6 Reset and Fresh Smoke)
- [x] Freeze all pre-v6 run artifacts into a timestamped archive.
- [x] Add protocol-v6 smoke/matrix orchestration scripts.
- [x] Update dashboard progress/report ingestion for v6 smoke + v6 matrix.
- [x] Execute full protocol-v6 smoke (`4 tasks x 1 model x 6 conditions x 10`) and generate per-task reports.
- [x] Build consolidated v6 smoke summary artifacts (`protocol_v6_smoke_summary.{md,json}`).
- [ ] Execute full protocol-v6 matrix (`4 tasks x 3 models x 6 conditions x 50`) with locked settings.

## P9 (Protocol-v7 Causal-Clarity Reset)
- [x] Lock canonical sequence: Matrix A (reasoning-only) -> Matrix B (tool-calling parity) -> Matrix C (engineering extension).
- [x] Publish protocol-v7 docs (`evaluation-protocol-v7.md`, `benchmark-matrix-v7.md`, `protocol-v7-execution.md`) as the new source of truth.
- [x] Implement Matrix A text-only ReAct path (no CodeAgent/tool execution) for parity with single/CoT/CoT-SC/ToT reasoning-only conditions.
- [x] Add Matrix A capability-gate checks (hard-fail when tools/execution/memory surfaces differ across conditions).
- [ ] Run Matrix A smoke (`n=10`) for all tasks/models and archive parity audit report.
- [ ] Execute full Matrix A confirmatory matrix (`4 tasks x 3 models x 5 conditions x 50`) with no substitutions.
- [ ] Build Matrix A summary and freeze claim scope for manuscript integration.
- [ ] Prepare Matrix B tool-calling parity freeze (shared tool registry hash, call budget, and agent policy).
- [ ] Run Matrix B smoke only after Matrix A is stable.
