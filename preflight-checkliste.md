# preflight-checkliste.md — Python-Projekt

> Ebene: PRIMING
> Rolle: diagnostisches Einstiegsgate
> Geltung: jeder nichttriviale Lauf
> Autoritative Frage: Welche Vorbedingungen muessen vor Arbeit geprueft werden?
> Nicht zustaendig fuer: lokale Architekturentscheidung, konkrete Ausfuehrungsfreigabe

> Diese Checkliste wird vor jeder nichttrivialen Änderung ausgeführt.
>
> Sie operationalisiert `AGENTS.md`. Sie ersetzt es nicht.
>
> Neue allgemeine Abbruchregeln gehören nach
> `blocker-und-abbruch-protokoll.md`, nicht hierher.

---

## 0. Zweck

Preflight beantwortet vor einer Änderung:

```text
Ist die Aufgabe fachlich, strukturell und testseitig ausführbar?
Ist der semantische Raum bekannt?
Ist die Reichweite bestimmbar?
Sind Schreibrechte erlaubt?
Sind Tests und Checks ableitbar?
Gibt es einen Abbruch- oder Sprechaktgrund?
```

Preflight ist kein Ritual.
Preflight ist der Schutz gegen Bedeutungsrekonstruktion aus Vermutung.
Preflight ersetzt kein Ausfuehrungsmandat.

---

## 0a. WG-MUTATION — Wirkungsgate

WG-MUTATION ist eine fortlaufende Invariante. Es wird vor der ersten
Repository-Mutation und erneut bei Wechsel von Wirkungstyp, Scope,
Schutzklasse, Mandatsstatus oder Grundlage geprüft.

```text
Wirkungstyp:
  diagnostisch | normativ | projekt-transformativ

Diagnostische Wirkung:
  Arbeitsmodus PLAN oder AUSFUEHRUNG?
  erlaubter diagnostischer Artefaktraum?
  keine normative Statusaenderung?

Normative oder projekt-transformative Wirkung:
  Arbeitsmodus AUSFUEHRUNG?
  aktives Ausfuehrungsmandat?
  passende Grundlage und Version?
  Mutation im Scope?
  Schutzklasse gedeckt?
  geschuetzte Datei ausdruecklich vom Mandat gedeckt?
```

Kurzform. Vollstaendige WG-MUTATION-Pruefliste:
`ausfuehrungsmandat-protokoll.md`, Abschnitt "Wirkungsgate WG-MUTATION".

Wenn WG-MUTATION nicht gruen ist: keine Mutation.

WG-MUTATION ist kein Preflight-Schritt. Die `PF-*`-IDs bleiben stabil.

---

## 0b. Risikoklassen-Weiche

Vor dem vollständigen Preflight: welche Risikoklasse hat diese Aufgabe?

Kanonische SICHER-Definition: `AGENTS.md`.

**SICHER** (kein neuer Begriff, keine neue Importkante, kein neuer Raum):

```text
Dokumentation, Kommentare, Typo-Korrekturen
Lint-Korrekturen ohne Logikänderung
Tote Imports entfernen
Bestehende Tests ergänzen (keine neue Semantik)
Lokale Refactorings ohne neue öffentliche Symbole
```

**Fast-Path** gilt nur wenn **alle** Bedingungen erfüllt sind:

```text
- keine geschützte Datei betroffen
- kein Glossar-Begriff aktiv gebraucht oder verändert
- keine Regeldatei berührt (AGENTS.md, package-schema.md, regelmatrix.md …)
- keine Bridge- oder Known-Breach-Zone im Scope berührt
- keine öffentliche API berührt
- keine neue oder veränderte Semantik
- keine neue Importkante
- keine Änderung an Tests, die Verhalten definieren
```

→ **Fast-Path:** PF-AGENTS + PF-RAEUME + PF-IMPORT + PF-TEST + PF-SCHREIBEN.
PF-SCHEMA, PF-GLOSSAR, PF-SCHNITT, PF-PLAN entfallen.

PF-SCHREIBEN (Schreibrechte) entfällt nie. Safe Task ist Risikoklasse, nicht Schreibrecht.

