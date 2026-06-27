# test-obligations.md — Python-Projekt: Test- und Checkpflichten

> Dieses Dokument beschreibt, welche Validierungen aus Datei- und Bedeutungsänderungen folgen.
>
> Es ersetzt keine Tests. Es macht Testpflichten ableitbar.
>
> Ziel ist nicht das Erzeugen von Unit-Tests.
> Ziel ist die stärkste praktikable Validierung der betroffenen Invarianten.
>
> Das konkrete Mapping Pfad → Testbefehl steht in `tools/resolve_test_obligations.py`.
> Wenn Mapping und dieses Dokument auseinanderlaufen: HARD-Abbruch H6.

---

## 1. Zweck

```text
Welche Änderung berührt welche Invariante?
Welche Validierung ist dafür mindestens nötig?
Welche Checks sind zusätzlich nötig?
Wann ist Testfreiheit zulässig?
Wann ist die Testpflicht unklar?
```

Wenn eine Änderung nicht klassifizierbar ist: HARD-Abbruch H6.

Tests sind keine Autorität.
Tests sind Projektionen von Invarianten.

Eine Änderung ist erst fertig, wenn die betroffenen Invarianten bestimmt und angemessen validiert wurden.

---

## 1b. Testphilosophie: Invariantentest vor Unit-Test

Der generelle Zielbegriff dieses Projekts ist nicht „Unit-Test“.

Der Zielbegriff ist:

```text
Invariantentest
```

oder allgemeiner:

```text
Validierung gegen Invarianten
```

Unit-Tests sind nur eine mögliche Prüfform.
Sie erfüllen die Testpflicht nur dann, wenn die betroffene Invariante lokal entscheidbar ist.

### Grundregel

```text
Änderung
  → betroffene Invarianten bestimmen
  → stärkste praktikable Validierung wählen
  → Evidence erzeugen
```

Nicht:

```text
Änderung
  → Unit-Test schreiben
```

### Teststärke-Hierarchie

Die stärkste sinnvolle Prüfform ist zu bevorzugen:

```text
1. Extern kontrollierter Systemtest
2. Invariantentest gegen laufendes oder simuliertes Gesamtsystem
3. Contract-/Adaptertest
4. Integrationstest
5. Struktur-/Layer-/Checker-Test
6. Unit-Test für lokal reine Logik
```

Ein Unit-Test ist ausreichend, wenn:

```text
- die Invariante vollständig lokal ist
- keine externen Protokolle beteiligt sind
- keine Lifecycle-, Retry-, Timeout-, Recovery- oder Fehlerklassifikationssemantik betroffen ist
- keine Raumgrenze überschritten wird
```

Ein Unit-Test ist nicht ausreichend, wenn die Invariante erst im Zusammenspiel mehrerer Räume sichtbar wird.

### Extern kontrollierter Systemtest

Ein externer kontrollierter Systemtest prüft das System unter kontrollierten Außenbedingungen.

Beispiele:

```text
Fake-Server
Devproxy
kontrollierter HTTP-Endpunkt
kontrolliertes Dateisystem
kontrollierter Queue-/Message-Broker
kontrollierter Prozess- oder CLI-Kontext
```

Stark daran ist:

```text
System under test
  → echte Ablaufkette
  → kontrollierte externe Antwort
  → beobachtbares Verhalten
  → prüfbare Invariante
```

Diese Testform ist besonders geeignet für:

```text
Retry-Verhalten
Timeout-Verhalten
Fehlerklassifikation
Boundary-/Adapter-Verhalten
Evidence-Erzeugung
Phasenübergänge
Idempotenz
Abbruchverhalten
Recovery-Pfade
keine stille Fehlerumdeutung
```

Wenn solche Invarianten betroffen sind, ist ein reiner Unit-Test unzureichend.

---

## 2. Platzhalter

```text
src  tests  docs  tools
python tools/check_import_layers.py --preflight src tests tools  python -m ruff check .  python -m ruff format --check .
python -m mypy src    python -m pytest  python tools/check_agent_docs_consistency.py --instantiated && python tools/check_import_layers.py --preflight src tests tools && python tools/resolve_test_obligations.py --selfcheck --instantiated && python -m pytest
```

---

## 3. Standard-Checks

Bei jeder Codeänderung:

```bash
python -m ruff check .
python -m ruff format --check .
python -m mypy src
```

Bei Import-/Raumänderung zusätzlich:

```bash
python tools/check_import_layers.py --preflight src tests tools
```

Bei Produktverhaltensänderung:

```bash
python -m pytest
```

Bei nichttrivialem Abschluss:

```bash
python tools/check_agent_docs_consistency.py --instantiated && python tools/check_import_layers.py --preflight src tests tools && python tools/resolve_test_obligations.py --selfcheck --instantiated && python -m pytest
```

Wenn ein Befehl nicht definiert ist und für die Aufgabe relevant wäre:
Testpflicht unklar → HARD-Abbruch H6.

---

## 4. Pfadbasierte Testpflicht

Pfadbasierte Testpflicht ist nur die erste Ableitung.

Sie ersetzt nicht die Invariantenfrage:

