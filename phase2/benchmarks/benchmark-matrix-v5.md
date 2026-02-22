# Benchmark Matrix v5 (Base Reasoning Patterns)

| Task ID | Description | Panel File | Items | Conditions | Notes |
|---|---|---|---:|---|---|
| `game24-demo` | Arithmetic expression synthesis | `phase2/benchmarks/panels/game24_lockset_v4.json` | 50 | `single,cot,cot_sc,react,tot` | disjoint panel reused from v4 |
| `subset-sum-demo` | Subset selection to target sum | `phase2/benchmarks/panels/subset_sum_lockset_v4.json` | 50 | `single,cot,cot_sc,react,tot` | disjoint panel reused from v4 |
| `linear2-demo` | 2x2 linear system solving | `phase2/benchmarks/panels/linear2_lockset_v4.json` | 50 | `single,cot,cot_sc,react,tot` | disjoint panel reused from v4 |
| `digit-permutation-demo` | Max divisible permutation | `phase2/benchmarks/panels/digit_permutation_lockset_v4.json` | 50 | `single,cot,cot_sc,react,tot` | disjoint panel reused from v4 |

Locked models:
- `Qwen/Qwen3-Coder-Next:novita`
- `Qwen/Qwen2.5-72B-Instruct`
- `Qwen/Qwen2.5-Coder-32B-Instruct`
