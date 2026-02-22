#!/usr/bin/env python3
"""Lightweight experiment dashboard server for Phase 2 artifacts."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
from typing import Any, Dict, List


ROOT = Path("/Users/quiznat/Desktop/Tree_of_Thought")
PHASE2 = ROOT / "phase2"
ANALYSIS_DIR = PHASE2 / "benchmarks/analysis"
RUNS_DIR = PHASE2 / "benchmarks/runs"
RUNTIME_DIR = PHASE2 / "reproducibility/runtime"


def utc_now() -> str:
    return subprocess.check_output(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"], text=True).strip()


def safe_read_json(path: Path) -> Dict[str, Any] | List[Any] | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def tail_text(path: Path, lines: int = 30) -> str:
    if not path.exists():
        return ""
    try:
        output = subprocess.check_output(["tail", "-n", str(lines), str(path)], text=True)
        return output
    except Exception:
        return ""


def parse_pid_file(pid_path: Path) -> int | None:
    if not pid_path.exists():
        return None
    try:
        return int(pid_path.read_text(encoding="utf-8").strip())
    except Exception:
        return None


def is_pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def pid_info(pid: int) -> Dict[str, str]:
    if not is_pid_alive(pid):
        return {"elapsed": "", "command": ""}
    try:
        output = subprocess.check_output(
            ["ps", "-p", str(pid), "-o", "etime=,command="],
            text=True,
        ).strip()
        if not output:
            return {"elapsed": "", "command": ""}
        parts = output.split(maxsplit=1)
        if len(parts) == 1:
            return {"elapsed": parts[0], "command": ""}
        return {"elapsed": parts[0], "command": parts[1]}
    except Exception:
        return {"elapsed": "", "command": ""}


def list_runtime_processes() -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    if not RUNTIME_DIR.exists():
        return results

    pid_files = sorted(RUNTIME_DIR.glob("*.pid"), key=lambda p: p.stat().st_mtime, reverse=True)
    for pid_file in pid_files:
        pid = parse_pid_file(pid_file)
        if pid is None:
            continue
        alive = is_pid_alive(pid)
        info = pid_info(pid) if alive else {"elapsed": "", "command": ""}
        log_file = pid_file.with_suffix(".log")
        last_line = ""
        if log_file.exists():
            text = tail_text(log_file, lines=1).strip()
            last_line = text
        results.append(
            {
                "name": pid_file.stem,
                "pid": pid,
                "alive": alive,
                "elapsed": info.get("elapsed", ""),
                "command": info.get("command", ""),
                "pid_file": str(pid_file),
                "log_file": str(log_file),
                "last_line": last_line,
            }
        )
    return results


def load_panel_items(panel_path: Path, limit: int = 50) -> List[str]:
    payload = safe_read_json(panel_path)
    if not isinstance(payload, dict):
        return []
    items = payload.get("items", [])
    if not isinstance(items, list):
        return []
    out: List[str] = []
    for row in items[:limit]:
        if isinstance(row, dict):
            item_id = row.get("item_id")
            if isinstance(item_id, str):
                out.append(item_id)
    return out


def compute_v31_progress() -> Dict[str, Any]:
    base = RUNS_DIR / "protocol_v31_diagnostic"
    tasks = {
        "linear2-demo": ("linear2_demo", PHASE2 / "benchmarks/panels/linear2_lockset_v1.json"),
        "digit-permutation-demo": (
            "digit_permutation_demo",
            PHASE2 / "benchmarks/panels/digit_permutation_lockset_v1.json",
        ),
    }
    models = {
        "Qwen/Qwen3-Coder-Next:novita": "qwen_qwen3_coder_next_novita",
        "Qwen/Qwen2.5-72B-Instruct": "qwen_qwen2_5_72b_instruct",
        "Qwen/Qwen2.5-Coder-32B-Instruct": "qwen_qwen2_5_coder_32b_instruct",
    }
    profiles = [
        "tot_model_self_eval",
        "tot_hybrid",
        "tot_rule_based",
        "tot_model_self_eval_lite",
    ]
    conditions = {"baseline-react", "tot-prototype"}

    blocks: List[Dict[str, Any]] = []
    for task_id, (task_slug, panel_path) in tasks.items():
        panel_items = load_panel_items(panel_path, limit=50)
        for model_id, model_slug in models.items():
            for profile in profiles:
                run_dir = base / task_slug / model_slug / profile
                seen: Dict[str, set[str]] = {item_id: set() for item_id in panel_items}
                if run_dir.exists():
                    for manifest_path in run_dir.glob("*.json"):
                        payload = safe_read_json(manifest_path)
                        if not isinstance(payload, dict):
                            continue
                        item_id = payload.get("item_id")
                        cond = payload.get("condition_id")
                        if isinstance(item_id, str) and isinstance(cond, str):
                            if item_id in seen and cond in conditions:
                                seen[item_id].add(cond)
                present_pairs = sum(len(seen[item_id]) for item_id in panel_items)
                complete_items = sum(1 for item_id in panel_items if len(seen[item_id]) == 2)
                state = "not_started"
                if present_pairs == 100:
                    state = "done"
                elif present_pairs > 0:
                    state = "partial"
                blocks.append(
                    {
                        "task_id": task_id,
                        "model_id": model_id,
                        "profile": profile,
                        "present_pairs": present_pairs,
                        "total_pairs": 100,
                        "complete_items": complete_items,
                        "state": state,
                    }
                )

    done = sum(1 for block in blocks if block["state"] == "done")
    partial = sum(1 for block in blocks if block["state"] == "partial")
    not_started = sum(1 for block in blocks if block["state"] == "not_started")
    present_pairs = sum(int(block["present_pairs"]) for block in blocks)
    total_pairs = len(blocks) * 100

    return {
        "done_blocks": done,
        "partial_blocks": partial,
        "not_started_blocks": not_started,
        "present_pairs": present_pairs,
        "total_pairs": total_pairs,
        "blocks": blocks,
    }


def load_v3_summary() -> Dict[str, Any]:
    summary_path = ANALYSIS_DIR / "protocol_v3_matrix_summary.json"
    payload = safe_read_json(summary_path)
    if not isinstance(payload, dict):
        return {"records": [], "tot_vs_react_positive": 0, "tot_vs_react_negative": 0}

    records = payload.get("records", [])
    if not isinstance(records, list):
        records = []

    pos = 0
    neg = 0
    for row in records:
        if not isinstance(row, dict):
            continue
        delta = row.get("tot_minus_react")
        try:
            value = float(delta)
        except Exception:
            continue
        if value > 0:
            pos += 1
        elif value < 0:
            neg += 1

    return {
        "records": records,
        "tot_vs_react_positive": pos,
        "tot_vs_react_negative": neg,
        "path": str(summary_path),
    }


def load_v31_summary() -> Dict[str, Any]:
    summary_path = ANALYSIS_DIR / "protocol_v31_diagnostic_summary.json"
    payload = safe_read_json(summary_path)
    if not isinstance(payload, dict):
        return {"records": [], "path": str(summary_path), "exists": False}
    records = payload.get("records", [])
    if not isinstance(records, list):
        records = []
    return {"records": records, "path": str(summary_path), "exists": True}


def list_latest_analysis(limit: int = 25) -> List[Dict[str, Any]]:
    if not ANALYSIS_DIR.exists():
        return []
    files = sorted(ANALYSIS_DIR.glob("*"), key=lambda p: p.stat().st_mtime, reverse=True)
    out: List[Dict[str, Any]] = []
    for path in files[:limit]:
        out.append(
            {
                "name": path.name,
                "path": str(path),
                "size_bytes": path.stat().st_size,
                "mtime_epoch": int(path.stat().st_mtime),
            }
        )
    return out


def diagnose_access() -> Dict[str, Any]:
    probe = PHASE2 / "README.md"
    try:
        text = probe.read_text(encoding="utf-8")
        return {"root_readable": True, "probe": str(probe), "probe_size": len(text)}
    except Exception as exc:
        return {"root_readable": False, "probe": str(probe), "error": str(exc)}


def build_overview() -> Dict[str, Any]:
    return {
        "generated_utc": utc_now(),
        "access": diagnose_access(),
        "runtime_processes": list_runtime_processes(),
        "v31_progress": compute_v31_progress(),
        "v3_summary": load_v3_summary(),
        "v31_summary": load_v31_summary(),
        "latest_analysis": list_latest_analysis(),
    }


def html_template() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>ToT-HF Experiment Dashboard</title>
  <style>
    :root {
      --bg: #f5efe3;
      --card: #fff9ee;
      --line: #d9c8a6;
      --ink: #2f2a22;
      --muted: #6e6456;
      --accent: #8f6b2b;
      --good: #2f7f4f;
      --warn: #c57d16;
      --bad: #b13d2c;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: linear-gradient(135deg, #f9f3e8 0%, #efe4ce 100%);
      color: var(--ink);
    }
    .wrap { max-width: 1320px; margin: 0 auto; padding: 18px; }
    h1 { margin: 0 0 10px; font-size: 24px; }
    h2 { margin: 0 0 10px; font-size: 16px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--muted); }
    .small { color: var(--muted); font-size: 12px; }
    .grid { display: grid; gap: 12px; }
    .grid.cards { grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); }
    .card {
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 10px;
      padding: 12px;
      box-shadow: 0 1px 0 rgba(0, 0, 0, 0.03);
    }
    .metric { font-size: 24px; font-weight: 700; color: var(--accent); }
    .row { display: flex; gap: 10px; align-items: center; }
    .row.space { justify-content: space-between; }
    .pill {
      font-size: 11px; padding: 2px 8px; border-radius: 999px; border: 1px solid var(--line);
      background: #fdf7eb;
    }
    .pill.good { color: var(--good); border-color: #9fd2b4; background: #eef9f1; }
    .pill.warn { color: var(--warn); border-color: #e4bf87; background: #fff7ea; }
    .pill.bad { color: var(--bad); border-color: #e2a29a; background: #fff1ef; }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
    }
    th, td {
      text-align: left;
      border-bottom: 1px solid var(--line);
      padding: 6px 6px;
      vertical-align: top;
    }
    th { color: var(--muted); font-weight: 600; }
    .log {
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      white-space: pre-wrap;
      background: #f3e8ce;
      border: 1px solid var(--line);
      padding: 8px;
      border-radius: 8px;
      min-height: 120px;
      max-height: 260px;
      overflow: auto;
      font-size: 12px;
    }
    .progress {
      width: 100%;
      height: 10px;
      border-radius: 999px;
      border: 1px solid var(--line);
      background: #f6ecda;
      overflow: hidden;
    }
    .progress > span {
      display: block;
      height: 100%;
      background: linear-gradient(90deg, #2f7f4f 0%, #5ca473 100%);
      width: 0%;
    }
    a { color: #725018; text-decoration: none; }
    a:hover { text-decoration: underline; }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="row space">
      <div>
        <h1>ToT-HF Experiment Dashboard</h1>
        <div class="small">Auto-refresh: 8s | Served locally</div>
      </div>
      <div class="small" id="generatedUtc">...</div>
    </div>
    <div id="accessWarn" class="card" style="display:none; margin-top:10px; border-color:#e2a29a; background:#fff1ef;">
      <h2 style="color:#b13d2c;">Filesystem Access Warning</h2>
      <div class="small" id="accessWarnText"></div>
    </div>

    <div class="grid cards" id="topCards"></div>

    <div class="grid" style="margin-top:12px;">
      <div class="card">
        <h2>Protocol v3.1 Progress</h2>
        <div class="progress"><span id="v31ProgressBar"></span></div>
        <div class="small" id="v31ProgressText" style="margin-top:6px;"></div>
        <table id="v31BlocksTable" style="margin-top:8px;">
          <thead>
            <tr>
              <th>Task</th><th>Model</th><th>Profile</th><th>Pairs</th><th>Status</th>
            </tr>
          </thead>
          <tbody></tbody>
        </table>
      </div>

      <div class="card">
        <h2>Runtime Processes</h2>
        <table id="procTable">
          <thead>
            <tr>
              <th>Name</th><th>PID</th><th>Alive</th><th>Elapsed</th><th>Last line</th>
            </tr>
          </thead>
          <tbody></tbody>
        </table>
      </div>

      <div class="card">
        <h2>v3 Snapshot</h2>
        <div class="small" id="v3SummaryText"></div>
        <table id="v3Table" style="margin-top:8px;">
          <thead>
            <tr>
              <th>Task</th><th>Model</th><th>Δ(ToT-ReAct)</th><th>Holm p</th>
            </tr>
          </thead>
          <tbody></tbody>
        </table>
      </div>

      <div class="card">
        <h2>Latest Analysis Files</h2>
        <table id="filesTable">
          <thead>
            <tr>
              <th>File</th><th>Size</th><th>Modified</th><th>View</th>
            </tr>
          </thead>
          <tbody></tbody>
        </table>
      </div>

      <div class="card">
        <h2>Selected Log Tail</h2>
        <div class="row">
          <select id="logPicker" style="min-width: 360px;"></select>
          <button id="loadLogBtn">Load</button>
        </div>
        <div id="logTail" class="log" style="margin-top:8px;"></div>
      </div>
    </div>
  </div>

  <script>
    function esc(s) {
      return String(s ?? "").replace(/[&<>"']/g, function(m) {
        return {"&":"&amp;","<":"&lt;",">":"&gt;","\\"":"&quot;","'":"&#39;"}[m];
      });
    }

    function fmtEpoch(epoch) {
      if (!epoch) return "";
      return new Date(epoch * 1000).toLocaleString();
    }

    function fmtSize(bytes) {
      if (bytes < 1024) return bytes + " B";
      if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
      return (bytes / (1024 * 1024)).toFixed(1) + " MB";
    }

    function statusPill(state) {
      if (state === "done") return '<span class="pill good">done</span>';
      if (state === "partial") return '<span class="pill warn">partial</span>';
      return '<span class="pill">not started</span>';
    }

    function alivePill(alive) {
      return alive ? '<span class="pill good">alive</span>' : '<span class="pill bad">dead</span>';
    }

    async function fetchJson(url) {
      const r = await fetch(url, {cache: "no-store"});
      if (!r.ok) throw new Error("HTTP " + r.status);
      return await r.json();
    }

    async function loadLog(path) {
      if (!path) return;
      const data = await fetchJson("/api/log?path=" + encodeURIComponent(path));
      document.getElementById("logTail").textContent = data.tail || "";
    }

    function render(data) {
      document.getElementById("generatedUtc").textContent = "Updated: " + (data.generated_utc || "");
      const access = data.access || {};
      const accessWarn = document.getElementById("accessWarn");
      if (access.root_readable === false) {
        accessWarn.style.display = "block";
        document.getElementById("accessWarnText").textContent =
          "Dashboard service cannot read workspace files (" + (access.error || "permission denied") +
          "). On macOS, grant Full Disk Access to the service python interpreter, then reinstall service.";
      } else {
        accessWarn.style.display = "none";
        document.getElementById("accessWarnText").textContent = "";
      }

      const v31 = data.v31_progress || {};
      const done = Number(v31.done_blocks || 0);
      const partial = Number(v31.partial_blocks || 0);
      const notStarted = Number(v31.not_started_blocks || 0);
      const pairs = Number(v31.present_pairs || 0);
      const totalPairs = Number(v31.total_pairs || 0);
      const pct = totalPairs > 0 ? Math.round((pairs / totalPairs) * 100) : 0;

      const v3 = data.v3_summary || {};
      const v3Pos = Number(v3.tot_vs_react_positive || 0);
      const v3Neg = Number(v3.tot_vs_react_negative || 0);
      const procCount = (data.runtime_processes || []).filter(p => p.alive).length;

      document.getElementById("topCards").innerHTML = [
        '<div class="card"><h2>v3.1 Blocks</h2><div class="metric">' + done + '/24</div><div class="small">partial: ' + partial + ' | not started: ' + notStarted + '</div></div>',
        '<div class="card"><h2>v3.1 Pairs</h2><div class="metric">' + pairs + '/' + totalPairs + '</div><div class="small">' + pct + '% complete</div></div>',
        '<div class="card"><h2>v3 Direction</h2><div class="metric">' + v3Pos + ' / ' + v3Neg + '</div><div class="small">ToT>ReAct / ToT<ReAct blocks</div></div>',
        '<div class="card"><h2>Active Processes</h2><div class="metric">' + procCount + '</div><div class="small">from runtime PID files</div></div>'
      ].join("");

      document.getElementById("v31ProgressBar").style.width = pct + "%";
      document.getElementById("v31ProgressText").textContent = "Pairs complete: " + pairs + "/" + totalPairs + " (" + pct + "%)";

      const blocks = (v31.blocks || []).slice().sort((a,b) => {
        const ak = [a.task_id, a.model_id, a.profile].join("|");
        const bk = [b.task_id, b.model_id, b.profile].join("|");
        return ak.localeCompare(bk);
      });
      document.querySelector("#v31BlocksTable tbody").innerHTML = blocks.map(b =>
        "<tr><td>" + esc(b.task_id) + "</td><td>" + esc(b.model_id) + "</td><td>" + esc(b.profile) +
        "</td><td>" + esc(String(b.present_pairs) + "/" + String(b.total_pairs)) + "</td><td>" + statusPill(b.state) + "</td></tr>"
      ).join("");

      const procs = data.runtime_processes || [];
      document.querySelector("#procTable tbody").innerHTML = procs.map(p =>
        "<tr><td>" + esc(p.name) + "</td><td>" + esc(p.pid) + "</td><td>" + alivePill(!!p.alive) +
        "</td><td>" + esc(p.elapsed || "") + "</td><td>" + esc(p.last_line || "") + "</td></tr>"
      ).join("");

      const v3Rows = (v3.records || []).slice().sort((a,b) => {
        const ak = [a.task_id, a.model_id].join("|");
        const bk = [b.task_id, b.model_id].join("|");
        return ak.localeCompare(bk);
      });
      document.querySelector("#v3Table tbody").innerHTML = v3Rows.map(r =>
        "<tr><td>" + esc(r.task_id) + "</td><td>" + esc(r.model_id) + "</td><td>" + esc(Number(r.tot_minus_react).toFixed(3)) +
        "</td><td>" + esc(String(r.holm_p_tot_vs_react)) + "</td></tr>"
      ).join("");
      document.getElementById("v3SummaryText").textContent = "Summary source: " + (v3.path || "");

      const files = data.latest_analysis || [];
      document.querySelector("#filesTable tbody").innerHTML = files.map(f =>
        "<tr><td>" + esc(f.name) + "</td><td>" + esc(fmtSize(f.size_bytes || 0)) + "</td><td>" + esc(fmtEpoch(f.mtime_epoch)) +
        "</td><td><a href='/api/file?path=" + encodeURIComponent(f.path) + "' target='_blank'>open</a></td></tr>"
      ).join("");

      const picker = document.getElementById("logPicker");
      const old = picker.value;
      picker.innerHTML = procs
        .filter(p => p.log_file)
        .map(p => "<option value='" + esc(p.log_file) + "'>" + esc(p.name + " :: " + p.log_file) + "</option>")
        .join("");
      if (old) picker.value = old;
      if (!picker.value && picker.options.length) picker.selectedIndex = 0;
    }

    async function refresh() {
      try {
        const data = await fetchJson("/api/overview");
        render(data);
      } catch (e) {
        console.error(e);
      }
    }

    document.getElementById("loadLogBtn").addEventListener("click", async function() {
      const path = document.getElementById("logPicker").value;
      await loadLog(path);
    });

    refresh();
    setInterval(refresh, 8000);
    setInterval(async () => {
      const path = document.getElementById("logPicker").value;
      if (path) await loadLog(path);
    }, 8000);
  </script>
</body>
</html>
"""


