# Plan: RegenbogenWahrscheinlichkeit — Eintragstiefe minimal → vollständig

Status: abgeschlossen
Datum: 2026-06-21
Bearbeiter: Dieter Haag

## Aufgabe

Den Glossar-Eintrag `RegenbogenWahrscheinlichkeit` in `glossar-domain.md` von
`Eintragstiefe: minimal` auf `Eintragstiefe: vollständig` upgraden.

Primärer Zweck: Erprobung des v0.2.7-Checker-Stands auf neuem Glossar-Content
(Nachweis, dass die Brownfield-Migration korrekt abgeschlossen ist und die neue
Checker-Logik fehlerfrei funktioniert). Sekundärer Zweck: echte inhaltliche Lücke
schließen — die `Abgrenzung` zwischen `RegenbogenWahrscheinlichkeit` und
`RegenbogenSichtbarkeit` fehlt, obwohl beide Scores in [0, 100] liegen.

Upgrade auf vollständig erfordert keinen Sprechakt (Glossar-Regel: „nur Pflege").

## Betroffene Räume

```text
glossar-domain.md           Zeile 152–168 (Eintrag RegenbogenWahrscheinlichkeit)
```

Kein Produktionscode, keine Tests, keine Box-Regeldokumente.

## Nicht-Ziele

- Andere Einträge upgraden
- `RegenbogenSichtbarkeit` oder andere Domain-Terme ändern
- Produktionscode oder Tests anpassen
- Sprechakt anlegen
- `learning-matrix.md` aktualisieren

## Schreibrechte

`glossar-domain.md` ist eine geschützte Datei (AGENTS.md §9, preserve-dominant).
Schreibrecht ausschließlich für den Eintrag `RegenbogenWahrscheinlichkeit`,
Zeilen 152–168. Alle anderen Einträge bleiben unberührt.

## Erwartete Änderungen

Vorher (minimal):

```markdown
### RegenbogenWahrscheinlichkeit

**Semantischer Raum:** domain
**Eintragstiefe:** minimal

**Bedeutung:**
Prozentwert in [0, 100] fuer die Wahrscheinlichkeit eines Regenbogens.

**Invarianten:**
- Ohne Sonnenschein: 0.
- Ohne Regen: 0.

**Projektionen:**
- Code: src/regenbogen/domain/regenbogen.py
- Tests: tests/domain/test_regenbogen.py

**Migrationsstatus:** canonical
```

Nachher (vollständig) — inhaltliche Basis ist `src/regenbogen/domain/regenbogen.py`:

```markdown
### RegenbogenWahrscheinlichkeit

**Semantischer Raum:** domain
**Eintragstiefe:** vollständig

**Bedeutung:**
Prozentwert in [0, 100] für die domänenlogische Einschätzung,
ob die Grundbedingungen für einen sichtbaren Regenbogen erfüllt sind.
Berücksichtigt Sonnenschein-Intensität (Gewicht 0,6) und
Regen-Intensität (Gewicht 0,4) sowie optional den geometrischen
Sonnenstands-Faktor.

**Invarianten:**
- Ohne Sonnenschein: 0.
- Ohne Regen: 0.
- Wert liegt in [0, 100].
- Der Sonnenstand ist optional; fehlt er, entfällt der geometrische Faktor.

**Erlaubt:**
- Alle Kombinationen aus positivem Sonnenschein und positivem Regen.
- `sonnenstand=None` (kein Geometrie-Einfluss).

**Verboten:**
- Werte außerhalb [0, 100].
- Interpretation als Sichtbarkeits-Score (das ist RegenbogenSichtbarkeit).
- Gleichsetzung mit der physikalischen Auftrittswahrscheinlichkeit
  eines Meteorologieereignisses.

**Projektionen:**
- Code: src/regenbogen/domain/regenbogen.py
- Tests: tests/domain/test_regenbogen.py

**Abgrenzung:**
- `RegenbogenSichtbarkeit`: bewertet die *optische Qualität* eines Bogens
  über 7 multiplikativ verknüpfte Faktoren (Sonnenstands-, Direktlicht-,
  Regen-, Tropfenqualitäts-, Sicht-, Hintergrundkontrast-, Phasenfaktor).
  Beide Scores liegen in [0, 100]; Wahrscheinlichkeit fragt „Grundbedingung
  erfüllt?", Sichtbarkeit fragt „Wie gut sieht man ihn?".
- `SonnenscheinAnteil`, `RegenIntensitaet`: Eingaben, keine aggregierten Scores.

**Migrationsstatus:** canonical
```

Netto-Delta: `Eintragstiefe` → vollständig; `Bedeutung` ausgebaut; `Erlaubt` /
`Verboten` / `Abgrenzung` neu.

## Testpflicht

Nach der Änderung volle Check-Suite auf Branch `brownfield/v0.2.3-to-v0.2.7`:

```text
python tools/check_agent_docs_consistency.py --instantiated
python tools/check_import_layers.py --preflight src tests tools
python tools/resolve_test_obligations.py --selfcheck --instantiated
python -m ruff check . --exclude tmp
python -m ruff format --check . --exclude tmp
python -m mypy src
python -m pytest
```

Alle sieben Checks müssen identisch grün sein wie die Migration-Baseline.
Jede Abweichung ist ein Blocker.

## Abbruchbedingungen

- Checker meldet ERROR oder neuen WARN für `glossar-domain.md`.
- Irgendeiner der sieben Checks wird rot (war vorher grün).
- Der Eintrag-Inhalt widerspricht dem Quellcode in `regenbogen.py` / `regenbogen_optik.py`.

## Wiedereinstiegspunkt

`glossar-domain.md` Zeile 152 — Eintrag bleibt in bearbeitetem Zustand, alle anderen
Einträge und Dateien unverändert.

## Abschlusskriterien

- `glossar-domain.md` Zeile 155 zeigt `**Eintragstiefe:** vollständig`.
- Alle sieben Checks identisch grün wie Baseline.
- Keine anderen Dateien geändert.

## Erfahrungsbericht

Nach Abschluss immer schreiben.

Protokoll (Format, Pflichtfelder, Ablageort): `erfahrungsbericht-protokoll.md`

Ablageort: `tmp/erfahrungsberichte/2026-06-21-EB-glossar-regenbogenwahrscheinlichkeit-vollstaendig.md`
