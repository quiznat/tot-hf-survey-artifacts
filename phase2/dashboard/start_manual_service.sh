#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
RUNTIME_DIR="${ROOT}/phase2/reproducibility/runtime"
PORT="${1:-8891}"
PYTHON_BIN="${PYTHON_BIN:-$(command -v python3 || true)}"

if [[ -z "${PYTHON_BIN}" ]]; then
  echo "python3 not found in PATH."
  exit 1
fi
PYTHON_BIN="$(cd "$(dirname "${PYTHON_BIN}")" && pwd)/$(basename "${PYTHON_BIN}")"

mkdir -p "${RUNTIME_DIR}"

if lsof -iTCP:"${PORT}" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "Dashboard already listening on port ${PORT}."
  exit 0
fi

ts="$(date -u +%Y%m%dT%H%M%SZ)"
log="${RUNTIME_DIR}/dashboard_manual_${ts}.log"
pidf="${RUNTIME_DIR}/dashboard_manual_${ts}.pid"

nohup env PYTHONUNBUFFERED=1 \
  TOT_HF_ROOT="${ROOT}" \
  "${PYTHON_BIN}" "${SCRIPT_DIR}/server.py" \
  --host 127.0.0.1 \
  --port "${PORT}" \
  > "${log}" 2>&1 < /dev/null &

echo $! > "${pidf}"
sleep 1
echo "Started dashboard manual service."
echo "URL: http://127.0.0.1:${PORT}"
echo "PID: $(cat "${pidf}")"
echo "Log: ${log}"
