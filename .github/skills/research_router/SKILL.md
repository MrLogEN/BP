---
name: research_router
description: "⚠️ DEPRECATED — Primární cesta je Zotero MCP. Tento skill slouží pouze jako fallback, pokud MCP není dostupný."
---

> **⚠️ DEPRECATED:** Pokud jsou dostupné Zotero MCP nástroje (`zotero_semantic_search`, `zotero_search_items`, `zotero_get_item_fulltext`), použij je přímo. Tento skill je fallback pro situace, kdy MCP není dostupný.

## Purpose

This skill handles the academic research workflow as a **fallback** when Zotero MCP is not available.
- transforms user queries into search queries
- searches Zotero as the primary source
- optionally expands to Google Scholar (with permission)

Zotero is the primary and authoritative source.

---

## Language Rules

- All communication with the user must be in Czech
- Generated search queries may be in English for better academic coverage
- Citations remain in original language

---

## Workflow

### Step 0 — Query Transformation (CRITICAL)

Transform the user query into 2–5 academic search queries.

Guidelines:
- Extract core concepts
- Convert natural language questions into search phrases
- Generate:
  - direct keyword query
  - domain-specific variation
  - synonym-based variation
- Prefer English queries unless Czech is clearly better

Examples:

User: "Co znamená H2O?"
→
- "H2O definition"
- "chemical composition of water"
- "what is H2O molecule"

User: "distributed consensus algorithms"
→
- "distributed consensus algorithms overview"
- "Paxos Raft consensus comparison"
- "fault tolerant distributed systems consensus"

---

### Step 1 — Local Search (MANDATORY)

Invoke `search_zotero` using the generated queries.

- Always perform BOTH:
  - metadata search
  - full-text attachment search

---

### Step 2 — Evaluate Results

If relevant results are found:
- extract key information
- prioritize full-text matches
- answer the user’s query
- include citations

---

### Step 3 — Fallback Permission

If no relevant results are found:

Ask the user:

"Nenašel jsem odpověď v Zoteru. Chcete hledat na Google Scholar?"

STOP and wait for user response.

---

### Step 4 — External Search (Fallback)

If the user explicitly agrees:
- invoke `search_scholar`
- present results in structured format

---

## Rules

- NEVER skip Zotero
- ALWAYS generate search queries internally
- NEVER require user to provide keywords
- NEVER call `search_scholar` without permission
- NEVER invent sources
- ALWAYS prefer full-text evidence
- ALWAYS keep responses concise and factual

---

## Output Format (Zotero results)

- Jasná odpověď na dotaz
- Citace:

Název (Autoři, Rok)  
URL / DOI (pokud existuje)

---

## Output Format (Scholar fallback)

```md
1. Název: ...
   Autoři: ...
   Rok: ...
   Zdroj: ...
   Abstrakt: zkrácený
   URL: ...
```

After results always add:
```md
Ověřte dostupnost plného textu přes SFX@VSE a přidejte relevantní zdroje do Zotera.
```
