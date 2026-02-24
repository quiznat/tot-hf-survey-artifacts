# Phase 2: ToT-HF Integration Project

This directory is the execution workspace for the novel contribution track: implementing and evaluating Tree-of-Thought-style reasoning in Hugging Face agent workflows with reproducible empirical results.

## Rendered Draft
- GitHub Pages (Phase 2 paper): `https://quiznat.github.io/tot-hf-survey-artifacts/phase2/paper.html`
- Source markdown: `phase2/manuscript/PREPAPER.md`
- Build command: `bash phase2/manuscript/build_phase2_html.sh`

## Current Evaluation Track
- Pre-v4 evidence is quarantined as exploratory and excluded from primary confirmatory claims:
  - registry: `phase2/benchmarks/evidence/series_registry.json`
  - reset record: `phase2/benchmarks/evidence/protocol_v4_reset_20260222T0600Z/README.md`
- Confirmatory reference track (completed and frozen):
  - protocol: `phase2/benchmarks/evaluation-protocol-v4.md`
  - matrix: `phase2/benchmarks/benchmark-matrix-v4.md`
  - execution guide: `phase2/benchmarks/protocol-v4-execution.md`
- Locked reset strategy (active):
  - protocol: `phase2/benchmarks/evaluation-protocol-v7.md`
  - matrix: `phase2/benchmarks/benchmark-matrix-v7.md`
  - execution guide: `phase2/benchmarks/protocol-v7-execution.md`
  - sequence: Matrix A (reasoning-only) -> Matrix B (tool-calling parity) -> Matrix C (engineering extension)

## Dashboard
- Service installer: `phase2/dashboard/install_service.sh`
- Service uninstaller: `phase2/dashboard/uninstall_service.sh`
- Local URL: `http://127.0.0.1:8787`
- Dashboard docs: `phase2/dashboard/README.md`

If the service runs but shows no data, macOS privacy controls may block LaunchAgents from reading Desktop paths.  
Run `phase2/dashboard/repair_permissions.sh`, grant Full Disk Access to the reported `python3`, then reinstall via `phase2/dashboard/install_service.sh`.

## Purpose
- Keep long-running project state stable across sessions.
- Separate planning and implementation artifacts from the survey manuscript workflow.
- Maintain publication-grade evidence and reproducibility discipline.

## Core Files
- `AGENT_CONTEXT.md`: session bootstrap and operating constraints (Claude/Codex equivalent context file).
- `ROADMAP.md`: milestones, gates, and deliverables.
- `PROJECT_STATE.md`: current status snapshot.
- `TASK_BACKLOG.md`: prioritized implementation and research tasks.
- `manuscript/PREPAPER.md`: living manuscript source of truth for methods, decisions, and claim boundaries.
- `benchmarks/`: benchmark design and run outputs.
  - `benchmarks/protocol-v2-search-ablation-execution.md`: canonical A1/A2 execution commands and artifact paths.
- `reproducibility/`: environment and run logging standards.
- `templates/`: reusable templates for experiments and reporting.

## Session Start Routine
1. Read `AGENT_CONTEXT.md`.
2. Read `PROJECT_STATE.md` and `TASK_BACKLOG.md`.
3. Execute the top-priority backlog item.
4. Update `PROJECT_STATE.md` and `TASK_BACKLOG.md` before ending the session.
