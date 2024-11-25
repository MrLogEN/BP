#!/bin/bash

# Název souboru bez přípony
filename="prace"

# První kompilace pomocí pdflatex
pdflatex "$filename.tex"

# Spuštění biber
biber "$filename"

# Druhá a třetí kompilace pomocí pdflatex
pdflatex "$filename.tex"
pdflatex "$filename.tex"

echo "Kompilace dokončena."
