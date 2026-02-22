#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_HTML="$ROOT_DIR/paper.html"

if [[ ! -f "$SRC_HTML" ]]; then
  echo "Error: paper.html not found at $SRC_HTML" >&2
  exit 1
fi

echo "Checking for pseudo-code listings in $SRC_HTML ..."

if grep -nE '<pre[^>]*data-listing="pseudo"' "$SRC_HTML"; then
  echo "Error: pseudo listings detected (data-listing=\"pseudo\")." >&2
  exit 1
fi

if grep -nF 'data-kind="Illustrative pseudo-code"' "$SRC_HTML"; then
  echo "Error: illustrative pseudo-code labels detected." >&2
  exit 1
fi

if grep -nE '<!--[[:space:]]*Illustrative[[:space:]]*/[[:space:]]*pseudo-code[[:space:]]*-->' "$SRC_HTML"; then
  echo "Error: illustrative pseudo-code comment markers detected." >&2
  exit 1
fi

echo "OK: no pseudo-code listings detected."
