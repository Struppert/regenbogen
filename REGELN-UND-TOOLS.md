# REGELN-UND-TOOLS.md — Allgemeine Regeln und Werkzeugkatalog

> Ebene: REPOSITORY
> Rolle: lokale Ergaenzung zum Template-Router: Projektbefehle, Werkzeugkatalog, lokale Regeln und Invarianten
> Geltung: dieses Projekt
> Autoritative Frage: Welche lokalen Regeln und Werkzeuge gelten ergaenzend zum Router AGENTS.md?
> Nicht zustaendig fuer: Router und Kernregeln (AGENTS.md), Abbruchcodes (blocker-und-abbruch-protokoll.md), Projektaufbau (PROJEKT.md), Begriffsbedeutungen (Glossar)

> Lokale Ergaenzung, kein Template-Dokument (Sprechakt
> `docs/sprechakte/2026-11-16-migration-v0.3.11-entscheidungen.md`, Entscheidung D1).
> Die Inhalte stammen aus der frueheren langen AGENTS.md und wurden verschoben, nicht
> neu formuliert. Sie sind Rueckfluss-Kandidaten fuer das Template. Bei Widerspruch zu
> `AGENTS.md` oder den Template-Protokollen gilt der Template-Text; der Widerspruch
> ist Abbruch H3.

---

## 1. Projektbefehle

```text
Projektname            Regenbogen
Python-Package         regenbogen
Quellcode-Wurzel       src
Test-Wurzel            tests
Docs-Wurzel            docs
Tools-Wurzel           tools
```

```text
Import-/Layer-Check    python tools/check_import_layers.py --preflight src tests tools
Lint                   python -m ruff check .
Format-Check           python -m ruff format --check .
Typecheck              python -m mypy src
Tests                  python -m pytest
Vollvalidierung        python tools/check_agent_docs_consistency.py --instantiated && python tools/check_import_layers.py --preflight src tests tools && python tools/resolve_test_obligations.py --selfcheck --instantiated && python -m pytest
```

Ist ein Wert in dieser Tabelle unklar oder fehlt er: Abbruch H7.

---

## 2. Werkzeugkatalog

| Werkzeug | Wann | Aufruf |
|---|---|---|
| `tools/check_import_layers.py` | vor jeder nichttrivialen Aenderung (PF-IMPORT) | `python tools/check_import_layers.py --preflight src tests tools` |
| `tools/check_agent_docs_consistency.py` | nach Aenderung an Agentendokumenten | `python tools/check_agent_docs_consistency.py --instantiated` (optional `--changed-file <pfad>` fuer Kopplungshinweise) |
| `tools/resolve_test_obligations.py` | um die Testpflicht abzuleiten (PF-TEST) | `python tools/resolve_test_obligations.py --changed-file <pfad>`; Selbstpruefung mit `--selfcheck --instantiated` |
| `tools/erzeuge_index_entwurf.py` | wenn der Begriffsindex neu aufgebaut oder abgeglichen wird | `python tools/erzeuge_index_entwurf.py` (schreibt nur einen Entwurf nach `tmp/`) |
| `tools/verdichte_aufgaben.py` | am Merge-Gate, wenn Plaene und Checkpoints eines Branches verdichtet werden | `python tools/verdichte_aufgaben.py` (schreibt nur einen Entwurf nach `tmp/`, aendert nichts) |
| `tools/instantiate/` | nur bei der Erstinstanziierung, danach verboten | siehe `tools/instantiate/README.md` |

### Formatregel: Markdown only

Dieses Projekt verwendet Markdown als operativen Artefaktraum.

```text
Evidence: Markdown
Instanziierungsnachweis: Markdown
Sprechakt-Artefakte: Markdown
Erfahrungsberichte: Markdown
Projekt-Metadaten der Agenten-Box: Markdown
```

JSON, YAML oder andere strukturierte Nebenformate dürfen nicht als zweite
operative Wahrheit eingeführt werden, außer ein Mensch hebt diese Regel
ausdrücklich für eine konkrete Aufgabe auf. Tools dürfen Markdown mit stabilen
Köpfen lesen und schreiben.

Alle Werkzeuge lesen Dokumente und Code und melden Befunde. Sie entscheiden
nichts. Ein gruener Lauf ist ein Strukturbefund, kein Beweis semantischer
Korrektheit. Ein roter Lauf ist ein Stoppsignal mit Evidence.

