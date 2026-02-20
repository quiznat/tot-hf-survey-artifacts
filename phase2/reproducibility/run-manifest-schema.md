# Run Manifest Schema (Draft v0)

Last updated: 2026-02-20

Every benchmark run must emit a manifest record with these fields.

## Required Fields
- `run_id`: unique identifier.
- `timestamp_utc`: ISO-8601 UTC timestamp.
- `task_id`: benchmark task identifier.
- `condition_id`: baseline or ToT variant identifier.
- `model_name`: full model identifier.
- `provider`: model/API provider.
- `agent_framework`: framework/library + version.
- `prompt_template_version`: prompt/config revision ID.
- `search_config`: depth, breadth, pruning, stop policy.
- `tool_config`: enabled tools and versions.
- `seed`: random seed (or `null` if unsupported).
- `budget`: token/time/cost budget settings.
- `outcome`: success/failure/invalid/timeout.
- `metrics`: success, latency_ms, tokens_in, tokens_out, cost_usd.
- `artifact_paths`: paths to logs, traces, outputs.
- `notes`: short free-text notes.

## Optional Fields
- `error_type`: categorized failure label.
- `hardware_context`: machine/runner details.
- `dependency_lock_hash`: environment lock fingerprint.

## Validation Rules
- No missing required fields.
- `timestamp_utc` must be UTC.
- `run_id` must be unique in run log.
- `artifact_paths` must resolve to existing files.
