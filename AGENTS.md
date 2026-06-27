# AGENTS.md — Python-Projekt: Operative Regeln für KI-Agenten

> Immer aktive Kernregeln und Ladeprotokoll. Detailregeln nur bei konkretem
> Task-Auslöser laden. Verlinkte Dokumente nicht pauschal laden.
>
> Der Modus ändert nichts an den Regeln. Eine Inline-Completion, die eine Invariante verletzt, ist genauso falsch wie ein autonomer Agent, der sie verletzt.

---

## 0. Geltung, Formatregel und Platzhalter

Dieses Template muss beim Einsetzen in ein konkretes Projekt angepasst werden.

```text
Regenbogen          Anzeigename des Projekts, z. B. Regenbogen
regenbogen          Python-Package-/Importname, z. B. regenbogen
src                  Quellcode-Wurzel, z. B. src/
tests                    Test-Wurzel, z. B. tests/
docs                    Dokumentations-Wurzel, z. B. docs/
tools                   Tooling-Wurzel, z. B. tools/
python tools/check_import_layers.py --preflight src tests tools       Projektbefehl für Import-/Layer-Check
python -m ruff check .              Projektbefehl für Lint
python -m ruff format --check .      Projektbefehl für Format-Check
python -m mypy src         Projektbefehl für Typecheck
python -m pytest              Projektbefehl für Tests
python tools/check_agent_docs_consistency.py --instantiated && python tools/check_import_layers.py --preflight src tests tools && python tools/resolve_test_obligations.py --selfcheck --instantiated && python -m pytest          vollständige Validierung
```

Wenn ein Platzhalter nicht ersetzt ist, darf der Agent ihn nicht still interpretieren.
Nicht ersetzter Platzhalter in einer für die Aufgabe relevanten Regel ist Abbruchgrund H7.

Warum dieses System so aufgebaut ist: `grundsatz.md`

Projektmarker: `.agent-box/instantiation.md` (Greenfield).

### 0.1 Formatregel: Markdown only

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

---

## 1. Autoritaet, Ladeprinzip und Spezialdokumente

`AGENTS.md` ist bindender Router und Einstieg. Spezialdokumente sind autoritativ für
ihre Detailfrage:

```text
Raum, Import, Architektur        -> package-schema.md
Begriff, Status, Fehler, Policy  -> glossar-README.md,
                                    glossar-domain.md,
                                    glossar-system.md,
                                    glossar-meta.md
Menschliche Entscheidung         -> sprechakt-protokoll.md
Semantischer Task-Schnitt        -> task-schnitt.md
Brownfield oder Altbruch         -> BROWNFIELD-MIGRATION.md
Testpflicht                      -> test-obligations.md
Schreibrechte, Schutz, Drift     -> regelmatrix.md
Arbeitsmodus, Mandat, WG-AUSFUEHRUNG -> ausfuehrungsmandat-protokoll.md
Blocker, Abbruch, Wiedereinstieg -> blocker-und-abbruch-protokoll.md
Bridge-Symbol                    -> migration-bridges.md
Erfahrungsbericht-Ausloeser      -> erfahrungsbericht-protokoll.md
Setup oder Instanziierung        -> AGENT-SETUP.md
```

Bei Widerspruch zwischen autoritativen Artefakten nicht selbst entscheiden.
Blocker klassifizieren und gültig stoppen.

---

## 2. Arbeitsmodus und Wirkungsgate

Ein Auftrag erlaubt nur den eindeutig ausgesprochenen Arbeitsmodus.

Ohne nachweisbares Ausfuehrungsmandat gilt `ANALYSE`.

```text
ANALYSE      lesen, untersuchen, im Chat berichten
PLAN         diagnostische Wirkung: Plan, Evidence, Sprechakt anlegen
AUSFUEHRUNG  freigegebenen Plan im Mandatsscope umsetzen
```

Vor jeder Repository-Mutation WG-AUSFUEHRUNG aus
`ausfuehrungsmandat-protokoll.md` pruefen. Diagnostische Wirkung (Plan,
Evidence, Sprechakt) erfordert PLAN- oder AUSFUEHRUNGS-Modus. Transformative
Wirkung (Code, Checker, normative Artefakte) erfordert zusaetzlich ein
aktives Ausfuehrungsmandat.

