# Agent rules
The goal of this thesis is to describe Indoor Environment Quality (IEQ), analyze existing open source applications collecting open data on IEQ, find requirements for the app and finaly to propose a solution and implement it.

## File edits
- Never modify the content of any files with .tex and .bib suffix (i.e. file.tex) unless specifically asked to do so. Other files are editable.

## AI Usage Logging
Viz sekce "AI Usage Logging" v `.github/copilot-instructions.md` pro pravidla dokumentace použití AI nástrojů.

## Suggestions
Use the `suggestions` skill for style and clarity improvements. Use `spellcheck` skill for spelling corrections.

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

### Primary source: Zotero MCP
The primary and authoritative source of academic materials is Zotero, accessed via **Zotero MCP tools**:

- `zotero_semantic_search` — sémantické hledání relevantních zdrojů
- `zotero_search_items` — metadata (titul, autor, rok)
- `zotero_get_item_fulltext` — plný text pro ověření konkrétních faktů
- `zotero_get_item_metadata` — detailní metadata položky
- `zotero_search_by_citation_key` — hledání podle citation key
- `zotero_get_annotations` — anotace a highlights

**Response format when source found:**
- Explain the answer based on the retrieved content
- Cite as: *Název (Autoři, Rok)* — the user generates the BibLaTeX key themselves
- Provide the URL/DOI if available

**If no relevant result found in Zotero:**
Ask the user: *"Nenašel jsem odpověď v Zoteru. Chcete hledat na Google Scholar?"*

### Fallback: Local scripts (when MCP is unavailable)
If Zotero MCP is not available, use the local scripts as fallback:

**Metadata search:**
```bash
curl -s "http://localhost:23119/better-bibtex/json-rpc" \
  -X POST -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"item.search","params":["<query>"],"id":1}'
```

**Full-text attachment search:**
```bash
python3 tools/search_zotero_attachments.py "<query>" --context 3
```

### Fallback: Google Scholar
If the user agrees to search Google Scholar, run:
```bash
python3 tools/search_scholar.py "<query>" [--limit 5]
```
Remind the user to verify full-text access via SFX@VSE and add relevant sources to Zotero.
