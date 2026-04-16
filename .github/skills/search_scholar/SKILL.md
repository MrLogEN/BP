---
name: search_scholar
description: "⚠️ DEPRECATED — Používej pouze jako poslední fallback, když Zotero MCP neobsahuje relevantní zdroje a uživatel explicitně souhlasí."
---

> **⚠️ DEPRECATED:** Tento skill je fallback pro situace, kdy Zotero neobsahuje relevantní zdroje. Vždy nejdřív prohledej Zotero přes MCP.

## Purpose

This skill retrieves academic sources from Google Scholar as a **last-resort fallback**.

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

## Logging to reserse.md

After presenting results and if the user decides to add sources to Zotero:
- Use the `log_research` skill to record the search in `reserse.md`
- Include the actual search query/keywords used
- Record which sources were selected for further review

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