Schreibrecht, Planexistenz, Fast-Path, festgelegter Sprechakt und fehlender
Blocker ersetzen kein Ausfuehrungsmandat.

---

## 3. Instanziierungs-Sprechakt

Die Box wird genau einmal vom Template-Zustand in den Projekt-Zustand überführt.
Dieser Übergang ist ein Instanziierungs-Sprechakt. Er wird ausschließlich durch
`tools/instantiate/instantiate_project_box.py` vollzogen.

Dabei gilt:

```text
Regenbogen   menschlicher Projektanzeigename, z. B. Regenbogen
regenbogen    Python-Import-/Pfadname, z. B. regenbogen
```

Das Tool schreibt `.agent-box/instantiation.md` als Markdown-Evidence und
verweigert weitere Läufe, sobald diese Datei existiert. Details, Parameter und
Sonderfälle stehen in `AGENT-SETUP.md` und `tools/instantiate/README.md`.

Nach der Instanziierung sind Änderungen an Projektname, Root-Verzeichnissen,
Layer-Struktur oder öffentlicher API keine Re-Instanziierung. Sie sind neue
Sprechakte über `sprechakt-protokoll.md`.

Brownfield-Arbeit ist keine Re-Instanziierung. Bestehende Projekte werden nach
`BROWNFIELD-MIGRATION.md` migriert oder aufgenommen.
Vorhandener Code ist dabei zuerst Befund, nicht automatisch lokale operative
Wahrheit. Brownfield-Aufnahme ist durch `.agent-box/adoption.md` belegt.

---

## 4. Grundmodell: Semantische Räume

Jeder produktive Code gehört zu genau einem semantischen Raum.

Die vollständige Raumkarte, Importmatrix und Known Breaches stehen in `package-schema.md`.
Dieses Dokument enthält nur die operative Kurzform.

```text
domain/
  Fachdomäne.
  Begriffe, Regeln und Objekte, die ein Domänenexperte ohne technische Laufzeitdetails prüfen kann.

system/
  System Semantics.
  Betriebsregeln des laufenden Systems: Use Cases, Policies, Lifecycle, Retry, Idempotenz,
  Validierung, Transaktionsregeln, Fehlerklassifikation, Orchestrierung.

infrastructure/
  Implementierungsdomäne.
  Datenbanken, Dateisystem, Netzwerk, Frameworks, HTTP-Clients, Queues, externe APIs,
  Zeit, Zufall, Prozessumgebung, Plattformmechanik.

adapters/
  Binding.
  Verbindet semantische Räume. Darf mehrere Räume kennen, erzeugt aber keine neue Semantik.

cli/ oder entrypoints/
  Einstiegspunkte.
  Parsen Umgebung, Argumente und Konfiguration und rufen freigegebene Use Cases auf.
  Keine Domänenlogik.

tests/
  Testprojektionen.
  Tests prüfen Verhalten und Struktur. Tests sind keine Quelle neuer Semantik.

tools/
  Entwicklungs- und Agententools.
  Checker, Generatoren, Testpflichtableitung, Dokumentkonsistenz.
```

Semantische Zugehörigkeit bestimmt erlaubte Imports, zulässige Begriffe,
zuständigen Experten, notwendige Tests und erlaubte Agentenoperationen.
Sie ist kein Dateigeschmack.

### Autonomieregel

Die schärfste Invariante ist epistemisch:

> Ein semantischer Raum ist gültig, wenn ein einzelner Experte ihn
> vollständig prüfen kann ohne die anderen Räume zu kennen.

```text
domain/customer:
  Domänenexperte urteilt ohne HTTP, Retry, DB zu kennen: ✓ → gültig

domain/customer mit retry_count:
  Domänenexperte kann nicht urteilen ohne Retry-Semantik: ✗ → Autonomie verletzt
```

Der Compiler schweigt hier prinzipiell — die Frage liegt außerhalb seiner Zuständigkeit.
Nur Mensch oder Agent mit Glossar-Zugang kann sie beantworten.
Das ist der Grund warum Preflight, Sprechakt und Abbruch nötig sind.

---

## 5. Glossar und Metasystem

Das Glossar ist operative Infrastruktur. Es trennt Fachbegriffe,
Betriebsbegriffe und Meta-Begriffe der Agentensteuerung.

