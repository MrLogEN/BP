---
name: search_scholar
description: Search for academic sources on Google Scholar when no relevant results are found in Zotero. Use only after explicit user confirmation.
---

## Purpose

This skill retrieves academic sources from Google Scholar as a fallback when Zotero does not contain relevant materials.

## When to use

- Only after Zotero search fails
- Only if the user explicitly agrees to search Google Scholar

## Query Handling

- Accept refined academic queries from `research_router`
- Do not modify queries further

## Workflow

Run:
```bash
python3 tools/search_scholar.py "<query>" --limit 5
```

## Output format

Present results in structured form:
```md
1. Název: ...
   Autoři: ...
   Rok: ...
   Zdroj: ...
   Abstrakt: zkrácený
   URL: ...
```
## After presenting results
Always add:

Ověřte dostupnost plného textu přes SFX@VSE a přidejte relevantní zdroje do Zotera.

## Limitations
Google Scholar scraping may fail due to CAPTCHA
If blocked, inform the user and suggest manual search
Full-text access is not guaranteed

## Rules
- All outputs must be in Czech
- Do not use this skill without user consent
- Do not invent publications
- Prefer highly relevant sources
- Avoid duplicates
- Keep summaries concise
- Clearly separate individual results
