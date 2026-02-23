#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <path-to-main.tex>" >&2
  exit 1
fi

TEX_FILE="$1"
if [ ! -f "$TEX_FILE" ]; then
  echo "Error: file not found: $TEX_FILE" >&2
  exit 1
fi

has_pattern() {
  local pattern="$1"
  local file="$2"
  if command -v rg >/dev/null 2>&1; then
    rg -q "$pattern" "$file"
  else
    grep -Eq "$pattern" "$file"
  fi
}

# Add robust line-breaking support for code blocks.
if ! has_pattern "\\\\usepackage\\{fvextra\\}" "$TEX_FILE"; then
  perl -0777 -i -pe '
    s~\\usepackage\{color\}~\\usepackage{color}\n\\usepackage{fvextra}~s;
  ' "$TEX_FILE"
fi

perl -0777 -i -pe '
  s~^\\DefineVerbatimEnvironment\{Highlighting\}\{Verbatim\}\{.*$~\\DefineVerbatimEnvironment{Highlighting}{Verbatim}{commandchars=\\\\\\{\\\\\\},fontsize=\\footnotesize,breaklines=true}~m;
' "$TEX_FILE"

# Configure longtable behavior for margin-safe rendering.
if ! has_pattern "\\\\newcolumntype\\{L\\}" "$TEX_FILE"; then
  perl -0777 -i -pe '
    s~\\makesavenoteenv\{longtable\}~\\makesavenoteenv{longtable}\n\\setlength{\\tabcolsep}{2pt}\n\\setlength{\\LTleft}{0pt}\n\\setlength{\\LTright}{0pt}\n\\setlength{\\LTcapwidth}{\\linewidth}\n\\renewcommand{\\arraystretch}{1.08}\n\\newcolumntype{L}[1]{>{\\raggedright\\arraybackslash}p{#1}}\n\\AtBeginEnvironment{longtable}{\\small}~s;
  ' "$TEX_FILE"
fi

# Replace fixed-width left-aligned columns with wrapped paragraph columns.
perl -i -pe '
  s/\\begin\{longtable\}(?:\[\])?\{\@\{\}lllllll\@\{\}\}/\\begin{longtable}[]{L{0.06\\linewidth}L{0.14\\linewidth}L{0.08\\linewidth}L{0.10\\linewidth}L{0.10\\linewidth}L{0.22\\linewidth}L{0.16\\linewidth}}/g;
  s/\\begin\{longtable\}(?:\[\])?\{\@\{\}lllll\@\{\}\}/\\begin{longtable}[]{L{0.17\\linewidth}L{0.13\\linewidth}L{0.16\\linewidth}L{0.10\\linewidth}L{0.30\\linewidth}}/g;
  s/\\begin\{longtable\}(?:\[\])?\{\@\{\}llll\@\{\}\}/\\begin{longtable}[]{L{0.13\\linewidth}L{0.27\\linewidth}L{0.27\\linewidth}L{0.19\\linewidth}}/g;
  s/\\begin\{longtable\}(?:\[\])?\{\@\{\}lll\@\{\}\}/\\begin{longtable}[]{L{0.21\\linewidth}L{0.14\\linewidth}L{0.57\\linewidth}}/g;
  s/\\begin\{longtable\}(?:\[\])?\{\@\{\}ll\@\{\}\}/\\begin{longtable}[]{L{0.30\\linewidth}L{0.62\\linewidth}}/g;
' "$TEX_FILE"
