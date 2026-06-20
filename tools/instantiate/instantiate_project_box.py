#!/usr/bin/env python3
"""
instantiate_project_box.py — einmalige Materialisierung von box-python.

Dieses Tool ist kein Packaging-Setup und kein normaler Projekt-Checker.
Es vollzieht den initialen Instanziierungs-Sprechakt:

    Template-Box -> instanziierte Projekt-Box

Die Box arbeitet nach der Regel: Markdown only.
Das Tool liest keine JSON-/YAML-Konfiguration und schreibt keinen JSON-Status.
Der Nachweis des vollzogenen Sprechakts ist:

    .agent-box/instantiation.md

Nach erfolgreicher Instanziierung verweigert das Tool weitere Läufe, außer
--force wird ausdrücklich gesetzt.
"""

from __future__ import annotations

import argparse
import keyword
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

ROOT_MARKER = Path("AGENTS.md")
TEMPLATE_MANIFEST = Path(".agent-box-template.md")
INSTANTIATION_FILE = Path(".agent-box/instantiation.md")
BOX_VERSION = "v0.2.3"
BOX_NAME = "box-python"

TEMPLATE_FILES = [
    "AGENTS.md",
    "AGENTS-COMPACT.md",
    "AGENT-SETUP.md",
    "package-schema.md",
    "preflight-checkliste.md",
    "regelmatrix.md",
    "task-schnitt.md",
    "test-obligations.md",
    "glossar-README.md",
    "glossar-domain.md",
    "glossar-system.md",
    "migration-bridges.md",
    "sprechakt-protokoll.md",
    "learning-matrix.md",
    "erfahrungsbericht-protokoll.md",
    "tools/check_import_layers.py",
    "tools/resolve_test_obligations.py",
    "docs/plans/template.md",
]

POST_CHECKS = [
    "python tools/check_agent_docs_consistency.py --instantiated",
    "python tools/check_import_layers.py --preflight <SOURCE_ROOT> <TEST_ROOT> <TOOLS_ROOT>",
    "python tools/resolve_test_obligations.py --selfcheck --instantiated",
]


@dataclass(frozen=True)
class Replacement:
    name: str
    value: str

    @property
    def token(self) -> str:
        return "<" + self.name + ">"


def ensure_project_root() -> None:
    if not ROOT_MARKER.exists():
        raise SystemExit(
            "AGENTS.md nicht gefunden. Starte tools/instantiate/instantiate_project_box.py "
            "aus dem Root des Zielprojekts."
        )
    if not TEMPLATE_MANIFEST.exists():
        raise SystemExit(
            f"Template-Manifest fehlt: {TEMPLATE_MANIFEST}. "
            "Die Box ist unvollständig oder wurde bereits falsch instanziiert."
        )


def non_empty(value: str | None, label: str) -> str:
    if value is None or not value.strip():
        raise SystemExit(f"Pflichtparameter fehlt oder ist leer: {label}")
    return value.strip()


def derive_python_package_name(display_name: str) -> str:
    value = display_name.strip().replace("-", "_").replace(" ", "_")
    value = re.sub(r"[^0-9A-Za-z_]", "_", value)
    value = re.sub(r"_+", "_", value).strip("_").lower()
    if not value:
        raise SystemExit(
            "Aus project-display-name konnte kein Python-Package-Name abgeleitet werden."
        )
    return value


def validate_python_package_name(value: str) -> str:
    if value != value.lower():
        raise SystemExit(
            "Python-Package-Name muss kleingeschrieben sein. "
            f"Erhalten: {value!r}. Beispiel: regenbogen."
        )
    if not re.fullmatch(r"[a-z_][a-z0-9_]*", value):
        raise SystemExit(
            "Python-Package-Name muss ein einfacher Python-Identifier sein "
            "([a-z_][a-z0-9_]*)."
        )
    if keyword.iskeyword(value):
        raise SystemExit(
            "Python-Package-Name darf kein Python-Schluesselwort sein. "
            f"Erhalten: {value!r}. Beispiel: regenbogen."
        )
    return value


