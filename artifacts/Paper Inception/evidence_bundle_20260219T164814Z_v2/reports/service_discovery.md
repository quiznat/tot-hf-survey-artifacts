# Service Discovery Report

**Collected:** 2026-02-19T16:55:00Z  
**System:** ClaudDib AI social media agent (OpenClaw engine)  
**Server:** DigitalOcean droplet, Linux 6.8.0-94-generic  

---

## 1. Systemd Services and Timers

### 1.1 Matching Units (`*claw*`, `*agent*`, `*openclaw*`, `*clauddib*`)

```
UNIT                  LOAD   ACTIVE SUB     DESCRIPTION
clawdbot.service      loaded active running Clawdbot Gateway Service
do-agent.service      loaded active running The DigitalOcean Monitoring Agent
droplet-agent.service loaded active running The DigitalOcean Droplet Agent
```

**Findings:**
- `clawdbot.service` is the primary OpenClaw gateway service (active and running)
- `do-agent.service` and `droplet-agent.service` are DigitalOcean infrastructure agents (not related to ClaudDib)
- No other OpenClaw/ClaudDib-related systemd units found
- No systemd timers matching these patterns -- all scheduled work uses cron

### 1.2 All System Timers

```
NEXT                          LEFT LAST                              PASSED UNIT                           ACTIVATES
Thu 2026-02-19 17:00:00 UTC   7min Thu 2026-02-19 16:50:01 UTC 2min 35s ago sysstat-collect.timer          sysstat-collect.service
Thu 2026-02-19 17:31:54 UTC  39min Thu 2026-02-19 16:13:30 UTC    39min ago fwupd-refresh.timer            fwupd-refresh.service
Thu 2026-02-19 23:33:07 UTC     6h Thu 2026-02-19 12:45:27 UTC  4h 7min ago apt-daily.timer                apt-daily.service
Fri 2026-02-20 00:00:00 UTC     7h Thu 2026-02-19 00:00:01 UTC      16h ago dpkg-db-backup.timer           dpkg-db-backup.service
Fri 2026-02-20 00:00:00 UTC     7h Thu 2026-02-19 00:00:01 UTC      16h ago logrotate.timer                logrotate.service
Fri 2026-02-20 00:07:00 UTC     7h Thu 2026-02-19 00:07:08 UTC      16h ago sysstat-summary.timer          sysstat-summary.service
Fri 2026-02-20 01:36:06 UTC     8h Thu 2026-02-19 13:51:08 UTC  3h 1min ago motd-news.timer                motd-news.service
Fri 2026-02-20 02:10:43 UTC     9h Thu 2026-02-19 02:10:43 UTC      14h ago update-notifier-download.timer update-notifier-download.service
Fri 2026-02-20 02:21:11 UTC     9h Thu 2026-02-19 02:21:11 UTC      14h ago systemd-tmpfiles-clean.timer   systemd-tmpfiles-clean.service
Fri 2026-02-20 02:49:42 UTC     9h Thu 2026-02-19 05:48:04 UTC      11h ago man-db.timer                   man-db.service
Fri 2026-02-20 06:50:44 UTC    13h Thu 2026-02-19 06:47:28 UTC      10h ago apt-daily-upgrade.timer        apt-daily-upgrade.service
Sun 2026-02-22 03:10:14 UTC 2 days Sun 2026-02-15 03:10:59 UTC   4 days ago e2scrub_all.timer              e2scrub_all.service
Mon 2026-02-23 01:39:27 UTC 3 days Mon 2026-02-16 01:33:02 UTC   3 days ago fstrim.timer                   fstrim.service
Wed 2026-02-25 20:01:20 UTC 6 days Mon 2026-02-16 15:45:37 UTC   3 days ago update-notifier-motd.timer     update-notifier-motd.service
-                                - -                                      - apport-autoreport.timer        apport-autoreport.service
-                                - -                                      - snapd.snap-repair.timer        snapd.snap-repair.service
-                                - -                                      - ua-timer.timer                 ua-timer.service
```

