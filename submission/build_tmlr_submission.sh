#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_HTML="$ROOT_DIR/paper.html"
TMLR_DIR="$ROOT_DIR/submission/tmlr"
ANON_DIR="$TMLR_DIR/anonymous"
ANON_HTML="$ANON_DIR/paper-anonymous.html"
ANON_MD="$ANON_DIR/paper-anonymous.md"
ANON_TEX="$ANON_DIR/main.tex"
OFFICIAL_DIR="$TMLR_DIR/official-anonymous"
OFFICIAL_TEX="$OFFICIAL_DIR/main-tmlr.tex"
TMLR_STYLE="$TMLR_DIR/template/tmlr.sty"

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

mkdir -p "$ANON_DIR"

if ! command -v pandoc >/dev/null 2>&1; then
  echo "Error: pandoc is required." >&2
  echo "Install pandoc, then rerun: bash submission/build_tmlr_submission.sh" >&2
  exit 1
fi

if command -v python3 >/dev/null 2>&1 && command -v dot >/dev/null 2>&1; then
  python3 "$ROOT_DIR/submission/render_manuscript_diagrams.py"
else
  echo "Warning: python3 and/or graphviz 'dot' not found; using existing diagram assets." >&2
fi

cp "$SRC_HTML" "$ANON_HTML"

# Replace identifying front matter with anonymous metadata suitable for double-blind review.
perl -0777 -i -pe 's#<section class="front-matter">.*?</section>#<section class="front-matter">\
            <p class="authors-line"><strong>Authors:</strong> Anonymous Authors</p>\
            <ol class="affiliation-list">\
                <li><strong>1</strong> Affiliation withheld for double-blind review</li>\
            </ol>\
            <p class="contact-line"><strong>Contact:</strong> withheld for double-blind review</p>\
            <p class="meta-line"><strong>Version:</strong> v1.1.1 -- Pre-submission corrections (21 February 2026)</p>\
            <p class="meta-line"><strong>Submission venue:</strong> TMLR (double-blind review track)</p>\
        </section>#s' "$ANON_HTML"

# Replace authorship note block with anonymous disclosure text.
perl -0777 -i -pe 's#<h2>Note on Authorship</h2>\s*(?:<p>.*?</p>\s*)+#<h2>Note on Authorship</h2>\
        <p>For double-blind review, identifying details are withheld. The manuscript workflow included autonomous system assistance and iterative human verification. The submitting author retains full responsibility for factual accuracy, editorial decisions, and policy-compliant disclosure upon acceptance.</p>#s' "$ANON_HTML"

# Redact the system-identifying monitoring appendix in anonymous review builds.
perl -0777 -i -pe 's#<h2 id="appendix-h-monitoring-snapshot">.*?<hr>#<h2 id="appendix-h-monitoring-snapshot">Appendix H: Redacted for Anonymous Review</h2>\
        <p>System-identifying screenshots, profile links, and leaderboard references are withheld for double-blind review. Redacted evidence materials are available to editors upon request.</p>\
\
        <hr>#s' "$ANON_HTML"

# Remove direct personal/system URLs and names that may de-anonymize the submission.
perl -i -pe '
  s#https://www\.linkedin\.com/in/michael-leydon/#https://example.com/redacted#g;
  s#https://www\.quiznat\.com/#https://example.com/redacted#g;
  s#https://clauddib\.quiznat\.com/#https://example.com/redacted#g;
  s#https://moltx\.io/ClaudDib#https://example.com/redacted#g;
  s#https://moltx\.io/leaderboard#https://example.com/redacted#g;
  s#https://github\.com/quiznat/tot-hf-survey-artifacts#https://example.com/redacted#g;
  s#github\.com/quiznat/tot-hf-survey-artifacts#example.com/redacted#g;
  s/Michael Leydon/Anonymous Author/g;
  s/Quiznat/Anonymous Contributor/g;
  s/Claud\x27Dib/System Contributor/g;
  s/ClaudDib/System Contributor/g;
' "$ANON_HTML"

