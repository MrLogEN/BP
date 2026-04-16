---
name: search_zotero
description: "⚠️ DEPRECATED — Primární cesta je Zotero MCP (zotero_semantic_search, zotero_search_items, zotero_get_item_fulltext). Tento skill slouží pouze jako fallback."
---

> **⚠️ DEPRECATED:** Pokud jsou dostupné Zotero MCP nástroje, použij je přímo. Tento skill je fallback pro situace, kdy MCP není dostupný.

## Purpose

This skill retrieves information from the local Zotero library as a **fallback** when Zotero MCP is not available.

## Query Handling

- Accept multiple generated queries
- Run searches for each query variation
- Merge and deduplicate results
- Prioritize:
  1. full-text matches
  2. strong metadata matches

## Workflow

### Step 1 — Metadata search (mandatory)

Search Zotero metadata (title, abstract, keywords):
```bash
curl -s "http://localhost:23119/better-bibtex/json-rpc
"
-X POST -H "Content-Type: application/json"
-d '{"jsonrpc":"2.0","method":"item.search","params":["<query>"],"id":1}'
```

### Step 2 — Full-text attachment search (mandatory)

Always run after metadata search:
```bash
python3 tools/search_zotero_attachments.py "<query>" --context 3
```
Searches local attachments in ~/Zotero/storage/ (PDF, DOCX, HTML, TXT).

If a Zotero MCP server is configured in Copilot CLI, use its search and full-text tools instead of the local script. Prefer the MCP path because it can query Zotero directly, while the script is only a local fallback.

## How to use results
- Combine metadata and full-text results
- Prefer full-text evidence when available
- Extract relevant facts, definitions, or explanations
- Do not copy long excerpts; summarize instead

## Output format

If relevant sources are found:

- Provide a clear answer based on the retrieved content
- Cite sources in this format:
- Název (Autoři, Rok)
- Include URL or DOI if available

If no relevant result is found in both metadata and attachment search, clearly state that the answer was not found in the local Zotero library.

## Rules
- Zotero is the only source of truth for thesis-related queries
- Always perform BOTH metadata and full-text search
- Never skip the attachment search
- Do not invent sources or citations
- Do not use external sources unless explicitly allowed
- Prefer sources with full-text matches over metadata-only matches
- Keep answers concise and fact-based
- If a source is weakly relevant, state uncertainty
