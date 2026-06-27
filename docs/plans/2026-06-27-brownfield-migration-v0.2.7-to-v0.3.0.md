# Plan: Brownfield-Migration box-python v0.2.7 → v0.3.0

Plan-ID: PLAN-2026-06-27-brownfield-v0.2.7-to-v0.3.0
Plan-Version: 1
Planstatus: abgeschlossen
Arbeitsmodus: AUSFUEHRUNG
Datum: 2026-06-27
Bearbeiter: Dieter Haag

## Ausführungsmandat

Mandatstatus: abgeschlossen
Freigegebene Plan-Version: 1
Freigabezeitpunkt: 2026-06-27
Freigabetext oder Freigabereferenz: "setze den Plan aktiv und starte die Ausführung" (Dieter Haag)
Freigegebener Scope: vollständiger Plan
Freigegebene geschützte Dateien: alle im Plan gelisteten Governance-Artefakte
Nicht freigegeben: Produktcode, src/, tests/, package-schema.md, Glossare, migration-bridges.md
Gültigkeit: bis Abschluss

## Mandatsrelevante Änderungen

Plan-Version erhöhen bei Änderung an Zielzustand, Scope, geschützten Dateien,
Semantik, Dependencies, öffentlicher API, Validierungs- oder Rollback-Grenze.

---

## Aufgabe

Brownfield-Migration Fall B: Box-Versionsmigration von v0.2.7 auf v0.3.0.

Die Migration umfasst vier Versionsschritte (v0.2.8, v0.2.9, v0.2.10, v0.3.0).
Die Kernneuerung ist `ausfuehrungsmandat-protokoll.md` (v0.3.0): Trennung von
semantischer Festlegung (Sprechakt) und Ausführungsberechtigung (Mandat/W0).

Herkunftsmarker: `.agent-box/instantiation.md` (Greenfield, Box-Version v0.2.7)

## Betroffene Räume

Ausschließlich Agenten-Box-Governance. Kein Produktcode, kein Fachcode, keine
Domain-Semantik, keine Tests, keine Dependencies.

## Nicht-Ziele

- Keine Produktcodeänderungen
- Kein Refactoring an `src/` oder `tests/`
- Keine neuen Fachbegriffe
- Keine Schemaänderungen an `package-schema.md`
- Keine Anpassung der Checker-Logik über Template-Replace hinaus

---

## Historischer Baseline-Anker

Commit: `09969c9` — "Brownfield-Migration box-python v0.2.3 → v0.2.7 + Glossar-Test"

Dieser Commit ist der Abschlusspunkt der letzten Migration. Lokale Divergenz
gegen das v0.2.7-Template wird gegen diesen Anker bestimmt.

## Aktuelle Ausführungsbaseline (vor Migration)

```text
check_agent_docs_consistency.py --instantiated  → OK (instantiated)
check_import_layers.py --preflight src tests tools → OK (38 Dateien)
resolve_test_obligations.py --selfcheck --instantiated → OK
pytest                                          → 64 passed
ruff check / ruff format --check               → OK (ohne tmp/)
mypy src                                        → Success, 22 source files
```

---

## Datei-Aktionsmatrix

### add — neue Template-Artefakte

| Datei | Herkunft | Bemerkung |
|---|---|---|
| `ausfuehrungsmandat-protokoll.md` | v0.3.0 | Kernartefakt dieser Migration |
| `blocker-und-abbruch-protokoll.md` | v0.2.10 | H1-H10, SA1-SA6, Abbruch-Evidence |

### merge — Box-Regeln mit lokalen Anpassungen

| Datei | Änderungsquelle | Inhalt der Änderung |
|---|---|---|
| `AGENTS.md` | v0.2.9, v0.3.0 | Router-Umbau, Abschnitt 3 Arbeitsmodus, Regel 12 (kein Mandat → keine Mutation), aktualisierte Routing-Tabelle |
| `preflight-checkliste.md` | v0.3.0 | Abschnitt 0a W0-Wirkungsgate vor P1 |
| `task-schnitt.md` | v0.2.9, v0.2.10 | „Blosse Teilbarkeit ist kein Schnittgrund", Abschnitt 4 Arbeitspaket/Phase-Modell |
| `sprechakt-protokoll.md` | v0.2.10, v0.3.0 | Status `widerrufen` ergänzt, §1 Ausfuehrungsmandat-Trennung explizit, §9 Wiedereinstieg nach Mandat-Prüfung |
| `regelmatrix.md` | v0.2.10, v0.3.0 | Zuständigkeitsmodell (statt Totalordnung), 3-Stufen-Schreibmodell (beschreibbar/geschützt/freigegeben) |
| `BROWNFIELD-MIGRATION.md` | v0.3.0 | §1 Zielmodell-Entscheidung ≠ Migrationsmandat, W0-Verweis |
| `docs/plans/template.md` | v0.3.0 | Plan-ID, Plan-Version, Planstatus, Arbeitsmodus, Mandatsfelder |
| `erfahrungsbericht-protokoll.md` | v0.2.9 | Erfahrungsbericht-Pflicht auf systemisch lernrelevante Auslöser begrenzt |

### replace — Tools ohne lokale Divergenz

| Datei | Bemerkung |
|---|---|
| `tools/check_agent_docs_consistency.py` | Prüfen ob lokal unverändert, dann ersetzen; sonst Drei-Wege-Merge |

### inspect → voraussichtlich entfernen

| Datei | Bemerkung |
|---|---|
| `AGENTS-COMPACT.md` | Seit v0.2.9 deprecated; entfernen wenn `AGENTS.md` als Router migriert ist |

