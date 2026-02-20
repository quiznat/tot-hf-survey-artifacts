# Phase 2: ToT-HF Integration Project

This directory is the execution workspace for the novel contribution track: implementing and evaluating Tree-of-Thought-style reasoning in Hugging Face agent workflows with reproducible empirical results.

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
- `reproducibility/`: environment and run logging standards.
- `templates/`: reusable templates for experiments and reporting.

## Session Start Routine
1. Read `AGENT_CONTEXT.md`.
2. Read `PROJECT_STATE.md` and `TASK_BACKLOG.md`.
3. Execute the top-priority backlog item.
4. Update `PROJECT_STATE.md` and `TASK_BACKLOG.md` before ending the session.
