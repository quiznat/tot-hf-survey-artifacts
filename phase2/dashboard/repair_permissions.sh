#!/usr/bin/env bash
set -euo pipefail

LABEL="com.quiznat.tothf.dashboard"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_SCRIPT="${SCRIPT_DIR}/install_service.sh"
PLIST_PATH="${HOME}/Library/LaunchAgents/${LABEL}.plist"

if [[ ! -f "${PLIST_PATH}" ]]; then
  echo "LaunchAgent is not installed yet. Installing now..."
  bash "${INSTALL_SCRIPT}"
fi

PYTHON_BIN="$(
  /usr/libexec/PlistBuddy -c "Print :ProgramArguments:0" "${PLIST_PATH}" 2>/dev/null || true
)"
if [[ -z "${PYTHON_BIN}" ]]; then
  PYTHON_BIN="$(command -v python3 || true)"
fi

echo "Service label: ${LABEL}"
echo "LaunchAgent plist: ${PLIST_PATH}"
echo "Service python interpreter: ${PYTHON_BIN}"
echo
echo "Opening macOS Full Disk Access settings..."
open "x-apple.systempreferences:com.apple.preference.security?Privacy_AllFiles" >/dev/null 2>&1 || true

cat <<MSG
Grant Full Disk Access to this exact interpreter binary:
  ${PYTHON_BIN}

After granting access, reinstall the dashboard service:
  bash ${INSTALL_SCRIPT}

Then verify:
  bash ${SCRIPT_DIR}/status_service.sh
MSG