```text
Welche Invariante ist betroffen?
Ist sie lokal prüfbar?
Ist sie nur im Zusammenspiel mehrerer Räume sichtbar?
Welche stärkste praktikable Validierung gibt es?
```

### `src/domain/**`

```text
Fachliche Invarianten-Tests, Value-Object-Tests,
negative Tests für ungültige Werte, Import-Layer-Check.
```

Wenn die fachliche Invariante lokal entscheidbar ist, sind lokale Domain-Tests ausreichend.

Nicht ausreichend:

```text
nur CLI-Test
nur Snapshot
Unit-Test auf Implementierungsdetails ohne fachliche Invariante
```

Neuer Domain-Begriff: Sprechakt SP1 oder Glossarentscheidung nötig.

---

### `src/system/**`

```text
Use-Case-Tests, Policy-Tests, Fehlerklassifikations-Tests,
Lifecycle-/State-Transition-Tests, Idempotenz-/Retry-/Timeout-Tests,
Import-Layer-Check.
```

System-Semantics sind häufig nicht lokal entscheidbar.

Wenn Ablauf-, Retry-, Timeout-, Recovery-, Idempotenz- oder Fehlerklassifikationssemantik betroffen ist, ist die stärkste verfügbare Systemvalidierung zu wählen:

```text
extern kontrollierter Systemtest
Contract-/Adaptertest
Integrationstest
Invariantentest über Trace/Evidence
```

Unit-Tests reichen nur für lokal reine Policy-Logik ohne Außenverhalten.

Neue Ablaufbedeutung: Sprechakt SP2.

---

### `src/infrastructure/**`

```text
Adapter-/Gateway-Tests, Fake-/Contract-Tests, technische Fehlerfälle,
Timeout-/IO-/Filesystem-/HTTP-Fehler.
Keine produktiven externen Zugriffe in Unit-Tests.
Import-Layer-Check.
```

Infrastrukturtests sollen Außenbedingungen kontrollieren, nicht produktive Außenwelt benutzen.

Bevorzugt:

```text
Fake-Server
Devproxy
temporäres Dateisystem
kontrollierte Netzwerkfehler
kontrollierte HTTP-Antworten
Contract-Test
```

Echte externe Dienste nötig: Integrationstest klar markieren oder Fake/Contract-Test bevorzugen.

---

### `src/adapters/**`

```text
Mapping-Tests, Fehlerübersetzungs-Tests, Roundtrip-Tests,
Tests für fehlende/ungültige Felder, Import-Layer-Check.
```

Adaptertests prüfen Übersetzung, nicht neue Bedeutung.

Wenn Adapterverhalten nur im Zusammenspiel mit Infrastruktur und System-Semantics sichtbar ist, ist ein Contract- oder extern kontrollierter Systemtest vorzuziehen.

Adapter müsste neue Bedeutung erzeugen: Sprechakt SP5.

---

### `src/cli/**` oder `src/entrypoints/**`

```text
CLI-/Entry-Point-Tests, Argument-/Environment-Tests,
Exit-Code-Tests, Smoke-Test.
Keine Domänenlogik im CLI-Test neu definieren.
```

CLI-Tests prüfen Prozessränder und Eintrittsverhalten.

Wenn CLI-Optionen Systemverhalten auslösen, reicht ein reiner Argumentparser-Test nicht.

Neue CLI-Option mit Bedeutung: Freigabe oder Sprechakt.

---

### `src/shared/**`

```text
Tests der Hilfstypen.
Import-Layer-Check (besonders wichtig — shared darf keine Projekträume importieren).
Überprüfung: ist der Code wirklich semantisch neutral?
```

Unit-Tests sind hier häufig ausreichend, aber nur wenn der Code wirklich lokal und semantisch neutral ist.

Wenn shared Code eine Bedeutungsebene trägt: Task-Schnitt oder Sprechakt SP1/SP2.

---

### `tests/**`

```text
Prüfen ob Test bestehendes Verhalten prüft oder neues definiert.
Bei neuem Verhalten: Plan / Sprechakt (I4).
Relevante Produkt-Checks ausführen.
```

Teständerung allein ist nicht automatisch sicher.

Wenn Test Erwartung ändert: Produktsemantik betroffen.

Tests dürfen keine neue Produktsemantik erzeugen.
Sie dürfen nur Invarianten projizieren, die in Code, Glossar, Schema oder Plan bereits existieren.

---

### `tools/**`

```text
Tool-Selbsttest (--selfcheck), Dry Run,
Vergleich gegen bekannte Beispiele,
Dokumentkonsistenz prüfen.
Keine Fehlerunterdrückung.
```

Tooling darf die Umgebung modellieren.
Tooling darf Produktartefakte lesen, prüfen, erzeugen oder transformieren.
Tooling darf keine Produktsemantik konstituieren.

Änderung an Checker-Tools ist geschützt (H1, H5).

---

### Agenten-Dokumente

```text
AGENTS.md, package-schema.md,
preflight-checkliste.md, task-schnitt.md, sprechakt-protokoll.md,
regelmatrix.md, test-obligations.md
```

Pflicht:

