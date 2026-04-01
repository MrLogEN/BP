# About the project
The goal of this thesis is to describe Indoor Environment Quality (IEQ), analyze existing open source applications collecting open data on IEQ, find requirements for the app and finaly to propose a solution and implement it.

# Available Skills & Orchestration

You have access to specialized skills located in the `@skills/` directory. You should act as an orchestrator and use these skills to fulfill user requests instead of running manual scripts or commands yourself.

## Text Improvement & Review
When asked to review, correct, or improve text:
- **`spellcheck`:** Use this skill first to identify and correct basic spelling and typographical errors.
- **`suggestions`:** Use this skill for deeper grammatical, stylistic, and clarity improvements to maintain an academic tone.

## Academic Research & Sourcing
When asked to find information, facts, or sources for the thesis:
- **`research_router`:** Use this skill exclusively. It acts as an orchestrator that will automatically query the local Zotero library (`search_zotero`) and, if necessary and permitted by the user, expand the search to Google Scholar (`search_scholar`).

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
