#!/usr/bin/env bash
set -euo pipefail

PORT="${1:-8891}"

pids="$(lsof -t -iTCP:${PORT} -sTCP:LISTEN || true)"
if [[ -z "${pids}" ]]; then
  echo "No dashboard process listening on port ${PORT}."
  exit 0
fi

echo "${pids}" | xargs kill
echo "Stopped dashboard process(es) on port ${PORT}: ${pids}"
