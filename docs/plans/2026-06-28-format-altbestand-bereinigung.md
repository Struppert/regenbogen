# Plan: Format-Altbestand in fünf Dateien bereinigen

> Ebene: PLAN/RUN
> Rolle: Transformationsplan für isolierte Formatbereinigung
> Geltung: dieses Projekt
> Autoritative Frage: Wie wird der bestehende Ruff-Format-Altbestand in fünf Dateien isoliert bereinigt?
> Nicht zustaendig fuer: konkrete Laufdurchführung ohne Freigabe, fachliche Modelländerung
> Instanzebene: PLAN/RUN

Plan-ID: PLAN-2026-06-28-format-altbestand-bereinigung
Plan-Version: 1
Plan-Schema-Version: v0.3.7
Planstatus: entscheidungsbereit
Erstellt im Modus: PLAN
Datum: 2026-06-28
Bearbeiter: Codex

## Laufbindung

Contract-ID: CONTRACT-2026-06-28-format-altbestand-bereinigung
Contract-Status: proposed
Run-ID: RUN-2026-06-28-format-altbestand-bereinigung
Priming-Revision: AGENTS.md@2026-06-28
Repository-Vertragsrevision: e370461
Plan-Revision: PLAN-2026-06-28-format-altbestand-bereinigung@1
Scope-ID: SCOPE-2026-06-28-format-altbestand-bereinigung
Scope-Version: 1
Authorization-Revision:
Base-Snapshot: e370461
Interaktionsprofil: interaktiv
Recovery-Profil: normal
Arbeitsprofil: feature

## Ausführungsmandat

Mandat-ID: MD-2026-06-28-format-altbestand-bereinigung
Mandatstatus: nicht erteilt
Mandatsgrundlage: Plan
Contract-ID: CONTRACT-2026-06-28-format-altbestand-bereinigung
Run-ID: RUN-2026-06-28-format-altbestand-bereinigung
Mandatsrevision:
Authorization-Revision: <Mandat-ID>@<Mandatsrevision>
Grundlagen-ID: PLAN-2026-06-28-format-altbestand-bereinigung
Grundlagen-Version: 1
Freigabezeitpunkt:
Freigabetext oder Freigabereferenz:
Freigegebener Scope:
Freigegebene geschützte Dateien:
Nicht freigegeben: alle Dateien außerhalb des Ressourcenscopes
Gültigkeit: bis Abschluss

## Ressourcenscope

Pfade:
- src/regenbogen/cli/gui_format.py
- src/regenbogen/system/core/tagesprognose_use_case.py
- tests/cli/test_gui_format.py
- tests/domain/test_regenbogen_geometrie.py
- tests/system/test_tagesprognose_use_case.py

Komponenten:
- CLI-Formatierung
- Use-Case-Implementierung
- zugehörige Testprojektionen

Semantische Räume:
- cli
- system
- tests

## Wirkungsscope

### Explizit erlaubte Wirkungen

- reine Ruff-Formatierung der fünf benannten Dateien
- minimale syntaktische Anpassungen, die ausschließlich aus `ruff format` resultieren
- Nachziehen lokaler Imports nur dann, wenn `ruff format` sie zwangsläufig umordnet

### Abgeleitete Wirkungen

- zugehörige Tests
- notwendige Imports
- Formatierung geänderter Dateien
- Dokumentationsprojektionen im freigegebenen Scope

### Verbotene Wirkungen

- Logikänderungen
- semantische Umbenennungen
- Änderungen an Governance-Dateien
- Änderungen an weiteren Produkt- oder Testdateien
- Dependency-Änderungen
- stille Mitnahme anderer Ruff-Befunde

## Capability-Scope

Normale Dateien:
- die fünf Dateien im Ressourcenscope

Geschützte Dateien:
- keine

Governance:
- keine

Dependencies:
- verboten

Priorität:

```text
verboten
> fehlende Capability
> explizit erlaubt
> abgeleitet
```

Verbotene Wirkung hat Vorrang. Eine abgeleitete Wirkung ist nur zulässig,
wenn sie innerhalb des freigegebenen semantischen Arbeitsschnitts bleibt und
die passende Capability vorhanden ist.

## Mandatsrelevante Änderungen

Plan-Version erhöhen bei Änderung an Zielzustand, Scope, geschützten Dateien,
Semantik, Dependencies, öffentlicher API, Validierungs- oder Rollback-Grenze.

## Aufgabe

