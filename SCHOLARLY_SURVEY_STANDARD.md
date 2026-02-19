# SCHOLARLY_SURVEY_STANDARD

Last updated: 2026-02-19

## Objective
Meet peer-review standards for a technical survey paper (not a blog post, not an opinion essay).

## Baseline Standard (What Reviewers Expect)
1. Clear scope and research questions:
   - Explicitly define what is in scope and out of scope.
   - State 2-5 research questions that structure the paper.
2. Transparent review method:
   - Report sources searched (databases/venues), query strings, and date window.
   - Report inclusion/exclusion criteria and screening procedure.
   - Keep a screening log with reasons for exclusion.
3. Evidence-first synthesis:
   - Every factual or quantitative claim must map to citations.
   - Separate reported results from author inference/speculation.
   - Use comparative tables based on extracted studies, not illustrative numbers.
4. Taxonomy and critical analysis:
   - Provide a defensible taxonomy and justify dimensions.
   - Analyze methodological trade-offs, assumptions, and failure modes.
   - Include contradictions and unresolved findings, not only positive results.
5. Reproducibility and reporting quality:
   - Provide extraction tables, evidence mapping, and limitations.
   - Include threats to validity (selection bias, metric mismatch, publication bias).
   - Ensure terminology and notation are consistent across sections.

## Hard Rejection Triggers To Avoid
1. Unsourced numeric claims or performance gains.
2. Mixed evidence levels (benchmarks + anecdotal examples) without labels.
3. No transparent literature selection method.
4. Promotional or speculative conclusions unsupported by the reviewed evidence.
5. Code/architecture sections presented as validated results without experiments.

## Publication Gates (Must Pass Before Submission)
1. Claim audit gate:
   - 100% of factual/quantitative statements have citations or are rewritten as non-claims.
2. Method gate:
   - Survey method section complete (search protocol, screening, criteria, dates).
3. Evidence gate:
   - Comparative tables linked to extraction sheet rows.
4. Writing gate:
   - Abstract, intro, and conclusion use scoped language (no overclaims).
5. Artifact gate:
   - References compile cleanly; figures/tables numbered and cross-referenced.

## arXiv-Specific Reality Check
1. arXiv is a preprint server, not peer review.
2. As announced by arXiv on 2025-10-31, Computer Science review/position papers are expected to be peer-reviewed before posting in CS categories.
3. Practical implication:
   - Build to peer-review standards first; treat arXiv as dissemination, not validation.

## Sources
1. IEEE Access reviewer guidance (survey expectations and review criteria): https://ieeeaccess.ieee.org/reviewers/reviewer-guidelines/
2. IEEE Communications Surveys and Tutorials policy scope (comprehensive survey/tutorial emphasis): https://www.comsoc.org/publications/journals/ieee-comst/policies
3. PRISMA 2020 statement and checklist (transparent review reporting): https://www.prisma-statement.org/prisma-2020
4. arXiv announcement (2025-10-31) on CS review/position papers: https://blog.arxiv.org/2025/10/31/attention-authors-updated-practice-for-review-articles-and-position-papers-in-arxiv-cs-category/
