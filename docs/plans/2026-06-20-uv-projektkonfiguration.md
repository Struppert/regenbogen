# Plan: uv-Projektkonfiguration

Status: abgeschlossen
Datum: 2026-06-20
Bearbeiter: Codex

## Aufgabe

`uv` fuer das Projekt einrichten.

Gewuenschter Schnitt:

- `pyproject.toml` erstellen
- keine `uv.lock`
- keine `requirements.txt`
- Runtime- und Entwicklungsabhaengigkeiten im `pyproject.toml` beschreiben

## Betroffene Raeume

- Projektmetadaten:
  - `pyproject.toml`
- Dokumentation:
  - `INSTALLATION.md`
  - `README.md`
- Git-Artefakte:
  - `.gitignore`

## Nicht-Ziele

- kein Lockfile
- kein Wechsel auf Poetry/Hatch als Bedienoberflaeche
- keine neue Runtime-Abhaengigkeit ueber den bereits festgelegten HTTP-Client
  hinaus
- keine Produktcode-Aenderung

## Schreibrechte

Die Aenderung an `pyproject.toml` ist geschuetzt und durch den Nutzer fuer
diesen Schnitt explizit freigegeben.

## Erwartete Aenderungen

1. `pyproject.toml` mit PEP-621-Metadaten erstellen.
2. Runtime-Dependency `httpx` eintragen.
3. Dev-Extra mit `pytest`, `ruff`, `mypy` eintragen.
4. `pytest` fuer `src`-Layout konfigurieren.
5. Installationsdoku auf `uv` aktualisieren.
6. Validierung ueber die `.venv` ausfuehren.

## Testpflicht

- Import-/Layer-Check
- volle Pytest-Suite
- Ruff Check
- Ruff Format-Check
- Mypy

## Abbruchbedingungen

- H8, falls eine weitere nicht freigegebene Runtime-Dependency noetig wuerde
- SA4, falls `uv` oder die lokale Umgebung die Installation nicht ausfuehren kann
- SA1/SA2/SA3 bei roten Tests, Lint oder Typecheck

## Wiedereinstiegspunkt

1. `pyproject.toml` schreiben
2. `.venv` mit `uv pip install -e ".[dev]"` aktualisieren
3. Validierung ausfuehren

## Abschlusskriterien

- `pyproject.toml` existiert
- kein `uv.lock`
- kein `requirements.txt`
- Tests und Checks laufen aus der `.venv`

## Ergebnis

- `pyproject.toml` erstellt
- `.gitignore` um `*.egg-info/` ergaenzt
- `INSTALLATION.md` und `README.md` auf uv-basierte Einrichtung aktualisiert
- Installation mit `uv pip install --python .venv/bin/python -e ".[dev]"`
  erfolgreich
- kein `uv.lock`
- keine `requirements.txt`

Validierung:

- `.venv/bin/python -m pytest`: 28 passed
- `.venv/bin/python tools/check_import_layers.py --preflight src tests tools`:
  gruen
- `.venv/bin/python -m ruff check .`: gruen
- `.venv/bin/python -m mypy src`: gruen
- `.venv/bin/python -m ruff format --check .`:
  gruen
- globale Ruff-Formatierung wurde nach expliziter Freigabe fuer geschuetzte
  Dateien einmalig ausgefuehrt