### preserve — keine Template-Änderung, lokaler Projektinhalt

```text
package-schema.md
glossar-domain.md
glossar-system.md
glossar-meta.md
glossar-README.md
migration-bridges.md
test-obligations.md
learning-matrix.md
grundsatz.md
regentropfen-und-wetterdaten.md
```

---

## Interne Phasen

Phasengrenzen sind keine Benutzer-Checkpoints.

```text
Phase A — add:
  ausfuehrungsmandat-protokoll.md kopieren (aus tmp/agent-templates-main/box-python/)
  blocker-und-abbruch-protokoll.md kopieren

Phase B — AGENTS.md merge:
  Drei-Wege-Merge gegen Baseline-Anker (09969c9) und Template v0.3.0
  Neue Abschnitte: Arbeitsmodus (§3), Regel 12, Routing-Tabelle anpassen

Phase C — preflight/task-schnitt/sprechakt merge:
  preflight-checkliste.md: W0 als §0a einfügen
  task-schnitt.md: Arbeitspaket/Phase-Modell in §4 mergen
  sprechakt-protokoll.md: widerrufen-Status, Mandat-Trennung in §1/§9

Phase D — regelmatrix/BROWNFIELD merge:
  regelmatrix.md: 3-Stufen-Modell, Zuständigkeitsmodell
  BROWNFIELD-MIGRATION.md: §1 Migrationsmandat-Trennung, W0-Verweis

Phase E — plan-template ersetzen:
  docs/plans/template.md mit neuem Format ersetzen

Phase F — checker replace:
  tools/check_agent_docs_consistency.py: Diff prüfen, dann ersetzen

Phase G — AGENTS-COMPACT.md entfernen

Phase H — Validierung:
  check_agent_docs_consistency.py --instantiated
  check_import_layers.py --preflight src tests tools
  resolve_test_obligations.py --selfcheck --instantiated
  pytest
```

## Gebündelte mechanische Änderungen

Die Routing-Tabelle in `AGENTS.md` (neue Zeile `ausfuehrungsmandat-protokoll.md`)
und alle zugehörigen Querverweise in den Merge-Dateien sind ein Arbeitspaket.

---

## Schreibrechte

Alle betroffenen Dateien sind Governance-Artefakte (geschützt gemäß regelmatrix.md).
Vollständige Freigabe aller gelisteten Dateien erforderlich, da die Migration
nur aus Governance-Änderungen besteht.

---

## Bereits erteilte Freigaben / Sprechakte

Keine. Mandatserteilung steht aus.

---

## Testpflicht

Ausschließlich Dokumenten-Checker und Struktur-Checker:

```bash
python tools/check_agent_docs_consistency.py --instantiated
python tools/check_import_layers.py --preflight src tests tools
python tools/resolve_test_obligations.py --selfcheck --instantiated
python -m pytest
```

Pytest läuft zur Regressionsprüfung (kein Produktcode betroffen, soll unverändert grün bleiben).

## Echter Task-Schnitt

Schnitt nötig: nein
Begründung: Alle Änderungen liegen im selben semantischen Raum (Agenten-Governance),
haben dieselbe Schreibrechte-Klasse (explizite Mandat-Freigabe für alle Governance-Dateien),
und die Validierungs- und Rollback-Grenze ist identisch.

---

## Abbruchbedingungen

```text
BF3   geschützte Datei wäre ohne Migrationsentscheidung betroffen
BF5   Konflikt zwischen Template-Regel und lokaler Projektregel bei einem Merge
BF6   Tool-Ersetzung würde lokale Anpassungen überschreiben
BF7   Migration würde neue Projektsemantik ohne Sprechakt erzeugen
BF11  Baseline, Zielmodell, Migrationsplan und Evidence werden vermischt
```

Bei BF-Abbruch: Evidence in `.agent-box/migrations/` schreiben, keine weiteren
Dateien ändern.

---

## Wiedereinstiegspunkt

Migrationsevidence: `.agent-box/migrations/2026-06-27-v0.2.7-to-v0.3.0-evidence.md`

Bei Abbruch innerhalb einer Phase: Evidence dokumentiert letzten sicheren Zustand
und nächste offene Entscheidung.

---

## Abschlusskriterien

```text
✓ ausfuehrungsmandat-protokoll.md vorhanden und vollständig
✓ blocker-und-abbruch-protokoll.md vorhanden und vollständig
✓ AGENTS.md hat Arbeitsmodus-Abschnitt und Regel 12
✓ preflight-checkliste.md hat W0 als §0a
✓ regelmatrix.md hat 3-Stufen-Schreibmodell
✓ AGENTS-COMPACT.md entfernt
✓ docs/plans/template.md hat Mandatsfelder
✓ .agent-box/instantiation.md Box-Version auf v0.3.0 aktualisiert
✓ check_agent_docs_consistency.py --instantiated → OK
✓ check_import_layers.py → OK
✓ resolve_test_obligations.py --selfcheck --instantiated → OK
✓ pytest → 64 passed (keine Regression)
✓ Migrationsevidence abgeschlossen
```

---

## Erfahrungsbericht

Auslöser geprüft: E1 | E2 | E3 | E4 | E5
Bericht erforderlich: ja (E3 — neues Governance-Verfahren erkannt)
Begründung: Erste Migration in dieses neue Mandats-Modell (v0.3.0); E3 (neues
Governance-Verfahren) wahrscheinlich zutreffend.

Protokoll: `erfahrungsbericht-protokoll.md`
Ablageort: `tmp/erfahrungsberichte/YYYY-MM-DD-EB-brownfield-v0.2.7-to-v0.3.0.md`
