# About the project
The goal of this thesis is to describe Indoor Environment Quality (IEQ), analyze existing open source applications collecting open data on IEQ, find requirements for the app and finaly to propose a solution and implement it.

# Available Skills & Orchestration

You have access to specialized skills located in the `@skills/` directory. You should act as an orchestrator and use these skills to fulfill user requests instead of running manual scripts or commands yourself.

## Two User Workflows

### Workflow A — Hledání informací (uživatel píše sám)
When the user wants to **find information** without automated text generation:
- Use **Zotero MCP tools** directly (`zotero_semantic_search`, `zotero_search_items`, `zotero_get_item_fulltext`) as the **primary source**
- If Zotero doesn't contain relevant results, ask: *„Nenašel jsem odpověď v Zoteru. Chcete hledat na Google Scholar?"*
- Only search Scholar with explicit user permission
- Present findings to the user; they write the text themselves

### Workflow B — Automatizované psaní textu (agent)
When the user wants AI to **write or rewrite academic text**:
- Delegate to the **`academic-text` agent** (claude-opus-4.6)
- The agent handles research, drafting, verification, and finalization autonomously
- Do NOT use this for simple information lookup

## Text Improvement & Review
When asked to review, correct, or improve text:
- **`spellcheck`:** Use this skill for spelling errors and typos
- **`suggestions`:** Use this skill for style, clarity, and academic tone improvements

## Research (deprecated skills — fallback only)
The following skills are **deprecated** and serve as fallback when Zotero MCP is unavailable:
- `research_router` — orchestrator for search workflow (use Zotero MCP directly instead)
- `search_zotero` — local Zotero search (use Zotero MCP instead)
- `search_scholar` — Google Scholar fallback (still usable as last resort with user permission)

## Research Logging
When sources are added during research or when asked to document the research process:
- **`log_research`:** Use this skill to record search steps and sources in `reserse.md`. This skill can also synchronize with the Zotero collection "Bakalářská práce" to document existing sources.

# AI Usage Logging

Dle požadavků VŠE musí být každé použití AI nástroje dokumentováno v příloze práce.

## Kdy logovat
**Loguje se:**
- Vyhledávání informací a literatury pro práci
- Generování nebo úprava textových částí
- Korektury (gramatika, styl, pravopis)
- Generování nebo úprava zdrojového kódu
- Generování dat

**Neloguje se:**
- Úpravy pravidel/instrukcí pro AI
- Testování nástrojů a ladění workflow
- Opravy chyb kompilace LaTeX
- Aktivity nesouvisející s obsahem práce

## Struktura logů
Logy jsou v LaTeX formátu v adresáři `ai-usage-log/`:

| Soubor | Kategorie |
|--------|-----------|
| `gramatika.tex` | Zlepšení gramatiky a jazykového stylu |
| `literatura.tex` | Vyhledávání a shrnutí literatury |
| `text.tex` | Úprava a rozšíření textových částí |
| `kod.tex` | Generování části zdrojových kódů |
| `data.tex` | Generování dat |
| `ostatni.tex` | Jiné použití (nezařaditelné) |

## Formát záznamu
Použij makro `\logentry{datum}{model}{soubory}{účel}{vstup}{výstup}{přínos}`:

```latex
\logentry
  {2026-03-30 14:00}
  {Claude Sonnet 4}
  {uvod.tex}
  {Stylistická korektura úvodní kapitoly}
  {Text kapitoly Úvod, žádost o kontrolu gramatiky}
  {Návrhy: oprava interpunkce, úprava slovosledu}
  {Přijaty 2 ze 3 návrhů, třetí ponechán původní}
```

## Workflow
1. **Sleduj provedené akce** během session (v paměti)
2. **Na vyžádání uživatele** (po dokončení úkolu):
   - Ověř, zda jsou změny stále platné (backtracking — zkontroluj, že uživatel změny nesmazal/nepřepsal)
   - Připrav záznam a zobraz náhled
   - Po potvrzení zapiš do příslušného `.tex` souboru v `ai-usage-log/`
3. **Pokud uživatel změny revertoval**, záznam nevytvářej nebo uprav dle skutečného stavu

## Výběr kategorie
- Vždy zvol nejvhodnější existující kategorii
- Pokud činnost spadá do více kategorií, zapiš do té primární
- `ostatni.tex` použij pouze pokud nelze zařadit jinam

# General Rules
- Always communicate your reasoning and findings in Czech unless explicitly asked otherwise.
- Strictly adhere to the output formats defined by the individual skills you invoke.
- Do not invent sources or facts.
