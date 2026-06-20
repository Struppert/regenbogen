# Instanziierung

Status: festgelegt
Sprechakttyp: Instanziierungs-Sprechakt
Box-Name: box-python
Box-Version: v0.2.3
Zeitpunkt-UTC: 2026-06-20T14:01:06+00:00
Formatregel: Markdown only

## Festgelegte Werte

```text
PROJECT_DISPLAY_NAME = Regenbogen
PYTHON_PACKAGE_NAME  = regenbogen
SOURCE_ROOT          = src
TEST_ROOT            = tests
DOCS_ROOT            = docs
TOOLS_ROOT           = tools
```

## Befehle

```text
IMPORT_LAYER_CHECK_CMD  = python tools/check_import_layers.py --preflight src tests tools
PYTHON_LINT_CMD         = python -m ruff check .
PYTHON_FORMAT_CHECK_CMD = python -m ruff format --check .
PYTHON_TYPECHECK_CMD    = python -m mypy src
PYTHON_TEST_CMD         = python -m pytest
FULL_VALIDATION_CMD     = python tools/check_agent_docs_consistency.py --instantiated && python tools/check_import_layers.py --preflight src tests tools && python tools/resolve_test_obligations.py --selfcheck --instantiated && python -m pytest
```

## Geänderte Dateien

- AGENTS.md
- AGENTS-COMPACT.md
- AGENT-SETUP.md
- package-schema.md
- preflight-checkliste.md
- regelmatrix.md
- test-obligations.md
- glossar-domain.md
- glossar-system.md
- migration-bridges.md
- tools/check_import_layers.py
- tools/resolve_test_obligations.py

## Angelegte Verzeichnisse

- .agent-box
- docs/sprechakte
- tmp/erfahrungsberichte
- src
- tests
- src/regenbogen
- src/regenbogen/system/ports

## Ausgeführte Post-Checks

- `python tools/check_agent_docs_consistency.py --instantiated`
- `python tools/check_import_layers.py --preflight src tests tools`
- `python tools/resolve_test_obligations.py --selfcheck --instantiated`

## Geltung

Dieses Artefakt ist der Nachweis des einmaligen Instanziierungs-Sprechakts.
Eine erneute Instanziierung ist verboten, außer sie wurde ausdrücklich
menschlich freigegeben und mit `--force` ausgeführt.