Den durch `ruff format --check . --exclude tmp` bestätigten Format-Altbestand
in genau fünf unveränderten Bestandsdateien separat bereinigen.

## Zugesagter semantischer Endzustand

Die fünf Dateien sind auf den aktuellen Ruff-Formatierungsstand gebracht,
ohne inhaltliche Änderung ihres Verhaltens. Der globale Format-Check ist
bezogen auf diesen Altbestand nicht mehr rot.

## Betroffene Räume

- `cli/` über `gui_format.py`
- `system/` über `tagesprognose_use_case.py`
- `tests/` über die drei Testdateien

## Nicht-Ziele

- keine funktionalen Änderungen
- keine neuen Tests
- keine Änderung an Tooling oder Ruff-Konfiguration
- keine Bereinigung anderer möglicher Altbestände
- keine Governance- oder Brownfield-Arbeit

## Schreibrechte

```text
Beschreibbar: src/, tests/
Geschützt: keine Datei im Scope
Append-only: nicht relevant
```

## Bereits erteilte Freigaben / Sprechakte

Keine Ausführungsfreigabe. Dieser Plan ist nur entscheidungsbereit.

## Erwartete Änderungen

- `ruff format` auf genau fünf Dateien ausführen
- formatbedingte Diff-Prüfung
- anschließende Verifikation mit globalem `ruff format --check . --exclude tmp`

## Interne Phasen

1. Baseline der fünf Dateien sichern und Diff-Scope bestätigen
2. `ruff format` auf die fünf Dateien anwenden
3. Diff auf reine Formatänderung prüfen
4. Verifikation mit Ruff-Format-Check und relevanten Tests

Phasengrenzen sind keine Benutzer-Checkpoints, solange keine neue Freigabe,
kein neuer Sprechakt und kein echter Task-Schnitt nötig wird.

Fortschritt wird nicht im Plan fortgeschrieben. Aktuelle Phase, erledigte
Schritte, offene Schritte, HEAD, Blocker und nächster zulässiger Schritt
stehen ausschließlich im Checkpoint.

## Gebündelte mechanische Änderungen

- eine gebündelte Formatierung über die fünf Scope-Dateien
- keine Mikroschnitte pro Datei

## Testpflicht

Mindestens:

```text
./.venv/bin/python -m ruff format --check src/regenbogen/cli/gui_format.py src/regenbogen/system/core/tagesprognose_use_case.py tests/cli/test_gui_format.py tests/domain/test_regenbogen_geometrie.py tests/system/test_tagesprognose_use_case.py
./.venv/bin/python -m ruff format --check . --exclude tmp
```

Zusätzlich sinnvoll:

```text
./.venv/bin/python -m pytest tests/cli/test_gui_format.py tests/domain/test_regenbogen_geometrie.py tests/system/test_tagesprognose_use_case.py
```

## Abbruchbedingungen

- wenn `ruff format` außerhalb der fünf Dateien Änderungen erzwingen würde
- wenn Diff mehr als reine Formatierung zeigt
- wenn während der Ausführung weitere nicht zum Scope gehörende rote Checks sichtbar werden
- wenn sich der Scope durch neue manuelle Änderungswünsche erweitert

## Echter Task-Schnitt

Schnitt nötig: nein
Begründung:
Es handelt sich um eine gleichartige mechanische Änderung innerhalb eines
klaren semantischen Schnitts. Die fünf Dateien werden bewusst als ein
gebündeltes Arbeitspaket behandelt.

## Wiedereinstiegspunkt

Phase 1: Baseline der fünf Dateien bestätigen und Formatierung auf Scope begrenzen.

## Abschlusskriterien

- genau fünf Dateien geändert
- Änderungen sind rein formatbedingt
- `./.venv/bin/python -m ruff format --check . --exclude tmp` ist grün
- relevante Tests bleiben grün

## Erfahrungsbericht

Auslöser geprüft: E1 | E2 | E3 | E4 | E5 | keiner
Bericht erforderlich: nein
Begründung:
Reine Altbestands-Formatbereinigung ist grundsätzlich kein systemischer
Lernbefund, sofern keine neue Checker-Lücke oder Prozessabweichung sichtbar wird.

Protokoll (Format, Pflichtfelder, Ablageort): `erfahrungsbericht-protokoll.md`

Ablageort: `.agent-box/evidence/erfahrungsberichte/YYYY-MM-DD-EB-<kurzbeschreibung>.md`
