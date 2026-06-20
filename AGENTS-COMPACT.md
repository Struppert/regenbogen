# AGENTS-COMPACT.md — Python-Projekt: Schnelleinstieg für Agenten

> Lies dies zuerst. Vollständige Regeln: `AGENTS.md`. Bei Widerspruch gilt `AGENTS.md`.

---

## 0. Platzhalter

```text
Regenbogen  regenbogen  src  tests
docs             tools            python tools/check_import_layers.py --preflight src tests tools
python -m ruff check .       python -m ruff format --check .
python -m mypy src  python -m pytest       python tools/check_agent_docs_consistency.py --instantiated && python tools/check_import_layers.py --preflight src tests tools && python tools/resolve_test_obligations.py --selfcheck --instantiated && python -m pytest
```

Nicht ersetzter Platzhalter in aktiver Regel → Abbruch H7.

Instanziierung läuft genau einmal über:

```bash
tools/instantiate/instantiate_project_box.py
```

Namensregel:

```text
Regenbogen = menschlicher Name, z. B. Regenbogen
regenbogen  = Python-Importname, z. B. regenbogen
```

Nach `.agent-box/instantiation.md` ist erneute Instanziierung verboten.
`tools/instantiate/*` ist kein normales Agentenwerkzeug.

---

## 1. Semantische Räume

Vollständige Raumkarte: `package-schema.md`.

```text
domain/          Fachdomäne. Kein HTTP, DB, Framework, datetime.now().
system/          Use Cases, Policies, Lifecycle, Fehlerklassifikation.
infrastructure/  DB, HTTP, Filesystem, Queues, externe APIs, Zeit, Zufall.
adapters/        Binding. Übersetzt zwischen Räumen. Erzeugt keine neue Semantik.
cli/             Prozessstart, Argumente, Environment. Keine Domänenlogik.
tests/           Testprojektionen. Keine neue Produktsemantik.
tools/           Checker, Generatoren, Entwicklungstools.
shared/          Nur semantisch neutrale Hilfstypen. Darf keine Projekträume importieren.
```

---

## 2. Glossar und Metasystem

```text
glossar-domain.md    → Fachbegriffe. Domänenexperte urteilt.
glossar-system.md    → Betriebsbegriffe. Systemarchitekt urteilt.
glossar-README.md    → Ladeprotokoll: welches Glossar wann laden.
```

Laderegel: nur aktiv gebrauchte Begriffe laden. Nie das gesamte Glossar.
Fehlender Begriff → Task-Schnitt T1. Danach noch nötig → Sprechakt SP7.

**Autonomieregel:** Ein Raum ist gültig wenn ein einzelner Experte ihn vollständig
beurteilen kann ohne andere Räume zu kennen. Verletzung → H10.

---

## 3. Schärfste Invarianten

```text
I1  domain ist frei von Laufzeitmechanik.
I2  infrastructure beobachtet. system urteilt.
I3  adapters übersetzen, erzeugen keine neue Semantik.
I4  Tests definieren keine Produktsemantik.
I5  Keine stillen Fallbacks.
I6  Keine Import-Side-Effects.
I7  Keine globalen Mutable Singletons ohne Lebensdauervertrag.
I8  Keine nackten Primitives für vorhandene Begriffe.
I9  Keine Runtime-Dependency ohne Freigabe.
I10 Keine Tool-Manipulation zur Fehlerunterdrückung.
```

---

## 4. Importregeln Kurzform

Vollständige Matrix: `package-schema.md`.

```text
domain        → nur domain, shared*
system        → domain, system, Ports*
infrastructure → Ports, technische Bibliotheken, domain nur an erlaubten Grenzen*
adapters      → domain, system, infrastructure
cli           → system-Services, Konfiguration
shared        → nur shared
tests         → alles
tools         → nur tools, shared

* = wenn in package-schema.md explizit erlaubt
```

Matrixwert `decision` bedeutet: nicht automatisch erlaubt, aber durch explizite
Projektentscheidung, Sprechakt oder klassifizierte Ausnahme möglich. Der Agent
darf `decision` nicht als freie Erlaubnis interpretieren.

Pflichtcheck:

```bash
python tools/check_import_layers.py --preflight src tests tools
```

Rot → Stoppsignal. Grün → kein Beweis semantischer Korrektheit.

---

## 5. Safe Tasks

```text
SICHER:
  Kommentare / Doku korrigieren, Lint beheben, tote Imports entfernen,
  bestehende Tests ergänzen, lokale Refactorings ohne neue Begriffe.

MITTEL:
  Modul splitten, Typ verschieben, Adapter ändern, Fehlerbehandlung verbessern.

FREIGABE / SPRECHAKT NÖTIG:
  neuer Fachbegriff (SP1), neuer Steuerwert (SP2), neue Fehlerbedeutung (SP3),
  neue Runtime-Dependency (SP4), Änderung an package-schema.md, AGENTS.md,
  AGENTS-COMPACT.md, Checker-Tools, pyproject.toml / Lockfiles,
  öffentlicher API (H9).
```

Safe Task = Risikoklasse, nicht Schreibrecht.

---

## 6. Sprechakte

Sprechakt = menschliche Festlegung. Agent hält an, liefert Evidence.

