# Plan: Brownfield-Migration box-python v0.2.3 → v0.2.7

Status: abgeschlossen
Datum: 2026-06-21
Bearbeiter: Dieter Haag

## Aufgabe

Die Agenten-Box dieses Projekts wurde am 2026-06-20 mit box-python v0.2.3 instanziiert.
Die neue Template-Version ist v0.2.7 (Quelle: `tmp/brownfield/agent-templates-main/box-python/`).

Brownfield-Fall B: bestehendes instanziiertes Box-Projekt auf neue Box-Version migrieren.
Herkunftsmarker: `.agent-box/instantiation.md` (genau einer vorhanden, kein `adoption.md`).

Ziel: Regeldokumente und Tools auf v0.2.7 nachziehen, ohne lokale operative Wahrheit durch
Template-Defaults zu ersetzen. Kein Produktionscode wird geändert.

## Leitprinzip (vom Menschen festgelegt)

```text
Nicht ersetzen, sondern sinnvoll mergen — ausnahmslos, auch bei Tools.
Große Diffs sind zuerst Befund (oft lokaler Projektinhalt), nicht Freigabe zum Überschreiben.
Template-Neuerung ist nicht automatisch lokale operative Wahrheit.
```

## Brownfield-Preflight

```text
Projektpfad:           /home/dieter/repos/regenbogen
Brownfield-Fall:       B
Ausgangsversion:       v0.2.3
Zielversion:           v0.2.7
Herkunftsmarker:       .agent-box/instantiation.md (vorhanden)
adoption.md vorhanden: nein
Genau ein Marker:      ja
.agent-box/migrations: fehlt (wird angelegt)
Bekannte rote Checks:  unbekannt — in Phase 1 Baseline erheben
Bekannte Known Breaches: keine (package-schema.md prüfen)
Migration Bridges:     migration-bridges.md prüfen
Lokale Tool-Anpassungen: JA (git: 495dd0b, b2a2b5b, 7e3e96f berührten tools/) → merge zwingend
```

## Betroffene Räume

Ausschließlich Agenten-Box-Artefakte (Regeldokumente, Glossare, Tools).
Kein Produktionscode unter `src/`, keine Tests unter `tests/`.

## Nicht-Ziele

- Produktionscode, Tests oder pyproject.toml ändern
- Re-Instanziierung oder globales Search/Replace
- Pauschale Dateiersetzung ohne Diff (auch nicht bei Tools)
- Known Breaches aus der Inventur erzeugen
- Lokal gefüllte Glossar-/Learning-Inhalte durch leere Template-Stände überschreiben

## Schreibrechte

Alle betroffenen Dateien sind geschützte Dateien (AGENTS.md Abschnitt 9).
Dieser Plan ist die explizite Freigabe für genau die in der Aktionsmatrix gelisteten Dateien.
Alle anderen geschützten Dateien bleiben gesperrt.

## Inhaltliche Änderungen v0.2.3 → v0.2.7 (Changelog-Zusammenfassung)

```text
v0.2.4  glossar-meta.md eingeführt (Metabegriffe aus glossar-system.md getrennt)
v0.2.5  BROWNFIELD-MIGRATION.md und .agent-box/migrations/ eingeführt
v0.2.6  Brownfield-Modell geschärft: Hochrisikozone scope-basiert, Known-Breach-Format,
        adoption.md, BF-Abbruch-Evidence, Pipeline Discover/Describe/…/Verify, BF-Metabegriffe
v0.2.7  Fast-Path P1+P4+P6+P7+P8 (statt P1+P7+P8), 8 explizite Bedingungen, P8 entfällt nie
        SP7/T1: "nicht ausreichend tief" statt "fehlt oder unvollständig" (Eintragstiefe-Modell)
        H10: konkrete Auslösekriterien ergänzt
        migration-bridges.md: H3 ersetzt H2 für Bridge-Diff-Verletzungen
        Learning-Matrix: Muster-Schwelle in Abschnitt 1a normiert
        glossar-meta.md: Ladebegrenzung bei normaler Facharbeit
```

## Befund-Inventur (Diff-Analyse, deskriptiv)

Diff-Zeilen lokal↔Template und ihre Deutung. Große Diffs sind hier überwiegend
**lokaler Projektinhalt**, nicht nachzuziehende Template-Änderung:

