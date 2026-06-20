# Instanziierung der Python-Agenten-Box

Dieses Verzeichnis enthält das einmalige Instanziierungswerkzeug der Box.
Es ist kein normales Agentenwerkzeug und kein Packaging-Setup.

## Regel

```text
tools/instantiate/* läuft genau einmal.
Nach .agent-box/instantiation.md ist erneute Instanziierung verboten.
```

Die Box verwendet **Markdown only**:

```text
kein JSON als Evidence
kein YAML als Konfiguration
kein zweiter maschinenlesbarer Wahrheitsraum
```

## Tool

```text
tools/instantiate/instantiate_project_box.py
```

Das Tool vollzieht den initialen Instanziierungs-Sprechakt:

```text
Template-Box -> lokale Projekt-Box
```

Es schreibt den Nachweis nach:

```text
.agent-box/instantiation.md
```

## Beispiel

```bash
python tools/instantiate/instantiate_project_box.py   --project-display-name Regenbogen   --source-root src   --test-root tests   --docs-root docs   --tools-root tools   --python-lint-cmd "python -m ruff check ."   --python-format-check-cmd "python -m ruff format --check ."   --python-typecheck-cmd "python -m mypy src"   --python-test-cmd "python -m pytest"   --full-validation-cmd "python tools/check_agent_docs_consistency.py --instantiated && python tools/check_import_layers.py --preflight src tests tools && python tools/resolve_test_obligations.py --selfcheck --instantiated && python -m pytest"
```

Wenn `--python-package-name` fehlt, wird er konservativ aus
`--project-display-name` abgeleitet:

```text
Regenbogen -> regenbogen
```

Ein expliziter Package-Name mit Großbuchstaben wird blockiert.


## Option `--skip-post-checks`

`--skip-post-checks` überspringt die Checks nach der Instanziierung. Nur verwenden,
wenn lokale Tool-Abhängigkeiten noch fehlen. Die Checks müssen nachgeholt werden.
