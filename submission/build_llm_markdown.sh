#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_HTML="$ROOT_DIR/paper.html"
OUT_MD="$ROOT_DIR/tot-hf-agents-llm.md"

if ! command -v pandoc >/dev/null 2>&1; then
  echo "Error: pandoc is required to generate tot-hf-agents-llm.md" >&2
  exit 1
fi

pandoc \
  "$SRC_HTML" \
  --from=html \
  --to=gfm \
  --strip-comments \
  --wrap=none \
  --output="$OUT_MD"

echo "Generated: $OUT_MD"
