#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SRC_MD="$ROOT_DIR/phase2/manuscript/PREPAPER.md"
OUT_HTML="$ROOT_DIR/phase2/paper.html"
CSS_REL="./manuscript/phase2-paper.css"

if ! command -v pandoc >/dev/null 2>&1; then
  echo "Error: pandoc is required to generate phase2/paper.html" >&2
  echo "Install pandoc, then rerun: bash phase2/manuscript/build_phase2_html.sh" >&2
  exit 1
fi

pandoc \
  "$SRC_MD" \
  --from gfm \
  --to html5 \
  --standalone \
  --toc \
  --toc-depth=3 \
  --number-sections \
  --metadata title="Tree-of-Thought Search with Hugging Face Inference Models" \
  --metadata subtitle="Phase 2 Prepaper (Living Draft)" \
  --css "$CSS_REL" \
  --output "$OUT_HTML"

echo "Built $OUT_HTML"