**Findings:** All standard OS timers. No custom ClaudDib-related systemd timers.

### 1.3 clawdbot.service Unit File

**File:** `/etc/systemd/system/clawdbot.service`

```ini
[Unit]
Description=Clawdbot Gateway Service
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=clawdbot
Group=clawdbot
WorkingDirectory=/opt/clawdbot
EnvironmentFile=/opt/clawdbot.env
Environment="HOME=/home/clawdbot"
Environment="NODE_ENV=production"
Environment="PATH=/home/clawdbot/.npm/bin:/home/clawdbot/homebrew/bin:/usr/local/bin:/usr/bin:/bin:"

ExecStart=/usr/bin/node /opt/clawdbot/dist/index.js gateway --port ${CLAWDBOT_GATEWAY_PORT}

Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
LimitNOFILE=65536

# Security hardening
NoNewPrivileges=yes
ProtectSystem=strict
PrivateTmp=yes
ProtectKernelTunables=yes
ProtectKernelModules=yes
ProtectControlGroups=yes
RestrictSUIDSGID=yes
ReadWritePaths=/home/clawdbot/.openclaw
ReadWritePaths=/home/clawdbot
ReadOnlyPaths=/opt/clawdbot

[Install]
WantedBy=multi-user.target
```

**Key observations:**
- Runs as `clawdbot:clawdbot` user/group
- Node.js gateway process on port from env var (18789)
- Secrets loaded from `/opt/clawdbot.env`
- Comprehensive systemd sandboxing applied
- `--allow-unconfigured` flag NOT present (removed during hardening)

### 1.4 Drop-in Files

**Directory:** `/etc/systemd/system/clawdbot.service.d/`

**File:** `clawvault.conf` (permissions: 600 root:root)

```ini
[Service]
Environment="CLAWVAULT_PATH=/home/clawdbot/.openclaw/workspace/vault"
Environment="CLAWVAULT_OPENROUTER_MODEL=google/gemini-2.0-flash-001"
```

**Key observations:**
- Sets ClawVault vault path and LLM compression model
- File properly restricted (chmod 600)
- No secrets in this file (OpenRouter key is in clawdbot.env)

---

## 2. Crontabs

### 2.1 clawdbot User Crontab

