# Návrh obsahu kapitoly „Implementace aplikace“

Cíl: max. 10 stran včetně obrázků. Níže je navržená struktura (mírně upravená oproti draftu v `implementace.tex`), u každé sekce konkrétní obsah, argumentace a doporučené obrázky. Sekce označené ★ považuji za klíčové pro obhajobu (OFN/linked data, ingestion pipeline, temporální verzování), ty by měly dostat nejvíc prostoru.

---

## Poznámky ke struktuře draftu

Draft je v zásadě dobrý, navrhuji tři úpravy:

1. **Sloučit „Datová vrstva“ částečně do služeb.** Temporální verzování je implementačním srdcem Evidence.Api a hypertable srdcem ingestion pipeline — popsat je u příslušné služby drží text pohromadě a šetří stránky. V sekci o datové vrstvě nechat jen ER diagram + separaci schémat.
2. **Přidat samostatnou podsekci o OFN / linked datech** (draft ji nemá explicitně, jen zmiňuje DCAT). Pro obhajobu je to nejdůležitější část — doporučuji ~1,5 strany.
3. **Frontend zhustit na ~1 stranu** — backend je jádro práce.

Rozpočet stránek (orientačně): stack 1,5 · datová vrstva 2 (s ER) · backend služby 3,5 · OFN/linked data 1,5 · frontend 1 · škálovatelnost + závěr 0,5.

---

## 1. Vývojové prostředí a technologický stack (~1,5 str.)

Nepopisovat technologie encyklopedicky — u každé jedna až dvě věty *proč právě tato volba*. Návrh formulací:

**Backend — .NET 10, ASP.NET Core Minimal APIs, C#.** Staticky typovaný jazyk usnadňuje orientaci v datech, se kterými kód pracuje (důležité u systému s mnoha datovými kontrakty — DTO, doménový model, wire format fronty). Platforma je navržená „cloud-first“ s důrazem na výkon (odlišnost od JVM ekosystému); autorova dlouholetá zkušenost s C# (od .NET Framework 2018, certifikační kurzy) snižuje riziko implementace. Minimal APIs odstraňují ceremonii MVC kontrolerů — endpoint je funkce, což sedí k mikroslužbám s úzkým API.

**Persistence — PostgreSQL + TimescaleDB.** Relační integrita pro katalog + specializovaná time-series vrstva pro měření v jedné databázové technologii (detail v sekci 2). Rozšíření `btree_gist` pro temporální exkluzivní omezení.

**Fronta — Redis Streams.** Již v stacku jako cache; consumer groups, acky a replay dávají sémantiku „at-least-once“ bez zavádění dedikovaného brokeru (Kafka/RabbitMQ by byl pro rozsah práce overkill). Trvanlivost přes AOF `appendfsync always`.

**Reverzní proxy — Caddy.** Automatická správa TLS certifikátů a deklarativní konfigurace o řádech jednodušší než Apache2/nginx; jediný vstupní bod směruje na služby podle prefixu cesty.

**Kontejnerizace — Podman (Compose).** Bezdémonový, rootless běh kontejnerů (vyšší bezpečnost — na rozdíl od Dockeru neobchází firewall pravidla hostitele); OCI kompatibilita znamená, že tytéž obrazy lze později nasadit do Kubernetes. Compose profil `development` zvedne celý stack (Postgres, Redis, Caddy, Mailpit, 6 služeb, migrační kontejnery) jedním příkazem → shodnost prostředí mezi vývojáři a s produkcí.

**Frontend — TypeScript, React 19 + React Router 7, Vite, Chakra UI v3, D3.js, MapLibre GL, TanStack Query.** TypeScript = de facto standard, statické typy + generování typů z OpenAPI (openapi-typescript/openapi-fetch) → typově bezpečné volání backendu end-to-end. Chakra: hotový přístupný design systém — Bootstrap generický vzhled, Tailwind příliš nízkoúrovňový pro rozsah práce. D3 pro plnou kontrolu nad vizualizací časových řad.

**Dokumentace API — OpenAPI + Scalar.** Scalar jako moderní OpenAPI frontend s generováním SDK.

**Metodika — TDD + AI asistence.** Testy psané před kódem nutí promyslet hraniční scénáře; zároveň dávají AI asistentovi (Claude) ověřitelné kritérium správnosti — kombinace TDD + LLM se ukázala jako efektivní smyčka (vygeneruj → spusť testy → oprav). Stav: 7 testovacích projektů (xUnit) + Postman/Newman API suita (60 požadavků / 86 asercí) + Playwright E2E na frontendu. Zmínit jednou větou, detaily patří do kapitoly Testování.

> Obrázek: žádný, případně tabulka stack → role.

## 2. Datová vrstva a perzistence (~2 str. včetně ER diagramu) ★

