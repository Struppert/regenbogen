# AGENTS.md — Python-Projekt: Operative Regeln für KI-Agenten

> Dieses Dokument ist die vollständige operative Regelreferenz für KI-Agenten in diesem Repository.
>
> Es gilt für autonome Agenten, Coding-Assistenten, IDE-Integrationen und jede andere Form KI-gestützter Code- oder Textänderung.
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

## 1. Instanziierungs-Sprechakt

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

---

## 2. Grundmodell: Semantische Räume

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

## 3. Glossar und Metasystem

Das Glossar ist operative Infrastruktur. Es enthält Projektbegriffe und
Metasystem-Begriffe, die ein Agent kennen muss, ohne dass `AGENTS.md` dadurch
zum Handbuch wird.

```text
glossar-domain.md    Fachbegriffe
glossar-system.md    System- und Metasystem-Begriffe
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

## 4. Import- und Abhängigkeitsregeln

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

## 5. Kritische Invarianten

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
  - Importverletzung reparieren, wenn Zielraum eindeutig ist

MITTEL:
  - bestehenden Typ verschieben
  - Modul splitten
  - Adapter vereinfachen
  - technische Fehlerbehandlung verbessern
  - neue Tests für Randfälle
  - bestehende Policy klarer ausdrücken

SPRECHAKT / FREIGABE NÖTIG:
  - neuer Fachbegriff (SP1)
  - neuer systemsemantischer Steuerwert (SP2)
  - neue Fehlerklasse oder Fehlerbedeutung (SP3)
  - neue Runtime-Dependency (SP4, H8)
  - Änderung an package-schema.md
  - Änderung an AGENTS.md / AGENTS-COMPACT.md
  - Änderung an Checker-Tools
  - Änderung an Testpflichtableitung
  - Änderung an pyproject.toml oder Lockfiles
  - Änderung an öffentlicher API (H9)
```

Safe Tasks beschreiben Risikoklassen, nicht Schreibrechte.
Geschützte Dateien bleiben geschützt, auch bei SICHER-Tasks.

---

## 7. Sprechakte

Ein Sprechakt ist eine menschliche Festlegung.
Der Agent hält an und liefert eine Entscheidungsvorlage.
Er entscheidet nicht selbst.

Sprechakt ist nötig bei:

```text
SP1  Neuer Fachbegriff würde entstehen
SP2  Neuer systemsemantischer Steuerwert würde entstehen
SP3  Neue Fehlerklasse oder neue Fehlerbedeutung würde entstehen
SP4  Neue Runtime-Dependency würde eingeführt
SP5  Binding-Code würde einen neuen Begriff einführen
SP6  Bekannter Bruch würde umklassifiziert oder verschoben
SP7  Semantic Working Set enthält einen aktiv benötigten Begriff,
    dessen Glossareintrag fehlt oder unvollständig ist
```

Bei SP7 gilt zuerst Task-Schnitt:
Ist der Begriff nur durch zu breiten Schnitt im SWS?
Wenn ja: Aufgabe enger schneiden.
Wenn nein: Sprechakt-Artefakt erzeugen.

Vollständiges Protokoll: `sprechakt-protokoll.md`

Sprechakt-Artefakte liegen unter `docs/sprechakte/` (append-only).

Sprechakt-Artefakte haben einen Status:

```text
offen | festgelegt | abgelehnt | superseded
```

Die Details stehen in `sprechakt-protokoll.md`.

---

## 8. Task-Schnitt

Task-Schnitt wird geprüft, wenn:

```text
T1  SWS enthält fehlenden oder unvollständigen Begriff
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

Wenn Teilung möglich ist, wird geteilt.
Kein „kurz noch". Kein Schritt aus Iteration B in Iteration A.

Vollständiges Protokoll: `task-schnitt.md`

---

## 9. Schreibrechte

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

### Geschützt — nur mit expliziter Freigabe der aktuellen Aufgabe

```text
AGENTS.md
AGENTS-COMPACT.md
AGENT-SETUP.md
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
glossar-README.md
tools/check_import_layers.py
tools/resolve_test_obligations.py
tools/check_agent_docs_consistency.py
tools/instantiate/instantiate_project_box.py
tools/instantiate/README.md
docs/plans/template.md
.agent-box-template.md
.agent-box/instantiation.md
pyproject.toml
requirements*.txt
poetry.lock
uv.lock
Pipfile
setup.cfg
setup.py
.github/workflows/
```

Geschützte Datei ohne Freigabe ändern müssen → HARD-Abbruch H1.

---

## 10. Abbruchbedingungen

### HARD-Abbruch

Der Agent stoppt. Fortsetzung nur nach expliziter Freigabe.

```text
H1  Geschützte Datei müsste ohne Freigabe geändert werden
H2  Import-/Layer-Verletzung ohne klassifizierten bekannten Bruch
H3  Widerspruch zwischen AGENTS.md, package-schema.md, Glossar und Code
H4  Neuer Begriff ohne Sprechakt
H5  Tool müsste verändert werden, um Fehler zu unterdrücken
H6  Testpflicht ist unklar
H7  Platzhalter in relevanter Regel ist nicht ersetzt
H8  Dependency-Änderung wäre nötig
H9  Öffentliche API-Änderung wäre nötig
H10 Autonomieregel verletzt: Code-Typ in Raum X setzt Wissen aus Raum Y voraus,
    aber Experte für X kann Y nicht beurteilen — ohne Sprechakt nicht lösbar