def build_replacements(args: argparse.Namespace) -> list[Replacement]:
    display_name = non_empty(args.project_display_name, "--project-display-name")
    package_name = (
        args.python_package_name.strip()
        if args.python_package_name
        else derive_python_package_name(display_name)
    )
    package_name = validate_python_package_name(package_name)

    values = {
        "PROJECT_DISPLAY_NAME": display_name,
        "PYTHON_PACKAGE_NAME": package_name,
        "SOURCE_ROOT": non_empty(args.source_root, "--source-root"),
        "TEST_ROOT": non_empty(args.test_root, "--test-root"),
        "DOCS_ROOT": non_empty(args.docs_root, "--docs-root"),
        "TOOLS_ROOT": non_empty(args.tools_root, "--tools-root"),
        "IMPORT_LAYER_CHECK_CMD": args.import_layer_check_cmd
        or "python tools/check_import_layers.py --preflight src tests tools",
        "PYTHON_LINT_CMD": args.python_lint_cmd or "python -m ruff check .",
        "PYTHON_FORMAT_CHECK_CMD": args.python_format_check_cmd
        or "python -m ruff format --check .",
        "PYTHON_TYPECHECK_CMD": args.python_typecheck_cmd or "python -m mypy src",
        "PYTHON_TEST_CMD": args.python_test_cmd or "python -m pytest",
        "FULL_VALIDATION_CMD": args.full_validation_cmd or "python -m pytest",
    }
    return [Replacement(k, v) for k, v in values.items()]


def replace_in_files(replacements: list[Replacement]) -> list[Path]:
    changed: list[Path] = []
    for rel in TEMPLATE_FILES:
        path = Path(rel)
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        new = text
        for repl in replacements:
            new = new.replace(repl.token, repl.value)
        if new != text:
            path.write_text(new, encoding="utf-8")
            changed.append(path)
    return changed


def replacement_map(replacements: list[Replacement]) -> dict[str, str]:
    return {r.name: r.value for r in replacements}


def create_directories(values: dict[str, str]) -> list[Path]:
    dirs = [
        Path(".agent-box"),
        Path(values["DOCS_ROOT"]) / "plans",
        Path(values["DOCS_ROOT"]) / "sprechakte",
        Path("tmp") / "erfahrungsberichte",
        Path(values["SOURCE_ROOT"]),
        Path(values["TEST_ROOT"]),
        Path(values["SOURCE_ROOT"]) / values["PYTHON_PACKAGE_NAME"],
        Path(values["SOURCE_ROOT"])
        / values["PYTHON_PACKAGE_NAME"]
        / "system"
        / "ports",
    ]
    created: list[Path] = []
    for d in dirs:
        if not d.exists():
            d.mkdir(parents=True, exist_ok=True)
            created.append(d)
    return created


def remove_generic_bridge_example() -> bool:
    path = Path("migration-bridges.md")
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")

    marker = "<!-- TEMPLATE-BRIDGE-EXAMPLE-BEGIN -->"
    end = "<!-- TEMPLATE-BRIDGE-EXAMPLE-END -->"
    if marker in text and end in text:
        pattern = re.compile(re.escape(marker) + r".*?" + re.escape(end), re.DOTALL)
        new = pattern.sub(
            "<!-- Kein aktiver Bridge-Eintrag nach Instanziierung. -->", text
        )
    else:
        # Ältere Template-Fassung ohne Marker: den BR-001-Beispielblock entfernen.
        pattern = re.compile(
            r"Beispiel \(Template — beim Instanziieren ersetzen oder entfernen\):\n\n"
            r"```text\nBR-001:.*?```",
            re.DOTALL,
        )
        new = pattern.sub("Kein aktiver Bridge-Eintrag nach Instanziierung.", text)

    if new != text:
        path.write_text(new, encoding="utf-8")
        return True
    return False


def fill_test_commands(values: dict[str, str]) -> bool:
    path = Path("tools/resolve_test_obligations.py")
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    test_cmd = values["PYTHON_TEST_CMD"]
    new = text

    # v0.2: Beim initialen Sprechakt wird jede Testgruppe konservativ auf den
    # Projekt-Testbefehl gesetzt. Feinere Befehle sind spätere Projektarbeit.
    labels = [
        "domain-tests",
        "negative-domain-tests",
        "system-tests",
        "policy-tests",
        "infrastructure-tests",
        "contract-or-fake-tests",
        "adapter-tests",
        "mapping-tests",
        "cli-tests",
        "smoke-tests",
        "affected-product-tests",
    ]
    for label in labels:
        new = re.sub(
            rf'("{re.escape(label)}"\s*:\s*)""',
            lambda match: match.group(1) + repr(test_cmd),
            new,
        )

    if new != text:
        path.write_text(new, encoding="utf-8")
        return True
    return False