**Tři izolované databáze v jedné instanci Postgres** (`auth`, `evidence`, `ieq`), každá vlastněná „svou“ službou přes dedikovanou DB roli (auth_api, evidence_api, ingestion_api rw / public_api ro / export_worker ro+insert). Zásadní rozhodnutí: **žádné cross-database cizí klíče** — identita uživatele cestuje v JWT claimu `sub` a Evidence.Api si ji líně projektuje do `user_projections`; měření odkazuje `sensor_id` na katalog jen logicky. Tím každá služba zůstává nezávisle nasaditelná a schéma migrovatelné bez koordinace (EF Core code-first migrace, každý kontext vlastní svou databázi, migrace běží v dedikovaných kontejnerech při startu).

**TimescaleDB hypertable `measurements`.** Partitiovaná podle `received_at`, kompozitní klíč `(id, received_at)`. Zdůvodnění: NFR ≥ 100 měření/s trvale a čtecí dotazy typu „časové okno × senzor × parametr“ — hypertable dělí data do chunků podle času, takže dotazy i retence pracují jen s relevantními oddíly; k dispozici funkce typu `time_bucket` pro agregace. Nemutabilita: měření se nikdy ne-UPDATE/DELETE, zneplatnění jen příznakem `is_invalid` + `invalidated_reason` (otevřená data nesmí tiše mizet).

**ER diagram** — doporučuji jeden souhrnný obrázek se třemi schématy a čárkovanými „soft“ vazbami přes hranice (JWT sub → user_projections; measurements.sensor_id ⇢ sensors). Podklad hotový: `docs/er/README.md` v backend repu obsahuje Mermaid erDiagramy všech tří schémat — stačí překreslit/exportovat. Pro úsporu místa zobrazit historické tabulky evidence agregovaně (jeden zástupný „<attr>_history“ vzor), ne všech 16 tabulek.

**Temporální verzování atributů (AS OF)** — vlajková loď datového modelu, doporučuji ~¾ strany:
- Budova/místnost/senzor jsou tenké agregátové kořeny; **každý atribut je proud historických řádků**, ne mutabilní sloupec. Řádek nese polootevřený UTC interval platnosti `tstzrange [valid_from, valid_to)` + auditní `recorded_at`/`recorded_by`.
- Změna = uzavření otevřeného řádku (UPDATE horní meze) + vložení nového (INSERT) v jedné transakci; nic se nepřepisuje → auditovatelný, nezměnitelný záznam vývoje katalogu, jak otevřená data vyžadují.
- Integritu vynucuje databáze: `btree_gist` **exkluzivní omezení** zakazuje překryv platností téhož atributu; je `DEFERRABLE INITIALLY DEFERRED`, protože EF může v transakci seřadit INSERT před UPDATE a kontrola smí proběhnout až při COMMIT. (Pěkný „technický problém a řešení“ moment pro text.)
- Čtení přijímá parametr `asOf` a rekonstruuje stav entity k libovolnému okamžiku (`validity @> asOf`).

> Obrázek: ER diagram (povinný) + případně malé schéma „timeline atributu“ (tři řádky historie s intervaly).

## 3. Realizace backendových služeb (~3,5 str.) ★

**Úvod sekce — architektura monorepa a separace zodpovědností (~½ str.).** Jedno řešení (`.slnx`), šest služeb + sdílená knihovna `Core` (EF kontext `IeqDbContext`, model měření, wire kontrakt fronty `MeasurementMessage`). Každá služba je samostatná bounded-context mikroslužba s DDD vrstvením `Api → Application → Domain ← Infrastructure` — adresářová struktura projektu přímo zrcadlí vrstvy, takže orientace v kódu je mechanická (motivace: autorova negativní zkušenost s orientací v monolitu; modulární služby s vlastním README výrazně snižují kognitivní zátěž). Komunikace standardizovaná: OpenAPI (Scalar UI) pro dokumentaci, **RFC 9457 ProblemDetails** pro jednotnou reprezentaci chyb napříč službami.

> Obrázek: komponentový diagram služeb (Caddy → Auth/Evidence/Ingestion.Api/Public.Api; Ingestion.Api → Redis → Worker → ieq; Export.Worker → S3). Pokud chcete class diagram, doporučuji jen jeden ukázkový — vrstvy Evidence.Api (aggregate root Sensor + historie + Validity value object); plné class diagramy všech služeb by sežraly stránkový rozpočet bez přidané hodnoty.

**3.1 Auth.Api (~¼ str. — stručně).** Registrace s e-mailovou verifikací (tokeny jednorázové, hashované), přihlášení s JWT access tokenem + rotovaným refresh tokenem, změna e-mailu/hesla. Bezpečnostní detail: brute-force se řeší throttlingem, ne zamykáním účtu (lockout = DoS vektor dle OWASP). Sdílený JWT secret → ostatní služby validují tokeny lokálně, bez volání Auth.

