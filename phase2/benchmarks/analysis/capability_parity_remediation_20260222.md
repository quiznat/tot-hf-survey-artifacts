# Capability Parity Remediation (2026-02-22)

## Scope Audited
- `phase2/code/src/phase2_baselines/tasks/arithmetic24.py`
- `phase2/code/src/phase2_baselines/tasks/subset_sum.py`
- `phase2/code/src/phase2_baselines/tasks/linear2.py`
- `phase2/code/src/phase2_baselines/tasks/digit_permutation.py`
- `phase2/code/src/phase2_baselines/runners/react.py`
- `phase2/code/src/phase2_baselines/runners/tot.py`
- `phase2/code/src/phase2_baselines/pipeline.py`
- `phase2/code/scripts/run_structured_lockset.py`
- `phase2/code/scripts/run_protocol_v3_matrix.py`
- `phase2/code/scripts/run_protocol_v31_diagnostics.py`
- `phase2/code/tests/test_pipeline_hf.py`
- `phase2/code/tests/test_runner_smoke.py`

## Historical Audit Result
- Source artifact: `phase2/benchmarks/analysis/capability_parity_audit.md`
- Machine-readable data: `phase2/benchmarks/analysis/capability_parity_audit.json`
- Findings summary:
  - `10` high-severity paired tool mismatches (`react` tool-enabled vs `tot` tool-disabled).
  - `9` medium-severity manifest tool declaration mismatches (React was hardcoded as `calc` even for non-Game24 tasks).
- Affected historical run series:
  - `protocol_v3_matrix`
  - `protocol_v31_diagnostic`
  - `protocol_v31_smoke_patch1`
  - `protocol_v32_diagnostic`

## Remediation Implemented
1. Enforced parity policy in runner launch path.
   - Added policy gate in `phase2/code/scripts/run_structured_lockset.py` (`_resolve_capability_plan`).
   - Added CLI option: `--capability-parity-policy {equalize_react_to_tot,strict,off}`.
   - Default policy is `equalize_react_to_tot` for paired `react,tot` runs.

2. Made React tool access explicit and controllable.
   - `phase2/code/src/phase2_baselines/runners/react.py` now honors `react_enable_tools`.
   - Prompt tool list respects enforced tool exposure via `tools_override`.

3. Fixed manifest tool declarations to be task-accurate.
   - `phase2/code/src/phase2_baselines/pipeline.py` no longer hardcodes `["calc"]` for all React runs.
   - React `tool_config` now reflects task tools or `[]` if parity equalization disables tools.

4. Added parity metadata to manifests and reports.
   - Manifests include `capability_parity_policy`, `task_tools_available`, and `condition_tools_exposed`.
   - Structured lockset report markdown/json now records the capability parity settings used.

5. Propagated policy through orchestrators/docs.
   - `phase2/code/scripts/run_protocol_v3_matrix.py`
   - `phase2/code/scripts/run_protocol_v31_diagnostics.py`
   - `phase2/benchmarks/evaluation-protocol-v3.md`
   - `phase2/benchmarks/evaluation-protocol-v31.md`
   - `phase2/benchmarks/protocol-v3-execution.md`
   - `phase2/benchmarks/protocol-v31-execution.md`

## Verification Evidence
- Unit tests: `34` passing
  - Command: `PYTHONPATH=... python3 -m unittest discover -s tests`
- New parity tests:
  - `test_react_tool_config_matches_task_tools`
  - `test_react_tools_can_be_disabled_for_parity`
  - `test_react_can_disable_tools_for_capability_parity`
- Strict policy guard behavior validated:
  - `--capability-parity-policy strict` aborts `react,tot` runs when tool exposure differs.
- Equalized run behavior validated:
  - sample run (`tmp_capability_equalized`) produced both conditions with `tool_config=[]`.
  - audit output: `phase2/benchmarks/analysis/capability_parity_audit_tmp_equalized.json` (`findings=0`).

## Current Rule For Future Runs
- Paired `react` vs `tot` comparisons must run with explicit capability parity policy.
- Default enforced behavior (`equalize_react_to_tot`) disables React tools when ToT has no tools.
- To run a mismatched comparison intentionally, operator must explicitly pass `--capability-parity-policy off` and disclose it as non-parity.
