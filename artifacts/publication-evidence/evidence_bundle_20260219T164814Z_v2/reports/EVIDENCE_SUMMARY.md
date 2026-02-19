# Evidence Summary: ClaudDib Autonomous Manuscript Claims

**Collection Date:** 2026-02-19 UTC
**Bundle:** `/root/evidence_bundle_20260219T164814Z_v2/`
**Integrity:** `manifests/SHA256SUMS.txt` (75 files hashed)

---

## Strongly Supported (E3)

### C3: Agent Completed Initial Version Autonomously After Recovery

This claim is now strongly supported by direct session evidence:

- In recovery session `ae315b53...`, the operator states the paper "got stuck" and asks the agent to recover progress (`raw_logs/sessions_research_paper/ae315b53-18b4-491a-8eb9-a846be9bd120.jsonl`, line 7).
- The agent identifies the manuscript as truncated (~1,207 lines), decides to complete missing sections 1-3.6, and spawns a sub-agent for that exact task (lines 40-41).
- Background task completion reports successful prepend of missing sections and expansion from 1,207 to 2,084 lines (line 43).
- Assistant confirms completion to user (line 44).
- Later tool output in the same session confirms the file has 2,084 lines (`wc -l`) (line 812).

**Verdict:** Evidence now supports autonomous completion of the initial full manuscript version after recovery workflow.

### C5: Runtime Stack = OpenClaw + Kimi K2.5 + ClawVault + Scheduled Jobs

The runtime stack claim is fully corroborated by multiple independent artifacts:

- **OpenClaw config** (`configs/openclaw.json.redacted`): model set to `moonshotai/kimi-k2.5` via OpenRouter
- **systemd service** (`configs/clawdbot.service`): confirms OpenClaw gateway as PID 1 process
- **Journal log** (`raw_logs/journalctl_clawdbot_feb17-19.log`): startup line reads `[gateway] agent model: openrouter/moonshotai/kimi-k2.5` and `Registered hook: clawvault`
- **Session transcript** (`raw_logs/sessions_research_paper/707a6a7c-...jsonl`): message metadata shows `model: moonshotai/kimi-k2.5`, `provider: openrouter`, `api: openai-completions`
- **Cron jobs** (`configs/cron-jobs.json`, `configs/crontab-clawdbot.txt`): 5 OpenClaw cron jobs + 19 system cron entries confirmed
- **ClawVault** hook registered on startup; `clawvault observe` runs hourly via system cron

**Verdict:** No gaps. All four stack components (OpenClaw, Kimi K2.5, ClawVault, scheduled jobs) are independently verified.

---

## Partially Supported (E2)

### C1: Survey Was Initiated Autonomously Without Human Prompt

**What IS supported:**

The session transcript (`timelines/autonomous_initiation_timeline.md`) proves:

1. Session `707a6a7c` started at `2026-02-18T06:24:53Z` from a heartbeat cron job (`configs/cron-jobs.json`, payload: "Create 1 express post with pixel art + work on long-form essay")
2. The HEARTBEAT.md in effect (`configs/HEARTBEAT.md.as_of_20260218`) contains no instruction to write a research paper
3. At `13:22:39Z`, the agent received a heartbeat tick (`"."`), not a human instruction
4. At `13:22:47Z`, the agent internally frames a research task and spawns a sub-agent to write the manuscript
5. No human message in the initiation window instructs it to write this paper

**What is NOT fully resolved:**

- The model text says "The user wants me to...", indicating possible context-window confabulation rather than explicit user intent.
- Earlier context may have influenced this initiation mechanism, even without a direct paper prompt.

**Key artifact:** `raw_logs/sessions_research_paper/707a6a7c-5c68-43c0-85bf-662503906206.jsonl`, lines 562-567

### C2: First Draft Was Discovered During/After Agent Stall

**What IS supported:**

- The first incomplete draft (1,207 lines) was discovered by the agent in the original session at `13:25`.
- Run-state degradation occurred soon after in the same operating window: gateway timeout and embedded run timeout at `13:30-13:32` (`raw_logs/journal_runstate_13h22_to_13h35.log`, lines 61 and 66).
- Later recovery session at `16:27` explicitly references the paper being "stuck" and triggers recovery/completion (`ae315...jsonl`, line 7).

**What is NOT fully resolved:**

- Strict phrasing "discovered during/after stall" is imprecise because initial discovery happened before timeout events were recorded.
- The evidence supports a **two-step sequence**: initial discovery in normal operation, then post-stall recovery and completion.

**Recommended wording:**
"The incomplete draft was first found in-session, then later recovered and completed after a stalled/degraded run period."

### C6: Leaderboard Rank #12 (Dated Capture)

**Supported by:**
- WebFetch capture of `moltx.io/ClaudDib` (`raw_logs/moltx_clauddib_profile_capture.txt`): shows rank #12, 156 followers at `2026-02-19T16:55:00Z`
- Local SQLite time-series from `track_leaderboard.py` (`raw_logs/moltx_leaderboard_capture.txt`): 183,220 hourly snapshots showing trajectory #82 -> #12 over Feb 4-19

**Limitation:** Local data is self-collected by the same system. The leaderboard page (JS SPA) could not be independently rendered via WebFetch.

---

## Not Supported / Unverifiable (E1)

### C4: Refinement Involved Grok + Codex 5.3 Loops

**Unverifiable from server-side evidence:**

- The artifacts repo has 18 commits over ~12 hours (Feb 19 03:30 - 15:39 UTC), all by Michael Leydon.
- No commit message or server-side transcript directly attributes edits to Grok or Codex.
- Editing likely occurred on a local macOS machine not accessible during collection.

**What would close the gap:** Local machine shell history, Grok/Codex chat logs, API usage records from xAI/OpenAI.

---

## Exact Gaps to Close Before Peer Review

| # | Gap | What Would Close It | Priority |
|---|-----|---------------------|----------|
| G1 | C2 wording is too strict for the observed two-step timeline | Reword C2 to separate initial discovery from later recovery completion | **HIGH** |
| G2 | C4 tool-attribution is still unverifiable from server-only artifacts | Collect local editing logs/chats/API records for Grok and Codex | **HIGH** |
| G3 | C6 rank evidence is partly self-collected | Add independent third-party captures (timestamped screenshot/archive observer) | MEDIUM |
| G4 | Run-state durability is weak (`runs.json` purged) | Preserve immutable run snapshots during future incidents | MEDIUM |
| G5 | No native screenshot artifact chain for web evidence | Add timestamped screenshot captures to future bundles | LOW |

---

## Verdict

**0 of 6 claims are directly contradicted by current v2 evidence.**

**2 claims are strongly supported (C3, C5).**

**3 claims are partially supported and need precise wording (C1, C2, C6).**

**1 claim remains unverifiable from this server alone (C4).**

Compared with the earlier pass, v2 materially improves the evidentiary position by adding direct recovery-session transcripts that support autonomous completion of the full manuscript. The main remaining publication blockers are wording precision (C2) and external tool-attribution evidence (C4).