**MITTEL oder höher** (Definition: `AGENTS.md`):

→ Vollständiger Preflight PF-AGENTS–PF-PLAN.

**Wenn Zweifel über die Risikoklasse:** vollständiger Preflight PF-AGENTS–PF-PLAN.

Brownfield-Arbeit ist nie SICHER. Jede Änderung die einen bekannten Bruch
im Scope berührt, erhöht die Klasse automatisch auf MITTEL.

---

## 1. Platzhalter

```text
Regenbogen  regenbogen  src  tests
docs             tools            python tools/check_import_layers.py --preflight src tests tools
python -m ruff check .       python -m ruff format --check .
python -m mypy src  python -m pytest       python tools/check_agent_docs_consistency.py --instantiated && python tools/check_import_layers.py --preflight src tests tools && python tools/resolve_test_obligations.py --selfcheck --instantiated && python -m pytest
```

Nicht ersetzter Platzhalter in aktiver Regel → Abbruch H7.

---

## 2. Kurzform

```text
PF-AGENTS       AGENTS.md lesen
PF-SCHEMA       package-schema.md gezielt prüfen
PF-RAEUME       betroffene semantische Räume bestimmen
PF-GLOSSAR      relevante Glossareinträge gezielt laden; bei Modellarbeit MODELL-README.md prüfen
PF-IMPORT       Import-/Layer-Checker ausführen
PF-TEST         Testpflicht ableiten
PF-SCHREIBEN    Schreibrechte prüfen
PF-SCHNITT      Task-Schnitt prüfen (wenn T1–T5 eintreten)
PF-PLAN         Plan anlegen, wenn Änderung nicht trivial ist
```

Die `PF-*`-IDs sind stabile semantische Identitäten. Reihenfolge und Gruppierung
koennen sich aendern; IDs werden niemals umbenannt oder wiederverwendet.

Jedes Nein oder Unklar ist entweder Sprechakt, Task-Schnitt, SOFT- oder HARD-Abbruch.
Abbruchklassen: `blocker-und-abbruch-protokoll.md`, `BROWNFIELD-MIGRATION.md`.

Nicht raten.

---

## 3. PF-AGENTS — AGENTS.md lesen

```text
Welche Safe-Task-Klasse hat die Aufgabe?
Welche Invarianten sind betroffen?
Welche Abbruchregeln können greifen?
Welche Schreibrechte gelten?
Welche Sprechaktklassen können ausgelöst werden?
Gibt es eine unmittelbare Sperre?
```

Wenn `AGENTS.md` fehlt: HARD-Abbruch H7.
Wenn relevante Platzhalter nicht ersetzt: HARD-Abbruch H7.

---

## 4. PF-SCHEMA — package-schema.md gezielt prüfen

Nicht das ganze Projekt laden. Nur die betroffenen Raumregeln.

```text
Welche Pakete/Module werden berührt?
Welchem semantischen Raum gehören sie an?
Welche Imports sind dort erlaubt?
Welche Imports sind dort verboten?
Gibt es bekannte Brüche?
Gibt es öffentliche API-Flächen?
```

Wenn ein betroffener Modulpfad nicht klassifiziert ist:
Sprechakt SP7 oder Schema-Freigabe nötig.

Wenn `package-schema.md` fehlt: HARD-Abbruch.

---

## 5. PF-RAEUME — Semantische Räume bestimmen

Für jede betroffene Datei:

```text
Datei:
Raum:
Rolle:
Erlaubte Imports:
Verbotene Imports:
Öffentliche API: ja/nein
Geschützt: ja/nein
```

Wenn eine Datei mehreren Räumen zugleich angehört:
Task-Schnitt oder Schemafehler.

---

## 6. PF-GLOSSAR — Glossar gezielt laden; bei Modellarbeit MODELL-README.md prüfen

Ladeprotokoll: `glossar-README.md`

**Schritt 1: Aktive Begriffe bestimmen**

