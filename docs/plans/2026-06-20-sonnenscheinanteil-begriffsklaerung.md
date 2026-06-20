aaffasdg    Plan: Sonnenscheinanteil statt Sonnenscheinwahrscheinlichkeit

Status: abgeschlossen
Datum: 2026-06-20
Bearbeiter: Codex

## Aufgabe

Die aktuelle Ausgabe `Sonnenschein (25 %)` wird leicht als
Sonnenscheinwahrscheinlichkeit verstanden. Tatsächlich berechnet das System
aber eine aus `sunshine_duration` abgeleitete Intensität beziehungsweise einen
Anteil der Stunde mit Sonnenschein:

```text
sonnenschein_intensitaet = min(sunshine_duration / 3600.0, 1.0)
```

Der Schnitt soll diese semantische Unschärfe beheben.

## Betroffene Räume

- `src/regenbogen/cli/`
  - menschenlesbare Ausgabe anpassen
- `src/regenbogen/system/core/`
  - nur prüfen; keine Modelländerung geplant, wenn die bestehende Ableitung
    korrekt bleibt
- `glossar-domain.md`
  - Begriff `SonnenscheinAnteil` oder präzisere Bedeutung von
    `sonnenschein_intensitaet` festlegen
- `MODELL-README.md`
  - Modellbeschreibung der Sonnenintensität präzisieren
- `README.md`
  - Programmdoku an geänderte Anzeige/Begriffe anpassen, falls betroffen
- `tests/`
  - Ausgabeformat und ggf. Modellbegriff testen

## Nicht-Ziele

- keine neue Wetterdatenquelle
- keine Änderung der numerischen Berechnung
- keine Einführung einer echten Sonnenscheinwahrscheinlichkeit
- keine Änderung der Regenbogen-Wahrscheinlichkeitsformel

## Schreibrechte

- erlaubt:
  - `src/`
  - `tests/`
  - `docs/plans/`
  - `tmp/erfahrungsberichte/`
  - `README.md`
  - `MODELL-README.md`
- explizit freigabepflichtig:
  - `glossar-domain.md`

Da der Nutzer Änderungen am Glossar ausdrücklich verlangt hat, ist eine
Änderung an `glossar-domain.md` für diesen Schnitt freigegeben, soweit sie auf
diese Begriffsklärung beschränkt bleibt.

## Erwartete Änderungen

1. Aktive Begriffe bestimmen:
   - `Sonnenschein`
   - `sonnenschein_intensitaet`
   - möglicher kanonischer Begriff `SonnenscheinAnteil`
2. Glossarentscheidung materialisieren:
   - entweder bestehenden Begriff ergänzen
   - oder neuen Fachbegriff `SonnenscheinAnteil` eintragen
3. CLI-/GUI-Format so ändern, dass nicht Wahrscheinlichkeit suggeriert wird.
4. Tests für Ausgabeformat anpassen/ergänzen.
5. `MODELL-README.md` aktualisieren.
6. `README.md` prüfen und bei Bedarf aktualisieren.

## Testpflicht

- CLI-/Format-Test für die menschenlesbare Ausgabe
- Domain-/Systemtests, falls der Begriff im Modellcode stärker sichtbar wird
- Vollständige Standardvalidierung:
  - Ruff Check
  - Ruff Format-Check
  - Mypy
  - Pytest
  - Import-/Layer-Check

## Sprechakte / Entscheidungen

### SP7

Der bisher aktiv genutzte Begriff `sonnenschein_intensitaet` ist im Code
vorhanden, aber im Glossar nicht als eigener Begriff vollständig geklärt.
Für diesen Schnitt ist eine Glossarklärung nötig.

### SP1

Wenn `SonnenscheinAnteil` als neuer fachlicher Begriff eingeführt wird, ist das
ein neuer Domain-Begriff. Der Nutzer hat die Glossaränderung für diesen Schnitt
angefordert; die Umsetzung muss dennoch explizit als fachliche Festlegung
dokumentiert werden.

Vorgeschlagene Festlegung:

```text
SonnenscheinAnteil:
  Anteil einer Bezugsstunde, in der direkte Sonneneinstrahlung beobachtet
  wurde. Wert in [0.0, 1.0]. Wird aus sunshine_duration / 3600 abgeleitet.
  Keine Wahrscheinlichkeit.
```

## Abbruchbedingungen

- H1, wenn die Glossaränderung über die freigegebene Begriffsklärung
  hinausgehen müsste
- H3, wenn Code, Modell-README und Glossar sich nicht konsistent auflösen
  lassen
- H4, wenn ein neuer Fachbegriff verwendet würde, ohne ihn im Glossar zu
  materialisieren
- SA1/SA2/SA3 bei roten Tests, Lint oder Typecheck

## Wiedereinstiegspunkt

Nach Freigabe dieses Plans:

1. Sprechakt-Artefakt für die Begriffsfestlegung schreiben
2. `glossar-domain.md` aktualisieren
3. Ausgabeformat ändern
4. Tests aktualisieren
5. `MODELL-README.md` und `README.md` nachziehen
6. Validierung ausführen

## Abschlusskriterien

- Die UI/CLI-Ausgabe suggeriert keine Sonnenscheinwahrscheinlichkeit mehr.
- Das Glossar enthält die fachliche Bedeutung des verwendeten Sonnenschein-
  Anteils.
- `MODELL-README.md` beschreibt die Ableitung eindeutig.
- Tests und Standardchecks sind grün.

## Ergebnis

- Sprechakt fuer `SonnenscheinAnteil` erstellt
- `glossar-domain.md` um `SonnenscheinAnteil` ergaenzt
- Ausgabeformat auf `Sonnenscheinanteil (... % der Stunde)` geaendert
- CLI-Format-Tests angepasst
- `MODELL-README.md` und `README.md` aktualisiert