# Pandoc may treat custom <pre data-*> wrappers as opaque HTML and drop
# language annotations. Normalize code wrappers for conversion fidelity.
perl -0777 -i -pe '
  s/<pre\s+data-listing="[^"]+"\s+data-kind="[^"]+">/<pre>/g;
  s#<picture>\s*<source[^>]*>\s*(<img[^>]+>)\s*</picture>#$1#gs;
  s#<div class="diagram-host"[^>]*>.*?</div>##gs;
' "$ANON_HTML"

pandoc \
  "$ANON_HTML" \
  --from=html \
  --to=gfm \
  --wrap=none \
  --output="$ANON_MD"

pandoc \
  "$ANON_HTML" \
  --from=html \
  --to=latex \
  --standalone \
  --output="$ANON_TEX"

# Normalize characters that can break default LaTeX font pipelines.
perl -i -CS -pe '
  s/₀/0/g; s/₁/1/g; s/₂/2/g; s/₃/3/g; s/₄/4/g;
  s/₅/5/g; s/₆/6/g; s/₇/7/g; s/₈/8/g; s/₉/9/g;
  s/ₖ/k/g;
  s/←/<-/g; s/→/->/g;
  s/∅/empty_set/g; s/∪/union/g;
  s/├──/|--/g; s/└──/`--/g; s/│/|/g; s/─/-/g;
' "$ANON_TEX"

bash "$ROOT_DIR/submission/postprocess_latex.sh" "$ANON_TEX"
copy_referenced_assets "$ANON_HTML" "$ROOT_DIR/assets" "$ANON_DIR/assets"

if command -v latexmk >/dev/null 2>&1; then
  (
    cd "$ANON_DIR"
    latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
  )
else
  echo "Warning: latexmk not found; skipping PDF compile for anonymous TMLR package." >&2
fi

# Optional: build an official-style anonymous PDF if tmlr.sty is available.
if [ -f "$TMLR_STYLE" ]; then
  mkdir -p "$OFFICIAL_DIR"
  cp "$ANON_TEX" "$OFFICIAL_TEX"
  cp "$TMLR_STYLE" "$OFFICIAL_DIR/tmlr.sty"
  rm -rf "$OFFICIAL_DIR/assets"
  if [ -d "$ANON_DIR/assets" ]; then
    cp -r "$ANON_DIR/assets" "$OFFICIAL_DIR/assets"
  fi

  # Inject official style package and keep anonymous author block.
  perl -0777 -i -pe '
    s#\\documentclass\\[\\s*english,\\s*\\]\\{article\\}#\\documentclass{article}\\n\\usepackage{tmlr}#s;
    s#\\title\\{[^}]*\\}#\\title{Tree of Thoughts Meets Hugging Face Agents: A Survey of Tree of Thoughts and Hugging Face Agent Frameworks}#s;
    s#\\author\\{[^}]*\\}#\\author{Anonymous Authors}#s;
    s#\\date\\{[^}]*\\}#\\date{}#s;
    s#\\n\\textbf\\{Authors:\\}.*?\\textbf\\{Submission venue:\\} TMLR \\(double-blind review track\\)\\n\\n#\\n#s;
  ' "$OFFICIAL_TEX"

  if command -v latexmk >/dev/null 2>&1; then
    (
      cd "$OFFICIAL_DIR"
      latexmk -xelatex -interaction=nonstopmode -halt-on-error main-tmlr.tex
    )
  else
    echo "Warning: latexmk not found; skipping official-style TMLR PDF compile." >&2
  fi
else
  echo "Info: $TMLR_STYLE not found; skipping official-style TMLR PDF build." >&2
fi

rm -f "$TMLR_DIR/tmlr-submission-anonymous.tgz"
tar -czf "$TMLR_DIR/tmlr-submission-anonymous.tgz" -C "$ANON_DIR" .

echo "Generated anonymous TMLR package assets:"
echo "  - $ANON_HTML"
echo "  - $ANON_MD"
echo "  - $ANON_TEX"
if [ -f "$ANON_DIR/main.pdf" ]; then
  echo "  - $ANON_DIR/main.pdf"
fi
echo "Optional official-style outputs (if style available):"
if [ -f "$OFFICIAL_TEX" ]; then
  echo "  - $OFFICIAL_TEX"
fi
if [ -f "$OFFICIAL_DIR/main-tmlr.pdf" ]; then
  echo "  - $OFFICIAL_DIR/main-tmlr.pdf"
fi
echo "  - $TMLR_DIR/tmlr-submission-anonymous.tgz"