**3.2 Evidence.Api (~½ str.).** Katalog budov, místností a senzorů (F05–F09). Senzory = kanonický registr zařízení (žádná separátní `devices` tabulka); senzor autentizuje ingestion API klíčem (hash v DB). Zápisy vyžadují token, čtení anonymní. Adresy dle OFN *Adresy* — detail v sekci 4. Temporální model už popsán v sekci 2, zde jen odkázat.

**3.3 Ingestion pipeline (~1 str.) — technický vrchol.** 
- **Oddělení příjmu od zápisu:** Ingestion.Api přijme dávku čtení jednoho senzoru, synchronně validuje (API klíč + aktivní senzor; pro každé čtení: parametr deklarován, jednotka odpovídá kanonické v `parameter_ranges`, hodnota v rozsahu; dávka all-or-nothing), orazítkuje `received_at` (jediné čtení hodin pro celou dávku) a **atomicky** (MULTI/EXEC) zapíše do Redis streamu. Vrací **202 Accepted** — sémanticky přesné „přijato, ne zpracováno“. Databáze měření se v request cestě vůbec nedotkne.
- **Trvanlivost před ack:** NFR „žádný ack před trvalým zápisem“ je reinterpretován jako *durably enqueued before 2xx* — AOF `appendfsync always` = fsync na každý XADD; stream je write-ahead log, zápis do hypertable jeho materializace. Selhání enqueue → 503, nic se nepotvrdí.
- **Ingestion.Worker:** XREADGROUP po dávkách → hromadný insert (raw Npgsql) → XACK až po commitu řádku. Fronta je at-least-once; idempotenci zajišťuje `ON CONFLICT (id, received_at) DO NOTHING` (id generuje API při enqueue) → efekt exactly-once. `XAUTOCLAIM` přebírá pending záznamy po pádu konzumenta. `received_at` razí API *před* frontou, takže zpoždění drainu nikdy neposune zaznamenaný čas.

> Obrázek: sekvenční diagram senzor → API → Redis → Worker → TimescaleDB s vyznačenými 202/503 a ack body. Druhý kandidát na povinný obrázek vedle ER.

**3.4 Public.Api + Export.Worker (~¾ str.).**
- Public.Api: read-only otevřená data (F11–F16). Pozorování s filtrováním (senzor, parametr, časové okno), keyset stránkování, formáty **JSON / JSON-LD / CSV** přes HTTP content negotiation, OpenAPI spec, číselníky (codelisty) jako dereferencovatelné SKOS koncepty. DCAT-AP 3.0 katalog (detail v sekci 4).
- Export.Worker: měsíční archivy (CSV + JSON-LD, zip) do objektového úložiště kompatibilního s S3 (Simple Storage Service); záznam v `ieq.measurement_exports`, který Public.Api publikuje jako `dcat:Distribution` s `downloadURL`, `byteSize`, `mediaType` (F17). Splňuje požadavek OFN na hromadné stažení datasetu vedle API přístupu.

## 4. Konformita s OFN a linked data (~1,5 str.) ★★ (klíčové pro obhajobu)

Navrhuji samostatnou sekci (v draftu chybí). Obsah:

**IRI jako identifikátory.** Každý zdroj (budova, místnost, senzor, pozorování, vlastnost, číselníková položka) má absolutní, dereferencovatelnou IRI (Internationalized Resource Identifier) tvořenou `IriBuilder`em pod verzovaným kořenem `/v1`. Implementační detail hodný zmínky: báze IRI se řeší per-request s respektem k `X-Forwarded-*` hlavičkám, protože Caddy (`handle_path`) prefix cesty odstraňuje — bez toho by linked-data odkazy ukazovaly na interní adresy.

**Externí ontologie.** JSON-LD odpovědi mapují data na zavedené slovníky:
- **SOSA/SSN** (W3C Semantic Sensor Network): měření = `sosa:Observation` s `sosa:madeBySensor`, `sosa:observedProperty`, `sosa:hasSimpleResult`, `sosa:resultTime`, `sosa:hasFeatureOfInterest` (= místnost, odvozená z temporální historie umístění senzoru v čase měření); senzor = `sosa:Sensor` se `sosa:observes`.
- **QUDT** pro jednotky a druhy veličin (`qudt:unit`, `qudt:hasQuantityKind`, `qudt:applicableUnit`).
- **SKOS** pro vlastní číselníky (typ budovy, funkce místnosti, ventilace, expozice, status senzoru…): `skos:ConceptScheme`/`skos:Concept` s `skos:notation` a vazbami `skos:exactMatch`/`closeMatch` na externí slovníky.
- **DCAT-AP 3.0 / DCTERMS** pro katalog: `dcat:Catalog` → `dcat:Dataset` → `dcat:Distribution` (API endpoint i archivy), `dcterms:temporal`/`spatial` (bbox), `accrualPeriodicity`, `license`, `conformsTo`.

