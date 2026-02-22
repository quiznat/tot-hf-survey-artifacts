#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/quiznat/Desktop/Tree_of_Thought"
RUNTIME_DIR="${ROOT}/phase2/reproducibility/runtime"
PORT="${1:-8891}"

mkdir -p "${RUNTIME_DIR}"

if lsof -iTCP:"${PORT}" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "Dashboard already listening on port ${PORT}."
  exit 0
fi

ts="$(date -u +%Y%m%dT%H%M%SZ)"
log="${RUNTIME_DIR}/dashboard_manual_${ts}.log"
pidf="${RUNTIME_DIR}/dashboard_manual_${ts}.pid"

nohup env PYTHONUNBUFFERED=1 \
  python3 "${ROOT}/phase2/dashboard/server.py" \
  --host 127.0.0.1 \
  --port "${PORT}" \
  > "${log}" 2>&1 < /dev/null &

echo $! > "${pidf}"
sleep 1
echo "Started dashboard manual service."
echo "URL: http://127.0.0.1:${PORT}"
echo "PID: $(cat "${pidf}")"
echo "Log: ${log}"