```text
Welche Begriffe werden in diesem Arbeitspaket aktiv gebraucht?
  - geändert, umbenannt oder verschoben
  - als Entscheidungsgrundlage gebraucht
  - in neuen Namen, Typen, Fehlern, Statuswerten oder Tests
```

**Schritt 2: Richtiges Glossar laden**

```text
domain/   → glossar-domain.md
system/   → glossar-system.md
meta      → glossar-meta.md
Mehrere   → alle betroffenen Glossare laden (Signal für Task-Schnitt T5)
Unbekannt → Sprechakt SP7 oder Task-Schnitt T1
```

**Schritt 3: Migrationsstatus prüfen**

```text
Begriff in migration-bridges.md?
  → do-not-touch-mechanically: STOPP, Sprechakt SP6
  → allow-read-only: nicht neu einführen
  → canonical: normal fortfahren
```

**Schritt 4: Eintragstiefe und Autonomieregel**

```text
Eintragstiefe des Glossareintrags prüfen:

  Für Referenz, Suche, bestehende Projektion lesen,
  semantikneutrale oder mechanische Änderung:
    minimaler Eintrag genügt

  Für neue Implementierung, neue Invariante, neue Zustände, neue API
  oder fachliche/systemische Entscheidung:
    vollständiger Eintrag nötig
    Nein → Task-Schnitt T1. Danach noch nötig → Sprechakt SP7.

Autonomieregel prüfen:
  Kann der zuständige Experte diesen Begriff vollständig beurteilen
  ohne andere Räume zu kennen?
  Nein → H10, Sprechakt nötig.
```

**Schritt 5: UI-Text bei cli/-Änderungen prüfen (→ M-6)**

```text
Wenn die Aufgabe cli/ berührt und Werte angezeigt werden:
  Stimmt der angezeigte Text mit dem Glossarbegriff überein?
  Ist der Wert ein Anteil, eine Intensität, eine Wahrscheinlichkeit
  oder ein technisches API-Feld?
  Checker und Tests finden diesen Fehlertyp nicht — nur Glossarabgleich.
```

Nicht laden:
- ganzes Glossar reflexhaft
- historisch relevante Begriffe die jetzt nicht aktiv gebraucht werden
- Begriffe aus Räumen die dieses Arbeitspaket nicht berührt

**Bei Modellarbeit: MODELL-README.md prüfen**

Wenn die Aufgabe das implementierte Modell berührt, zusätzlich prüfen:

```text
Ist MODELL-README.md vorhanden?
Beschreibt es den aktuell implementierten Modellstand?
Würde die geplante Änderung Modellannahmen, Faktoren, Zielgrößen oder die
Übersetzung technischer Eingangsdaten in fachliche Begriffe ändern?
```

Wenn ja: MODELL-README.md ist Pflichtprojektion und muss im selben Schnitt geprüft
und bei Bedarf aktualisiert werden.
Neue fachliche Modellbegriffe dürfen dort nicht still entstehen.
Wenn Begriff aktiv nötig und fehlt: Task-Schnitt T1, danach Sprechakt SP7.

---

## 7. PF-IMPORT — Import-/Layer-Checker ausführen

```bash
python tools/check_import_layers.py --preflight src tests tools
```

```text
grün:
  Strukturcheck bestanden.
  Kein Beweis semantischer Korrektheit.

rot mit unbekanntem Bruch:
  HARD-Abbruch H2.

rot mit bekanntem Bruch:
  Prüfen ob Aufgabe den Bruch aktiv berührt.
  Wenn aktiv: Task-Schnitt oder Freigabe.
  Wenn passiv: vorsichtig fortfahren, Evidence notieren.

Befehl fehlt oder trifft keine Aussage:
  HARD-Abbruch H7.
```

Der Checker ist Alarm, nicht Architekturautorität.

**Format-Check Scope (→ M-1)**

```text
ruff format --check meldet Verstöße auf tool-Dateien die nicht berührt wurden:
  Das ist ein passiver Altbefund — SA6, nicht SA2.
  Nicht durch unerlaubte Nebenreparatur verdecken.
  Separaten Format-Schnitt mit expliziter Freigabe für tools/ beantragen.

SA2 gilt nur wenn geänderter Code (src/, tests/) den Format-Check nicht besteht.
```

