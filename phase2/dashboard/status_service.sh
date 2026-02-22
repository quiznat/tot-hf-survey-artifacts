#!/usr/bin/env bash
set -euo pipefail

LABEL="com.quiznat.tothf.dashboard"
PLIST_PATH="${HOME}/Library/LaunchAgents/${LABEL}.plist"

launchctl print "gui/$(id -u)/${LABEL}" | sed -n '1,120p'

if [[ -f "${PLIST_PATH}" ]]; then
  echo
  echo "Configured interpreter:"
  /usr/libexec/PlistBuddy -c "Print :ProgramArguments:0" "${PLIST_PATH}" 2>/dev/null || true
  echo "Configured TOT_HF_ROOT:"
  /usr/libexec/PlistBuddy -c "Print :EnvironmentVariables:TOT_HF_ROOT" "${PLIST_PATH}" 2>/dev/null || true
fi

echo
echo "HTTP check:"
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8787/ || true
