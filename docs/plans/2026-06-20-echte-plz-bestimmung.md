# Plan: Echte PLZ-Bestimmung fuer Standortkoordinaten

Status: abgeschlossen
Datum: 2026-06-20
Bearbeiter: Codex

## Aufgabe

Die bisherige Demo-Standorttabelle soll durch eine echte PLZ-Bestimmung
erweitert werden. Ziel ist, deutsche Postleitzahlen ueber einen externen
PLZ-Geocoding-Dienst in Koordinaten zu uebersetzen und fuer bekannte Orte eine
kleine lokale Fallback-Tabelle zu behalten.

Konkreter Nutzerfall: `72138` fuer Kirchentellinsfurt soll funktionieren.

## Betroffene Raeume

- `src/regenbogen/infrastructure/`
  - Standort-Adapter fuer PLZ-Aufloesung
- `src/regenbogen/adapters/`
  - Wiring auf den neuen Adapter umstellen
- `tests/`
  - Infrastrukturtests fuer erfolgreiche PLZ-Aufloesung, Fallback und
    unbekannte PLZ
- `README.md`
  - Beschreibung der Standortauflosung aktualisieren

## Nicht-Ziele

- keine Domain-Aenderung
- kein neuer Domain-Begriff
- keine neue Runtime-Dependency
- keine vollstaendige lokale deutsche PLZ-Datenbank
- keine neue Fehlerklasse fuer einen Standortdienst

## Schreibrechte

- erlaubt:
  - `src/`
  - `tests/`
  - `docs/plans/`
  - `tmp/erfahrungsberichte/`
  - `README.md`

## Erwartete Aenderungen

1. `DemoStandortLookup` zu einem PLZ-gestuetzten Standortlookup erweitern.
2. Externe PLZ-Aufloesung ueber HTTP implementieren.
3. Lokale Fallback-Daten fuer Berlin, Muenchen und Kirchentellinsfurt halten.
4. Wiring auf den neuen Namen umstellen.
5. Tests ohne produktiven HTTP-Zugriff ergaenzen.
6. Programmdoku nachziehen.

## Testpflicht

- Infrastrukturtests mit gefaktem HTTP-Client
- Import-/Layer-Check
- relevante Pytest-Tests

## Abbruchbedingungen

- H8, falls eine neue Runtime-Dependency noetig waere
- SP3, falls eine neue Fehlerbedeutung fuer einen Standortdienst noetig wird
- H2, falls der Import-/Layer-Check eine neue unbekannte Verletzung zeigt

## Wiedereinstiegspunkt

1. Standortadapter implementieren
2. Wiring aktualisieren
3. Tests ergaenzen
4. README aktualisieren
5. Validierung ausfuehren

## Abschlusskriterien

- `72138` wird in Koordinaten fuer Kirchentellinsfurt uebersetzt
- Tests pruefen HTTP-Erfolg, lokalen Fallback und unbekannte PLZ
- README beschreibt nicht mehr nur eine reine Demo-Tabelle

## Ergebnis

- Standortadapter auf PLZ-gestuetzte HTTP-Aufloesung mit lokalem Fallback
  erweitert
- Wiring auf den neuen Adapter umgestellt
- Infrastrukturtests fuer HTTP-Erfolg, lokalen Fallback, unbekannte PLZ und
  Ortsfallback ergaenzt
- README aktualisiert
- Import-/Layer-Check gruen
- `compileall` gruen
- Pytest und direkter Laufcheck nach Installation in `.venv` erfolgreich

Validierung nach Wiedereinstieg:

- `PYTHONPATH=src .venv/bin/python -m pytest tests/infrastructure/test_plz_lookup.py tests/system/test_use_case.py tests/system/test_winkelmodell.py`:
  10 passed
- `PYTHONPATH=src .venv/bin/python -m pytest`:
  28 passed
- direkter Adaptercheck fuer `72138`:
  `StandortKoordinaten(latitude=48.5314, longitude=9.1386, zeitzone='Europe/Berlin')`
