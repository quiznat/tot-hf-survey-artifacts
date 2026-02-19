# Chain of Custody

## Collection Metadata

| Field | Value |
|-------|-------|
| **Collector** | Claude Code (Anthropic Opus 4.6) acting as forensic evidence collector |
| **Operator** | Root user on production host (see system_provenance.md) |
| **Collection Start (UTC)** | 2026-02-19T16:48:14Z |
| **Collection End (UTC)** | 2026-02-19T16:55:00Z (latest explicit capture timestamp in bundle artifacts) |
| **Host** | openclaw124onubuntu-s-2vcpu-4gb-120gb-intel-nyc3-01 |
| **Host IP** | DigitalOcean droplet (NYC3 region) |
| **OS** | Ubuntu 24.04.1 LTS, kernel 6.8.0-94-generic |
| **Timezone** | UTC (Etc/UTC), NTP synchronized |
| **Collection Method** | Read-only file inspection, git log queries, journalctl reads, WebFetch captures |

## Hash Manifest

- **File:** `manifests/SHA256SUMS.txt`
- **Algorithm:** SHA-256
- **Scope:** All files in this bundle except the manifest itself
- **Verification:** `cd <bundle_dir> && sha256sum -c manifests/SHA256SUMS.txt`

## What Was Collected

### From This Server (read-only)
1. **System provenance:** hostname, kernel, timezone, software versions
2. **Service configs:** systemd unit, drop-ins, OpenClaw config (redacted), cron jobs, crontabs
3. **Session transcripts:** 12 JSONL files from OpenClaw agent sessions (Feb 18-19)
4. **System journal:** journalctl output for clawdbot service (Feb 17-19)
5. **Application logs:** 22 log files from workspace/logs/ (date-filtered for large files)
6. **Git history:** Full git log/blame/diff for manuscript files in agent and website repos
7. **File metadata:** stat/ls output for all manuscript files
8. **Web captures:** WebFetch of moltx.io/ClaudDib profile, attempted moltx.io/leaderboard

### From GitHub (via gh CLI, read-only)
9. **Artifacts repo metadata:** quiznat/tot-hf-survey-artifacts commit history, file tree, README
10. **Artifacts repo content:** README.md, ARXIV_CONVERSION_NOTES.md, paper.html search

## What Was NOT Collected (Limitations)

1. **Local macOS machine:** The artifacts repo originated on a local machine (`/Users/quiznat/Desktop/Tree_of_Thought/drafts/`). That machine was not accessible during this collection. Evidence of Grok/Codex 5.3 usage would reside there.
2. **Full paper content:** The 87KB research paper was not copied into the bundle to avoid IP concerns. Git history and first-20-line excerpts were captured instead.
3. **WebFetch limitations:** The MoltX leaderboard page is a JavaScript SPA and could not be rendered by WebFetch. Only the profile page was captured.
4. **Screenshots:** No actual screenshot tool was available. Text-based captures were substituted.
5. **Third-party verification:** Leaderboard data is self-collected by the agent's own `track_leaderboard.py` script. No independent third-party archive exists.
6. **OpenRouter API logs:** No access to OpenRouter's logs to independently verify model usage/token counts.
7. **Intermediate file versions:** The paper grew from 32KB to 87KB between sessions. No intermediate versions were found on this server — the expansion likely occurred on the local macOS machine.

## Integrity Notes

- **No system modifications were made** during this collection. All operations were read-only (file reads, git log, journalctl, stat, WebFetch).
- **Secret redaction** was applied to all config files. Redaction used pattern matching for API keys, tokens, passwords. Redacted values replaced with `[REDACTED]`.
- **Session transcripts** were copied verbatim from source files. No content was added or removed.
- **Timestamps** are from the host system clock, which is NTP-synchronized to UTC.
- **Git history** reflects the state of repositories at collection time. Git objects are content-addressed (SHA-1) and tamper-evident.

## Custody Transfer

This bundle was collected on the production server and resides at:
```
/root/evidence_bundle_20260219T164814Z_v2/
```

To verify integrity after transfer:
```bash
cd /path/to/evidence_bundle_20260219T164814Z_v2
sha256sum -c manifests/SHA256SUMS.txt
```
