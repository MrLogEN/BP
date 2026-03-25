#!/bin/bash
set -euo pipefail

# Název souboru bez přípony
filename="prace"

latexmk -c 
latexmk -pdf "$filename.tex"

echo "Kompilace dokončena."