---

## 3. Import- und Abhaengigkeitsregeln

Die vollständige Importmatrix steht in `package-schema.md`.
Die Standardsperre gilt immer, sofern package-schema.md keine explizite Ausnahme definiert:

```text
domain
  darf nicht importieren:
    system, infrastructure, adapters, cli / entrypoints
  darf importieren:
    domain
    shared, wenn in package-schema.md als semantisch neutral klassifiziert

system
  darf nicht importieren:
    infrastructure-Details, cli / entrypoints
  darf importieren:
    domain, system
    abstrakte Ports / Protokolle, wenn in package-schema.md definiert

infrastructure
  darf nicht importieren:
    cli / entrypoints
  darf importieren:
    system-Ports, technische Bibliotheken
  darf Domain-Objekte nur an explizit erlaubten Adaptergrenzen sehen

adapters
  darf importieren:
    domain, system, infrastructure
  darf nicht:
    neue Fachbegriffe erzeugen
    neue System-Semantics erzeugen
    Fehler still umdeuten

cli / entrypoints
  darf importieren:
    freigegebene Application-/System-Services, Konfigurationsadapter
  darf nicht:
    Domänenlogik enthalten
    Infrastrukturentscheidungen in Fachbegriffe übersetzen

shared
  darf importieren:
    shared
  darf nicht importieren:
    domain, system, infrastructure, adapters, cli
  Wenn ein shared-Typ eine Bedeutungsebene trägt: gehört nicht nach shared.
```

### Import-Checker

Vor jeder nichttrivialen Änderung:

```bash
python tools/check_import_layers.py --preflight src tests tools
```

Grün = Strukturcheck bestanden. Kein Beweis semantischer Korrektheit.
Rot = Stoppsignal. Abbruch mit Evidence.

Wenn der Befehl fehlt oder für die berührten Dateien keine Aussage trifft:
Abbruch H7.

---

## 4. Python-spezifische Coding-Sperren

```text
Verboten:
  - broad except ohne Bindung
  - except Exception: pass
  - relative Imports im Produktionscode (absolute Imports = semantische Adressen; siehe package-schema.md 8.1)
  - sys.path-Manipulation zur Importreparatur
  - dynamische Imports zur Umgehung von Layer-Regeln
  - Monkeypatching in Produktionscode
  - globale mutable Caches ohne Lebensdauervertrag (→ I7)
  - IO beim Import (→ I6)
  - Netzwerk beim Import (→ I6)
  - echte Secrets im Repository
  - echte Secrets in Logs, Evidence oder Tests
  - produktive HTTP-/DB-Zugriffe in Unit-Tests
  - Tests, die nur durch Reihenfolge bestehen
```

---

## 5. Tests und Validierung

Tests sind Projektionen, keine Autorität.

Mindestregeln:

```text
- Geänderte Produktdatei braucht passende Tests oder begründete Testfreiheit.
- Neue Fehlerbehandlung braucht Negativtest.
- Neuer Adapter braucht Integrationstest oder Fake-/Contract-Test.
- Neuer Domain-Begriff braucht Domain-Test oder Glossarentscheidung.
- Importregeländerung braucht Import-Checker-Lauf.
- Öffentliche API-Änderung braucht Doku-/Example-/Compatibility-Prüfung.
- Modelländerung braucht Prüfung von MODELL-README.md; bei geänderten
  Modellannahmen oder Faktoren muss das Dokument nachgezogen werden.
```

Testpflicht ableiten:

```bash
tools/resolve_test_obligations.py --changed-file <path>
```

Nicht ableitbar → HARD-Abbruch H6.

Vollständige Matrix: `test-obligations.md`

---

## 6. Safe Tasks und Grenzen

### Autonom erlaubt

```text
SICHER:
  - Dokumentation und Kommentare aktualisieren
  - kleine Tippfehler beheben
  - bestehende Tests für bestehendes Verhalten ergänzen
  - interne Hilfsfunktion extrahieren, wenn Raumgrenzen unverändert bleiben
  - Lint-/Format-Verstöße beheben
  - klar lokale Refactorings ohne neue Begriffe
  - tote Imports entfernen

MITTEL:
  - bestehenden Typ verschieben
  - Modul splitten
  - Adapter vereinfachen
  - technische Fehlerbehandlung verbessern
  - neue Tests für Randfälle
  - bestehende Policy klarer ausdrücken
  - Importverletzung reparieren (Zielraum prüfen; kann Typ, Binding oder API betreffen)
```

