# Structured Lockset Report

Generated UTC: 2026-02-24T20:49:17Z
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
Condition tools exposed: baseline_chain_of_thought_reasoning_only_v1=[none]; baseline_chain_of_thought_self_consistency_reasoning_only_v1=[none]; baseline_react_reasoning_text_loop_only_v1=[none]; baseline_single_path_reasoning_only_v1=[none]; baseline_tree_of_thoughts_search_reasoning_only_v1=[none]
Condition surfaces: baseline_chain_of_thought_reasoning_only_v1=(cond_id:baseline-cot,alg:algorithm.reasoning.chain_of_thought_single_trajectory.v1,exec:execution_surface.prompt_reasoning_loop.v1,tools:tool_surface.no_tools.v1,memory:memory_surface.item_stateless.v1); baseline_chain_of_thought_self_consistency_reasoning_only_v1=(cond_id:baseline-cot-sc,alg:algorithm.reasoning.chain_of_thought_self_consistency_majority_vote.v1,exec:execution_surface.prompt_reasoning_loop.v1,tools:tool_surface.no_tools.v1,memory:memory_surface.item_stateless.v1); baseline_react_reasoning_text_loop_only_v1=(cond_id:baseline-react-text,alg:algorithm.reasoning.react_text_loop_reasoning_only_no_tools.v1,exec:execution_surface.prompt_reasoning_loop.v1,tools:tool_surface.no_tools.v1,memory:memory_surface.item_stateless.v1); baseline_single_path_reasoning_only_v1=(cond_id:baseline-single-path,alg:algorithm.reasoning.single_path_direct_answer.v1,exec:execution_surface.prompt_reasoning_loop.v1,tools:tool_surface.no_tools.v1,memory:memory_surface.item_stateless.v1); baseline_tree_of_thoughts_search_reasoning_only_v1=(cond_id:tot-prototype,alg:algorithm.reasoning.tree_of_thoughts_search_reasoning_only.v1,exec:execution_surface.prompt_reasoning_loop.v1,tools:tool_surface.no_tools.v1,memory:memory_surface.item_stateless.v1)
Items evaluated: 10
Runs executed: 50
Confidence level: 0.95

## Condition Summary

| Condition Key | Condition ID | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---|---:|---:|---:|---|---:|---:|---:|
| baseline_chain_of_thought_reasoning_only_v1 | baseline-cot | 10 | 1 | 0.100 | [0.018, 0.404] | 3869.1 | 34.0 | 227.0 |
| baseline_chain_of_thought_self_consistency_reasoning_only_v1 | baseline-cot-sc | 10 | 2 | 0.200 | [0.057, 0.510] | 6226.5 | 410.0 | 2235.9 |
| baseline_react_reasoning_text_loop_only_v1 | baseline-react-text | 10 | 0 | 0.000 | [0.000, 0.278] | 2421.4 | 47.0 | 157.3 |
| baseline_single_path_reasoning_only_v1 | baseline-single-path | 10 | 2 | 0.200 | [0.057, 0.510] | 1245.9 | 21.0 | 9.2 |
| baseline_tree_of_thoughts_search_reasoning_only_v1 | tot-prototype | 10 | 9 | 0.900 | [0.596, 0.982] | 25624.9 | 11448.4 | 612.6 |

## Paired Success Comparison

| Condition A Key | Condition A ID | Condition B Key | Condition B ID | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline_chain_of_thought_reasoning_only_v1 | baseline-cot | baseline_chain_of_thought_self_consistency_reasoning_only_v1 | baseline-cot-sc | 10 | 1 | 2 | 7 | -0.100 | [-0.400, 0.200] | 1.000000 | 1.000000 |
| baseline_chain_of_thought_reasoning_only_v1 | baseline-cot | baseline_react_reasoning_text_loop_only_v1 | baseline-react-text | 10 | 1 | 0 | 9 | 0.100 | [0.000, 0.300] | 1.000000 | 1.000000 |
| baseline_chain_of_thought_reasoning_only_v1 | baseline-cot | baseline_single_path_reasoning_only_v1 | baseline-single-path | 10 | 1 | 2 | 7 | -0.100 | [-0.400, 0.200] | 1.000000 | 1.000000 |
| baseline_chain_of_thought_reasoning_only_v1 | baseline-cot | baseline_tree_of_thoughts_search_reasoning_only_v1 | tot-prototype | 10 | 0 | 8 | 2 | -0.800 | [-1.000, -0.500] | 0.007812 | 0.070312 |
| baseline_chain_of_thought_self_consistency_reasoning_only_v1 | baseline-cot-sc | baseline_react_reasoning_text_loop_only_v1 | baseline-react-text | 10 | 2 | 0 | 8 | 0.200 | [0.000, 0.500] | 0.500000 | 1.000000 |
| baseline_chain_of_thought_self_consistency_reasoning_only_v1 | baseline-cot-sc | baseline_single_path_reasoning_only_v1 | baseline-single-path | 10 | 1 | 1 | 8 | 0.000 | [-0.300, 0.300] | 1.000000 | 1.000000 |
| baseline_chain_of_thought_self_consistency_reasoning_only_v1 | baseline-cot-sc | baseline_tree_of_thoughts_search_reasoning_only_v1 | tot-prototype | 10 | 0 | 7 | 3 | -0.700 | [-1.000, -0.400] | 0.015625 | 0.125000 |
| baseline_react_reasoning_text_loop_only_v1 | baseline-react-text | baseline_single_path_reasoning_only_v1 | baseline-single-path | 10 | 0 | 2 | 8 | -0.200 | [-0.500, 0.000] | 0.500000 | 1.000000 |
| baseline_react_reasoning_text_loop_only_v1 | baseline-react-text | baseline_tree_of_thoughts_search_reasoning_only_v1 | tot-prototype | 10 | 0 | 9 | 1 | -0.900 | [-1.000, -0.700] | 0.003906 | 0.039062 |
| baseline_single_path_reasoning_only_v1 | baseline-single-path | baseline_tree_of_thoughts_search_reasoning_only_v1 | tot-prototype | 10 | 0 | 7 | 3 | -0.700 | [-1.000, -0.400] | 0.015625 | 0.125000 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
