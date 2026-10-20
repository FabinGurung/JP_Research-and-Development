#!/usr/bin/env bash
# Git-managed Saugat source + SINGLE R&D shared academic LaTeX style.
# Not a CP114 production replacement until a governed exact-font/visual gate succeeds.
set -euo pipefail
here="$(cd -- "$(dirname -- "$0")" && pwd)"
repo="$(git -C "$here" rev-parse --show-toplevel)"
template="$repo/controls/latex/template"
test -f "$template/pumlsc-shared.sty" || { echo 'Missing canonical Git LaTeX template' >&2; exit 2; }
# No research binaries are committed to public Git. Require exact recovered CP114 assets.
# Restore once from verified Drive source ZIP with ../scripts/restore_cp114_assets.py.
python3 "$repo/researchers/saugat-paneru/latex/scripts/restore_cp114_assets.py" --check --root "$here"
mode="${1:-preview}"
if [[ "$mode" == preview ]]; then
  fontflag='\def\PUPreviewTinosFont{1}'
elif [[ "$mode" == production ]]; then
  fontflag=''
  fc-match -f '%{family}' 'Times New Roman' | grep -q '^Times New Roman' || { echo 'Exact Times New Roman not registered' >&2; exit 3; }
else echo 'usage: ./build.sh preview|production' >&2;exit 2;fi
mkdir -p "$here/.build"
# Calendar-driven title-page month follows Nepal local time at month boundaries.
export TZ=Asia/Kathmandu
cd "$here"
export TEXINPUTS="$template/:$repo/researchers/saugat-paneru/latex/extensions/:${TEXINPUTS:-}:"
for pass in 1 2 3 4; do
 xelatex -no-pdf -interaction=nonstopmode -halt-on-error -file-line-error -output-directory="$here/.build" "$fontflag\input{main.tex}"
 if [[ $pass == 1 ]];then biber --input-directory "$here/.build" --output-directory "$here/.build" main;fi
done
xdvipdfmx -o "$here/.build/main.pdf" "$here/.build/main.xdv"
if grep -Eq 'Overfull \\[hv]box|Float too large for page' "$here/.build/main.log";then echo 'Layout QA failed' >&2; exit 4;fi
pdffonts "$here/.build/main.pdf"
echo "Built $here/.build/main.pdf — no PDF current promotion implied"