Sprechakt oder Freigabe ist noetig bei:

```text
SPRECHAKT / FREIGABE NÖTIG:
  - neuer Fachbegriff (SP1)
  - neuer systemsemantischer Steuerwert (SP2)
  - neue Fehlerklasse oder Fehlerbedeutung (SP3)
  - neue Runtime-Dependency (SP4, H8)
  - Änderung an package-schema.md
  - Änderung an AGENTS.md
  - Änderung an Checker-Tools
  - Änderung an Testpflichtableitung
  - Änderung an pyproject.toml oder Lockfiles
  - Änderung an öffentlicher API (H9)
```

Safe Tasks beschreiben Risikoklassen, nicht Schreibrechte.
Geschützte Dateien bleiben geschützt, auch bei SICHER-Tasks.

Fast-Path: kanonische Definition `preflight-checkliste.md` §0b.

---

## 7. Git- und Commit-Regeln

```text
Erlaubt:
  git status, git diff, git log, git add, git commit
```

```text
Verboten ohne explizite Freigabe:
  git push
  git remote ändern
  git branch löschen
  git tag erstellen
  git config --global ändern
  History rewrite
```

Commit-Präfixe: `agent: <beschreibung>` | `wip(agent): <beschreibung>`

Ein Commit ist ein lokaler Evidence-/Recovery-Snapshot.
Kein Merge. Kein Release.

---

## 8. Dokumentdrift

Wenn `AGENTS.md` geändert wird:

```text
preflight-checkliste.md prüfen
package-schema.md prüfen
regelmatrix.md prüfen
ausfuehrungsmandat-protokoll.md prüfen
blocker-und-abbruch-protokoll.md prüfen
```

Wenn `package-schema.md` geändert wird:

```text
AGENTS.md prüfen
check_import_layers.py → LAYER_BY_PACKAGE_PART nachziehen
test-obligations.md prüfen
```

Wenn Checker geändert werden:

```text
AGENTS.md prüfen
package-schema.md prüfen
preflight-checkliste.md prüfen
CI-Konfiguration prüfen
```

Dokumentdrift ist kein Stilproblem. Dokumentdrift ist ein Operationsfehler.
Exakte Drift-Regeln und Kopplungshinweise: `regelmatrix.md`

---

## 9. Meta-Index: Begriff zu Regeldokument

Dieser Index sagt, wo ein Agenten- oder Regelbegriff definiert ist. Die
Bedeutung steht in `glossar-meta.md`.

| Begriff | Zustaendiges Dokument |
|---|---|
| H-Code, SA-Code, Abbruch, Wiedereinstieg | `blocker-und-abbruch-protokoll.md` |
| SP-Code, Sprechakt | `sprechakt-protokoll.md` |
| BF-Code, Brownfield-Aufnahme, Baseline, Migrationsevidence | `BROWNFIELD-MIGRATION.md` |
| Wirkungsgate, WG-MUTATION, Ausfuehrungsmandat, Arbeitsmodus | `ausfuehrungsmandat-protokoll.md` |
| Plan, Laufbindung, Contract, Scope | `docs/plans/template.md` |
| Checkpoint, Run-Status | `docs/runs/checkpoint-template.md` |
| Semantic Working Set, Task-Schnitt | `task-schnitt.md` |
| Preflight, Preflight-Schritte, Fast-Path, Risikoklassen | `preflight-checkliste.md` |
| Schreibrechte, Autoritaet, Datei-Aktionsklasse | `regelmatrix.md` |
| Testpflicht | `test-obligations.md` |
| Known Breach, Importmatrix, Raumkarte | `package-schema.md` |
| Migration Bridge | `migration-bridges.md` |
| Erfahrungsbericht, Evidence | `erfahrungsbericht-protokoll.md` |
| Glossar-Ladeprotokoll, Eintragstiefe | `glossar-README.md` |
| Instanziierungs-Sprechakt | `AGENT-SETUP.md`, `tools/instantiate/README.md` |
| Plan-Form, Merge-Gate, Abschlussdokument, Aufgabenindex | `aufgaben-lebenszyklus-protokoll.md` |
| Autonomieregel, Reifizierung | `grundsatz.md` |

