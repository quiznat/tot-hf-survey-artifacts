# AGENT CONTEXT (Phase 2)

Last updated: 2026-02-20

## Mission
Build a publication-grade, reproducible implementation and evaluation of Tree of Thoughts integration with Hugging Face agent frameworks.

## Non-Negotiables
- No performance claim without traceable evidence.
- Every reported metric must include dataset/task, model, baseline, prompt/config, and run timestamp.
- Distinguish clearly between:
  - runnable implementation,
  - illustrative pseudo-code,
  - conceptual diagrams.
- Keep human-only byline for venue submissions unless venue policy explicitly permits otherwise.
- Preserve anonymization-safe and camera-ready variants separately.

## Canonical Inputs (Phase 1 Dependencies)
- Survey manuscript: `/Users/quiznat/Desktop/Tree_of_Thought/paper.html`
- LLM markdown export: `/Users/quiznat/Desktop/Tree_of_Thought/tot-hf-agents-llm.md`
- Evidence index: `/Users/quiznat/Desktop/Tree_of_Thought/artifacts/publication-evidence/evidence-index.md`

## Canonical Outputs (Phase 2)
- Implementation code (to be added under `/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/`)
- Benchmark definitions and results under `/Users/quiznat/Desktop/Tree_of_Thought/phase2/benchmarks/`
- Reproducibility logs under `/Users/quiznat/Desktop/Tree_of_Thought/phase2/reproducibility/`
- Draft manuscript updates for novel contribution track (separate from survey-only release)

## Session Protocol
1. Review `PROJECT_STATE.md` and top `TASK_BACKLOG.md` items.
2. Execute one bounded unit of work.
3. Record outcomes, artifacts, and unresolved issues.
4. Update gate status in `ROADMAP.md` only when acceptance criteria are met.

## Evidence and Logging Rules
- Every experiment run gets a unique run ID.
- Store run metadata using `templates/experiment_record.md`.
- Use UTC timestamps in logs.
- Never delete failed run logs; mark them as invalid with reason.

## Publication Target
Primary target: TMLR-level quality (methodological rigor, reproducibility, and conservative claims), with alternate venue packaging if needed.
