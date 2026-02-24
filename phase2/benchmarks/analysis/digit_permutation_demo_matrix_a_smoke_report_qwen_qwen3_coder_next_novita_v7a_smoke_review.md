# Structured Lockset Report

Generated UTC: 2026-02-24T18:34:54Z
Task ID: digit-permutation-demo
Panel ID: digit-permutation-lockset-v4
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
Task tools available: best_divisible, is_divisible
Condition tools exposed: baseline_chain_of_thought_reasoning_only_v1=[none]; baseline_chain_of_thought_self_consistency_reasoning_only_v1=[none]; baseline_react_reasoning_text_loop_only_v1=[none]; baseline_single_path_reasoning_only_v1=[none]; baseline_tree_of_thoughts_search_reasoning_only_v1=[none]
Condition surfaces: baseline_chain_of_thought_reasoning_only_v1=(cond_id:baseline-cot,alg:algorithm.reasoning.chain_of_thought_single_trajectory.v1,exec:execution_surface.prompt_reasoning_loop.v1,tools:tool_surface.no_tools.v1,memory:memory_surface.item_stateless.v1); baseline_chain_of_thought_self_consistency_reasoning_only_v1=(cond_id:baseline-cot-sc,alg:algorithm.reasoning.chain_of_thought_self_consistency_majority_vote.v1,exec:execution_surface.prompt_reasoning_loop.v1,tools:tool_surface.no_tools.v1,memory:memory_surface.item_stateless.v1); baseline_react_reasoning_text_loop_only_v1=(cond_id:baseline-react-text,alg:algorithm.reasoning.react_text_loop_reasoning_only_no_tools.v1,exec:execution_surface.prompt_reasoning_loop.v1,tools:tool_surface.no_tools.v1,memory:memory_surface.item_stateless.v1); baseline_single_path_reasoning_only_v1=(cond_id:baseline-single-path,alg:algorithm.reasoning.single_path_direct_answer.v1,exec:execution_surface.prompt_reasoning_loop.v1,tools:tool_surface.no_tools.v1,memory:memory_surface.item_stateless.v1); baseline_tree_of_thoughts_search_reasoning_only_v1=(cond_id:tot-prototype,alg:algorithm.reasoning.tree_of_thoughts_search_reasoning_only.v1,exec:execution_surface.prompt_reasoning_loop.v1,tools:tool_surface.no_tools.v1,memory:memory_surface.item_stateless.v1)
Items evaluated: 10
Runs executed: 50
Confidence level: 0.95

## Condition Summary

| Condition Key | Condition ID | Runs | Successes | Success Rate | Success CI | Latency Mean (ms) | Tokens In Mean | Tokens Out Mean |
|---|---|---:|---:|---:|---|---:|---:|---:|
| baseline_chain_of_thought_reasoning_only_v1 | baseline-cot | 10 | 5 | 0.500 | [0.237, 0.763] | 3837.3 | 41.0 | 266.7 |
| baseline_chain_of_thought_self_consistency_reasoning_only_v1 | baseline-cot-sc | 10 | 5 | 0.500 | [0.237, 0.763] | 4618.3 | 480.0 | 2652.1 |
| baseline_react_reasoning_text_loop_only_v1 | baseline-react-text | 10 | 10 | 1.000 | [0.722, 1.000] | 2994.0 | 86.6 | 175.1 |
| baseline_single_path_reasoning_only_v1 | baseline-single-path | 10 | 8 | 0.800 | [0.490, 0.943] | 2962.0 | 28.0 | 193.7 |
| baseline_tree_of_thoughts_search_reasoning_only_v1 | tot-prototype | 10 | 10 | 1.000 | [0.722, 1.000] | 4746.5 | 438.1 | 65.3 |

## Paired Success Comparison

| Condition A Key | Condition A ID | Condition B Key | Condition B ID | Matched Items | A Better | B Better | Ties | Delta (A-B)/N | Delta CI | McNemar p | Holm p |
|---|---|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| baseline_chain_of_thought_reasoning_only_v1 | baseline-cot | baseline_chain_of_thought_self_consistency_reasoning_only_v1 | baseline-cot-sc | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline_chain_of_thought_reasoning_only_v1 | baseline-cot | baseline_react_reasoning_text_loop_only_v1 | baseline-react-text | 10 | 0 | 5 | 5 | -0.500 | [-0.800, -0.200] | 0.062500 | 0.625000 |
| baseline_chain_of_thought_reasoning_only_v1 | baseline-cot | baseline_single_path_reasoning_only_v1 | baseline-single-path | 10 | 0 | 3 | 7 | -0.300 | [-0.600, 0.000] | 0.250000 | 1.000000 |
| baseline_chain_of_thought_reasoning_only_v1 | baseline-cot | baseline_tree_of_thoughts_search_reasoning_only_v1 | tot-prototype | 10 | 0 | 5 | 5 | -0.500 | [-0.800, -0.200] | 0.062500 | 0.625000 |
| baseline_chain_of_thought_self_consistency_reasoning_only_v1 | baseline-cot-sc | baseline_react_reasoning_text_loop_only_v1 | baseline-react-text | 10 | 0 | 5 | 5 | -0.500 | [-0.800, -0.200] | 0.062500 | 0.625000 |
| baseline_chain_of_thought_self_consistency_reasoning_only_v1 | baseline-cot-sc | baseline_single_path_reasoning_only_v1 | baseline-single-path | 10 | 0 | 3 | 7 | -0.300 | [-0.600, 0.000] | 0.250000 | 1.000000 |
| baseline_chain_of_thought_self_consistency_reasoning_only_v1 | baseline-cot-sc | baseline_tree_of_thoughts_search_reasoning_only_v1 | tot-prototype | 10 | 0 | 5 | 5 | -0.500 | [-0.800, -0.200] | 0.062500 | 0.625000 |
| baseline_react_reasoning_text_loop_only_v1 | baseline-react-text | baseline_single_path_reasoning_only_v1 | baseline-single-path | 10 | 2 | 0 | 8 | 0.200 | [0.000, 0.500] | 0.500000 | 1.000000 |
| baseline_react_reasoning_text_loop_only_v1 | baseline-react-text | baseline_tree_of_thoughts_search_reasoning_only_v1 | tot-prototype | 10 | 0 | 0 | 10 | 0.000 | [0.000, 0.000] | 1.000000 | 1.000000 |
| baseline_single_path_reasoning_only_v1 | baseline-single-path | baseline_tree_of_thoughts_search_reasoning_only_v1 | tot-prototype | 10 | 0 | 2 | 8 | -0.200 | [-0.500, 0.000] | 0.500000 | 1.000000 |

## Notes
- This is a paired-condition report; each row compares outcomes on shared item IDs only.
- Claims remain scoped to the specified task/panel/model configuration.