```text
glossar-domain.md    Fachbegriffe
glossar-system.md    System- und Betriebsbegriffe des Zielprojekts
glossar-meta.md      Agenten-, Regel-, Evidence- und Prozessbegriffe
glossar-README.md    Ladeprotokoll
MODELL-README.md     zusammenhängende Beschreibung des aktuell implementierten Modells
```

Preflight lädt nur aktiv benötigte Begriffe. Fehlt ein aktiv benötigter Begriff,
gilt Task-Schnitt T1; bleibt der Begriff nötig, gilt Sprechakt SP7.

`MODELL-README.md` ist kein Glossarersatz und keine neue semantische
Autorität neben Glossar und Code. Es ist die verpflichtende
Zusammenhangsbeschreibung des aktuell implementierten Modells und muss bei
Modelländerungen geprüft und bei Bedarf aktualisiert werden.

---

## 6. Import- und Abhängigkeitsregeln

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

## 7. Kritische Invarianten

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
Vor der ersten Mutation WG-AUSFUEHRUNG aus `ausfuehrungsmandat-protokoll.md` prüfen.

---

## 8. Safe Tasks und Grenzen

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

## 9. Sprechakte

Ein Sprechakt ist eine menschliche Festlegung.
Der Agent hält an und liefert eine Entscheidungsvorlage.
Er entscheidet nicht selbst.

Ein festgelegter Sprechakt autorisiert nicht automatisch die Umsetzung seiner
Folgeprojektionen. Semantische Festlegung und Ausfuehrungsmandat sind getrennt.

Sprechakt ist nötig bei:

```text
SP1  Neuer Fachbegriff würde entstehen
SP2  Neuer systemsemantischer Steuerwert würde entstehen
SP3  Neue Fehlerklasse oder neue Fehlerbedeutung würde entstehen
SP4  Neue Runtime-Dependency würde eingeführt
SP5  Binding-Code würde einen neuen Begriff einführen
SP6  Bekannter Bruch würde umklassifiziert oder verschoben
SP7  Semantic Working Set enthält einen aktiv benötigten Begriff,
    für den kein hinsichtlich der geplanten Nutzung ausreichender
    Glossareintrag vorliegt
```

Bei SP7 gilt zuerst Task-Schnitt:
Ist der Begriff nur durch zu breiten Schnitt im SWS?
Wenn ja: Aufgabe enger schneiden.
Wenn nein: Sprechakt-Artefakt erzeugen.

Vollständiges Protokoll: `sprechakt-protokoll.md`

Sprechakt-Artefakte liegen unter `docs/sprechakte/` (append-only).

Sprechakt-Artefakte haben einen Status:

```text
offen | festgelegt | abgelehnt | superseded | widerrufen
```

Die Details stehen in `sprechakt-protokoll.md`.

---

## 10. Task-Schnitt

Task-Schnitt wird geprüft, wenn:

```text
T1  SWS enthält Begriff ohne für die geplante Nutzung ausreichenden Glossareintrag
T2  Aufgabe berührt mehrere semantische Räume
T3  Aufgabe berührt Binding-Grenze
T4  Preflight zeigt bekannte Brüche
T5  mehrere Glossarbereiche wären nötig
```

Ziel:

```text
SWS klein:      nur was diese Iteration braucht
SWS vollständig: kein aktiv benötigter Begriff fehlt
SWS scharf:     keine Räume laden, die diese Iteration nicht berührt
```

Blosse Teilbarkeit ist kein Schnittgrund. Ausfuehrungsbreite: Gleichartige
Änderungen innerhalb eines mandatsgedeckten semantischen Schnitts werden
gebündelt ausgeführt.

Vollständiges Protokoll: `task-schnitt.md`

---

## 11. Schreibrechte

### Erlaubt ohne Sonderfreigabe

```text
src/
tests/
docs/plans/
tmp/
CHANGELOG.md
```

### Append-only

```text
docs/sprechakte/
tmp/erfahrungsberichte/
```

### Geschützt — nur mit expliziter Mandatsdeckung

