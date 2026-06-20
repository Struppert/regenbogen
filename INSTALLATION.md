# Installation

## uv

Das Projekt verwendet `uv` fuer die lokale Python-Umgebung.

Einrichtung aus dem Projektroot:

```bash
uv venv .venv
uv pip install --python .venv/bin/python -e ".[dev]"
```

Das Projekt fuehrt bewusst kein `uv.lock` und keine `requirements.txt`.
Die kanonische Dependency-Spur ist `pyproject.toml`.

## Runtime-Dependency

Dieses Projekt verwendet `httpx` fuer den Wetter- und PLZ-HTTP-Client.

## Entwicklungsabhaengigkeiten

Fuer Validierung und Tests werden ueber das `dev`-Extra installiert:

- `pytest`
- `ruff`
- `mypy`

## Optionale GUI-Abhaengigkeit

Die CLI funktioniert ohne Tkinter.
Die GUI benoetigt die Tk-Plattformbindung der lokalen Python-Installation.
Je nach Distribution muss ein zusaetzliches Systempaket installiert werden,
z. B. `python3-tk` oder `tk`.