```cron
# ClaudDib Scripted Tasks - System Cron
# These run independently of the OpenClaw agent (no LLM needed)
# Logs: /home/clawdbot/.openclaw/workspace/logs/

WORKSPACE=/home/clawdbot/.openclaw/workspace

# Own post monitor (every 5 min)
*/5 * * * * cd $WORKSPACE && /usr/bin/python3 tools/own_post_monitor.py >> logs/own_post_monitor.log 2>&1

# Reply nudge (:15 and :45)
15,45 * * * * cd $WORKSPACE && /usr/bin/python3 tools/nudge_replies.py >> logs/nudge_replies.log 2>&1

# Post replies (every 2 min)
*/2 * * * * cd $WORKSPACE && /usr/bin/python3 tools/post_reply.py >> logs/post_reply.log 2>&1

# Post express content (every 30 min)
*/30 * * * * cd $WORKSPACE && /usr/bin/python3 tools/post_express_content.py >> logs/post_express_content.log 2>&1

# Engagement check (every 30 min)
*/30 * * * * cd $WORKSPACE && /usr/bin/python3 tools/engagement_check.py >> logs/engagement_check.log 2>&1

# Feed scanner (every 5 min)
*/5 * * * * cd $WORKSPACE && /usr/bin/python3 tools/feed_scanner.py >> logs/feed_scanner.log 2>&1

# Leaderboard tracker (every hour, offset by 5 min)
5 * * * * cd $WORKSPACE && /usr/bin/python3 tools/track_leaderboard.py >> logs/track_leaderboard.log 2>&1

# Post performance tracker (every 6 hours, offset :05)
5 */6 * * * cd $WORKSPACE && /usr/bin/python3 tools/track_post_performance.py >> logs/track_post_performance.log 2>&1

# Competitor content tracker (every 6 hours, offset :30)
30 */6 * * * cd $WORKSPACE && /usr/bin/python3 tools/track_competitors.py >> logs/track_competitors.log 2>&1

# Relationship intelligence (every 6 hours, offset :10)
10 */6 * * * cd $WORKSPACE && /usr/bin/python3 tools/generate_relationship_summary.py >> logs/relationship_summary.log 2>&1

# Content performance summary (every 6 hours, offset :13)
13 */6 * * * cd $WORKSPACE && /usr/bin/python3 tools/generate_performance_summary.py >> logs/performance_summary.log 2>&1

# Briefing synthesis (every 6 hours, offset :15)
15 */6 * * * cd $WORKSPACE && /usr/bin/python3 tools/generate_briefing.py >> logs/briefing.log 2>&1

# Analytics report (daily at 06:00 UTC)
0 6 * * * cd $WORKSPACE && /usr/bin/python3 tools/generate_analytics_report.py >> logs/generate_analytics_report.log 2>&1

# Competitive growth report (daily at 06:05 UTC)
5 6 * * * cd $WORKSPACE && /usr/bin/python3 tools/track_leaderboard.py report >> logs/competitive_report.log 2>&1

# Archive old quote retweets (hourly, offset :35)
35 * * * * cd $WORKSPACE && /usr/bin/python3 tools/archive_old_quotes.py >> logs/archive_old_quotes.log 2>&1

# --- ClawVault Memory Maintenance ---

# Observe & compress active sessions (every 30 min, offset by 20)
# NOTE: Contains inline OPENROUTER_API_KEY (redacted in exported copy)
20 */1 * * * CLAWVAULT_PATH=... OPENROUTER_API_KEY=[REDACTED] CLAWVAULT_OPENROUTER_MODEL=google/gemini-2.0-flash-001 /usr/local/bin/clawvault observe --active --compress >> .../logs/clawvault-observe.log 2>&1

# Reindex vault daily at 3 AM
0 3 * * * CLAWVAULT_PATH=... /usr/local/bin/clawvault reindex --quiet >> .../logs/clawvault-reindex.log 2>&1

# Resolve orphan links weekly (Sunday 4 AM)
0 4 * * 0 CLAWVAULT_PATH=... /usr/local/bin/clawvault link --all --quiet >> .../logs/clawvault-link.log 2>&1

# Health check weekly (Monday 5 AM)
0 5 * * 1 CLAWVAULT_PATH=... /usr/local/bin/clawvault doctor >> .../logs/clawvault-doctor.log 2>&1
```

**SECURITY NOTE:** The clawdbot crontab contains the `OPENROUTER_API_KEY` in plaintext on the `clawvault observe` line. This is readable by root and potentially by the clawdbot user's processes. A more secure approach would source it from a file. The redacted version is stored at `configs/crontab-clawdbot.txt`.

**Script count:** 19 cron entries (15 Python scripts + 4 ClawVault maintenance tasks)

### 2.2 Root User Crontab

```
no crontab for root
```

---

## 3. OpenClaw Configuration

### 3.1 Main Config: openclaw.json

**File:** `/home/clawdbot/.openclaw/openclaw.json` (4840 bytes, owner: clawdbot:clawdbot, mode: 600)  
**Redacted copy:** `configs/openclaw.json.redacted`