```text
AGENTS.md
AGENT-SETUP.md
BROWNFIELD-MIGRATION.md
ausfuehrungsmandat-protokoll.md
blocker-und-abbruch-protokoll.md
package-schema.md
preflight-checkliste.md
task-schnitt.md
sprechakt-protokoll.md
regelmatrix.md
test-obligations.md
migration-bridges.md
erfahrungsbericht-protokoll.md
learning-matrix.md
grundsatz.md
glossar-domain.md
glossar-system.md
glossar-meta.md
glossar-README.md
tools/check_import_layers.py
tools/resolve_test_obligations.py
tools/check_agent_docs_consistency.py
tools/instantiate/instantiate_project_box.py
tools/instantiate/README.md
docs/plans/template.md
.agent-box-template.md
.agent-box/instantiation.md
.agent-box/adoption.md
.agent-box/migrations/
pyproject.toml
requirements*.txt
poetry.lock
uv.lock
Pipfile
setup.cfg
setup.py
.github/workflows/
```

Geschützte Datei ohne Mandatsdeckung ändern müssen → HARD-Abbruch H1.
Beschreibbarkeit ist keine Mandatserteilung.

Exakte Schreibrechte-Klassifikation: `regelmatrix.md`

---

## 12. Abbruchbedingungen

Vollständige Abbruchdefinitionen, Evidence-Format und Wiedereinstieg:
`blocker-und-abbruch-protokoll.md`

### HARD-Abbruch H1–H10

Der Agent stoppt. Fortsetzung nur nach expliziter Freigabe oder Klärung.

```text
H1   Geschützte Datei ohne Mandatsdeckung betroffen
H2   Import-/Layer-Verletzung ohne klassifizierten bekannten Bruch
H3   Widerspruch zwischen operativen Projektartefakten, Code oder Checker
H4   Neuer Begriff, Status oder neue Bedeutung ohne Sprechakt/Freigabe
H5   Tooländerung wäre nötig, um einen Fehler zu unterdrücken
H6   Testpflicht ist nicht ableitbar
H7   Setup-/Template-Zustand unklar, Platzhalter aktiv oder Pflichtdatei fehlt
H8   Runtime-Dependency- oder Packaging-Änderung ohne Freigabe
H9   Öffentliche API-Fläche ohne Freigabe betroffen
H10  Autonomieregel eines semantischen Raums verletzt
```

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

## 13. Abbruch-Artefakt

Bei jedem Abbruch:

```text
tmp/erfahrungsberichte/YYYY-MM-DD-ABBRUCH-<kurzbeschreibung>.md
```

Format:

```markdown
# Abbruch: <Kurzbeschreibung>

Datum:
Aufgabe:
Abbruchklasse: H<Nummer> | SA<Nummer>
Abbruchregel:
Betroffene Dateien:
Letzter sicherer Zustand:
Beobachtete Evidence:
Keine Vermutungen:
Empfohlene nächste Entscheidung:
Wiedereinstiegspunkt:
```

Wenn eine State-Datei existiert, muss sie das Abbruch-Artefakt referenzieren.
Bei BF-Abbruch gilt zusätzlich `BROWNFIELD-MIGRATION.md`.

---

## 14. Preflight

Vor jeder nichttrivialen Änderung zuerst WG-AUSFUEHRUNG prüfen (→ `ausfuehrungsmandat-protokoll.md`),
dann Preflight:

```text
PF-ROUTER       AGENTS.md lesen
PF-SCHEMA       package-schema.md gezielt prüfen
PF-RAEUME       betroffene semantische Räume bestimmen
PF-GLOSSAR      relevante Glossareinträge gezielt laden; bei Modellarbeit MODELL-README.md prüfen
PF-IMPORTLAYER  Import-/Layer-Checker ausführen
PF-TESTPFLICHT  Testpflicht ableiten
PF-SCHREIBRECHT Schreibrechte prüfen
PF-TASKSCHNITT  Task-Schnitt prüfen, wenn T1–T5 eintreten
PF-PLAN         Plan unter docs/plans/ anlegen, wenn Änderung nicht trivial ist
```

Fast-Path, Governance-Ausloeser und Ausfuehrungsbreite: kanonische Definitionen `preflight-checkliste.md` §0b.

Vollständige Schrittfolge: `preflight-checkliste.md`

Standardbefehle:

```bash
python tools/check_import_layers.py --preflight src tests tools
python -m ruff check .
python -m ruff format --check .
python -m mypy src
python -m pytest
```

Vollvalidierung:

```bash
python tools/check_agent_docs_consistency.py --instantiated && python tools/check_import_layers.py --preflight src tests tools && python tools/resolve_test_obligations.py --selfcheck --instantiated && python -m pytest
```

