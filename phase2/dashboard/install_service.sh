#!/usr/bin/env bash
set -euo pipefail

LABEL="com.quiznat.tothf.dashboard"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
PHASE2="${ROOT}/phase2"
SOURCE_SERVER="${SCRIPT_DIR}/server.py"
SERVICE_HOME="${HOME}/.tot_hf_dashboard"
SERVER="${SERVICE_HOME}/server.py"
PYTHON_BIN="${PYTHON_BIN:-$(command -v python3 || true)}"
RUNTIME_DIR="${PHASE2}/reproducibility/runtime"
PLIST_DIR="${HOME}/Library/LaunchAgents"
PLIST_PATH="${PLIST_DIR}/${LABEL}.plist"
SERVICE_RUNTIME_DIR="${SERVICE_HOME}/runtime"
LOG_OUT="${SERVICE_RUNTIME_DIR}/dashboard_service.out.log"
LOG_ERR="${SERVICE_RUNTIME_DIR}/dashboard_service.err.log"
HOST="127.0.0.1"
PORT="8787"

if [[ -z "${PYTHON_BIN}" ]]; then
  echo "python3 not found in PATH."
  exit 1
fi
if [[ ! -f "${SOURCE_SERVER}" ]]; then
  echo "Dashboard server not found: ${SOURCE_SERVER}"
  exit 1
fi

PYTHON_BIN="$(cd "$(dirname "${PYTHON_BIN}")" && pwd)/$(basename "${PYTHON_BIN}")"

mkdir -p "${PLIST_DIR}"
mkdir -p "${RUNTIME_DIR}"
mkdir -p "${SERVICE_HOME}"
mkdir -p "${SERVICE_RUNTIME_DIR}"

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
      <string>${PYTHON_BIN}</string>
      <string>${SERVER}</string>
      <string>--host</string>
      <string>${HOST}</string>
      <string>--port</string>
      <string>${PORT}</string>
    </array>

    <key>EnvironmentVariables</key>
    <dict>
      <key>PYTHONUNBUFFERED</key>
      <string>1</string>
      <key>TOT_HF_ROOT</key>
      <string>${ROOT}</string>
    </dict>

    <key>WorkingDirectory</key>
    <string>${SERVICE_HOME}</string>

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
echo "Python interpreter: ${PYTHON_BIN}"
echo "Dashboard URL: http://${HOST}:${PORT}"
echo "Stdout log: ${LOG_OUT}"
echo "Stderr log: ${LOG_ERR}"
echo "If macOS blocks Desktop file access, run:"
echo "  bash ${SCRIPT_DIR}/repair_permissions.sh"
echo "Status:"
launchctl print "gui/$(id -u)/${LABEL}" | sed -n '1,40p' || true
