# Abbruch: Globaler Format-Check rot

Aufgabe:
uv-Projektkonfiguration einrichten.

Zeitpunkt:
2026-06-20

Abbruchklasse: SOFT

Abbruchregel:
SA2 Format-Check rot

Betroffene Dateien:
- src/regenbogen/domain/regenbogen.py
- src/regenbogen/system/core/optische_bedingungen.py
- src/regenbogen/system/core/sonnenstand.py
- src/regenbogen/system/core/wahrscheinlichkeit_use_case.py
- tests/domain/test_regenbogen_optik.py
- tests/system/test_logging.py
- tools/check_agent_docs_consistency.py
- tools/check_import_layers.py
- tools/instantiate/instantiate_project_box.py
- tools/resolve_test_obligations.py

Letzter sicherer Zustand:
uv-Konfiguration ist eingerichtet. Tests, Import-/Layer-Check, Ruff-Lint und
Mypy sind gruen. Die in diesem Schnitt beruehrten Python-Dateien bestehen den
Format-Check.

Beobachtete Evidence:
Der globale Befehl `.venv/bin/python -m ruff format --check .` meldet 10
Dateien, die reformatiert wuerden. Darunter liegen geschuetzte Tool-Dateien.

Keine Vermutungen:
Es wurde nicht angenommen, dass eine globale Formatierung in diesem Schnitt
erlaubt ist. Geschuetzte Dateien wurden nicht mechanisch formatiert.

Empfohlene nächste Entscheidung:
Separaten Format-Schnitt freigeben, wenn das Projekt global mit Ruff formatiert
werden soll. Dann muessen die geschuetzten Tool-Dateien explizit Teil der
Freigabe sein.

## Aufloesung

Zeitpunkt:
2026-06-20

Der Nutzer hat Ruff fuer alle geschuetzten Dateien fuer einen Durchlauf
freigegeben.

Ausgefuehrt:

```text
.venv/bin/python -m ruff format .
```

Ergebnis:

```text
10 files reformatted, 23 files left unchanged
```

Anschliessende Validierung:

```text
.venv/bin/python -m ruff format --check .
→ 33 files already formatted

.venv/bin/python -m ruff check .
→ All checks passed

.venv/bin/python -m pytest
→ 28 passed

.venv/bin/python -m mypy src
→ Success: no issues found in 20 source files

.venv/bin/python tools/check_import_layers.py --preflight src tests tools
→ PREFLIGHT IMPORT-LAYER OK
```
