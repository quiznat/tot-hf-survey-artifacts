# Phase 2 Mini Roadmap: Protocol-v4 Reset

Status date: 2026-02-22

## Objective
Produce publication-grade confirmatory evidence under a pre-registered protocol with strict exploratory-vs-confirmatory separation.

## Roadmap
1. Quarantine pre-v4 evidence.
- Mark all existing Phase 2 runs as `exploratory_invalid_for_primary_claim`.
- Keep only for diagnostics/failure taxonomy.

2. Freeze confirmatory protocol-v4.
- Lock tasks, panels, models, conditions, parity policy, metrics, stats, retries, stop rules.
- No model substitution and no code/prompt changes during matrix execution.

3. Generate disjoint confirmatory panels.
- Build v4 panels with no overlap against v1 tuned panels.
- Validate disjointness and archive the report.

4. Pass gates before matrix launch.
- Unit/integration tests pass.
- Capability audit on smoke series shows zero findings.
- Smoke coverage complete on all tasks.
- `--report-only` parity check passes.

5. Run full confirmatory matrix once.
- Execute frozen v4 matrix in one uninterrupted run family.
- Analyze only predeclared tests (paired delta CI + exact McNemar + Holm).

6. Enforce claim discipline.
- Report underperformance directly when observed.
- Scope all claims to protocol-v4 task/model/panel boundaries.