---

## 15. Python-spezifische Coding-Sperren

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

## 16. Tests und Validierung

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

## 17. Git- und Commit-Regeln

```text
Erlaubt:
  git status, git diff, git log, git add, git commit

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

## 18. Wiedereinstieg

Nach SOFT-Abbruch:

```text
1. State-Datei lesen
2. Abbruch-Evidence lesen
3. Preflight ausführen
4. ab letztem sicheren Zustand fortsetzen
```

Nach HARD-Abbruch:

```text
1. State-Datei lesen
2. Abbruch-Evidence lesen
3. STOPP — explizite Freigabe abwarten
4. erst dann Preflight und Fortsetzung
```

Nach Sprechakt:

```text
1. Sprechakt-Artefakt lesen
2. menschliche Festlegung lesen
3. Glossar-/Schema-Nachzug prüfen
4. WG-AUSFUEHRUNG und Ausfuehrungsmandat prüfen
5. Preflight ausführen
6. ab definiertem Wiedereintrittspunkt fortsetzen
```

Bei Kontextwechsel oder neuem Agenten:
Mandat und Plan-Version prüfen (→ `ausfuehrungsmandat-protokoll.md` §9).

---

## 19. Dokumentdrift

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

## 20. Schnellreferenz: Wo gehört was hin?

```text
Fachlicher Begriff                              → domain
Use Case / Ablaufregel / Policy                 → system
Fehlerklassifikation                            → system
DB / HTTP / Filesystem / Queue / Framework      → infrastructure
Übersetzung zwischen Räumen                     → adapters
CLI / Prozessstart / Argumente / Environment    → cli oder entrypoints
Tests                                           → tests
Agenten-/Entwicklungstools                      → tools
Semantisch neutrale Hilfstypen                  → shared (mit Vorsicht)
```

Wenn keine Zuordnung möglich ist:
Task-Schnitt prüfen. Dann Sprechakt. Nicht raten.

---

## 21. Erfahrungsberichte

Erfahrungsberichte werden nur bei systemisch lernrelevanten Auslösern geschrieben.

Pflicht-Trigger:

```text
E1  Systemische Schwäche oder unerwartetes Regelversagen wurde sichtbar.
E2  Nach jedem HARD-Abbruch.
E3  Nach sichtbarer Systemschwäche oder neu erkanntem Governance-Muster.
E4  Nach SOFT-Abbruch, wenn der Abbruchgrund systemisch ist.
E5  Nach unerwarteter Interaktion zwischen Regeln.
```

Ort: `tmp/erfahrungsberichte/YYYY-MM-DD-EB-<kurzbeschreibung>.md` (append-only)

Vollständiges Protokoll: `erfahrungsbericht-protokoll.md`

Erfahrungsberichte sind kein Änderungsauftrag.
Systemänderungen folgen aus menschlicher Entscheidung über Muster in der `learning-matrix.md` —
nicht automatisch aus dem Bericht.

---

## 22. Symbolsperren und Bridge-Begriffe

Neben den Dateisperren in §11 gibt es Bedeutungssperren auf Symbole und Begriffe.

Ein Symbol kann in einer frei beschreibbaren Datei stehen und trotzdem nicht mechanisch
angefasst werden dürfen — weil es eine Bridge-Funktion trägt, eine laufende Migration
begleitet oder ein bekannter Bruch bewusst bestehen bleibt.

Kanonische Quelle: `migration-bridges.md`

Vor jeder Änderung die ein Symbol aus der Bridge-Registry berührt:

```text
1. Symbol in BR-Registry suchen.
2. Migrationsstatus lesen.
3. Bei do-not-touch-mechanically: STOPP. Sprechakt SP6.
4. Bei allow-read-only: lesen erlaubt, nicht neu einführen.
5. Bei do-not-introduce: Ablaufplan prüfen. Wenn kein Plan: Sprechakt SP6.
```

Umklassifizierung eines Bridge-Begriffs ist Sprechakt SP6.

---

## 23. Schlussregel

Der Agent optimiert nicht auf maximale Änderung.
Der Agent optimiert auf kontrollierte, prüfbare und abbrechbare Änderung.

Ein gültiger Abbruch ist besser als eine erfundene Lösung.
Eine kleine, vollständig validierte Änderung ist besser als eine große, plausible Änderung.
