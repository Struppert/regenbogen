#!/usr/bin/env python3
"""
resolve_test_obligations.py — Testpflichtableitung für Python-Projekte.

Ziel:
    Aus geänderten Dateien ableiten, welche Tests und Checks mindestens laufen müssen.

Dieses Tool entscheidet nicht, ob Tests erfolgreich sind.
Es macht Pflichten sichtbar — und unbekannte Pflichten explizit als Fehler.

Anpassen:
    - SOURCE_ROOT, TEST_ROOT, DOCS_ROOT, TOOLS_ROOT
    - STANDARD_CHECKS
    - IMPORT_LAYER_CHECK, FULL_VALIDATION, PYTHON_TEST
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from pathlib import Path


# ---------------------------------------------------------------------------
# Projektlokale Konfiguration
# ---------------------------------------------------------------------------

SOURCE_ROOT = Path("src")
TEST_ROOT = Path("tests")
DOCS_ROOT = Path("docs")
TOOLS_ROOT = Path("tools")

STANDARD_CHECKS = {
    "lint": "python -m ruff check .",
    "format": "python -m ruff format --check .",
    "typecheck": "python -m mypy src",
}

IMPORT_LAYER_CHECK = "python tools/check_import_layers.py --preflight src tests tools"
FULL_VALIDATION = "python tools/check_agent_docs_consistency.py --instantiated && python tools/check_import_layers.py --preflight src tests tools && python tools/resolve_test_obligations.py --selfcheck --instantiated && python -m pytest"
PYTHON_TEST = "python -m pytest"

AGENT_DOCS = {
    "AGENTS.md",
    "package-schema.md",
    "preflight-checkliste.md",
    "task-schnitt.md",
    "sprechakt-protokoll.md",
    "regelmatrix.md",
    "test-obligations.md",
    "migration-bridges.md",
    "erfahrungsbericht-protokoll.md",
    "learning-matrix.md",
}

PACKAGING_FILES = {
    "pyproject.toml",
    "setup.py",
    "setup.cfg",
    "Pipfile",
    "poetry.lock",
    "uv.lock",
}

PACKAGING_PREFIXES = ("requirements",)

# Mapping Testgruppe → konkreter Projektbefehl.
#
# Template-Zustand: alle Werte leer ("") — die Gruppe ist ein TODO.
# Instantiated-Zustand: jeder aktiv gebrauchte Eintrag muss einen echten Befehl haben.
#
# Beispiel nach Instanziierung:
#   "domain-tests": "pytest tests/domain",
#   "system-tests": "pytest tests/system",
TEST_COMMANDS: dict[str, str] = {
    "domain-tests": "python -m pytest",
    "negative-domain-tests": "python -m pytest",
    "system-tests": "python -m pytest",
    "policy-tests": "python -m pytest",
    "infrastructure-tests": "python -m pytest",
    "contract-or-fake-tests": "python -m pytest",
    "adapter-tests": "python -m pytest",
    "mapping-tests": "python -m pytest",
    "cli-tests": "python -m pytest",
    "smoke-tests": "python -m pytest",
    "affected-product-tests": "python -m pytest",
}


# Ein Label ist TODO, solange es keinen konkreten Befehl in TEST_COMMANDS hat.
def todo_test_labels() -> set[str]:
    return {label for label, cmd in TEST_COMMANDS.items() if not cmd.strip()}


# Rückwärtskompatibler Alias.
TODO_TEST_LABELS: set[str] = {
    label for label, cmd in TEST_COMMANDS.items() if not cmd.strip()
}


def command_for_test(label: str) -> str | None:
    """Gibt den konkreten Testbefehl oder None (= noch TODO) zurück."""
    cmd = TEST_COMMANDS.get(label, "")
    return cmd if cmd.strip() else None


# ---------------------------------------------------------------------------
# Datenmodell
# ---------------------------------------------------------------------------


@dataclass
class Obligation:
    reason: str
    checks: set[str] = field(default_factory=set)
    tests: set[str] = field(default_factory=set)
    notes: list[str] = field(default_factory=list)
    requires_human: bool = False
    hard_stop: bool = False


@dataclass
class FileObligations:
    path: Path
    obligations: list[Obligation] = field(default_factory=list)

    def add(self, obligation: Obligation) -> None:
        self.obligations.append(obligation)

    @property
    def hard_stop(self) -> bool:
        return any(ob.hard_stop for ob in self.obligations)

    @property
    def requires_human(self) -> bool:
        return any(ob.requires_human for ob in self.obligations)


# ---------------------------------------------------------------------------
# Hilfsfunktionen
# ---------------------------------------------------------------------------


def is_under(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def path_parts_after_root(path: Path, root: Path) -> tuple[str, ...]:
    try:
        return path.relative_to(root).parts
    except ValueError:
        return ()


def is_packaging_file(path: Path) -> bool:
    name = path.name
    return name in PACKAGING_FILES or any(
        name.startswith(p) for p in PACKAGING_PREFIXES
    )


def standard_code_obligation(reason: str) -> Obligation:
    return Obligation(
        reason=reason,
        checks={"lint", "format", "typecheck", "import-layer-check"},
    )


def classify_path(path: Path) -> FileObligations:
    result = FileObligations(path=path)
    p = Path(path.as_posix())

    # Agentendokumente im Root
    if p.name in AGENT_DOCS and len(p.parts) == 1:
        result.add(
            Obligation(
                reason="Agenten-Dokument geändert.",
                checks={"agent-docs-consistency"},
                notes=[
                    "Nach regelmatrix.md gekoppelte Dokumente prüfen (Inhalt, nicht nur Präsenz).",
                    "Nach regelmatrix.md Drift-Regeln: Kopplungspflichten aktiv prüfen.",
                    "ERFAHRUNGSBERICHT (E1): Agentendokument-Änderung ist nichttrivial — Erfahrungsbericht nach Session schreiben.",
                ],
                requires_human=True,
            )
        )
        return result

    # Packaging / Dependencies
    if is_packaging_file(p):
        result.add(
            Obligation(
                reason="Packaging-/Dependency-Datei geändert.",
                checks={"full-validation"},
                notes=[
                    "Dependency-Änderungen sind freigabepflichtig (HARD-Abbruch H8).",
                    "Runtime-Dependency ohne Freigabe ist nicht erlaubt.",
                ],
                requires_human=True,
                hard_stop=True,
            )
        )
        return result

    # Tools
    if is_under(p, TOOLS_ROOT):
        result.add(
            Obligation(
                reason="Tooling geändert.",
                checks={
                    "lint",
                    "format",
                    "typecheck",
                    "tool-selfcheck",
                    "agent-docs-consistency",
                },
                notes=[
                    "Checker-Änderungen sind geschützt (HARD-Abbruch H5).",
                    "Keine Tooländerung zur Fehlerunterdrückung.",
                    "Nach Änderung an check_import_layers.py: LAYER_BY_PACKAGE_PART gegen package-schema.md prüfen.",
                ],
                requires_human=True,
            )
        )
        return result

    # Tests
    if is_under(p, TEST_ROOT):
        result.add(
            Obligation(
                reason="Testdatei geändert.",
                checks={"lint", "format"},
                tests={"affected-product-tests"},
                notes=[
                    "Prüfen: prüft der Test bestehendes Verhalten oder definiert er neues?",
                    "Neue Produktsemantik im Test erfordert Plan oder Sprechakt (I4).",
                    "TODO: 'affected-product-tests' durch projektspezifischen Befehl ersetzen.",
                ],
            )
        )
        return result

    # Source
    if is_under(p, SOURCE_ROOT):
        parts = path_parts_after_root(p, SOURCE_ROOT)

        if not parts:
            result.add(
                Obligation(
                    reason="Source-Datei nicht klassifizierbar — kein Unterraum erkennbar.",
                    hard_stop=True,
                    notes=[
                        "Pfad liegt unter SOURCE_ROOT ohne klassifizierbares Segment."
                    ],
                )
            )
            return result

        semantic_parts = set(parts)

        if "domain" in semantic_parts:
            ob = standard_code_obligation("Domain-Code geändert.")
            ob.tests.update({"domain-tests", "negative-domain-tests"})
            ob.notes.append(
                "Neuer Domain-Begriff erfordert Sprechakt SP1 oder Glossarentscheidung."
            )
            ob.notes.append(
                "TODO: 'domain-tests' durch projektspezifischen Befehl ersetzen."
            )
            result.add(ob)
            return result

        if "system" in semantic_parts:
            ob = standard_code_obligation("System-Semantics-Code geändert.")
            ob.tests.update({"system-tests", "policy-tests"})
            ob.notes.append("Neue Ablaufbedeutung erfordert Sprechakt SP2.")
            ob.notes.append(
                "TODO: 'system-tests' durch projektspezifischen Befehl ersetzen."
            )
            result.add(ob)
            return result

        if "infrastructure" in semantic_parts:
            ob = standard_code_obligation("Infrastructure-Code geändert.")
            ob.tests.update({"infrastructure-tests", "contract-or-fake-tests"})
            ob.notes.append("Keine produktiven externen Zugriffe in Unit-Tests.")
            ob.notes.append(
                "TODO: 'infrastructure-tests' durch projektspezifischen Befehl ersetzen."
            )
            result.add(ob)
            return result

        if "adapters" in semantic_parts:
            ob = standard_code_obligation("Adapter-/Binding-Code geändert.")
            ob.tests.update({"adapter-tests", "mapping-tests"})
            ob.notes.append("Adapter dürfen keine neue Semantik erzeugen (I3, SP5).")
            ob.notes.append(
                "TODO: 'adapter-tests' durch projektspezifischen Befehl ersetzen."
            )
            result.add(ob)
            return result

        if "cli" in semantic_parts or "entrypoints" in semantic_parts:
            ob = standard_code_obligation("CLI-/Entrypoint-Code geändert.")
            ob.tests.update({"cli-tests", "smoke-tests"})
            ob.notes.append("Neue CLI-Option mit Bedeutung ist freigabepflichtig.")
            ob.notes.append(
                "TODO: 'cli-tests' durch projektspezifischen Befehl ersetzen."
            )
            result.add(ob)
            return result

        if "shared" in semantic_parts:
            ob = standard_code_obligation("Shared-Code geändert.")
            ob.tests.update({"affected-product-tests"})
            ob.notes.append(
                "WARNUNG: shared/ ist gefährlich. "
                "Prüfen ob der Code wirklich semantisch neutral ist. "
                "Shared mit Domänen- oder Systembedeutung gehört nicht nach shared."
            )
            ob.notes.append(
                "Import-Checker schlägt an, wenn shared projektinterne Räume importiert."
            )
            ob.notes.append(
                "TODO: 'affected-product-tests' durch projektspezifischen Befehl ersetzen."
            )
            result.add(ob)
            return result

        result.add(
            Obligation(
                reason="Source-Datei keinem bekannten semantischen Raum zugeordnet.",
                checks={"import-layer-check"},
                hard_stop=True,
                notes=[
                    "package-schema.md unvollständig oder Datei falsch verortet.",
                    "Testpflicht unklar → HARD-Abbruch H6.",
                ],
            )
        )
        return result

    # Docs
    if is_under(p, DOCS_ROOT):
        result.add(
            Obligation(
                reason="Dokumentation geändert.",
                notes=[
                    "Prüfen: sind operative Agentenregeln betroffen?",
                    "Bei reiner Dokumentation ohne Regeländerung: Testfreiheit begründen.",
                ],
            )
        )
        return result

    # Unbekannt
    result.add(
        Obligation(
            reason="Datei liegt außerhalb bekannter Projektbereiche.",
            hard_stop=True,
            notes=[
                "Schreibrechte und Testpflicht unklar.",
                "Pfad in AGENTS.md / package-schema.md klassifizieren.",
            ],
        )
    )
    return result


def command_for_check(check: str) -> str | None:
    mapping = {
        "lint": STANDARD_CHECKS["lint"],
        "format": STANDARD_CHECKS["format"],
        "typecheck": STANDARD_CHECKS["typecheck"],
        "import-layer-check": IMPORT_LAYER_CHECK,
        "full-validation": FULL_VALIDATION,
        "agent-docs-consistency": f"{TOOLS_ROOT}/check_agent_docs_consistency.py",
        "tool-selfcheck": f"{TOOLS_ROOT}/resolve_test_obligations.py --selfcheck",
    }
    return mapping.get(check)


def print_result(results: list[FileObligations]) -> None:
    all_checks: set[str] = set()
    all_tests: set[str] = set()
    hard_stop = False
    requires_human = False

    for file_result in results:
        print(f"\n{file_result.path}")
        print("-" * len(str(file_result.path)))

        for obligation in file_result.obligations:
            print(f"Grund: {obligation.reason}")

            if obligation.checks:
                print("Checks:")
                for check in sorted(obligation.checks):
                    all_checks.add(check)
                    cmd = command_for_check(check)
                    if cmd:
                        print(f"  - {check}: {cmd}")
                    else:
                        # Unbekannter Check — explizit sichtbar machen, nicht still ignorieren.
                        print(
                            f"  - {check}: [KEIN BEFEHL KONFIGURIERT — bitte eintragen]"
                        )

            if obligation.tests:
                print("Tests:")
                for test in sorted(obligation.tests):
                    all_tests.add(test)
                    cmd = command_for_test(test)
                    if cmd:
                        print(f"  - {test}: {cmd}")
                    else:
                        print(
                            f"  - {test} [TODO: projektspezifischen Befehl in TEST_COMMANDS eintragen]"
                        )

            if obligation.notes:
                print("Hinweise:")
                for note in obligation.notes:
                    print(f"  - {note}")

            if obligation.requires_human:
                requires_human = True
                print("Freigabe/Sprechakt: erforderlich")

            if obligation.hard_stop:
                hard_stop = True
                print("Status: HARD-ABBRUCH")

            print()

    print("\nZusammenfassung")
    print("--------------")

    if all_checks:
        print("Auszuführende Checks:")
        for check in sorted(all_checks):
            cmd = command_for_check(check)
            if cmd:
                print(f"  - {check}: {cmd}")
            else:
                print(f"  - {check}: [KEIN BEFEHL KONFIGURIERT]")

    if all_tests:
        print("Auszuführende Testgruppen:")
        for test in sorted(all_tests):
            cmd = command_for_test(test)
            if cmd:
                print(f"  - {test}: {cmd}")
            else:
                print(
                    f"  - {test} [TODO: projektspezifischen Befehl in TEST_COMMANDS eintragen]"
                )

    if requires_human:
        print("Freigabe/Sprechakt: erforderlich")

    if hard_stop:
        print("Ergebnis: HARD-ABBRUCH — Testpflicht oder Schreibrecht unklar.")
    else:
        print("Ergebnis: Testpflicht ableitbar.")


def selfcheck(strict: bool = False) -> int:
    """
    strict=False (Template-Modus, Default):
        Platzhalter und offene TEST_COMMANDS sind erlaubt.
    strict=True (Instantiated-Modus):
        Platzhalter und offene TEST_COMMANDS sind ERROR.
    """
    import re as _re

    # Platzhalter werden per Muster erkannt: <GROSSBUCHSTABEN_MIT_UNTERSTRICH>.
    # Das ist robuster als eine Literalliste, die bei einer pauschalen
    # Projekt-Ersetzung versehentlich mitverändert würde.
    placeholder_re = _re.compile(r"<[A-Z][A-Z0-9_]*>")

    values = [
        str(SOURCE_ROOT),
        str(TEST_ROOT),
        str(DOCS_ROOT),
        str(TOOLS_ROOT),
        *STANDARD_CHECKS.values(),
        PYTHON_TEST,
        FULL_VALIDATION,
        IMPORT_LAYER_CHECK,
    ]

    unresolved = [v for v in values if placeholder_re.search(v)]

    if strict:
        # Instantiated-Modus
        if unresolved:
            print("Selfcheck (instantiated): FAILED — unresolved placeholders:")
            for value in unresolved:
                print(f"  - {value}")
            return 1
        open_labels = sorted(todo_test_labels())
        if open_labels:
            print(
                f"Selfcheck (instantiated): FAILED — "
                f"{len(open_labels)} Testgruppen ohne konkreten Befehl in TEST_COMMANDS:"
            )
            for label in open_labels:
                print(f"  - {label}")
            print("Im instanziierten Projekt muss jede aktiv gebrauchte Testgruppe")
            print(
                "einen echten Befehl in TEST_COMMANDS haben (z.B. 'pytest tests/domain')."
            )
            return 1
        print("Selfcheck (instantiated): OK")
        return 0

    # Template-Modus
    if unresolved:
        print("Selfcheck (template): OK")
        print(f"  ({len(unresolved)} Platzhalter vorhanden — im Template erwartet)")
    else:
        print("Selfcheck (template): WARN")
        print("  Keine Platzhalter gefunden — Box möglicherweise bereits instanziiert?")
        print("  Dann --instantiated verwenden.")

    print()
    print("Erfahrungsbericht-Trigger aktiv:")
    print(
        "  E1 — nach Session mit Plan/MITTEL/Sprechakt/Task-Schnitt/API/Dokumentdrift"
    )
    print("  E2 — nach HARD-Abbruch")
    print("  E3 — nach sichtbarer Systemschwäche")
    print("  E4 — nach systemischem SOFT-Abbruch")
    print("  E5 — nach unerwarteter Regelinteraktion")
    print("Protokoll: erfahrungsbericht-protokoll.md")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Leitet Test- und Checkpflichten aus geänderten Dateien ab."
    )
    parser.add_argument(
        "--changed-file",
        action="append",
        default=[],
        help="Geänderte Datei. Kann mehrfach angegeben werden.",
    )
    parser.add_argument(
        "--selfcheck",
        action="store_true",
        help="Prüft Konfiguration. Default: Template-Modus.",
    )
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--template",
        action="store_const",
        dest="mode",
        const="template",
        help="Template-Modus (Default für selfcheck): Platzhalter und TODOs erlaubt.",
    )
    mode_group.add_argument(
        "--instantiated",
        action="store_const",
        dest="mode",
        const="instantiated",
        help="Instantiated-Modus: Platzhalter und TODOs sind ERROR.",
    )

    args = parser.parse_args()

    if args.selfcheck:
        strict = args.mode == "instantiated"
        return selfcheck(strict=strict)

    if not args.changed_file:
        print("Keine --changed-file angegeben.")
        return 2

    results = [classify_path(Path(p)) for p in args.changed_file]
    print_result(results)

    return 1 if any(r.hard_stop for r in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
