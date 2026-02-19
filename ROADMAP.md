# ROADMAP

## Track 1: Scholarly Survey Publication

### Goal
Deliver a publication-grade survey manuscript on Tree of Thoughts and Hugging Face agents that meets peer-review expectations for rigor, transparency, and scholarly synthesis.

### Milestones
1. Scope and review protocol
   - Freeze explicit research questions (RQs).
   - Define search sources, query strings, and date window.
   - Define inclusion/exclusion and quality appraisal criteria.
2. Evidence acquisition
   - Run literature search and deduplicate records.
   - Build screening log with reasons for exclusion.
   - Build study extraction table (task, model, metrics, limitations).
3. Synthesis and taxonomy
   - Create defensible taxonomy for methods and evaluation settings.
   - Add comparative analysis grounded in extracted studies.
   - Separate reported evidence from design speculation.
4. Manuscript hardening
   - Add explicit methods section for the survey process.
   - Add evidence-boundary statements and threats to validity.
   - Complete citation audit and claim-evidence mapping.
5. Submission package
   - Final manuscript + bibliography + appendix artifacts.
   - PRISMA-style flow figure/checklist (adapted for CS survey use).
   - Cover letter template and venue-specific formatting pass.

### Current Progress Snapshot (2026-02-19)
1. Milestone 1: complete.
2. Milestone 2: complete (frozen run `TOT-HF-SURVEY-2026-02-19`).
3. Milestone 3: complete for survey scope (with evidence-boundary controls).
4. Milestone 4: complete (citation audit, tone neutralization, claim-evidence mapping, snippet labeling).
5. Milestone 5: in progress:
   - completed: Word export, submission manifest, arXiv conversion scaffold.
   - pending: artifact repository content publication/verification, arXiv source conversion, bibliography style normalization.

### Definition of Done (Track 1)
1. Every factual/quantitative claim is traceable to a citation or removed.
2. Survey method is transparent and reproducible.
3. Taxonomy, tables, and conclusions are evidence-backed and non-promotional.
4. Manuscript is suitable for peer-reviewed survey venues.

---

## Track 2: Original Research Project

### Goal
Produce a credible, reproducible research artifact on ToT-enhanced agent behavior.

### Milestones
1. Research question and hypothesis
   - Choose one narrow, testable claim.
2. Experimental design
   - Task suite, baselines, metrics, compute budget.
3. Implementation
   - Reproducible code path, config files, logging.
4. Evaluation
   - Main results + ablations + error analysis.
5. Paper drafting
   - Methods, experiments, limitations, ethics.
6. Release package
   - Code, configs, data instructions, reproducibility appendix.

### Definition of Done (Track 2)
1. Claims are backed by measured experiments.
2. Another person can reproduce core results from instructions.
3. Paper is category-appropriate for arXiv submission.
