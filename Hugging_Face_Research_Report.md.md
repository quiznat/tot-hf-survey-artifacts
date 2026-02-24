# Hugging Face Primer for Phase 2 Reset

Date: 2026-02-23  
Authoring intent: canonical decision primer for what to introduce, when, and why across the experimental -> engineering spectrum.

## 0) Canonical frame from Phase 1 paper

This primer is anchored to the project's own survey framing in `/Users/quiznat/Desktop/Tree_of_Thought/paper.html`:

1. Section 3.1 defines the active HF agent ecosystem for this work as:
`Agent Course` + `smolagents` + `legacy transformers-agents docs for migration context`.
2. Section 3.1 explicitly notes `transformers` agents are deprecated and migrated to `smolagents`.
3. Sections 3.4-3.7 frame `CodeAgent`, `MultiStepAgent`, tools, security, and deployment as the practical implementation surface.

Interpretation for Phase 2:

1. The canonical runtime stack for this project is `smolagents` first.
2. `transformers` agents are historical context, not a runtime target.
3. If we claim "dogfood the survey," Phase 2 must run on the smolagents-native capability surface with strict parity controls.

## 1) Real Hugging Face state (as of this reset)

## 1.1 Agent layer (directly relevant now)

| Capability | Current state | Why it matters for Phase 2 |
|---|---|---|
| `smolagents` | Active HF agent framework | Canonical runtime for ReAct/ToT-style agent experiments |
| `CodeAgent` | Code-as-action agent | Powerful, but adds execution capability confounds |
| `ToolCallingAgent` | Structured tool-calling agent | Better controlled capability surface for fair comparisons |
| `MultiStepAgent` | Planning-oriented orchestration | Useful when studying planning/replanning, but must be parity-matched |
| Secure executors (`local`, `docker`, `e2b`, `modal`, `wasm`, etc.) | Available in smolagents patterns | Security and runtime policy controls; also a confound source if inconsistent |

## 1.2 Inference layer (directly relevant now)

| Capability | Current state | Why it matters for Phase 2 |
|---|---|---|
| Inference Providers router | Unified multi-provider inference | Good for velocity; risky for reproducibility unless model+provider are pinned |
| `InferenceClient` / `InferenceClientModel` | Standard client path | Should be the common model interface across all conditions |
| OpenAI-compatible HF router endpoint | Available | Useful integration path, but avoid dynamic routing policies for confirmatory runs |
| Dedicated Inference Endpoints | Available (managed, dedicated infra) | Best route for confirmatory stability once protocol is frozen |

## 1.3 Platform/ops layer (mostly later-stage)

| Capability | Current state | Why it matters for Phase 2 |
|---|---|---|
| Hub repos + cards + revisions | Core platform substrate | Needed for artifact provenance and citation-quality traceability |
| Jobs (scheduled/background) | Available | Good for matrix automation after protocol freeze |
| Spaces | Available | Best for demos and public presentation, not primary inferential evidence |
| Webhooks and org controls | Available | Useful for CI/governance once moving beyond research-only execution |

## 2) What your current Phase 2 code is actually doing

Code truth in this repo:

1. Provider is hard-locked to smolagents path:
`/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src/phase2_baselines/pipeline.py`
2. ReAct path uses smolagents `CodeAgent`:
`/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src/phase2_baselines/runners/react.py`
3. ToT path currently runs prompt-driven tree search without CodeAgent execution:
`/Users/quiznat/Desktop/Tree_of_Thought/phase2/code/src/phase2_baselines/runners/tot.py`

Reset implication:

1. Some condition families are not capability-parity equivalent.
2. Historical deltas can reflect capability differences (execution/tool affordances), not just reasoning strategy quality.
3. Prior runs should remain frozen as exploratory engineering evidence unless parity is demonstrated.

## 3) Canonical introduction plan: experimental -> engineering

Stages:

1. `S0` Exploratory: rapid iteration, no inferential claims.
2. `S1` Controlled experiments: fair strategy comparison.
3. `S2` Confirmatory research: publication-grade inference.
4. `S3` Engineering hardening: reliability/security/cost.
5. `S4` Production/public surface: demos and operations.

### 3.1 Earliest safe introduction point

