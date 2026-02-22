#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_HTML="$ROOT_DIR/paper.html"
OUT_DIR="$ROOT_DIR/submission/arxiv"
TMP_HTML="$(mktemp "${TMPDIR:-/tmp}/paper-arxiv-sanitized.XXXXXX.html")"
trap 'rm -f "$TMP_HTML"' EXIT

mkdir -p "$OUT_DIR"

if ! command -v pandoc >/dev/null 2>&1; then
  echo "Error: pandoc is required for arXiv source conversion." >&2
  echo "Install pandoc, then rerun: bash submission/convert_to_arxiv.sh" >&2
  exit 1
fi

# Pandoc may treat custom <pre data-*> wrappers as opaque HTML and drop
# language annotations. Normalize code wrappers for conversion fidelity.
perl -0777 -pe '
  s/<pre\s+data-listing="[^"]+"\s+data-kind="[^"]+">/<pre>/g;
  s#<div class="diagram-host"[^>]*>.*?</div>##gs;
' "$SRC_HTML" > "$TMP_HTML"

pandoc \
  "$TMP_HTML" \
  --from=html \
  --to=latex \
  --standalone \
  --output="$OUT_DIR/main.tex"

# Normalize symbols that frequently break CI LaTeX engines or default fonts.
# Keep semantics while using ASCII-safe equivalents in generated source.
perl -i -CS -pe '
  s/₀/0/g; s/₁/1/g; s/₂/2/g; s/₃/3/g; s/₄/4/g;
  s/₅/5/g; s/₆/6/g; s/₇/7/g; s/₈/8/g; s/₉/9/g;
  s/ₖ/k/g;
  s/←/<-/g; s/→/->/g;
  s/∅/empty_set/g; s/∪/union/g;
  s/├──/|--/g; s/└──/`--/g; s/│/|/g; s/─/-/g;
' "$OUT_DIR/main.tex"

echo "Generated: $OUT_DIR/main.tex"
