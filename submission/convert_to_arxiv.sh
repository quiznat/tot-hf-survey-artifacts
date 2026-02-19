#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_HTML="$ROOT_DIR/paper.html"
OUT_DIR="$ROOT_DIR/submission/arxiv"

mkdir -p "$OUT_DIR"

if ! command -v pandoc >/dev/null 2>&1; then
  echo "Error: pandoc is required for arXiv source conversion." >&2
  echo "Install pandoc, then rerun: bash submission/convert_to_arxiv.sh" >&2
  exit 1
fi

pandoc \
  "$SRC_HTML" \
  --from=html \
  --to=latex \
  --standalone \
  --output="$OUT_DIR/main.tex"

echo "Generated: $OUT_DIR/main.tex"
