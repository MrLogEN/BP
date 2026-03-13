# Agent rules
The goal of this thesis is to describe Indoor Environment Quality (IEQ), analyze existing open source applications collecting open data on IEQ, find requirements for the app and finaly to propose a solution and implement it.

## File edits
- Never modify the content of any files with .tex and .bib suffix (i.e. file.tex) unless specifically asked to do so. Other files are editable.

## Suggestions
- When providining text improvements suggestions, base them on the czech language stylistics and facts from existing text in this repo or in the refenreces.
- When providing text improvement or stylistic suggestions, always format them clearly and with extra spacing between items. For each recommendation, include: file path, line number, start and end character position of the problematic span on that line, the problematic snippet, the suggested replacement, and a brief rationale in Czech.

Example output:

12. `vymezeni.tex`, ř. 86, poz. 101–127
    **Úsek:** `dochází většímu ochlazování`
    **Doporučení:** `dochází k většímu ochlazování`
    **Důvod:** chybí předložka.

13. `vymezeni.tex`, ř. 90, poz. 241–285
    **Úsek:** `Při provedené studii mezi žáky bylo zjištěno,`
    **Doporučení:** `Ve studii mezi žáky bylo zjištěno,`
    **Důvod:** přirozenější odborný styl.

14. `vymezeni.tex`, ř. 92, poz. 37–61
    **Úsek:** `učení, paměť, kreativitu.`
    **Doporučení:** `učení, paměť i kreativitu.`
    **Důvod:** plynulejší výčet.

## Spell and style checking

Run only when explicitly requested by the user. Never run proactively.

**Prerequisites:** `pacman -S aspell aspell-cs aspell-en`

**Scope:** The user may specify a file (`--file <soubor.tex>`), a section heading (`--section "<nadpis>"`), or omit both to check the entire thesis.

### Step 1 — Spell check
```bash
python3 tools/spellcheck.py [--file <soubor.tex>] [--section "<nadpis>"]
```
The script strips LaTeX commands, detects the language per paragraph (Czech diacritics → `cs`, otherwise `en`), and reports misspelled words with aspell suggestions.

### Step 2 — Grammar and style review
After running the script, read the relevant plain-text passages and evaluate:
- **Czech:** sentence variety, clarity, academic register, stylistic correctness per Czech academic writing conventions.
- **English:** grammar, style, clarity.

### Response format
Return a numbered list of recommendations. Each item must include:
1. **Location** — file name and approximate line/paragraph
2. **Issue type** — spelling / grammar / style / clarity
3. **Original text** — the problematic snippet
4. **Suggested replacement** — proposed corrected text
5. **Rationale** — brief explanation in Czech

**Constraints:** Preserve the original meaning and factual content in full. Do not alter the structure of sentences beyond what is necessary to fix the identified issue.

## References and text search

### Primary source: Zotero
The only source of truth is Zotero. Always search Zotero first using the local Better BibTeX JSON-RPC API before answering any thesis-related question.

**Step 1 — metadata search (title, abstract, keywords):**
```bash
curl -s "http://localhost:23119/better-bibtex/json-rpc" \
  -X POST -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"item.search","params":["<query>"],"id":1}'
```

**Step 2 — full-text PDF search (always run after metadata search):**
```bash
python3 tools/search_zotero_pdf.py "<query>" --context 3
```
This searches all PDFs stored in `~/Zotero/storage/` and returns excerpts with context.
Note: Zotero JSON-RPC only searches metadata — always also search PDFs to avoid missing content.

**Response format when source found:**
- Explain the answer based on the source content (metadata or PDF excerpt)
- Cite as: *Název (Autoři, Rok)* — the user generates the BibLaTeX key themselves
- Provide the URL/DOI if available

**If no relevant result found in Zotero (neither metadata nor PDFs):**
Ask the user: *"Nenašel jsem odpověď v Zoteru. Chcete hledat na Google Scholar?"*

### Fallback: Google Scholar
If the user agrees to search Google Scholar, run:
```bash
python3 tools/search_scholar.py "<query>" [--limit 5]
```
The script returns JSON. Present results as:
- Název, Autoři, Rok, Venue, Abstrakt (zkrácený), URL
- Remind the user to verify full-text access via SFX@VSE and add relevant sources to Zotero

**Limitations:**
- `scholarly` scrapes Google Scholar and may be blocked by CAPTCHA — inform the user if this happens
- SFX@VSE institutional access cannot be filtered programmatically; user verifies manually
