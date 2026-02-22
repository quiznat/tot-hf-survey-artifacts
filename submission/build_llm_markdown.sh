#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_HTML="$ROOT_DIR/paper.html"
OUT_MD="$ROOT_DIR/tot-hf-agents-llm.md"
TMP_HTML="$(mktemp "${TMPDIR:-/tmp}/paper-llm-sanitized.XXXXXX.html")"
trap 'rm -f "$TMP_HTML"' EXIT

if ! command -v pandoc >/dev/null 2>&1; then
  echo "Error: pandoc is required to generate tot-hf-agents-llm.md" >&2
  exit 1
fi

# Pandoc may treat custom <pre data-*> wrappers as opaque HTML and drop
# language annotations. Normalize code wrappers for conversion fidelity.
perl -0777 -pe '
  s/<pre\s+data-listing="[^"]+"\s+data-kind="[^"]+">/<pre>/g;
  s#<picture>\s*<source[^>]*>\s*(<img[^>]+>)\s*</picture>#$1#gs;
  s#<div class="diagram-host"[^>]*>.*?</div>##gs;
' "$SRC_HTML" > "$TMP_HTML"

pandoc \
  "$TMP_HTML" \
  --from=html \
  --to=gfm \
  --strip-comments \
  --wrap=none \
  --output="$OUT_MD"

echo "Generated: $OUT_MD"
