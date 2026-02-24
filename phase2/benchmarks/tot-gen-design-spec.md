# ToT-Gen Design Spec (Concise)

Status: Draft for review  
Scope: Target algorithm design (not current `tot_gen` implementation)

## 1) Goal
Build a general Tree-of-Thought generator that searches over **problem decompositions**, not just candidate final answers.

The algorithm must:
- decompose problems into subproblems when useful,
- recursively solve subproblems,
- recompose child outputs into a parent result,
- validate at each level and backtrack on failure.

## 2) Core Idea
Each branch is a **reasoning plan** with an explicit recomposition contract.

Branch lifecycle:
1. Propose decomposition plan.
2. Attach recomposition contract.
3. Recursively solve child goals.
4. Recompose child results.
5. Verify parent result.
6. Keep/prune branch by score.

## 3) Required Node Schema
Every search node must carry:
- `goal`: what this node is trying to solve.
- `mode`: one of `decompose`, `solve`, `chain`.
- `children`: zero or more child goals.
- `contract`: how child outputs are combined.
- `result`: node output (if solved).
- `verification`: pass/fail + diagnostics.
- `score`: branch quality for frontier ranking.

Action semantics:
- `decompose`: split goal into child goals + attach recomposition contract.
- `solve`: attempt direct solution for current goal.
- `chain`: take one forward reasoning step and hand off to next step node.

## 4) Recomposition Contract (Mandatory)
No decomposition is valid without a contract.

Contract fields:
- `child_specs`: required output type for each child.
- `combine_instruction`: how parent merges child outputs.
- `verify_instruction`: how to test merged output.
- `failure_policy`: retry/replan/backtrack rules.

## 5) Recursion Semantics
`solve(goal)` may call `solve(subgoal_i)` for each child in a decomposition.

Base case:
- node solves directly and returns typed output.

Recursive case:
- node decomposes, solves children, recomposes, verifies.

If recomposition or verification fails:
- branch is penalized or terminated,
- search continues on alternate branches.

## 6) Search Policy
Use bounded frontier search at every level:
- branch factor `b`,
- frontier width `w`,
- max recursion depth `d`.

Ranking signal combines:
- decomposition quality,
- child completion quality,
- recomposition verification confidence.

## 7) Correctness Gates
A branch can be accepted only if:
- contract exists and is well-formed,
- all required child outputs are present and typed,
- recomposition executes,
- verification passes (task or checker-level).

Final answer must pass top-level task validation.

## 8) Failure Modes to Handle
- invalid/underspecified decomposition,
- child dependency leakage across branches,
- recomposition mismatch despite good children,
- infinite decomposition loops,
- cost blow-up from recursive branching.

Controls:
- depth/fanout/token budgets,
- cycle detection on equivalent goals,
- strict branch invalidation on missing contract.

## 9) Experimental Positioning
Treat this as a new lane: `tot_gen_recursive`.

Comparison set:
- `single`, `cot`, `cot_sc`, `react`, `tot` (legacy), `tot_gen_recursive`.

Claim boundary:
- no claim beyond tasks/models/policy frozen in the run protocol.

## 10) Acceptance Criteria (Engineering)
- recursion implemented as explicit `solve(goal)` calls, not flattened text-only loop.
- recomposition contracts logged per node.
- node-level verification trace persisted.
- deterministic replay from manifest.
- parity audit passes before confirmatory runs.