```text
SP1  Neuer Fachbegriff
SP2  Neuer systemsemantischer Steuerwert
SP3  Neue Fehlerklasse oder Fehlerbedeutung
SP4  Neue Runtime-Dependency
SP5  Binding-Code erzeugt neue Semantik
SP6  Bekannter Bruch wird verschoben oder umklassifiziert
SP7  Aktiv benötigter Begriff im SWS fehlt im Glossar
```

SP7: zuerst Task-Schnitt prüfen. Wenn Aufgabe enger geschnitten werden kann → kein Sprechakt.

Artefakte: `docs/sprechakte/YYYY-MM-DD-kurzbeschreibung.md` (append-only).

Vollständiges Protokoll: `sprechakt-protokoll.md`

---

## 7. Task-Schnitt

Prüfen bei T1 (fehlender Begriff), T2 (mehrere Räume), T3 (Binding-Grenze),
T4 (bekannter Bruch), T5 (mehrere Glossarbereiche).

```text
SWS klein · SWS vollständig · SWS scharf
```

Wenn Teilung möglich: teilen. Kein „kurz noch".

Vollständiges Protokoll: `task-schnitt.md`

---

## 8. Schreibrechte

```text
Erlaubt:        src/, tests/, docs/plans/, tmp/, CHANGELOG.md
Append-only:    docs/sprechakte/, tmp/erfahrungsberichte/
Geschützt:      AGENTS.md, AGENTS-COMPACT.md, package-schema.md,
                preflight-checkliste.md, task-schnitt.md, sprechakt-protokoll.md,
                regelmatrix.md, test-obligations.md,
                migration-bridges.md, erfahrungsbericht-protokoll.md, learning-matrix.md,
                tools/check_import_layers.py,
                tools/resolve_test_obligations.py,
                tools/check_agent_docs_consistency.py,
                tools/instantiate/instantiate_project_box.py,
                pyproject.toml, requirements*.txt, poetry.lock, uv.lock,
                Pipfile, setup.cfg, setup.py, .github/workflows/
```

Geschützte Datei ohne Freigabe → HARD-Abbruch H1.

---

## 9. Abbruchbedingungen

HARD (Stopp, Freigabe nötig):

```text
H1  geschützte Datei ohne Freigabe
H2  Import-/Layer-Verletzung ohne klassifizierten Bruch
H3  Widerspruch AGENTS / Schema / Glossar / Code
H4  neuer Begriff ohne Sprechakt
H5  Tool zur Fehlerunterdrückung nötig
H6  Testpflicht unklar
H7  relevanter Platzhalter nicht ersetzt
H8  Dependency-Änderung nötig
H9  öffentliche API-Änderung nötig
H10 Autonomieregel verletzt: Raum X setzt Wissen aus Raum Y voraus
```

SOFT (Stopp mit Evidence, Preflight dann möglich):

```text
SA1 Test rot   SA2 Lint rot   SA3 Typecheck rot
SA4 Build-/Installationsfehler
SA5 unvollständige Migration entdeckt
SA6 lokale Inkonsistenz ohne semantischen Widerspruch
```

Abbruch-Artefakt: `tmp/erfahrungsberichte/YYYY-MM-DD-ABBRUCH-kurzbeschreibung.md`

---
## 10. Preflight Kurzform

```text
1. AGENTS-COMPACT.md lesen
2. AGENTS.md lesen
3. package-schema.md gezielt prüfen
4. relevante Glossareinträge laden
5. Import-Checker ausführen
6. Testpflicht ableiten
7. Schreibrechte prüfen
8. Task-Schnitt prüfen (wenn T1–T5)
9. Plan anlegen wenn nicht trivial
```

```bash
python tools/check_import_layers.py --preflight src tests tools
python -m ruff check .
python -m ruff format --check .
python -m mypy src
python -m pytest
python tools/check_agent_docs_consistency.py --instantiated && python tools/check_import_layers.py --preflight src tests tools && python tools/resolve_test_obligations.py --selfcheck --instantiated && python -m pytest
```

Vollständige Schrittfolge: `preflight-checkliste.md`

---

## 11. Git-Regeln

```text
Erlaubt:   git status / diff / log / add / commit
Verboten:  git push, remote ändern, branch löschen, tag, config --global, history rewrite
```

Commit = lokaler Evidence-/Recovery-Snapshot. Kein Merge. Kein Release.

---

## 12. Erfahrungsberichte und Symbolsperren

Erfahrungsberichte:
```text
E1  nach Session mit Plan/MITTEL/Sprechakt/Task-Schnitt/API/Dokumentdrift
E2  nach HARD-Abbruch
E3  nach sichtbarer Systemschwäche
E4  nach systemischem SOFT-Abbruch
E5  nach unerwarteter Regelinteraktion
```

Ort: `tmp/erfahrungsberichte/YYYY-MM-DD-EB-kurzbeschreibung.md`
Protokoll: `erfahrungsbericht-protokoll.md`
Kein Änderungsauftrag — Eingabe für menschliche Entscheidung via `learning-matrix.md`.

**Symbolsperren** — vor Änderung an einem Symbol: `migration-bridges.md` prüfen.
`do-not-touch-mechanically` → STOPP, Sprechakt SP6.
Umklassifizierung eines Bridge-Begriffs → Sprechakt SP6.

---

## 13. Schlussregel

```text
Lieber gültig abbrechen als Bedeutung erfinden.
Lieber kleine validierte Änderung als große plausible Änderung.
```