**Vlastní ontologie.** Pro pojmy bez vhodného externího protějšku (IEQ parametry, atributy místností) definuje aplikace vlastní slovník `ambiq:` — vlastnosti jsou samy dereferencovatelné (`/v1/properties/{code}` vrací `sosa:ObservableProperty` s QUDT vazbami), takže klient si význam pole „doklikne“.

**OFN Adresy + RÚIAN.** Adresa budovy dle OFN *Adresy* (2020-07-01): kanonickou kotvou je kód adresního místa RÚIAN (Registr územní identifikace, adres a nemovitostí), JSON-LD emituje IRI `linked.cuzk.cz/resource/ruian/adresni-misto/{kód}` + strukturované komponenty + složený text — celé preferenční pořadí normy (IRI → struktura → text). Územní prvky (obec, část obce, okres, kraj, ulice) se odkazují RÚIAN IRI, názvy jako jazykově označené literály `{"cs": …}`. (Poznámka pro vás: živá dereference linked.cuzk.cz už nefunguje — IRI slouží jako identifikátory; v textu formulovat jako „identifikátory dle normy, živá rezoluce mimo rozsah“.)

**Sémantika HTTP.** Správné status kódy nesoucí význam: 202 (přijato k asynchronnímu zpracování), 503 (trvanlivost nezaručena), 422 (validace), 401 (autentizace senzoru), ProblemDetails těla dle RFC 9457; content negotiation `Accept: application/ld+json` vs `application/json` vs `text/csv`; CSV doplněno CSVW metadaty (`observations.csv-metadata.json`).

## 5. Realizace webové aplikace (~1 str.)

Stručně, feature-first struktura:
- **Architektura:** SPA (single-page application), React 19 + React Router 7, adresáře `features/` (public-map, catalogue, entity-detail, evidence-admin, account, archive…) — kód organizovaný podle domén, ne podle technických vrstev (stejná motivace jako u backendu: orientovatelnost).
- **Typová bezpečnost end-to-end:** typy klienta generované z OpenAPI specifikace backendu (`openapi-typescript` + `openapi-fetch`) — kontrakt se nemůže rozjet tiše, rozbití se projeví při kompilaci.
- **Správa stavu:** TanStack Query — cache, invalidace, stránkování, retry; žádný globální state manager není potřeba, serverová data jsou jediný podstatný stav.
- **Vizualizace:** MapLibre GL (interaktivní mapa budov, F18) + D3.js (grafy časových řad parametrů — plná kontrola nad osami, brush výběrem okna apod.).
- **Internacionalizace:** i18next, čeština + angličtina, detekce jazyka prohlížeče.
- **Testy:** Vitest + Testing Library + MSW (mock API), Playwright E2E včetně axe-core přístupnostních kontrol — jedna věta, zbytek do kapitoly Testování.

> Obrázek: 1 screenshot (mapa nebo detail místnosti s grafem) — víc ne, ať se vejde rozpočet.

## 6. Škálovatelnost a závěr (~½ str.)

Krátká syntéza, jak architektura plní NFR:
- **Horizontální škálování čtení a zápisu odděleně:** read-heavy Public.Api a write-heavy ingestion jsou samostatné služby; bezstavové API se škálují přidáním replik za Caddy.
- **Tlumení špiček:** Redis stream odděluje rychlost příjmu od rychlosti zápisu — nápor senzorů nezpomalí HTTP odpovědi; worker škáluje konzumenty v rámci consumer group (každý zpracovává jiné záznamy) a propustnost zvyšuje dávkový bulk-insert.
- **Datová vrstva:** hypertable chunking drží dotazy lokální v čase; read-only DB role umožňují později čtecí repliky; Redis dostupný i jako cache vrstva.
- **Provoz:** kontejnery (Podman/OCI) → přímá cesta ke Kubernetes při růstu.

Závěrečný odstavec: systém implementuje F01–F17 a je připraven k ověření (→ kapitola Testování).

---

## Souhrn doporučených obrázků (4, vejde se do 10 stran)

1. **ER diagram** tří schémat se „soft“ hranicemi (podklad `docs/er/README.md`) — povinný.
2. **Komponentový diagram** služeb + infrastruktury (Caddy, Redis, Postgres, S3).
3. **Sekvenční diagram ingestion pipeline** (202/503, ack sémantika).
4. **Screenshot frontendu** (mapa/graf).

Volitelně 5. mini-diagram temporálních intervalů, pokud zbyde místo. Class diagramy doporučuji vynechat nebo nahradit jediným výřezem Evidence domény — komponentový + sekvenční + ER pokryjí argumentaci lépe na menší ploše.