def write_instantiation_markdown(
    values: dict[str, str],
    changed_files: list[Path],
    created_dirs: list[Path],
    checks: list[str],
) -> None:
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    changed = "\n".join(f"- {p.as_posix()}" for p in changed_files) or "- keine"
    created = "\n".join(f"- {p.as_posix()}" for p in created_dirs) or "- keine"
    check_lines = "\n".join(f"- `{c}`" for c in checks) or "- keine"
    text = f"""# Instanziierung

Status: festgelegt
Sprechakttyp: Instanziierungs-Sprechakt
Box-Name: {BOX_NAME}
Box-Version: {BOX_VERSION}
Zeitpunkt-UTC: {now}
Formatregel: Markdown only

## Festgelegte Werte

```text
PROJECT_DISPLAY_NAME = {values["PROJECT_DISPLAY_NAME"]}
PYTHON_PACKAGE_NAME  = {values["PYTHON_PACKAGE_NAME"]}
SOURCE_ROOT          = {values["SOURCE_ROOT"]}
TEST_ROOT            = {values["TEST_ROOT"]}
DOCS_ROOT            = {values["DOCS_ROOT"]}
TOOLS_ROOT           = {values["TOOLS_ROOT"]}
```

## Befehle

```text
IMPORT_LAYER_CHECK_CMD  = {values["IMPORT_LAYER_CHECK_CMD"]}
PYTHON_LINT_CMD         = {values["PYTHON_LINT_CMD"]}
PYTHON_FORMAT_CHECK_CMD = {values["PYTHON_FORMAT_CHECK_CMD"]}
PYTHON_TYPECHECK_CMD    = {values["PYTHON_TYPECHECK_CMD"]}
PYTHON_TEST_CMD         = {values["PYTHON_TEST_CMD"]}
FULL_VALIDATION_CMD     = {values["FULL_VALIDATION_CMD"]}
```

## Geänderte Dateien

{changed}

## Angelegte Verzeichnisse

{created}

## Ausgeführte Post-Checks

{check_lines}

## Geltung

Dieses Artefakt ist der Nachweis des einmaligen Instanziierungs-Sprechakts.
Eine erneute Instanziierung ist verboten, außer sie wurde ausdrücklich
menschlich freigegeben und mit `--force` ausgeführt.
"""
    INSTANTIATION_FILE.parent.mkdir(parents=True, exist_ok=True)
    INSTANTIATION_FILE.write_text(text, encoding="utf-8")


def instantiate_checks(commands: list[str], values: dict[str, str]) -> list[str]:
    expanded = []
    for cmd in commands:
        expanded.append(
            cmd.replace("<SOURCE_ROOT>", values["SOURCE_ROOT"])
            .replace("<TEST_ROOT>", values["TEST_ROOT"])
            .replace("<TOOLS_ROOT>", values["TOOLS_ROOT"])
        )
    return expanded


def run_post_checks(commands: list[str]) -> None:
    for cmd in commands:
        print(f"[check] {cmd}")
        result = subprocess.run(cmd, shell=True)
        if result.returncode != 0:
            raise SystemExit(f"Post-Check fehlgeschlagen: {cmd}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Instanziiert box-python einmalig in einem Zielprojekt."
    )
    parser.add_argument("--project-display-name", required=True)
    parser.add_argument("--python-package-name")
    parser.add_argument("--source-root", default="src")
    parser.add_argument("--test-root", default="tests")
    parser.add_argument("--docs-root", default="docs")
    parser.add_argument("--tools-root", default="tools")
    parser.add_argument("--import-layer-check-cmd")
    parser.add_argument("--python-lint-cmd")
    parser.add_argument("--python-format-check-cmd")
    parser.add_argument("--python-typecheck-cmd")
    parser.add_argument("--python-test-cmd")
    parser.add_argument("--full-validation-cmd")
    parser.add_argument("--skip-post-checks", action="store_true")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Erlaubt erneuten Lauf trotz .agent-box/instantiation.md. Nur mit Freigabe.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    ensure_project_root()
    if INSTANTIATION_FILE.exists() and not args.force:
        raise SystemExit(
            f"Bereits instanziiert: {INSTANTIATION_FILE}. "
            "Erneuter Lauf ist verboten. Nur mit expliziter Freigabe --force nutzen."
        )

    replacements = build_replacements(args)
    values = replacement_map(replacements)
    changed = replace_in_files(replacements)
    created = create_directories(values)
    remove_generic_bridge_example()
    fill_test_commands(values)
    checks = instantiate_checks(POST_CHECKS, values)
    write_instantiation_markdown(
        values, changed, created, checks if not args.skip_post_checks else []
    )

    if not args.skip_post_checks:
        run_post_checks(checks)

    print(f"Instanziierung abgeschlossen: {INSTANTIATION_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
