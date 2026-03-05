#!/bin/bash

# Smazání souborů dle seznamu
for pattern in "*.aux" "*.log" "*.out" "*.toc" "*.lof" "*.lot" "*.bbl" "*.blg" "*.synctex.gz" "*.fls" "*.fdb_latexmk" "*.xmpi" "*.txss2"; do
    find . -type f -name "$pattern" -exec rm -f {} +
done

echo "Nepotřebné soubory byly smazány."
