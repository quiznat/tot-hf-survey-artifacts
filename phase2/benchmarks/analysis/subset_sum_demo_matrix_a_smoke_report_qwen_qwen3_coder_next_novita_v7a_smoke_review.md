# Structured Lockset Report

Generated UTC: 2026-02-24T18:34:54Z
Task ID: subset-sum-demo
Panel ID: subset-sum-lockset-v4
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
Task tools available: check_target, sum_list
Condition tools exposed: baseline_chain_of_thought_reasoning_only_v1=[none]; baseline_chain_of_thought_self_consistency_reasoning_only_v1=[none]; baseline_react_reasoning_text_loop_only_v1=[none]; baseline_single_path_reasoning_only_v1=[none]; baseline_tree_of_thoughts_search_reasoning_only_v1=[none]
Condition surfaces: baseline_chain_of_thought_reasoning_only_v1=(cond_id:baseline-cot,alg:algorithm.reasoning.chain_of_thought_single_trajectory.v1,exec:execution_surface.prompt_reasoning_loop.v1,tools:tool_surface.no_tools.v1,memory:memory_surface.item_stateless.v1); baseline_chain_of_thought_self_consistency_reasoning_only_v1=(cond_id:baseline-cot-sc,alg:algorithm.reasoning.chain_of_thought_self_consistency_majority_vote.v1,exec:execution_surface.prompt_reasoning_loop.v1,tools:tool_surface.no_tools.v1,memory:memory_surface.item_stateless.v1); baseline_react_reasoning_text_loop_only_v1=(cond_id:baseline-react-text,alg:algorithm.reasoning.react_text_loop_reasoning_only_no_tools.v1,exec:execution_surface.prompt_reasoning_loop.v1,tools:tool_surface.no_tools.v1,memory:memory_surface.item_stateless.v1); baseline_single_path_reasoning_only_v1=(cond_id:baseline-single-path,alg:algorithm.reasoning.single_path_direct_answer.v1,exec:execution_surface.prompt_reasoning_loop.v1,tools:tool_surface.no_tools.v1,memory:memory_surface.item_stateless.v1); baseline_tree_of_thoughts_search_reasoning_only_v1=(cond_id:tot-prototype,alg:algorithm.reasoning.tree_of_thoughts_search_reasoning_only.v1,exec:execution_surface.prompt_reasoning_loop.v1,tools:tool_surface.no_tools.v1,memory:memory_surface.item_stateless.v1)
Items evaluated: 10
Runs executed: 50
Confidence level: 0.95

## Condition Summary

| Condition Key | Condition ID | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---|---:|---:|---:|---|---:|---:|---:|
| baseline_chain_of_thought_reasoning_only_v1 | baseline-cot | 10 | 8 | 0.800 | [0.490, 0.943] | 3220.5 | 66.2 | 176.7 |
| baseline_chain_of_thought_self_consistency_reasoning_only_v1 | baseline-cot-sc | 10 | 9 | 0.900 | [0.596, 0.982] | 4911.0 | 732.0 | 2071.6 |
| baseline_react_reasoning_text_loop_only_v1 | baseline-react-text | 10 | 2 | 0.200 | [0.057, 0.510] | 4719.2 | 378.1 | 276.2 |
| baseline_single_path_reasoning_only_v1 | baseline-single-path | 10 | 5 | 0.500 | [0.237, 0.763] | 974.0 | 53.2 | 1.9 |
| baseline_tree_of_thoughts_search_reasoning_only_v1 | tot-prototype | 10 | 10 | 1.000 | [0.722, 1.000] | 5051.8 | 555.7 | 72.7 |

## Paired Success Comparison

| Condition A Key | Condition A ID | Condition B Key | Condition B ID | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline_chain_of_thought_reasoning_only_v1 | baseline-cot | baseline_chain_of_thought_self_consistency_reasoning_only_v1 | baseline-cot-sc | 10 | 0 | 1 | 9 | -0.100 | [-0.300, 0.000] | 1.000000 | 1.000000 |
| baseline_chain_of_thought_reasoning_only_v1 | baseline-cot | baseline_react_reasoning_text_loop_only_v1 | baseline-react-text | 10 | 6 | 0 | 4 | 0.600 | [0.300, 0.900] | 0.031250 | 0.250000 |
| baseline_chain_of_thought_reasoning_only_v1 | baseline-cot | baseline_single_path_reasoning_only_v1 | baseline-single-path | 10 | 4 | 1 | 5 | 0.300 | [-0.100, 0.700] | 0.375000 | 1.000000 |
| baseline_chain_of_thought_reasoning_only_v1 | baseline-cot | baseline_tree_of_thoughts_search_reasoning_only_v1 | tot-prototype | 10 | 0 | 2 | 8 | -0.200 | [-0.500, 0.000] | 0.500000 | 1.000000 |
| baseline_chain_of_thought_self_consistency_reasoning_only_v1 | baseline-cot-sc | baseline_react_reasoning_text_loop_only_v1 | baseline-react-text | 10 | 7 | 0 | 3 | 0.700 | [0.400, 1.000] | 0.015625 | 0.140625 |
| baseline_chain_of_thought_self_consistency_reasoning_only_v1 | baseline-cot-sc | baseline_single_path_reasoning_only_v1 | baseline-single-path | 10 | 4 | 0 | 6 | 0.400 | [0.100, 0.700] | 0.125000 | 0.750000 |
| baseline_chain_of_thought_self_consistency_reasoning_only_v1 | baseline-cot-sc | baseline_tree_of_thoughts_search_reasoning_only_v1 | tot-prototype | 10 | 0 | 1 | 9 | -0.100 | [-0.300, 0.000] | 1.000000 | 1.000000 |
| baseline_react_reasoning_text_loop_only_v1 | baseline-react-text | baseline_single_path_reasoning_only_v1 | baseline-single-path | 10 | 2 | 5 | 3 | -0.300 | [-0.800, 0.200] | 0.453125 | 1.000000 |
| baseline_react_reasoning_text_loop_only_v1 | baseline-react-text | baseline_tree_of_thoughts_search_reasoning_only_v1 | tot-prototype | 10 | 0 | 8 | 2 | -0.800 | [-1.000, -0.500] | 0.007812 | 0.078125 |
| baseline_single_path_reasoning_only_v1 | baseline-single-path | baseline_tree_of_thoughts_search_reasoning_only_v1 | tot-prototype | 10 | 0 | 5 | 5 | -0.500 | [-0.800, -0.200] | 0.062500 | 0.437500 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
