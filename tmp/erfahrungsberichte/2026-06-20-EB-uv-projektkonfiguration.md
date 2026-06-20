# Erfahrungsbericht: uv-Projektkonfiguration

Zeitpunkt: 2026-06-20
Bezug auf Plan: `docs/plans/2026-06-20-uv-projektkonfiguration.md`

## Kontext

Das Projekt sollte eine explizite `uv`-basierte Dependency-Spur bekommen:
`pyproject.toml`, aber kein `uv.lock` und keine `requirements.txt`.

## Beobachtungen

1. `uv` war lokal bereits installiert.
2. Das Repo hatte vorher keine Projektmetadaten-Datei fuer Dependencies.
3. Die vorhandene `.venv` konnte weiterverwendet werden.
4. `uv pip install -e ".[dev]"` erzeugte kein `uv.lock`.

## Was gut funktioniert hat

- `pyproject.toml` konnte als einzige kanonische Dependency-Spur eingefuehrt
  werden.
- `pytest` kann jetzt ohne `PYTHONPATH=src` laufen, weil `pyproject.toml`
  `pythonpath = ["src"]` setzt.
- Runtime-Dependency und Dev-Abhaengigkeiten sind getrennt.
- CLI-Skripte `regenbogen` und `regenbogen-gui` sind als Einstiegspunkte
  definiert.

## Reibungspunkte

- Der globale Ruff-Format-Check war zunaechst rot auf bereits vorhandenen
  Dateien, darunter geschuetzte Tools. Nach expliziter Freigabe wurde ein
  einmaliger globaler Ruff-Formatlauf ausgefuehrt.
- Das Projekt hat jetzt eine echte Projektmetadaten-Datei; damit werden
  kuenftige Dependency-Aenderungen sichtbarer und sollten weiter ueber
  Sprechakt/Freigabe laufen.

## Lernwert fuer das Priming

Dieser Schnitt zeigt, dass eine Infrastrukturverbesserung auch dann sinnvoll
abgeschlossen werden kann, wenn ein globaler Check einen passiven Altbefund
meldet. Wichtig ist, den Befund nicht durch unerlaubte Nebenreparaturen zu
verdecken.

## Naechste Folgerung

Die volle Standardvalidierung ist nach dem freigegebenen Formatlauf gruen.