---

## 10. Kritische Invarianten (lokale Vertiefung)

Die Kernregeln stehen im Router `AGENTS.md`. Hier stehen die ausfuehrlichen
Formulierungen mit Beispielen.

### I1. Domain bleibt frei von Laufzeitmechanik

```text
Kein HTTP-Statuscode in domain.
Kein Retry-Zähler in domain.
Kein Datenbankmodell als Domain-Modell tarnen.
Kein Framework-Typ in domain.
Kein datetime.now(), time.time(), random(), requests, pathlib-IO in domain.
```

### I2. System Semantics urteilt, Infrastruktur beobachtet

```text
infrastructure beobachtet technische Tatsachen:
  HTTP 404, Timeout, Connection refused, Datei fehlt, Constraint verletzt

system entscheidet, was das für den Ablauf bedeutet:
  retryable, terminal, invalid request, conflict, forbidden transition
```

Infrastruktur darf technische Fehler liefern.
Sie darf keine fachliche oder systemsemantische Endentscheidung erfinden.

### I3. Binding verbindet, erzeugt aber keine neue Semantik

```text
Erlaubt:
  DTO → Domain-Objekt
  technische Exception → technischer Fehlerwert
  externer Response-Code → beobachteter Infrastruktur-Fact
  Use-Case-Request → Domain-Operation

Verboten:
  neuer Fachbegriff im Adapter
  neue Policy im Adapter
  stiller Fallback im Adapter
  implizite Fehlerumdeutung im Adapter
```

### I4. Tests definieren keine Produktsemantik

Tests dürfen erwartetes Verhalten ausdrücken.
Sie dürfen keine neue Bedeutung einführen, die in Code, Glossar oder Projektregeln fehlt.

Wenn ein Test einen neuen Begriff, Status, Fehlercode oder Ablauf erfordert:
Sprechakt oder Planentscheidung nötig.

### I5. Keine stillen Fallbacks

```python
# verboten:
except Exception:
    return None

except Exception:
    pass

value = config.get("x", "irgendein-default")
```

Jeder Fallback braucht eine explizite Bedeutung:
technischer Fallback, fachlicher Fallback, Kompatibilitätsfallback oder Abbruch.

### I6. Keine Import-Side-Effects

```text
kein Netzwerkzugriff beim Import
kein Dateisystem-Write beim Import
kein Start von Threads/Tasks beim Import
kein Lesen produktiver Secrets beim Import
kein globaler Client mit echter Verbindung beim Import
```

### I7. Keine globalen Mutable Singletons

Verboten, sofern nicht explizit im Projekt freigegeben:

```python
GLOBAL_CLIENT = ...
GLOBAL_CACHE  = {}
CONFIG        = load_config()
```

Erlaubt nur als bewusst gebundene Infrastruktur- oder Runtime-Komponente
mit klarer Lebensdauer und explizitem Freigabedokument.

### I8. Keine nackten Primitives für vorhandene Begriffe

Wenn ein Begriff im Glossar existiert, darf er nicht dauerhaft als nackter
`str`, `int`, `dict` oder `tuple` durch das System geschoben werden.

```text
UserId      nicht dauerhaft als str
OrderId     nicht dauerhaft als str
Money       nicht als tuple[int, str]
RetryBudget nicht als int ohne Bedeutung
```

Ausnahme: technische Randzonen wie Parser, Serializer, CLI und Adapter.
Dort muss die Umwandlung sichtbar und lokal sein.

### I9. Keine Dependency-Einführung ohne Freigabe

Der Agent darf keine neue Runtime-Dependency hinzufügen. → Abbruch H8.

Betroffen:

```text
pyproject.toml, requirements*.txt, poetry.lock, uv.lock,
Pipfile, setup.cfg, setup.py, tox.ini, noxfile.py
```

### I10. Keine Tool-Manipulation zur Fehlerunterdrückung

```text
Verboten:
  Lint-Regel deaktivieren
  Test skippen ohne Freigabe
  xfail ohne Freigabe
  Type ignore breit setzen
  Import-Checker entschärfen
  Konfiguration so ändern, dass der Fehler verschwindet statt behoben wird
```