---

## 8. PF-TEST — Testpflicht ableiten

```bash
tools/resolve_test_obligations.py --changed-file <path>
```

Für jede geänderte Datei bestimmen:

```text
Produktionscode geändert?
Testcode geändert?
Schema/Doku geändert?
Tooling geändert?
Öffentliche API geändert?
Fehlerbehandlung geändert?
Dependency geändert?
```

**Umgebungscheck (→ M-2)**

```text
Wenn die Aufgabe Laufzeitbezug hat (HTTP-Adapter, DB, externe API):
  Sind Test- und Runtime-Abhängigkeiten installiert?
    Ja  → normal fortfahren
    Nein → jetzt dokumentieren, nicht erst am Ende scheitern.
           SA4-Bedingung als bekannte Einschränkung notieren.
           Menschenentscheidung abwarten, bevor Testvalidierung beansprucht wird.
```

Wenn Testpflicht nicht ableitbar: HARD-Abbruch H6.
Wenn keine Tests nötig: Begründung als Evidence notieren (Testfreiheitsformat: `test-obligations.md`).

---

## 9. PF-SCHREIBEN — Schreibrechte prüfen

Kanonische Quelle: `regelmatrix.md`; `AGENTS.md` enthält die Kategorien.

Kurzform:

```text
Erlaubt:        src/, tests/, docs/plans/, docs/runs/<Run-ID>/, tmp/, CHANGELOG.md
Append-only:    docs/sprechakte/, .agent-box/evidence/erfahrungsberichte/
Geschützt:      alle Agentendokumente, Checker-Tools, docs/plans/template.md,
                docs/runs/checkpoint-template.md,
                pyproject.toml, Lockfiles, .github/workflows/
```

Wenn geschützte Datei ohne Mandatsdeckung geändert werden müsste: HARD-Abbruch H1.

---

## 10. PF-SCHNITT — Task-Schnitt prüfen

Task-Schnitt bei:

```text
T1  SWS enthält fehlenden/unvollständigen Begriff
T2  Aufgabe berührt mehrere semantische Räume
T3  Binding-Grenze betroffen
T4  bekannter Bruch betroffen
T5  mehrere Glossarbereiche nötig
```

```text
Kann die Aufgabe auf einen Raum eingeschränkt werden?
Kann eine Seite der Binding-Grenze zuerst bearbeitet werden?
Kann der fehlende Begriff aus dem aktiven SWS entfernt werden?
Unterscheiden sich menschliche Festlegung, Urteilskompetenz,
Schreibrecht, Validierung oder Rollback-Grenze?
```

Blosse Teilbarkeit ist kein Schnittgrund.
Wenn nur gleichartige Arbeit in einem semantischen Schnitt vorliegt: bündeln.
Wenn echte semantische Grenze vorliegt: schneiden.
Wenn nicht möglich und Begriff fehlt: Sprechakt SP7.

Vollständiges Protokoll: `task-schnitt.md`

---

## 11. PF-PLAN — Plan anlegen

Nichttriviale Änderungen brauchen Plan:

```text
docs/plans/YYYY-MM-DD-kurzbeschreibung.md
```

Verwende das Plan-Template:

```text
docs/plans/template.md
```

Kein Plan außerhalb von `docs/plans/`.

---

## 13. Preflight-Evidence

Für nichttriviale Änderungen:

```text
Preflight:
  AGENTS gelesen:    ja
  Schema geprüft:    ja
  Räume:
  Glossar:
  MODELL-README:
  Import-Checker:
  Testpflicht:
  Schreibrechte:
  Task-Schnitt:
  Plan:
  WG-MUTATION:
  Ergebnis:
```

---

## 14. Schlussregel

Preflight endet nur mit einem dieser Zustände:

```text
FORTSETZEN
TEILEN
SPRECHAKT
SOFT-ABBRUCH
HARD-ABBRUCH
```

Andere Zustände sind unzulässig.