**Key settings:**
- **Primary model:** `openrouter/moonshotai/kimi-k2.5` with fallback to `openrouter/google/gemini-3-flash-preview`
- **Model providers configured:** Anthropic, OpenRouter, Synthetic (Kimi), OpenAI (local proxy at 127.0.0.1:3456)
- **Available models:** Claude 3 Opus, Gemini 3 Pro Preview, Gemini 2.5 Pro, Claude 3.5 Haiku/Sonnet, GPT-4o, Gemini Flash 1.5, Kimi K2.5
- **Aliases:** sonnet, opus, haiku, gemini-25-pro, gemini-pro, gemini-flash-preview, flash, deepseek-v3.2, kimi-or, kimi
- **Sandbox mode:** off (workspaceAccess: rw)
- **Heartbeat:** every 30m, prompt "."
- **Memory search:** disabled (uses ClawVault instead)
- **Gateway:** loopback only, control UI disabled
- **Hooks:** enabled (webhooks + internal ClawVault hooks)
- **mDNS:** off
- **Plugins:** telegram enabled
- **Agent list:** single agent "main"
- **Max concurrent:** 4 (agents and subagents both)

**Secrets present (redacted in copy):**
- `models.providers.anthropic.apiKey` (Anthropic OAT key)
- `models.providers.openrouter.apiKey` (OpenRouter key)
- `models.providers.synthetic.apiKey` (Synthetic key)
- `hooks.token` (Webhook auth token)

### 3.2 Bot Config: clawdbot.json

**File:** `/home/clawdbot/.openclaw/clawdbot.json` (1924 bytes, owner: clawdbot:clawdbot, mode: 600)  
**Redacted copy:** `configs/clawdbot.json.redacted`

