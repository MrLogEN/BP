# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## About

Bachelor thesis (bakalářská práce) in LaTeX at VŠE Prague. Topic: designing and implementing an application for Indoor Environment Quality (IEQ) monitoring using open-source tools and open data. Author: Vilém Charwot. Submission: May 2026.

## Build & Compile

```bash
./compile.sh          # compile to prace.pdf (runs latexmk -pdf prace.tex)
./cleanup.sh          # remove LaTeX build artifacts (runs latexmk -c)
./find.sh [dir]       # find U+200E (left-to-right mark) characters in files
```

Prerequisites: TeX Live + biber (latexmk handles multi-pass pdflatex + biber automatically).

## Tools

```bash
python3 tools/spellcheck.py                   # spell-check all .tex files
python3 tools/spellcheck.py --file ch.tex     # single file
python3 tools/spellcheck.py --section "Úvod"  # specific section
# prereq: pacman -S aspell aspell-cs aspell-en

python3 tools/search_scholar.py               # Google Scholar search
# prereq: pip install scholarly
```

Zotero is available via MCP (`mcp__zotero__*` tools) for searching the library, fetching PDFs, and managing references.

## Document Structure

The main entry point is `prace.tex`. Chapters are included in this order:

| File | Content |
|------|---------|
| `uvod.tex` | Introduction |
| `metody.tex` | Methodology |
| `reserse.tex` | Literature review (sub-files in `reserse/`) |
| `zarizeni_analyza.tex` | IoT device analysis |
| `aplikace_analyza.tex` | Application analysis |
| `pozadavky.tex` | Requirements (sub-files in `pozadavky/`) |
| `archimate.tex` | ArchiMate architecture |
| `navrh_architektury.tex` | Architecture design |
| `implementace.tex` | Implementation |
| `zaver.tex` | Conclusion |
| `literatura.tex` + `literatura.bib` | Bibliography (BibLaTeX/biber) |
| `appendices/` | Appendices |

Supporting files: `makra.tex` (custom macros/packages), `biblatex-setup.tex` (citation style), `zkratky.tex` (abbreviations), `zacatek.tex` (title page).

## Subfolder Instructions

- `pozadavky/CLAUDE.md` — FURPS+ requirements structure, macros, ID prefixes, and UC↔F mapping rules
- `usecase/` — use cases UC01–UC18 map 1:1 to functional requirements F01–F18

## Custom LaTeX Macros

Reusable table/list macros are defined in these files (used via `\input{}`):

- `pozadavky/funkcni-tabulka.tex` — `\FunkcniTabulka` + `\FunkcniPozadavekRow` for functional requirements
- `pozadavky/poz-tabulka.tex` — general requirements table
- `pozadavky/pripad-uziti.tex` — use case descriptions
- `pozadavky/usecase-actor.tex` — use case actor definitions
- `img/funkcni-tabulka.tex`, `img/poz-tabulka.tex` — image-side versions
- `notes/footnotes.tex`, `notes/tablenotes.tex` — reusable footnotes/table notes

## Architecture Modelling

For better understanding the ArchiMate language, there is a skill `archimate-architecture-modeling`.
ArchiMate models are maintained in Archi via MCP (`mcp__archi-mcp__*` tools). The Archi model lives in `/home/vilem/Repositories/ambiquality/ambiquality-archimate`.

The modeling worflow should be in this order:
1. Inform yourself about ArchiMate by utilizing the necessary skill `archimate-architecture-modeling`
2. Inform yourself about the current state of the model via the `archi-mcp` 
2. Gather necessary context from the user and the repository (mainly the `pozadavky/`, `useacase/` and `navrh_architektury/`  directories)
3. Propose changes using the `archi-mcp` or let the user handle it themselve.

## AI Usage Log

All AI-assisted work must be logged in `ai-usage-log/` (one `.tex` file per category: `literatura`, `gramatika`, `kod`, `text`, `data`, `ostatni`). The log is compiled as a separate document via `ai-usage-log/main.tex`.

## Language

The thesis is written in Czech. New content should be in Czech unless quoting English sources. Technical terms follow Czech academic convention.
