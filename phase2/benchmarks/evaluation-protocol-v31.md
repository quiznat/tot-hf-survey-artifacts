# Evaluation Protocol v3.1 (Diagnostic Track)

Status: active  
Protocol ID: `TOT-HF-P2-EPV31-2026-02-22`

## 1. Purpose
Protocol-v3 showed task-dependent ToT behavior: strong gains over ReAct on `game24-demo` but losses on `linear2-demo` and `digit-permutation-demo`.  
This diagnostic track tests whether evaluator/search-profile changes recover ToT performance on those failure tasks.

## 2. Scope
- Tasks: `linear2-demo`, `digit-permutation-demo`
- Models (locked, no substitution):
  - `Qwen/Qwen3-Coder-Next:novita`
  - `Qwen/Qwen2.5-72B-Instruct`
  - `Qwen/Qwen2.5-Coder-32B-Instruct`
- Panel size: `n=50` paired items/task/model/profile
- Conditions per profile: `react,tot` (paired within-block comparison)

## 3. Diagnostic Profiles
- `tot_model_self_eval`:
  - evaluator: `model_self_eval`
  - search: `depth=3, branch=3, frontier=3`
- `tot_hybrid`:
  - evaluator: `hybrid`
  - search: `depth=3, branch=3, frontier=3`
- `tot_rule_based`:
  - evaluator: `rule_based`
  - search: `depth=3, branch=3, frontier=3`
- `tot_model_self_eval_lite` (lower-cost profile):
  - evaluator: `model_self_eval`
  - search: `depth=2, branch=2, frontier=2`

## 4. Locked Controls
- Sampling policy: `hf_temperature=0.0`, `hf_top_p=1.0`
- Seed policy: `item_hash`
- Bootstrap samples: `10000`
- Confidence level: `0.95`
- Max workers: `8`

## 5. Run Volume
- Blocks: `2 tasks x 3 models x 4 profiles = 24`
- Runs per block: `50 items x 2 conditions = 100`
- Total: `2400` runs

## 6. Endpoints
- Primary: `Delta(ToT - ReAct)` success rate per task/model/profile.
- Secondary:
  - Holm-corrected paired McNemar p-value for ToT vs ReAct,
  - mean ToT and ReAct latency,
  - mean token usage.

## 7. Decision Criteria
- Recovery criterion:
  - A profile is considered recovered for a task if it yields positive `ToT-ReAct` delta on at least `2/3` models with at least one Holm-corrected significant contrast (`p<0.05`).
- If no profile recovers a task:
  - move that task to adaptive routing (prefer ReAct for that task family),
  - preserve ToT for task families where paired delta remains positive.

## 8. Claim Boundaries
- Allowed:
  - "Under protocol-v3.1 profile P, ToT outperformed/underperformed ReAct on task T for model M by delta D."
- Not allowed:
  - universal claims across all tasks/models from this diagnostic subset.