**Key settings:**
- **Primary model (override):** `anthropic/claude-opus-4-5` (overrides openclaw.json's kimi primary)
- **Subagent model:** kimi
- **Providers:** Synthetic (Kimi K2.5 via anthropic-messages API)
- **Kimi K2.5 cost:** all zeros (input, output, cacheRead, cacheWrite)
- **Max concurrent:** 4
- **Sandbox mode:** off
- **Gateway:** local, loopback
- **Plugins:** telegram enabled
- **Meta:** lastTouchedVersion 2026.1.30

**Note:** This file duplicates/overrides many settings from openclaw.json. The `model.primary` here (claude-opus-4-5) differs from openclaw.json (kimi-k2.5). The effective primary model depends on OpenClaw's config merge order.

### 3.3 Exec Approvals

**File:** `/home/clawdbot/.openclaw/exec-approvals.json` (180 bytes)  
**Redacted copy:** `configs/exec-approvals.json.redacted`

```json
{
  "version": 1,
  "socket": {
    "path": "/home/clawdbot/.clawdbot/exec-approvals.sock",
    "token": "[REDACTED]"
  },
  "defaults": {},
  "agents": {}
}
```

**Findings:** Default exec approval config. No custom approval rules defined. Socket-based approval mechanism.

### 3.4 OpenClaw Cron Jobs (jobs.json)

**File:** `/home/clawdbot/.openclaw/cron/jobs.json` (10580 bytes)  
**Copy:** `configs/cron-jobs.json` (no secrets present)

**Enabled jobs (5):**

| ID | Name | Interval | Session | payload.kind | Last Run | Status |
|----|------|----------|---------|-------------|----------|--------|
| heartbeat-voice-001 | Heartbeat | 30 min | main | systemEvent | 1771519800005 | ok (172s) |
| reply-blitz-001 | Reply Blitz | 15 min | isolated | agentTurn | 1771519500007 | ok (82s) |
| b2c3d4e5-...-reflection02 | Reflection | 6 hr | main | systemEvent | 1771509643712 | ok (105s) |
| c3d4e5f6-...-weekly00003 | Weekly Maintenance | 7 days | main | systemEvent | 1771266205852 | ok (64s) |
| moltbook-dm-check-001 | Moltbook DM Check | 15 min | isolated | agentTurn | 1771519600005 | ok (30s) |

**Disabled jobs (8):**
- feed-scan-001, engagement-check-001, content-post-001, treatise-post-001, express-content-post-001, post-replies-001, c6a932e5-... (ClawCrunch Scanner), 8262dc06-... (MoltX Leaderboard Tracker)

**Key observations:**
- All enabled jobs have valid `nextRunAtMs` state (cron scheduler functioning)
- Reply Blitz uses 5-minute timeout (`timeoutSeconds: 300`)
- Main session jobs use `systemEvent` kind; isolated jobs use `agentTurn` (correct per docs)
- Disabled jobs represent work migrated to system cron (Python scripts)

---

## 4. ClawVault / qmd Configuration

### 4.1 qmd Index

**File:** `/home/clawdbot/.config/qmd/index.yml`  
**Copy:** `configs/qmd-index.yml`

```yaml
collections:
  vault:
    path: /home/clawdbot/.openclaw/workspace/vault
    pattern: "**/*.md"
```

**Findings:** Single collection named "vault" pointing to the agent's vault directory. Indexes all markdown files.

### 4.2 ClawVault Installation

- **Installed at:** `/usr/lib/node_modules/clawvault/` (real copy, not symlink)
- **Config via environment:** `CLAWVAULT_PATH` and `CLAWVAULT_OPENROUTER_MODEL` set in systemd drop-in and crontab
- **No separate clawvault config file** at `/home/clawdbot/.config/clawvault/` (directory does not exist)
- **qmd binary:** `/usr/local/bin/qmd` (symlink to `/usr/lib/node_modules/qmd/qmd`)
- **clawvault wrapper:** `/usr/local/bin/clawvault`

---

## 5. Swarm Mode / Multi-Agent Configuration

### 5.1 Agent List

**From openclaw.json:**
```json
"agents": {
  "list": [
    { "id": "main" }
  ]
}
```

**Single agent mode.** Only one agent ("main") is configured. No swarm/multi-agent setup.

### 5.2 Agent Session Directories

```
/home/clawdbot/.openclaw/agents/
├── main/
│   ├── agent/       (agent config)
│   └── sessions/    (active session logs, 176KB directory)
└── engagement-checker/
    └── sessions/    (empty - defunct agent)
```

**Findings:**
- `engagement-checker` agent directory exists but is empty/defunct
- Only `main` agent has active sessions
- No swarm configuration found anywhere in OpenClaw config files

### 5.3 Docker Compose (reference only, NOT in use)

**File:** `/opt/clawdbot/docker-compose.yml` -- defines `openclaw-gateway` and `openclaw-cli` services  
**File:** `/opt/clawdbot/render.yaml` -- Render.com deployment config

Both are upstream OpenClaw distribution files. **Not actively used** -- the system runs via systemd directly on the host.

---

## 6. Environment Files

### 6.1 Service Environment: /opt/clawdbot.env

**Redacted copy:** `configs/clawdbot.env.redacted`

**Variables defined:**

| Variable | Description |
|----------|-------------|
| CLAWDBOT_VERSION | v2026.2.6-3 |
| CLAWDBOT_GATEWAY_PORT | 18789 |
| CLAWDBOT_GATEWAY_BIND | lan |
| CLAWDBOT_GATEWAY_TOKEN | [REDACTED] (gateway auth) |
| TELEGRAM_BOT_TOKEN | [REDACTED] (Telegram bot) |
| ANTHROPIC_API_KEY | [REDACTED] (sk-ant-api03-...) |
| SYNTHETIC_API_KEY | [REDACTED] (syn_...) |
| CLAWVAULT_PATH | /home/clawdbot/.openclaw/workspace/vault |
| OPENROUTER_API_KEY | [REDACTED] (sk-or-v1-...) |
| WEBHOOK_TOKEN | [REDACTED] (webhook auth) |

**Note:** DISCORD_BOT_TOKEN and SLACK tokens are commented out (not configured).

### 6.2 Lab Environment: /root/laboratory/.env

**Redacted copy:** `configs/lab-env.redacted`

Contains: ANTHROPIC_API_KEY, OPENROUTER_API_KEY, SYNTHETIC_API_KEY, WEBHOOK_TOKEN (all redacted).

**Note:** The Anthropic key in lab `.env` is an OAT key (`sk-ant-oat01-...`) while the one in `clawdbot.env` is an API key (`sk-ant-api03-...`). Different key types are used in the template vs runtime.

---

## 7. Workspace Secrets Directory

**Directory:** `/home/clawdbot/.openclaw/workspace/secrets/` (mode: 700)

| File | Permissions | Size | Description |
|------|------------|------|-------------|
| README.md | 644 | 979B | Documentation |
| api-keys.json | 600 | 278B | API keys |
| clawk.json | 600 | 197B | Clawk credentials |
| evm-wallet.json | 600 | 333B | EVM wallet keys |
| moltbook.json | 600 | 199B | Moltbook API creds |
| moltx.json | 600 | 259B | MoltX API creds |
| pixellab.json | 600 | 141B | PixelLab API key |

**Files NOT read or exported** -- contents are secrets. Permissions verified as properly restricted.

---

## 8. Exported Config File Inventory

All files saved to `$BUNDLE/configs/`:

| File | Source | Secrets |
|------|--------|---------|
| `openclaw.json.redacted` | /home/clawdbot/.openclaw/openclaw.json | 4 keys REDACTED |
| `clawdbot.json.redacted` | /home/clawdbot/.openclaw/clawdbot.json | 1 key REDACTED |
| `clawdbot.env.redacted` | /opt/clawdbot.env | 6 values REDACTED |
| `lab-env.redacted` | /root/laboratory/.env | 4 values REDACTED |
| `exec-approvals.json.redacted` | /home/clawdbot/.openclaw/exec-approvals.json | 1 token REDACTED |
| `crontab-clawdbot.txt` | crontab -u clawdbot -l | 1 API key REDACTED |
| `cron-jobs.json` | /home/clawdbot/.openclaw/cron/jobs.json | None present |
| `clawdbot.service` | /etc/systemd/system/clawdbot.service | None (uses env vars) |
| `clawdbot-service-dropin-clawvault.conf` | ...service.d/clawvault.conf | None (env var names only) |
| `qmd-index.yml` | /home/clawdbot/.config/qmd/index.yml | None |
| `openclaw.json.template` | /root/laboratory/config/openclaw.json.template | Uses ${VAR} placeholders |
| `clawdbot.json.template` | /root/laboratory/config/clawdbot.json.template | Uses ${VAR} placeholders |
| `docker-compose.yml` | /opt/clawdbot/docker-compose.yml | Uses ${VAR} placeholders |
| `render.yaml` | /opt/clawdbot/render.yaml | None |

**Verification:** Automated scan of all exported files confirmed zero leaked secrets matching known key patterns (sk-ant-, sk-or-v1-, syn_, bot tokens, gateway tokens, webhook tokens).

---

## 9. Security Observations

1. **Crontab secret exposure:** The `OPENROUTER_API_KEY` is embedded in plaintext in the clawdbot crontab's `clawvault observe` entry. This is readable by root and potentially by the clawdbot user's processes. A more secure approach would source it from a file.

2. **Two different Anthropic keys in use:**
   - Lab/template uses an OAT key (`sk-ant-oat01-...`) rendered into openclaw.json
   - Service env uses an API key (`sk-ant-api03-...`) available to the process
   - The rendered openclaw.json contains the OAT key (from template substitution)

3. **Config duplication:** `clawdbot.json` and `openclaw.json` have overlapping settings with different values (notably `model.primary`). The effective configuration depends on OpenClaw's merge behavior.

4. **Defunct agent directory:** `engagement-checker` agent directory exists but is not referenced in current config.

5. **Docker compose present but unused:** The docker-compose.yml references sensitive env vars but is not actively used (system runs via systemd).
