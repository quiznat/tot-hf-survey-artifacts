# Evaluation Protocol v5.1 (Hybrid Profile Sweep)

Status: active scaffold (frozen profile grid)
Freeze date: 2026-02-22
Protocol ID: `TOT-HF-P2-EPV51-2026-02-22`

## 1. Purpose
Run controlled profile sweeps after base-pattern v5 mapping to test hybrid combinations of:
- ToT evaluator strategy (`model_self_eval`, `hybrid`, `rule_based`)
- ToT search budget (`3/3/3`, `4/4/4`)

Base conditions remain fixed (`single,cot,cot_sc,react,tot`) so profile changes isolate ToT-policy effects.

## 2. Series
- primary series: `protocol_v51_hybrid_matrix`
- report tag: `v51`

## 3. Frozen Profiles
- `tot_model_self_eval`: evaluator=`model_self_eval`, depth/breadth/frontier=`3/3/3`, `cot_sc_samples=5`
- `tot_hybrid_eval`: evaluator=`hybrid`, depth/breadth/frontier=`3/3/3`, `cot_sc_samples=5`
- `tot_rule_based_eval`: evaluator=`rule_based`, depth/breadth/frontier=`3/3/3`, `cot_sc_samples=5`
- `tot_deep_search`: evaluator=`model_self_eval`, depth/breadth/frontier=`4/4/4`, `cot_sc_samples=5`

## 4. Frozen Tasks/Models/Panels
Tasks:
- `game24-demo`
- `subset-sum-demo`
- `linear2-demo`
- `digit-permutation-demo`

Panels:
- same disjoint v4 panels used by v5

Models:
- `Qwen/Qwen3-Coder-Next:novita`
- `Qwen/Qwen2.5-72B-Instruct`
- `Qwen/Qwen2.5-Coder-32B-Instruct`

## 5. Run Volume
Per task-model-profile block:
- `5 conditions x 50 items = 250` runs.

Full matrix:
- `4 tasks x 3 models x 4 profiles x 250 = 12000` runs.

## 6. Statistical Plan
Per block:
- condition-level Wilson CI
- paired bootstrap delta CI
- exact McNemar + Holm correction

Primary profile-level contrasts:
- `ToT - ReAct`
- `ToT - CoT-SC`

## 7. Guardrails
- no model substitution in-run
- no mid-run prompt/code changes
- capability parity for `react`/`tot` locked to `equalize_react_to_tot` or `strict`