| Element | Earliest stage | Must be parity-equalized for comparative claims? | Notes |
|---|---|---|---|
| Fixed `HF_TOKEN` auth + pinned model/provider | S0 | Yes | Mandatory baseline control |
| `InferenceClientModel` as shared model interface | S0 | Yes | Keep one interface across all conditions |
| Tool-free prompting baselines (single/CoT/ToT) | S0 | Yes | Best clean algorithmic baseline family |
| `ToolCallingAgent` with shared tool set | S1 | Yes | Good agentic comparison surface |
| `CodeAgent` with execution | S2 | Yes | Only valid if every compared condition has equivalent execution power |
| External web/search/data tools | S2 | Yes | Treat tool surface as part of hypothesis class |
| Dedicated Inference Endpoints | S2 | No (infra) | Strongly recommended for confirmatory stability |
| Sandboxed executors (`docker`/`e2b`/`modal`/`wasm`) | S3 | Yes if used in compared arms | Introduce after method freeze unless this is the variable under study |
| Jobs orchestration | S3 | No (infra) | Useful once command set and image are frozen |
| Spaces deployment | S4 | No (presentation) | Demo/reporting layer, not evidence generator |

## 4) Three valid matrix designs (pick one per series)

## 4.1 Matrix A: Reasoning-only (cleanest science)

1. No runtime code execution.
2. No external tools.
3. Compare single vs CoT vs CoT-SC vs ReAct-style text-only vs ToT.
4. Primary question: reasoning policy effect under matched capability.

## 4.2 Matrix B: Tool-calling parity (agentic but controlled)

1. Shared `ToolCallingAgent` (or shared equivalent abstraction) across all conditions.
2. Identical tool registry, schemas, and call budget.
3. No condition-specific hidden tools.
4. Primary question: planning/search policy effect with fixed tool access.

## 4.3 Matrix C: Code-execution parity (full smolagents dogfood)

1. Shared CodeAgent execution policy across all conditions.
2. Identical executor type, import allowlist, step budget, and sandbox policy.
3. ToT, CoT, ReAct differ only in planning/search logic, not runtime affordances.
4. Primary question: planning/search effect in code-executing agent regime.

Invalid design pattern:
mixing prompt-only ToT with code-executing ReAct in a single inferential claim table.

## 5) Recommended Phase 2 reset choice

If the goal is publication-grade causal clarity first:

1. Run Matrix A first (reasoning-only) as canonical baseline.
2. Then run Matrix B (tool-calling parity).
3. Treat Matrix C as engineering-forward extension once A/B are stable.

If the goal is "100% survey dogfood" first:

1. Jump directly to Matrix C.
2. Accept that this becomes an agent-runtime study, not pure reasoning-only comparison.
3. Keep a separate reasoning-only appendix for causal grounding.

## 6) Concrete checklist for the next frozen protocol

1. Declare matrix mode (`A`, `B`, or `C`) in protocol header.
2. Publish a capability manifest per condition:
model interface, executor policy, tool registry hash, import allowlist, memory policy.
3. Add startup hard-fail checks:
abort run if condition capabilities diverge from frozen manifest.
4. Freeze provider/model/runtime versions and prompt hashes.
5. Keep exploratory and confirmatory panels disjoint.
6. Predeclare tests and multiplicity correction.
7. Record every run manifest with seed, temperature, provider, model, tool/executor policy.

## 7) Full HF capability landscape (for planning beyond Phase 2)

This is the "whole map" so you can decide what stays out of scope now.

1. Hub substrate: repos, revisions, PRs/discussions, cards, collections, paper pages/DOI, webhooks, governance controls.
2. Inference: Providers router, OpenAI-compatible endpoint, InferenceClient APIs, dedicated Endpoints, engine selection.
3. Agents: smolagents (CodeAgent, ToolCallingAgent, MultiStep patterns), secure executors, MCP integration surfaces.
4. Data/training: `datasets`, `transformers`, `accelerate`, `peft`, `trl`, `optimum`, `diffusers`.
5. Evaluation: `evaluate`, `lighteval`, benchmark/report publishing.
6. App/ops: Spaces, Jobs, scheduled Jobs, CI automation.
7. Security/compliance: token scopes, gated assets, malware/pickle scanning, org audit/security controls.

Planning note:
for this project's current research question, categories 1-3 are core; 4-7 are mostly expansion/production layers.

## 8) Source anchors

Project anchor:

1. `/Users/quiznat/Desktop/Tree_of_Thought/paper.html` (Section 3.1 through 3.7).

Official Hugging Face docs:

1. Hub docs index: https://huggingface.co/docs/hub/en/index
2. Inference Providers: https://huggingface.co/docs/inference-providers/index
3. Inference Endpoints: https://huggingface.co/docs/inference-endpoints/main/en/about
4. `huggingface_hub` InferenceClient: https://huggingface.co/docs/huggingface_hub/en/package_reference/inference_client
5. smolagents docs: https://huggingface.co/docs/smolagents/en/index
6. smolagents secure execution: https://huggingface.co/docs/smolagents/en/tutorials/secure_code_execution
7. Spaces overview: https://huggingface.co/docs/hub/en/spaces-overview
8. Jobs overview: https://huggingface.co/docs/hub/en/jobs
9. Security tokens: https://huggingface.co/docs/hub/main/security-tokens