```

### SOFT-Abbruch

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
H1–H10 = HARD-Abbruch · SA1–SA6 = SOFT-Abbruch · SP1–SP7 = Sprechakt.

Die Abbruchklasse richtet sich nach der verletzten Regel, nicht nach dem Werkzeug.

---

## 11. Abbruch-Artefakt

Bei jedem Abbruch:

```text
tmp/erfahrungsberichte/YYYY-MM-DD-ABBRUCH-kurzbeschreibung.md
```

Format:

```markdown
# Abbruch: <Kurzbeschreibung>

Aufgabe:
Zeitpunkt:
Abbruchklasse: SOFT | HARD
Abbruchregel:
Betroffene Dateien:
Letzter sicherer Zustand:
Beobachtete Evidence:
Keine Vermutungen:
Empfohlene nächste Entscheidung:
```

Wenn eine State-Datei existiert, muss sie das Abbruch-Artefakt referenzieren.

---

## 12. Preflight

Vor jeder nichttrivialen Änderung:

```text
1. AGENTS-COMPACT.md lesen
2. AGENTS.md lesen
3. package-schema.md gezielt prüfen
4. relevante Glossareinträge gezielt laden
5. Bei Modellarbeit MODELL-README.md lesen und Updatepflicht prüfen
6. Import-/Layer-Checker ausführen
7. Testpflicht ableiten
8. Schreibrechte prüfen
9. Task-Schnitt prüfen, wenn T1–T5 eintreten
10. Plan unter docs/plans/ anlegen, wenn Änderung nicht trivial ist
```

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

## 13. Python-spezifische Coding-Sperren

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

Alles in dieser Liste, das eine freigabepflichtige Änderung erfordern würde,
ist über H8/H9 und die Sprechakt-Klassen SP1–SP6 abgedeckt.

---

## 14. Tests und Validierung

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

## 15. Git- und Commit-Regeln

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

## 16. Wiedereinstieg

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
4. Preflight ausführen
5. ab definiertem Wiedereintrittspunkt fortsetzen
```

---

## 17. Dokumentdrift

Wenn `AGENTS.md` geändert wird:

```text
AGENTS-COMPACT.md prüfen — Invarianten, Abbrüche, Schreibrechte abgleichen
preflight-checkliste.md prüfen
package-schema.md prüfen
regelmatrix.md prüfen
```

Wenn `package-schema.md` geändert wird:

```text
AGENTS.md prüfen
AGENTS-COMPACT.md prüfen
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

---

## 18. Schnellreferenz: Wo gehört was hin?

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

## 19. Erfahrungsberichte

Nach jeder nichttrivialen Agentensession wird ein Erfahrungsbericht geschrieben.

Pflicht-Trigger:

```text
E1  Nach abgeschlossener Agentensession mit Plan, MITTEL-Task,
    Sprechakt, Task-Schnitt, öffentlicher API-Änderung oder Dokumentdrift.
E2  Nach jedem HARD-Abbruch.
E3  Nach sichtbarer Systemschwäche.
E4  Nach SOFT-Abbruch, wenn der Abbruchgrund systemisch ist.
E5  Nach unerwarteter Interaktion zwischen Regeln.
```

Ort: `tmp/erfahrungsberichte/YYYY-MM-DD-EB-kurzbeschreibung.md` (append-only)

Vollständiges Protokoll: `erfahrungsbericht-protokoll.md`

Erfahrungsberichte sind kein Änderungsauftrag.
Systemänderungen folgen aus menschlicher Entscheidung über Muster in der `learning-matrix.md` —
nicht automatisch aus dem Bericht.

---

## 20. Symbolsperren und Bridge-Begriffe

Neben den Dateisperren in Abschnitt 9 gibt es Bedeutungssperren auf Symbole und Begriffe.

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

## 21. Schlussregel

Der Agent optimiert nicht auf maximale Änderung.
Der Agent optimiert auf kontrollierte, prüfbare und abbrechbare Änderung.

Ein gültiger Abbruch ist besser als eine erfundene Lösung.
Eine kleine, vollständig validierte Änderung ist besser als eine große, plausible Änderung.
