# CLAUDE.md — pozadavky/

Tato složka obsahuje požadavky na systém strukturované podle metodiky **FURPS+** v rámci metodiky **MMSP** (adaptace OpenUP pro Fakultu informatiky a statistiky VŠE). Každý soubor odpovídá jedné kategorii FURPS+.

## Struktura složky

```
pozadavky/
├── funkcni.tex            # Funkční požadavky (F)
├── nefunkcni/
│   ├── vykon.tex          # Výkon (VYK) — součást Reliability v FURPS+
│   ├── spolehlivost.tex   # Spolehlivost (SPO)
│   ├── pouzitelnost.tex   # Použitelnost (POU) + Podpora (POD)
│   └── podpora.tex        # (obsah sloučen do pouzitelnost.tex)
├── rozhrani/
│   ├── externi.tex        # Rozhraní na external systémy (EXT)
│   └── uzivatelske/
│       ├── rozlozeni.tex  # Rozložení a navigace (ROZ)
│       ├── konzistence.tex# Konzistence (KON)
│       ├── personalizace.tex # Personalizace (PER)
│       └── vzhled.tex     # Vzhled (VZH)
├── dokumentace.tex        # Požadavky na dokumentaci (DOK)
└── standardy.tex          # Standardy (STA) + Systémová omezení (SYS)
```

## LaTeX makra

### Funkční požadavky (`funkcni.tex`)

```latex
\begin{FunkcniTabulka}
  \FunkcniPozadavekRow{Název}{Popis požadavku.}{priorita}{UCXX}
\end{FunkcniTabulka}
```

- `priorita`: číslo 1–5 (1 = vysoká, 5 = nízká)
- `UCXX`: odkaz na případ užití (UC01–UC18)
- Identifikátory funkčních požadavků jsou automaticky číslovány jako F01, F02, …

### Nefunkční a ostatní požadavky (všechny ostatní soubory)

```latex
\begin{OstatniPozadavkyTabulka}{PREFIX}{Název kategorie}
  \OstatniPozadavekRow{Název}{Popis požadavku.}{priorita}
\end{OstatniPozadavkyTabulka}
```

- `PREFIX`: třípísmenný prefix kategorie (viz níže), použitý v ID požadavku (např. `VYK-01`)
- `priorita`: 1–5

## Prefixy identifikátorů

| Prefix | Kategorie | Soubor |
|--------|-----------|--------|
| F | Funkční požadavky | `funkcni.tex` |
| VYK | Výkon | `nefunkcni/vykon.tex` |
| SPO | Spolehlivost | `nefunkcni/spolehlivost.tex` |
| POU | Použitelnost | `nefunkcni/pouzitelnost.tex` |
| POD | Podpora | `nefunkcni/pouzitelnost.tex` |
| DOK | Dokumentace | `dokumentace.tex` |
| STA | Standardy | `standardy.tex` |
| SYS | Systémová omezení | `standardy.tex` |
| EXT | Rozhraní na external systémy | `rozhrani/externi.tex` |
| ROZ | Rozložení a navigace | `rozhrani/uzivatelske/rozlozeni.tex` |
| KON | Konzistence | `rozhrani/uzivatelske/konzistence.tex` |
| PER | Personalizace | `rozhrani/uzivatelske/personalizace.tex` |
| VZH | Vzhled | `rozhrani/uzivatelske/vzhled.tex` |

## Vztah k případům užití

Funkční požadavky (F01–F18) jsou navázány na případy užití UC01–UC18 přes čtvrtý parametr `\FunkcniPozadavekRow`. Vazba je **1:1** — každý funkční požadavek odkazuje na právě jeden případ užití a naopak.

Případy užití jsou definovány ve složce `usecase/` (sourozeneč složky `pozadavky/`):
- `usecase/usecase.tex` — diagram a seznam UC
- `usecase/akteri.tex` — definice aktérů
- `usecase/cases/uc01.tex` … `uc18.tex` — specifikace jednotlivých UC pomocí makra `\begin{UseCaseTable}…\end{UseCaseTable}`

Při přidání nového funkčního požadavku je nutné přidat i odpovídající případ užití v `usecase/cases/` a aktualizovat odkaz v diagramu v `usecase/usecase.tex`.

## Aktéři systému

Systém definuje tyto aktéry (viz `usecase/akteri.tex`):

| Aktér | Popis |
|-------|-------|
| Provozovatel monitorovaného prostoru | Registruje budovy, místnosti, senzory a publikuje měření |
| Vývojář aplikací třetí strany | Konzumuje veřejné čtecí API strojově |
| Výzkumný pracovník | Stahuje archivní datové sady |
| Senzor | Strojový aktér odesílající pozorování |
| Datový katalog | Strojový aktér harvestující DCAT-AP metadata |
| Návštěvník | Anonymní uživatel veřejného webového rozhraní |

## Pravidla při úpravách

1. **Priorita**: Používej jen hodnoty 1–5; nekombinuj s textovými popisy.
2. **Jazyk**: Veškerý obsah je v češtině. Anglické termíny (zkratky, standardy) se uvádějí v závorce nebo kurzívou.
3. **Citace**: Popisy kategorií citují metodiku přes `\parencite{rejnkovaLokalizacePrizpusobeniMetodiky}`. Zachovej tento vzor u každého nadpisu sekce/podsekce.
4. **Nové požadavky**: Přidávej jako nový `\FunkcniPozadavekRow` nebo `\OstatniPozadavekRow` na konec příslušné tabulky — ID se číslují automaticky.
5. **Koherence F↔UC**: Každý nový funkční požadavek musí mít odpovídající UC v `usecase/cases/`.
