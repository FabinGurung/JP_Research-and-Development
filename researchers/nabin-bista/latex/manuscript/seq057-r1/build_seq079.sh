#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export TEXINPUTS="./controls/latex/template//:${TEXINPUTS:-}"
# Requires the owner's licensed Times New Roman installation; never distribute fonts.
# Preserve the existing IEEE numeric bibliography selection.
xelatex -no-pdf -interaction=nonstopmode -halt-on-error main.tex
bibtex8 -8 main
xelatex -no-pdf -interaction=nonstopmode -halt-on-error main.tex
xelatex -no-pdf -interaction=nonstopmode -halt-on-error main.tex
xdvipdfmx -V 7 -o main.pdf main.xdv