| Datei | Diff | lokal/templ. Zeilen | Deutung |
| --- | --- | --- | --- |
| `glossar-domain.md` | 217 | 310 / 147 | Mit echten Wetter-Fachbegriffen gefüllt → **preserve-dominant** |
| `glossar-system.md` | 144 | 223 / 147 | Gefüllt → **preserve-dominant** |
| `learning-matrix.md` | 255 | 346 / 151 | Mit echten Mustern gefüllt → **preserve-dominant** |
| `glossar-meta.md` | 270 | 141 / 323 | Handgemacht (commit c307ebf), abweichende Struktur, **BF-Begriffe fehlen** → echter merge |
| `AGENTS-COMPACT.md` | 85 | — | Template-Evolution + Platzhalterersetzung |
| `package-schema.md` | 62 | — | Known-Breach-Format + Platzhalter |
| `glossar-README.md` | 65 | — | Eintragstiefe / P5 |
| `migration-bridges.md` | 53 | — | H3 statt H2, Platzhalter |
| `test-obligations.md` | 36 | — | Template-Evolution |
| `regelmatrix.md` | 19 | — | Template-Evolution |
| `sprechakt-protokoll.md` | 10 | — | SP7 Eintragstiefe |
| `erfahrungsbericht-protokoll.md` | 6 | — | klein |
| `task-schnitt.md` | 5 | — | T1 Eintragstiefe |
| `grundsatz.md` | 0 | — | identisch, **kein Handlungsbedarf** |
| `check_agent_docs_consistency.py` | 745 | — | Template-Evolution; lokal NICHT in git berührt → trotzdem diffen |
| `resolve_test_obligations.py` | 408 | — | Lokal angepasst (git) → **merge** |
| `check_import_layers.py` | 378 | — | Lokal angepasst (git) → **merge** |

Hinweis Strukturanomalie: Lokales `glossar-meta.md` nutzt `## 2. Begriffe`; der v0.2.7-Checker
verlangt Einträge unter `## 3. Begriffe`. `glossar-domain.md`/`glossar-system.md` nutzen bereits
`## 3. Begriffe` (template-kompatibel).

## Datei-Aktionsmatrix

### add — fehlen im Repo, direkt aus Template übernehmen

| Datei | Begründung |
| --- | --- |
| `BROWNFIELD-MIGRATION.md` | Neu seit v0.2.5, fehlt komplett. Platzhalter beim Kopieren ersetzen. |
| `.agent-box/migrations/` | Verzeichnis neu seit v0.2.5 |
| `.agent-box/migrations/2026-06-21-v0.2.3-to-v0.2.7-migration.md` | Pflicht-Evidence (Verfahren B) |

### merge — Regeldokumente: Template-Neuerung einarbeiten, lokale Wahrheit + Platzhalterersetzung erhalten

