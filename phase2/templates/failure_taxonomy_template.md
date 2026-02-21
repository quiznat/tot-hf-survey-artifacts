# Failure Taxonomy Template

## Metadata
- Protocol ID:
- Panel ID:
- Model:
- Provider:
- Source manifests directory:
- Generated UTC:

## Taxonomy Table
| Bucket | Count | Conditions | Representative Run IDs | Typical Signature |
|---|---:|---|---|---|
| depth_limit_no_solution |  |  |  |  |
| format_or_notation_mismatch |  |  |  |  |
| invalid_candidate_retained |  |  |  |  |
| timeout_no_final |  |  |  |  |
| other_failure |  |  |  |  |

## Bucket Definitions
- `depth_limit_no_solution`:
- `format_or_notation_mismatch`:
- `invalid_candidate_retained`:
- `timeout_no_final`:
- `other_failure`:

## Actionable Mitigations
| Bucket | Candidate Fix | Expected Effect | Validation Plan |
|---|---|---|---|
|  |  |  |  |
|  |  |  |  |

## Notes
- Keep failed manifests immutable and reference run IDs directly.
- Update this taxonomy after each ablation batch to avoid stale failure narratives.
