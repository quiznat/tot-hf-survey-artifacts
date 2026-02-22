#!/usr/bin/env bash
set -euo pipefail

LABEL="com.quiznat.tothf.dashboard"
ROOT="/Users/quiznat/Desktop/Tree_of_Thought"
PHASE2="${ROOT}/phase2"
SOURCE_SERVER="${PHASE2}/dashboard/server.py"
SERVICE_HOME="${HOME}/.tot_hf_dashboard"
SERVER="${SERVICE_HOME}/server.py"
RUNTIME_DIR="${PHASE2}/reproducibility/runtime"
PLIST_DIR="${HOME}/Library/LaunchAgents"
PLIST_PATH="${PLIST_DIR}/${LABEL}.plist"
LOG_OUT="${RUNTIME_DIR}/dashboard_service.out.log"
LOG_ERR="${RUNTIME_DIR}/dashboard_service.err.log"
HOST="127.0.0.1"
PORT="8787"

mkdir -p "${PLIST_DIR}"
mkdir -p "${RUNTIME_DIR}"
mkdir -p "${SERVICE_HOME}"

cp "${SOURCE_SERVER}" "${SERVER}"
chmod +x "${SERVER}"

cat > "${PLIST_PATH}" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>Label</key>
    <string>${LABEL}</string>

    <key>ProgramArguments</key>
    <array>
      <string>/usr/bin/env</string>
      <string>PYTHONUNBUFFERED=1</string>
      <string>python3</string>
      <string>${SERVER}</string>
      <string>--host</string>
      <string>${HOST}</string>
      <string>--port</string>
      <string>${PORT}</string>
    </array>

    <key>WorkingDirectory</key>
    <string>${ROOT}</string>

    <key>RunAtLoad</key>
    <true/>

    <key>KeepAlive</key>
    <true/>

    <key>StandardOutPath</key>
    <string>${LOG_OUT}</string>

    <key>StandardErrorPath</key>
    <string>${LOG_ERR}</string>
  </dict>
</plist>
PLIST

# Reload cleanly if already present.
launchctl bootout "gui/$(id -u)" "${PLIST_PATH}" >/dev/null 2>&1 || true
launchctl bootstrap "gui/$(id -u)" "${PLIST_PATH}"
launchctl kickstart -k "gui/$(id -u)/${LABEL}"

echo "Installed launch agent: ${PLIST_PATH}"
echo "Dashboard URL: http://${HOST}:${PORT}"
echo "Stdout log: ${LOG_OUT}"
echo "Stderr log: ${LOG_ERR}"
echo "Status:"
launchctl print "gui/$(id -u)/${LABEL}" | sed -n '1,40p' || true
