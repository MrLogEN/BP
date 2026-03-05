# Bakalářská práce v LaTeXu / Bachelor Thesis in LaTeX

## Obsah / Table of Contents

- [Jak zkompilovat práci](#jak-zkompilovat-práci)
  - [Prerekvizity](#prerekvizity)
  - [Vlastní kompilace](#vlastní-kompilace)
- [How to Compile the Thesis](#how-to-compile-the-thesis)
  - [Prerequisites](#prerequisites)
  - [Compilation](#compilation)

## Jak zkompilovat práci

### Prerekvizity

1. Nainstalovaný [TeX live](https://tug.org/texlive/)
2. Nainstalované balíčky [biber](https://ctan.org/pkg/biber)

### Vlastní kompilace 

Je potřeba spustit script pro kompilaci
```bash
./compile.sh
```
Tento skript spouští příkazy `pdflatex` a `biber` a generuje výsledné pdf `prace.pdf`.

---

## How to Compile the Thesis

### Prerequisites

1. Installed [TeX live](https://tug.org/texlive/)
2. Installed [biber](https://ctan.org/pkg/biber) package

### Compilation

Run the compilation script
```bash
./compile.sh
```
This script runs `pdflatex` and `biber` commands and generates the final PDF `prace.pdf`.

---

## Nástroje v `tools/`

### Prerekvizity

**`tools/search_zotero_pdf.py`** — fulltextové vyhledávání v PDF souborech Zotero:
```bash
pacman -S poppler   # poskytuje příkaz pdftotext
```
Vyžaduje nainstalované a spuštěné [Zotero](https://www.zotero.org/) s doplňkem [Better BibTeX](https://retorque.re/zotero-better-bibtex/) — aplikace musí běžet a naslouchat na portu `23119`.

**`tools/search_scholar.py`** — vyhledávání na Google Scholar:
```bash
pip install scholarly
```

**`tools/spellcheck.py`** — kontrola pravopisu `.tex` souborů:
```bash
pacman -S aspell aspell-cs aspell-en
```
Volitelně přidejte vlastní výjimky do `tools/wordlist.txt` (jeden výraz na řádek).

---

## Tools in `tools/`

### Prerequisites

**`tools/search_zotero_pdf.py`** — full-text search across Zotero PDFs:
```bash
pacman -S poppler   # provides the pdftotext command
```
Requires [Zotero](https://www.zotero.org/) with the [Better BibTeX](https://retorque.re/zotero-better-bibtex/) plugin installed and running — the application must be open and listening on port `23119`.

**`tools/search_scholar.py`** — Google Scholar search:
```bash
pip install scholarly
```

**`tools/spellcheck.py`** — spell-check `.tex` files:
```bash
pacman -S aspell aspell-cs aspell-en
```
Optionally add custom exceptions to `tools/wordlist.txt` (one word per line).
