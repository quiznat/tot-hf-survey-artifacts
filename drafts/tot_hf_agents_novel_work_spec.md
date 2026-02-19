# ToT-HF Agents: Novel Work Specification and Research Plan

## 1. Working Title

Tree-of-Thought Search for Tool-Using Agents: A Reproducible Evaluation on Planning, Recovery, and Cost.

## 2. Research Question

Does explicit Tree-of-Thought search improve tool-using agent reliability on complex multi-step tasks under fixed compute/tool-call budgets, compared with strong linear-agent baselines?

## 3. Hypotheses

H1. ToT-enhanced agents improve task success rate on high-complexity tasks versus linear baselines.

H2. ToT-enhanced agents improve recovery rate after tool errors (API failure, malformed outputs, invalid parameters).

H3. ToT-enhanced agents increase cost and latency; hybrid gating can recover part of that overhead while preserving most quality gains.

## 4. Claimed Novelty (Target)

The novel contribution should be empirical and methodological, not rhetorical.

Candidate novelty points:
1. A concrete ToT control policy for tool-using agents with budgeted branching.
2. A reliability-centric benchmark protocol (success + recovery + cost + latency).
3. Reproducible ablations separating where gains come from:
   - search depth
   - branch factor
   - evaluator strategy
   - complexity gating

## 5. Experimental Design

### 5.1 Task suite

Use a mixed suite of tool-using tasks with at least three difficulty tiers:
- Tier A: deterministic short-horizon tasks.
- Tier B: multi-step retrieval + transformation tasks.
- Tier C: fragile tasks with injected tool failures and ambiguous plans.

Potential categories:
- Structured data extraction and synthesis.
- Multi-source retrieval with comparison and constrained output.
- Debugging/repair tasks requiring hypothesis testing.

### 5.2 Agent variants

Evaluate at least these variants:
1. Baseline linear agent (no branching).
2. ToT fixed search (beam `b`, depth `d`).
3. ToT + recovery tree around fragile steps.
4. Hybrid agent (complexity gate: linear for easy tasks, ToT for hard tasks).

### 5.3 Controlled variables

Keep fixed where possible:
- Model family/version.
- Tool set and schema definitions.
- Max total model calls.
- Max tool-call budget.
- Prompt template families.

### 5.4 Evaluation metrics

Primary:
- Task success rate.
- Recovery success rate after tool faults.

Secondary:
- Mean and p95 latency.
- Total token usage.
- Tool-call count.
- Cost per successful task.

Stability:
- Variance across seeds.
- Prompt sensitivity across predefined prompt variants.

## 6. Fault Injection Protocol

To measure recovery, inject controlled failures:
1. Timeout or transient API errors.
2. Invalid JSON/tool schema responses.
3. Missing fields or null payloads.
4. Conflicting tool results.

Report performance with and without injection.

## 7. Ablation Matrix

Minimum ablations:
1. Branch factor: 1, 2, 3, 5.
2. Depth: 1, 2, 4, 6.
3. Evaluator type:
   - scalar LLM score
   - vote-based score
   - rule-based heuristic score
4. Gating threshold for hybrid mode.

## 8. Statistical Reporting

For each metric:
- Mean and confidence interval.
- Effect size versus baseline.
- Number of runs and seeds.

Avoid single-run claims.

## 9. Reproducibility Package

Required artifacts:
1. Exact prompts and system instructions.
2. Tool schemas and implementations.
3. Config files for each variant.
4. Raw run logs with seeds and timestamps.
5. Analysis scripts that regenerate figures/tables.

Recommended:
- Public repository with tagged release.
- Frozen dependency lockfile.
- Container recipe for environment recreation.

## 10. Paper Structure (for arXiv-ready novel work)

1. Introduction and problem statement.
2. Related work (ToT, ReAct, agent planning, recovery methods).
3. Method: ToT control policy for tool-using agents.
4. Experimental setup and benchmark protocol.
5. Results (main + ablations + robustness).
6. Error analysis and failure taxonomy.
7. Limitations and ethical considerations.
8. Reproducibility checklist.
9. Conclusion.

## 11. Non-Negotiable Integrity Rules

1. No illustrative numbers in result tables.
2. No claims of improvement without measured comparison.
3. Mark all pseudo-code as pseudo-code.
4. Separate architecture proposals from validated findings.

## 12. Immediate Next Steps

1. Finalize one narrow task suite for pilot.
2. Implement baseline linear-agent harness.
3. Implement minimal ToT variant with fixed budget.
4. Run pilot on a small task subset to validate instrumentation.
5. Freeze protocol before full benchmark run.

