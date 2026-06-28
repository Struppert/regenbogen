# Abbruch: PLZ-Validierung blockiert

Aufgabe:
Echte PLZ-Bestimmung fuer Standortkoordinaten einfuehren.

Zeitpunkt:
2026-06-20

Abbruchklasse: SOFT

Abbruchregel:
SA4 technischer Build-/Installationsfehler

Betroffene Dateien:
- src/regenbogen/infrastructure/plz_lookup.py
- src/regenbogen/adapters/wiring.py
- tests/infrastructure/test_plz_lookup.py
- README.md
- docs/plans/2026-06-20-echte-plz-bestimmung.md

Letzter sicherer Zustand:
Implementierung und Doku sind geschrieben. Import-/Layer-Check und
`compileall` laufen gruen.

Beobachtete Evidence:
- `python tools/check_import_layers.py --preflight src tests tools`:
  PREFLIGHT IMPORT-LAYER OK
- `python -m compileall src tests`: erfolgreich
- `python -m pytest ...`: `/usr/bin/python: No module named pytest`
- direkter Adaptercheck: `ModuleNotFoundError: No module named 'httpx'`

Keine Vermutungen:
Es wurde nicht angenommen, dass die Tests in einer vollstaendig installierten
Umgebung gruen waeren. Die Validierung bleibt offen.

Empfohlene nächste Entscheidung:
Projektabhaengigkeiten lokal installieren oder eine definierte Projektumgebung
bereitstellen, dann Pytest und den direkten Adaptercheck erneut ausfuehren.

## Aufloesung

Zeitpunkt:
2026-06-20

Die benoetigten Pakete wurden mit `uv` in die vorhandene lokale `.venv`
installiert:

```text
httpx
pytest
ruff
mypy
```

Danach liefen die Validierungen erfolgreich:

```text
PYTHONPATH=src .venv/bin/python -m pytest tests/infrastructure/test_plz_lookup.py tests/system/test_use_case.py tests/system/test_winkelmodell.py
→ 10 passed

PYTHONPATH=src .venv/bin/python -m pytest
→ 28 passed

python tools/check_import_layers.py --preflight src tests tools
→ PREFLIGHT IMPORT-LAYER OK
```

Der direkte Adaptercheck fuer `72138` lieferte:

```text
StandortKoordinaten(latitude=48.5314, longitude=9.1386, zeitzone='Europe/Berlin')
```
