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
