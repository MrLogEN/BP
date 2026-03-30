---
name: log_research
description: Zaznamenává kroky rešerše do reserse.md. Používá se po přidání zdrojů přes Scholar nebo pro synchronizaci existujících zdrojů ze Zotera.
---

## Účel

Tento skill zajišťuje systematické zaznamenávání postupu rešerše do souboru `reserse.md`. Každý zdroj přidaný během rešerše musí být zdokumentován, aby bylo možné sledovat celý proces hledání informací.

---

## Kdy použít

1. **Po přidání zdroje přes Scholar** — zaznamenat nově nalezený zdroj
2. **Po přidání zdroje do Zotera uživatelem** — zaznamenat zdroj s odhadem postupu
3. **Synchronizace se Zotero kolekcí** — jednorázový průchod existujících zdrojů

---

## Formát záznamu

Každý zdroj se zapisuje do `reserse.md` v následujícím formátu:

```markdown
## [Název zdroje]
- **Autor(ři):** [jména autorů]
- **Rok:** [rok vydání]
- **URL/DOI:** [odkaz, pokud je k dispozici]
- **Zdroj vyhledání:** [Scholar / Zotero / ProQuest / IEEE / DuckDuckGo / knihovna / ChatGPT / jiné]
- **Klíčová slova:** [použité dotazy pro hledání]
- **Relevance:** [krátký popis obsahu a relevance pro téma práce]
- **Poznámka:** [volitelné poznámky]
```

---

## Označení odhadů agenta

Pokud agent **neví přesný postup hledání** (např. zdroj byl přidán uživatelem bez záznamu), musí jasně označit odhadnuté informace:

```markdown
- **Klíčová slova:** `[ODHAD AGENTA]` "indoor air quality" OR "IAQ guidelines"
```

Toto označení umožňuje autorovi provést manuální kontrolu a cleanup.

---

## Workflow: Záznam nového zdroje

### Krok 1 — Získat metadata

Z výsledků hledání (Scholar, Zotero) extrahovat:
- Název
- Autor(ři)
- Rok
- URL/DOI
- Abstrakt (pro popis relevance)

### Krok 2 — Určit klíčová slova

- Pokud byl zdroj nalezen hledáním: použít skutečná klíčová slova
- Pokud byl zdroj přidán uživatelem: odhadnout klíčová slova z titulku/abstraktu a označit `[ODHAD AGENTA]`

### Krok 3 — Zapsat do reserse.md

Přidat záznam na konec souboru `reserse.md` ve správném formátu.

---

## Workflow: Synchronizace se Zotero

Tento postup slouží k jednorázovému doplnění záznamů o zdrojích, které jsou v Zotero kolekci "Bakalářská práce" (key: `E3Y8285B`), ale nejsou v `reserse.md`.

### Krok 1 — Načíst existující záznamy

Přečíst `reserse.md` a extrahovat seznam již zaznamenaných zdrojů (podle názvů).

### Krok 2 — Načíst položky z Zotera

Použít Zotero MCP nebo API pro získání položek z kolekce:
- Collection key: `E3Y8285B`
- Filtrovat pouze hlavní položky (ne attachmenty)

### Krok 3 — Porovnat a identifikovat chybějící

Pro každou položku v Zoteru zkontrolovat, zda již existuje v `reserse.md`.

### Krok 4 — Doplnit chybějící záznamy

Pro každý chybějící zdroj:
1. Získat metadata ze Zotera
2. Odhadnout možná klíčová slova z titulku a abstraktu
3. Označit odhad: `[ODHAD AGENTA]`
4. Zapsat do `reserse.md`

### Krok 5 — Informovat uživatele

Po dokončení synchronizace informovat uživatele:
- Kolik zdrojů bylo přidáno
- Které zdroje vyžadují manuální kontrolu (všechny s `[ODHAD AGENTA]`)

---

## Rekonstrukce klíčových slov

Při odhadu klíčových slov z titulku a abstraktu:

1. **Extrahovat hlavní pojmy** — substantiva, odborné termíny
2. **Identifikovat zkratky** — IEQ, IAQ, CO2, PM2.5, atd.
3. **Kombinovat do vyhledávacích frází** — použít Boolean operátory (AND, OR)
4. **Zohlednit kontext práce** — Indoor Environment Quality, open data, open source

Příklad:
- Titulek: "Indoor Environmental Quality in Schools: NOTECH Solution vs. Standard Solution"
- Abstrakt: mentions IEQ, schools, temperature, ventilation
- Odhad: `[ODHAD AGENTA]` "indoor environmental quality schools" OR "IEQ NOTECH solution"

---

## Pravidla

- Všechny záznamy musí být v češtině (kromě názvů a citací v originálním jazyce)
- Nikdy nevynechávat označení `[ODHAD AGENTA]` u rekonstruovaných informací
- Neměnit existující záznamy v `reserse.md` bez výslovného pokynu
- Zachovat chronologické pořadí (nové záznamy na konec)
- Neopakovat záznamy, které již v souboru existují

---

## Omezení

- Tento skill nemůže přidávat zdroje do Zotera
- Nemůže ověřit, zda zdroj byl skutečně použit v práci
- Odhady klíčových slov jsou pouze aproximací — vyžadují kontrolu autora