```text
check_agent_docs_consistency.py
Manuelle Driftprüfung nach regelmatrix.md (Inhalt, nicht nur Präsenz).
Falls Schema betroffen: Import-Checker-Konfiguration prüfen.
```

---

### Packaging / Dependencies

```text
pyproject.toml, requirements*.txt, poetry.lock, uv.lock,
Pipfile, setup.cfg, setup.py
```

Pflicht:

```text
Explizite Freigabe (H8).
Dependency-Begründung.
Installations-/Lockfile-Prüfung.
Full Validation.
Security-/Lizenzprüfung, wenn im Projekt definiert.
```

Runtime-Dependency ohne Freigabe: HARD-Abbruch H8.

---

## 5. Änderungstyp-basierte Testpflicht

### Neuer Begriff

```text
Sprechakt SP1 oder Glossarentscheidung.
Domain-/System-Invariante bestimmen.
Stärkste praktikable Validierung wählen.
Schema prüfen. Öffentliche API prüfen.
```

### Neuer Fehlerfall

```text
Negativtest, Fehlerklassifikations-Test,
Adapter-/Infrastructure-Test wenn technische Quelle betroffen.
Keine broad-except-Lösung (I5).
```

Wenn der Fehlerfall durch externe Bedingungen entsteht, ist ein kontrollierter externer Test vorzuziehen.

### Fehler-Mapping geändert

```text
Mapping-Test, alter Fall, neuer Fall,
Recoverable/Terminal-Bedeutung prüfen.
Neue Bedeutung: Sprechakt SP3.
```

Wenn das Mapping Systemverhalten auslöst, reicht ein isolierter Mapping-Unit-Test nicht.
Dann ist zusätzlich ein Ablauf-/Systemtest nötig.

### Importstruktur geändert

```text
Import-Layer-Check.
Betroffene Invarianten bestimmen.
Betroffene lokale oder systemische Tests ausführen.
package-schema.md prüfen. Known Breach prüfen.
```

### Modul verschoben

```text
Import-Layer-Check.
Alle direkten Tests.
Öffentliche Importpfade prüfen.
__init__.py prüfen.
Dokumentation / Examples prüfen wenn öffentlich.
```

### Öffentliche API geändert

```text
Freigabe (H9).
API-Test. Doku-/Example-Prüfung.
Compatibility-Entscheidung.
Changelog wenn Projekt das verlangt.
```

### Dependency geändert

```text
Freigabe (H8).
Installationscheck. Lockfile-Check. Full Validation.
Sicherheits-/Lizenzcheck wenn definiert.
```

### Refactoring ohne Verhaltensänderung

```text
Betroffene Invarianten benennen.
Bestehende Validierung ausführen.
Lint. Format. Typecheck.
Import-Layer-Check wenn Imports betroffen.
```

Wenn Tests geändert werden müssen, war es möglicherweise kein reines Refactoring.

---

## 6. Testfreiheit

Testfreiheit ist erlaubt, aber muss begründet werden.

Zulässige Gründe:

```text
- nur Kommentar
- reine Dokumentation ohne operative Regeländerung
- reine Formatierung ohne Semantik
- tote Datei entfernt, keine Projektion
- Änderung liegt außerhalb produktiver Oberfläche
```

Nicht zulässig:

```text
- zu klein
- offensichtlich
- nur schnell
- Tests dauern lange
- Unit-Test wäre schwierig
- externe Umgebung ist unbequem
```

Format:

```markdown
Testfreiheit:
  Grund:
  Betroffene Dateien:
  Warum keine Produktsemantik betroffen ist:
  Welche Invarianten nicht betroffen sind:
  Welche Checks trotzdem liefen:
```

---

## 7. Mindest-Evidence nach Tests

```text
Betroffene Invarianten:
Stärkste gewählte Validierung:
Warum diese Validierung ausreichend ist:
Unit-Test ausreichend: ja/nein/begründung
Checks:
  Import-Layer:
  Lint:
  Format:
  Typecheck:
  Tests:
  Full Validation:
  Nicht ausgeführt:
  Begründung:
```

---

## 8. Unklare Testpflicht

Testpflicht ist unklar, wenn:

```text
- geänderte Datei keinem Raum zugeordnet ist
- betroffene Invariante nicht bestimmbar ist
- Änderungstyp nicht klassifizierbar ist
- stärkste sinnvolle Validierung nicht bestimmbar ist
- Tool zur Testpflichtableitung fehlt
- Tests existieren nicht und Testfreiheit ist nicht begründbar
- öffentliche API betroffen sein könnte, aber nicht dokumentiert ist
- Checker und Dokument widersprechen sich
```

Unklare Testpflicht → HARD-Abbruch H6.

---

## 9. Schlussregel

Eine Änderung ohne ableitbare Testpflicht ist nicht fertig.

Eine Änderung ohne bestimmte betroffene Invariante ist nicht fertig.

Ein Unit-Test ist kein Ziel.
Ein Unit-Test ist nur dann ausreichend, wenn die betroffene Invariante lokal entscheidbar ist.

Wenn keine Testpflicht ableitbar ist: nicht raten. Abbrechen.