class DashboardHandler(BaseHTTPRequestHandler):
    def _send_json(self, payload: Dict[str, Any], status: int = 200) -> None:
        data = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _send_text(self, text: str, status: int = 200, ctype: str = "text/plain; charset=utf-8") -> None:
        data = text.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format: str, *args: Any) -> None:
        return

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)

        if path == "/":
            self._send_text(html_template(), ctype="text/html; charset=utf-8")
            return

        if path == "/api/overview":
            self._send_json(build_overview())
            return

        if path == "/api/log":
            raw = (qs.get("path") or [""])[0]
            req = Path(raw)
            try:
                req.resolve().relative_to(ROOT)
            except Exception:
                self._send_json({"error": "path outside workspace"}, status=400)
                return
            tail = tail_text(req, lines=50)
            self._send_json({"path": str(req), "tail": tail})
            return

        if path == "/api/file":
            raw = (qs.get("path") or [""])[0]
            req = Path(raw)
            try:
                req.resolve().relative_to(ROOT)
            except Exception:
                self._send_text("invalid path", status=400)
                return
            if not req.exists() or req.is_dir():
                self._send_text("not found", status=404)
                return
            max_bytes = 300_000
            try:
                data = req.read_bytes()[:max_bytes]
                text = data.decode("utf-8", errors="replace")
            except Exception:
                self._send_text("unable to read file", status=500)
                return
            self._send_text(text, ctype="text/plain; charset=utf-8")
            return

        self._send_text("not found", status=404)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Phase2 experiment dashboard server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8787)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    server = ThreadingHTTPServer((args.host, args.port), DashboardHandler)
    print(f"dashboard_start host={args.host} port={args.port}", flush=True)
    try:
        server.serve_forever(poll_interval=0.5)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    print("dashboard_stop", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