| Datei | Konkret nachzuziehen |
| --- | --- |
| `AGENTS.md` | Abschn. 3 Glossar-Trennung domain/system/**meta**; SP7/T1 Eintragstiefe-Wortlaut; SICHER: Importverletzung-Klassifizierung; Brownfield-Verweis. **MODELL-README-Block** (lokal vorhanden) bewahren. |
| `AGENTS-COMPACT.md` | Synchron zu AGENTS.md |
| `preflight-checkliste.md` | Fast-Path P1+P4+P6+P7+P8, 8 Bedingungen, P8 entfällt nie, SICHER-Verweis auf AGENTS.md §6 |
| `sprechakt-protokoll.md` | SP7 "nicht ausreichend tief" |
| `task-schnitt.md` | T1 "nicht ausreichend tief" |
| `glossar-README.md` | Eintragstiefe-Modell in P5 |
| `migration-bridges.md` | H3 ersetzt H2/BF12; Beispiel-Bridge-Stand prüfen |
| `package-schema.md` | Known-Breach-Format (Scope, No-growth, Review/Ablauf, Freigabe); lokale Raumkarte bewahren |
| `regelmatrix.md` | Template-Evolution v0.2.4–v0.2.7 |
| `test-obligations.md` | Template-Evolution v0.2.4–v0.2.7 |
| `erfahrungsbericht-protokoll.md` | Kleine Template-Evolution |

### merge — preserve-dominant: lokalen Inhalt bewahren, nur Strukturmodell behutsam ergänzen

| Datei | Konkret |
| --- | --- |
| `glossar-domain.md` | Echte Begriffe **bewahren**. Nur Eintragstiefe-Modell (minimal/vollständig) ergänzen, falls ohne Konflikt. |
| `glossar-system.md` | Wie glossar-domain.md |
| `learning-matrix.md` | Echte Muster **bewahren**. Nur Muster-Schwelle Abschn. 1a strukturell nachziehen. |
| `glossar-meta.md` | Struktur auf `## 3. Begriffe` angleichen (Checker-Pflicht); **fehlende BF-Metabegriffe ergänzen** (Observed State, Accepted Local Truth/Alternative, Migration Candidate, Legacy Defect, Baseline, Zielmodell, Migrationsevidence, Datei-Aktionsklasse, BF-Code); lokale Begriffe + Wortlaut bewahren. |

### merge — Tools: erst diffen, Template-Logik einarbeiten, lokale Anpassungen erhalten

| Datei | Hinweis |
| --- | --- |
| `tools/check_import_layers.py` | Lokal in git angepasst → semantisch mergen, `LAYER_BY_PACKAGE_PART` lokal halten |
| `tools/resolve_test_obligations.py` | Lokal in git angepasst → semantisch mergen, `TEST_COMMANDS` lokal halten |
| `tools/check_agent_docs_consistency.py` | Lokal nicht in git berührt, aber Diff prüfen; muss lokale Glossarstruktur akzeptieren |

### preserve — nicht ändern

| Datei | Begründung |
| --- | --- |
| `README.md` | Gehört dem Zielprojekt |
| `docs/agent-box-instantiation.md` | Bereits verschobenes AGENT-SETUP.md |
| `MODELL-README.md` | Lokales Projektartefakt |

### forbidden — nicht anfassen

| Datei | Begründung |
| --- | --- |
| `.agent-box/instantiation.md` | Greenfield-Evidence, unveränderbar |
| `tools/instantiate/*` | Kein Brownfield-Werkzeug |

---

## Phase 1 — Feature-Branch (zuerst)

```text
1.1  Sauberen Arbeitszustand sichern (git status; ggf. LICENSE separat behandeln).
1.2  Branch anlegen:
       git checkout -b brownfield/v0.2.3-to-v0.2.7
1.3  Baseline VOR jeder Änderung erheben und festhalten:
       python tools/check_agent_docs_consistency.py --instantiated
       python tools/check_import_layers.py --preflight src tests tools
       python tools/resolve_test_obligations.py --selfcheck --instantiated
       python -m pytest
     Ergebnis (grün/rot je Check) in die Migrations-Evidence schreiben.
     Rote Checks hier = dokumentierter Ausgangszustand, kein Migrationsfehler.
1.4  .agent-box/migrations/ anlegen.
1.5  Migrations-Evidence-Datei anlegen (Status: offen) nach Minimalformat
     aus BROWNFIELD-MIGRATION.md Abschnitt 10.
```

## Phase 2 — Update (die Migration)

```text
2.1  add: BROWNFIELD-MIGRATION.md aus Template kopieren, Platzhalter ersetzen
       (Regenbogen / regenbogen / src / tests / docs / tools + Befehle).
2.2  merge Regeldokumente, Reihenfolge nach Risiko/Abhängigkeit:
       preflight-checkliste.md → AGENTS.md → AGENTS-COMPACT.md
       → sprechakt-protokoll.md → task-schnitt.md → regelmatrix.md
       → test-obligations.md → package-schema.md → migration-bridges.md
       → glossar-README.md → erfahrungsbericht-protokoll.md
     Pro Datei: Template-Diff lesen, nur Template-Neuerung übernehmen,
     lokale Platzhalterersetzung und lokale Inhalte erhalten.
2.3  merge preserve-dominant:
       glossar-domain.md, glossar-system.md  (nur Eintragstiefe-Modell)
       learning-matrix.md                    (nur Muster-Schwelle 1a)
       glossar-meta.md                        (Struktur ## 3. Begriffe + BF-Begriffe)
2.4  merge Tools:
       check_import_layers.py, resolve_test_obligations.py,
       check_agent_docs_consistency.py
     Pro Tool: Diff lesen, Template-Logik einarbeiten, lokale Config/Anpassung halten.
2.5  Dokumentdrift-Abgleich (AGENTS.md §17): Compact, preflight, package-schema,
     regelmatrix, Checker-LAYER_BY_PACKAGE_PART gegeneinander prüfen.
2.6  Migrations-Evidence fortschreiben: übernommene/bewusst nicht übernommene
     Änderungen, menschliche Entscheidungen, offene Befunde.
```

Entscheidungspunkte, die menschliche Festlegung brauchen (sonst BF12/BF7-Abbruch):

```text
- glossar-meta.md: nur Heading umbenennen (Checker-Minimum) ODER volle BF-Begriffe ergänzen?
- glossar-domain/system: Eintragstiefe-Modell jetzt übernehmen oder zurückstellen?
- Tool-Konflikt: falls Template-Logik mit lokaler Anpassung kollidiert → STOPP, vorlegen.
```

## Phase 3 — Gründliche Validierung

```text
3.1  Abschlusschecks im instanziierten Modus:
       python tools/check_agent_docs_consistency.py --instantiated
       python tools/check_import_layers.py --preflight src tests tools
       python tools/resolve_test_obligations.py --selfcheck --instantiated
3.2  Projektlokale Validierung:
       python -m ruff check .
       python -m ruff format --check .
       python -m mypy src
       python -m pytest
3.3  Gegen Baseline aus 1.3 vergleichen:
       Jeder Check, der vorher grün war, muss grün bleiben.
       Vorher rote Checks: in Evidence als Altlast belegt, nicht neu verschlechtert.
3.4  Strukturkonsistenz manuell prüfen:
       - keine unersetzten Platzhalter in aktiven Regeln (sonst H7)
       - glossar-meta.md Einträge unter ## 3. Begriffe (Checker bestätigt)
       - lokale Fachbegriffe in glossar-domain/system unverändert vorhanden
       - lokale Muster in learning-matrix unverändert vorhanden
       - Tool-Config (LAYER_BY_PACKAGE_PART, TEST_COMMANDS) projektlokal erhalten
3.5  Dokumentdrift final: AGENTS.md §17 Abgleichlisten durchgehen.
3.6  git diff vollständig review: keine ungewollte Inhaltslöschung in gefüllten Dateien.
3.7  Migrations-Evidence abschließen (Status: abgeschlossen), Zielversion v0.2.7
     und ausgeführte Checks eintragen.
```

## Testpflicht / Abschlusschecks (Referenz)

```bash
python tools/check_agent_docs_consistency.py --instantiated
python tools/check_import_layers.py --preflight src tests tools
python tools/resolve_test_obligations.py --selfcheck --instantiated
python -m ruff check . && python -m ruff format --check . && python -m mypy src && python -m pytest
```

## Abbruchbedingungen

BF1–BF12 aus `BROWNFIELD-MIGRATION.md` gelten. Besonders relevant:

```text
BF5   Konflikt Template-Regel ↔ lokale Projektregel (z. B. Tool-Anpassung)
BF6   Tool-Ersetzung würde lokale Anpassung überschreiben
BF7   Migration würde neue Projektsemantik ohne Sprechakt erzeugen
BF9   Observed State würde ohne Entscheidung als Accepted Local Truth gelten
BF11  Baseline/Zielmodell/Plan/Evidence vermischt
BF12  Agent müsste menschliche Architekturentscheidung selbst treffen
```

Bei BF-Abbruch: Evidence unter `.agent-box/migrations/YYYY-MM-DD-BF<nr>-<kurz>-abbruch.md`
schreiben, keine weiteren Dateien ändern.

## Wiedereinstiegspunkt

`.agent-box/migrations/2026-06-21-v0.2.3-to-v0.2.7-migration.md` lesen,
letzten dokumentierten sicheren Zustand und nächste offene Phase ermitteln.

## Abschlusskriterien

```text
- Feature-Branch brownfield/v0.2.3-to-v0.2.7 enthält alle Änderungen
- .agent-box/migrations/ existiert mit vollständiger Evidence (Status: abgeschlossen)
- Box-Version v0.2.7 in Evidence festgehalten
- BROWNFIELD-MIGRATION.md im Repo vorhanden, Platzhalter ersetzt
- Alle merge-Dateien geprüft und nachgezogen; grundsatz.md unverändert
- Alle drei Box-Checks grün (oder rote Checks als Altlast belegt, nicht verschlechtert)
- ruff/mypy/pytest nicht schlechter als Baseline
- Kein lokal gefüllter Inhalt (Glossare, learning-matrix, Tool-Config) verloren
- Kein Template-Default hat lokale operative Wahrheit verdeckt
```

## Erfahrungsbericht

Nach Abschluss immer schreiben.

Protokoll (Format, Pflichtfelder, Ablageort): `erfahrungsbericht-protokoll.md`

Ablageort: `tmp/erfahrungsberichte/2026-06-21-EB-brownfield-v0.2.3-to-v0.2.7.md`