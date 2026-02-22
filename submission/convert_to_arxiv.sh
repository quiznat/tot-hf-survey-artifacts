#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_HTML="$ROOT_DIR/paper.html"
OUT_DIR="$ROOT_DIR/submission/arxiv"
TMP_HTML="$(mktemp "${TMPDIR:-/tmp}/paper-arxiv-sanitized.XXXXXX.html")"
ASSETS_SRC_DIR="$ROOT_DIR/assets"
ASSETS_DST_DIR="$OUT_DIR/assets"
trap 'rm -f "$TMP_HTML"' EXIT

mkdir -p "$OUT_DIR"

copy_referenced_assets() {
  local html_file="$1"
  local source_assets_dir="$2"
  local target_assets_dir="$3"

  rm -rf "$target_assets_dir"
  mkdir -p "$target_assets_dir"

  local asset_paths
  asset_paths="$(
    perl -nE '
      while (/(?:src|href)=["\x27]\.\/assets\/([^"\x27?#]+)/g) { print "$1\n"; }
      while (/srcset=["\x27]\.\/assets\/([^"\x27?#\s,]+)/g) { print "$1\n"; }
      while (/url\(["\x27]?\.\/assets\/([^)"\x27?#]+)/g) { print "$1\n"; }
    ' "$html_file" | sort -u
  )"

  while IFS= read -r rel_path; do
    [ -z "$rel_path" ] && continue
    if [ -f "$source_assets_dir/$rel_path" ]; then
      mkdir -p "$target_assets_dir/$(dirname "$rel_path")"
      cp "$source_assets_dir/$rel_path" "$target_assets_dir/$rel_path"
    else
      echo "Warning: referenced asset not found: $source_assets_dir/$rel_path" >&2
    fi
  done <<< "$asset_paths"
}

if ! command -v pandoc >/dev/null 2>&1; then
  echo "Error: pandoc is required for arXiv source conversion." >&2
  echo "Install pandoc, then rerun: bash submission/convert_to_arxiv.sh" >&2
  exit 1
fi

if command -v python3 >/dev/null 2>&1; then
  python3 "$ROOT_DIR/submission/render_manuscript_diagrams.py"
else
  echo "Warning: python3 not found; skipping diagram regeneration." >&2
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

copy_referenced_assets "$TMP_HTML" "$ASSETS_SRC_DIR" "$ASSETS_DST_DIR"
bash "$ROOT_DIR/submission/postprocess_latex.sh" "$OUT_DIR/main.tex"

echo "Generated: $OUT_DIR/main.tex"
