# Structured Lockset Report

Generated UTC: 2026-02-24T02:59:27Z
Task ID: game24-demo
Panel ID: game24-lockset-v4
Provider: smolagents
Model: Qwen/Qwen3-Coder-Next:novita
ToT evaluator mode: model_self_eval
ToT mode: model_decompose_search
ToT-gen mode: model_decompose_search
ToT decomposition rounds: 1
ToT search settings: depth=4, branch_factor=3, frontier_width=3
ToT per-condition depth overrides: legacy=4, gen=4
Seed policy: item_hash
HF temperature: 0.0
CoT temperature: 0.0
CoT-SC temperature: 0.7
ReAct temperature: 0.0
HF top-p: 1.0
Capability parity policy: strict
Parity profile: matrix_a_reasoning_only
Task tools available: calc
Condition tools exposed: cot=[none]; cot_sc=[none]; react_text=[none]; single=[none]; tot=[none]
Condition surfaces: cot=(cond_id:baseline-cot,alg:alg.reasoning.cot.v1,exec:exec.prompt_loop.v1,tools:tools.none.v1,memory:memory.item_stateless.v1); cot_sc=(cond_id:baseline-cot-sc,alg:alg.reasoning.cot_self_consistency.v1,exec:exec.prompt_loop.v1,tools:tools.none.v1,memory:memory.item_stateless.v1); react_text=(cond_id:baseline-react-text,alg:alg.reasoning.react_text_loop.v1,exec:exec.prompt_loop.v1,tools:tools.none.v1,memory:memory.item_stateless.v1); single=(cond_id:baseline-single-path,alg:alg.reasoning.single_path.v1,exec:exec.prompt_loop.v1,tools:tools.none.v1,memory:memory.item_stateless.v1); tot=(cond_id:tot-prototype,alg:alg.reasoning.tot_prototype.v1,exec:exec.prompt_loop.v1,tools:tools.none.v1,memory:memory.item_stateless.v1)
Items evaluated: 1
Runs executed: 5
Confidence level: 0.95

## Condition Summary

| Condition | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---:|---:|---:|---|---:|---:|---:|
| baseline-cot | 1 | 0 | 0.000 | [0.000, 0.793] | 3776.0 | 34.0 | 281.0 |
| baseline-cot-sc | 1 | 0 | 0.000 | [0.000, 0.793] | 4862.0 | 410.0 | 2669.0 |
| baseline-react-text | 1 | 0 | 0.000 | [0.000, 0.793] | 5273.0 | 385.0 | 401.0 |
| baseline-single-path | 1 | 1 | 1.000 | [0.207, 1.000] | 2016.0 | 21.0 | 118.0 |
| tot-prototype | 1 | 1 | 1.000 | [0.207, 1.000] | 5734.0 | 542.0 | 252.0 |

## Paired Success Comparison

| Condition A | Condition B | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline-cot | baseline-cot-sc | 1 | 0 | 0 | 1 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-cot | baseline-react-text | 1 | 0 | 0 | 1 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-cot | baseline-single-path | 1 | 0 | 1 | 0 | -1.000 | [-1.000, -1.000] | 1.000000 | 1.000000 |
| baseline-cot | tot-prototype | 1 | 0 | 1 | 0 | -1.000 | [-1.000, -1.000] | 1.000000 | 1.000000 |
| baseline-cot-sc | baseline-react-text | 1 | 0 | 0 | 1 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline-cot-sc | baseline-single-path | 1 | 0 | 1 | 0 | -1.000 | [-1.000, -1.000] | 1.000000 | 1.000000 |
| baseline-cot-sc | tot-prototype | 1 | 0 | 1 | 0 | -1.000 | [-1.000, -1.000] | 1.000000 | 1.000000 |
| baseline-react-text | baseline-single-path | 1 | 0 | 1 | 0 | -1.000 | [-1.000, -1.000] | 1.000000 | 1.000000 |
| baseline-react-text | tot-prototype | 1 | 0 | 1 | 0 | -1.000 | [-1.000, -1.000] | 1.000000 | 1.000000 |
| baseline-single-path | tot-prototype | 1 | 0 | 0 | 1 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
