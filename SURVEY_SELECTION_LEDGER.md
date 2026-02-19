# SURVEY_SELECTION_LEDGER

Run ID: `TOT-HF-SURVEY-2026-02-19`  
Run date: 2026-02-19  
Manuscript anchor: `/Users/quiznat/Desktop/Tree_of_Thought/Tree of Thoughts Meets Hugging Face Agents — ClaudDib.html`

## Purpose
Provide a fixed, auditable selection ledger for the current survey manuscript version.

## Scope and Criteria Snapshot
- Scope: Tree-of-Thought-style reasoning and Hugging Face agent ecosystem integration, including method, benchmark, and implementation documentation evidence.
- Include if: record supports at least one RQ with extractable method/evidence/framework details.
- Exclude if: out of direct ToT-agent synthesis scope or lacks extractable fields for this survey.

## Fixed Counts
| Phase | Count |
|---|---:|
| Records identified | 30 |
| Duplicates removed | 0 |
| Title/abstract screened | 30 |
| Excluded at title/abstract | 0 |
| Full-text assessed | 30 |
| Full-text excluded (scope mismatch) | 8 |
| Included in qualitative thematic synthesis | 22 |
| Included in quantitative benchmark evidence tables | 2 |

Quantitative benchmark evidence table sources: `[1]`, `[26]`.

## Decision Log
### Included (22)
- `[1]` Yao et al. (ToT NeurIPS 2023)
- `[2]` Long (LLM Guided ToT)
- `[3]` Wei et al. (CoT)
- `[4]` Kojima et al. (Zero-shot CoT)
- `[5]` Wang et al. (Self-Consistency)
- `[6]` Yao et al. (ReAct)
- `[7]` Park et al. (Generative Agents)
- `[8]` Wang et al. (LLM Agents Survey)
- `[9]` Xi et al. (LLM Agents Survey)
- `[10]` Hugging Face smolagents docs
- `[11]` Hugging Face Agents Course
- `[12]` smolagents repository reference
- `[13]` Transformers agents/tools docs
- `[18]` Shinn et al. (Reflexion)
- `[20]` Schick et al. (Toolformer)
- `[21]` Qin et al. (ToolLLM)
- `[22]` Patil et al. (Gorilla)
- `[26]` Klein et al. (Fleet of Agents, ICML 2025)
- `[27]` Page et al. (PRISMA 2020 statement)
- `[28]` Wohlin (snowballing guidelines)
- `[29]` Wohlin et al. (database + snowballing study)
- `[30]` Petersen et al. (systematic mapping studies)

### Excluded (8) with reasons
- `[14]` BLOOM paper: general model-release source; out of direct ToT-agent extraction scope.
- `[15]` AI textbook: background-only source, not a primary empirical/method record for this survey.
- `[16]` AlphaGo: historical search precedent; not direct LLM-agent evidence for this scope.
- `[17]` Bandit MCTS: foundational algorithm reference used for context only.
- `[19]` API shipping-cost case study: narrow task scope, weak alignment with ToT-agent integration RQs.
- `[23]` Sociotechnical safety evaluation: broad safety framework, not direct ToT-agent method comparison.
- `[24]` Foundation model risks: broad governance/risk synthesis outside method-performance scope.
- `[25]` Unsolved ML safety problems: broad agenda paper, no direct ToT-agent extraction fields.

## Change Policy
Any record additions/removals after this run require a new run ID (e.g., `TOT-HF-SURVEY-2026-02-19-v2`) and an updated count table plus diff log.