### I11. Keine Repository-Mutation ohne aktives Ausfuehrungsmandat

Beschreibbarkeit einer Datei ist kein Ausfuehrungsmandat.
Vor der ersten Mutation WG-MUTATION aus `ausfuehrungsmandat-protokoll.md` prüfen.

### I12. Keine ungefragten Schätzungen oder Scorecard-Zahlen

Keine quantifizierten Schätzungen, Prozentangaben oder Scores ohne explizite Anfrage
(Regel E-X, übernommen aus dem Hauptzweig, Commit `b240562`).

```text
Verboten (ungefragte Agentenerfindung):
  ✗ "Aufwand: 2-3 Stunden"
  ✗ "Klarheit: +50%"
  ✗ "Risiko: ⭐⭐⭐⭐ (4/5)"
  ✗ "Fortschritt: ▓▓▓▓ (80%)"

Erlaubt:
  ✓ "Das erfordert länger als das" (relativ, keine Zahlen)
  ✓ "Aufwandsschätzung angefordert? (Annahmen nötig, bin ich bereit?)" (reflektiv)
  ✓ Tabellen/Scores nur auf explizite Anfrage: "Vergleiche diese 3 Ansätze"
```

Grund: Modelle erzeugen Zahlen durch Genre-Modus (Beratungsberichte sehen mit Tabellen
"fertig" aus), nicht durch Grundlage. Ungefragte Prozente wirken wie Datenanalyse, sind aber
freihändige Schätzung und werden in Dokumenten als autoritativ zitiert. Zahlen ohne
Messgrundlage als Zahlen auszugeben ist falsch, unabhängig davon, ob jemand danach fragt.

Handlung: Wenn eine Schätzung nötig ist, fragen: "Soll ich einen Aufwandsrahmen skizzieren?
Welche Annahmen sind tragbar?" Dann transparent, was gemessen und was spekulativ ist.

---

## 11. H10-Erkennungsregeln

#### H10 — Erkennungsregeln

H10 auslösen wenn mindestens eine der folgenden Bedingungen zutrifft:

```text
1. Ein domain-Typ enthält ein Feld dessen Name aus Infrastruktur- oder
   System-Vokabular stammt (retry_count, http_status, db_id, request_id).

2. Eine domain-Funktion gibt einen Wert zurück, der nur mit Kenntnis eines
   Laufzeitprotokolls (Retry, Transaktion, HTTP-Zyklus) korrekt
   interpretierbar ist.

3. Eine Invariante eines domain-Begriffs im Glossar kann nur ein
   Systemarchitekt, nicht ein Domänenexperte beurteilen.

4. Ein system-Begriff setzt im Glossar oder im Code voraus, dass der
   Beurteiler konkrete Plattformdetails (DB-Typ, HTTP-Library,
   Queue-Semantik) kennt.
```

Prüfhilfe: Kompetenzfrage des Glossareintrags lesen.
Wenn die Antwort ein Systemarchitekt statt ein Domänenexperte liefern muss
(für domain-Begriffe) oder ein Plattformexperte statt ein Systemarchitekt
(für system-Begriffe): H10.

### SOFT-Abbruch SA1–SA6

Der Agent stoppt mit Evidence. Fortsetzung nach Preflight möglich.

```text
SA1  Test rot
SA2  Lint rot
SA3  Typecheck rot
SA4  technischer Build-/Installationsfehler
SA5  unvollständige Migration entdeckt
SA6  lokale Inkonsistenz ohne semantischen Widerspruch
```

Code-Familien sind disjunkt:
H1–H10 = HARD-Abbruch · SA1–SA6 = SOFT-Abbruch · SP1–SP7 = Sprechakt ·
BF1–BF12 = Brownfield-spezifischer HARD-Abbruch (→ `BROWNFIELD-MIGRATION.md`).

Die Abbruchklasse richtet sich nach der verletzten Regel, nicht nach dem Werkzeug.

---

## 12. Schlussregel

Regeln und Werkzeuge dienen der kontrollierten, pruefbaren und abbrechbaren
Aenderung. Eine Aussage steht in genau einem Dokument. Wer hier eine Regel
findet, die in `AGENTS.md` oder einem Protokoll anders lautet, stoppt mit
Abbruch H3.
