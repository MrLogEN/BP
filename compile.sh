#!/bin/bash
set -euo pipefail

# Název souboru bez přípony
filename="prace"

pdflatex -interaction=nonstopmode -halt-on-error -file-line-error "$filename.tex"
biber "$filename"
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error "$filename.tex"
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error "$filename.tex"

echo "Kompilace dokončena."
