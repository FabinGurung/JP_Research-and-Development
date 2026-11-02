#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
# Install licensed Times New Roman locally; do not distribute private font files.
xelatex -interaction=nonstopmode -halt-on-error main.tex
bibtex8 -8 main
xelatex -interaction=nonstopmode -halt-on-error main.tex
xelatex -interaction=nonstopmode -halt-on-error main.tex
