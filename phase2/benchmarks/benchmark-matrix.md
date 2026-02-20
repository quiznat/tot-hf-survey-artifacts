# Benchmark Matrix (Draft v0)

Last updated: 2026-02-20

## Selection Criteria
- Multi-step reasoning requirement.
- Objective scoring where possible.
- Feasible repeat runs under fixed budgets.
- Relevance to tool-augmented agent workflows.

## Candidate Task Panel

| Task Family | Example Task | Baselines | ToT Variant | Primary Metric | Secondary Metrics | Notes |
|---|---|---|---|---|---|---|
| Arithmetic Reasoning | Game of 24 style solving | Single-path, ReAct | ToT-search | Solve rate (%) | Latency, tokens, cost | Good for search-depth ablations |
| Constrained Planning | Multi-step tool sequence with constraints | Single-path, ReAct | ToT-search + pruning | Task completion (%) | Invalid-step rate, latency | Tests backtracking value |
| Retrieval + Synthesis | Multi-document answer with tool calls | Single-path, ReAct | ToT with evaluator | Exactness/faithfulness | Citation quality, cost | Requires strict rubric |
| Program Repair | Small bug-fix tasks with tests | Single-path, ReAct | ToT with branch scoring | Pass@1 / pass@k | Iterations, runtime | Strong practical signal |

## Baseline Definitions
- Baseline A: Single-path reasoning with one action trajectory.
- Baseline B: ReAct-style reasoning-action loop without tree search.

## ToT Definition (Initial)
- Generator: branch candidate reasoning/action steps.
- Evaluator: score branch viability at each depth.
- Search: bounded breadth/depth with pruning.
- Stop: solution found, budget reached, or no viable branches.

## Protocol Defaults (Initial)
- Repetitions per condition: 5
- Fixed model per sweep: yes
- Fixed prompt template per task: yes
- Random seed control where supported: required

## Open Decisions
- Final task dataset sources.
- Scoring rubric for retrieval+synthesis tasks.
- Budget caps for comparable cost reporting.
