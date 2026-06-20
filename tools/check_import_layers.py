#!/usr/bin/env python3
"""
check_import_layers.py — Import-/Layer-Checker für Python-Projekte.

Ziel:
    Prüft ob Imports zwischen semantischen Paket-/Modulräumen gegen
    package-schema.md / AGENTS.md verstoßen.

Dieses Tool ist absichtlich konservativ.
Wenn eine Datei nicht klassifizierbar ist, meldet es einen Fehler — nie still.

Modi:
  (Standard)   Vollständiger Output mit Farbe.
  --preflight  Agenten-Modus: kompakter Markdown-Output,
               klare Exit-Codes. Für Preflight-Schritt P6.

Exit-Codes:
  0  Keine Verletzungen (bei --preflight: Preflight bestanden)
  1  Verletzungen gefunden
  2  Konfigurationsfehler (SOURCE_ROOTS nicht gefunden, Platzhalter nicht ersetzt)

Anpassen:
    - PROJECT_PACKAGE
    - SOURCE_ROOTS
    - LAYER_BY_PACKAGE_PART
    - FORBIDDEN_IMPORTS
    - KNOWN_BREACHES
"""

from __future__ import annotations

import argparse
import ast
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


def placeholder_token(name: str) -> str:
    """Return a template token without embedding the token literal in checker logic.

    Die Konfigurationswerte unten duerfen direkte Platzhalter enthalten, damit
    die Box per einfachem Replace instanziiert werden kann. Die Prueflogik darf
    diese direkten Literale aber nicht selbst enthalten, sonst ersetzt eine
    globale Instanziierung auch die Sentinel und erzeugt false positives.
    """
    return "<" + name + ">"


# ---------------------------------------------------------------------------
# Projektlokale Konfiguration
# ---------------------------------------------------------------------------

PROJECT_PACKAGE = "regenbogen"

SOURCE_ROOTS = [
    Path("src"),
]

TEST_ROOTS = [
    Path("tests"),
]

TOOLS_ROOTS = [
    Path("tools"),
]

SCAN_ROOTS = SOURCE_ROOTS + TEST_ROOTS + TOOLS_ROOTS

# Paketsegment → semantischer Raum.
# Muss zu package-schema.md passen.
# Wenn package-schema.md einen neuen Raum einführt: hier nachziehen —
# sonst läuft der Checker mit veralteter Konfiguration (check_agent_docs_consistency prüft das).
LAYER_BY_PACKAGE_PART: dict[str, str] = {
    "domain":         "domain",
    "system":         "system",
    "infrastructure": "infrastructure",
    "adapters":       "adapters",
    "cli":            "cli",
    "entrypoints":    "cli",
    "shared":         "shared",
    "tools":          "tools",
    "tests":          "tests",
}

# Raum → verbotene Zielräume.
#
# Diese Tabelle ist die maschinenlesbare Spiegelung von package-schema.md
# Abschnitt 5 "Capability-Matrix (Importmatrix)". Wichtig: Der Checker darf
# nicht schwächer sein als die Matrix. Deshalb werden alle Matrixwerte außer
# "yes" als verboten behandelt und müssen bei Bedarf kantenbezogen über
# KNOWN_BREACHES klassifiziert werden.
#
# Matrix-Codes in package-schema.md:
#   yes     → erlaubt
#   no      → verboten
#   decision → nur mit Sprechakt / Known Breach / expliziter Ausnahme
#   ports   → erlaubt nur für system.ports; maschinell geprüft
#   init    → nur Initialisierung beim Prozessstart; statisch nicht sicher
#             erkennbar, deshalb Known Breach / Ausnahme nötig
FORBIDDEN_IMPORTS: dict[str, set[str]] = {
    # domain: yes -> domain; decision -> shared; alles andere no
    "domain": {"system", "infrastructure", "adapters", "cli", "shared", "tools"},

    # system: yes -> domain, system; decision -> shared; no -> infra/adapters/cli/tools
    "system": {"infrastructure", "adapters", "cli", "shared", "tools"},

    # system.ports ist ein Unterraum von system. Es darf wie system keine
    # konkreten Implementierungsräume importieren.
    "system.ports": {"infrastructure", "adapters", "cli", "shared", "tools"},

    # infrastructure: yes -> infrastructure; ports -> system.ports;
    # decision -> domain/shared; no -> adapters/cli/tools; system.* sonst verboten
    "infrastructure": {"domain", "system", "adapters", "cli", "shared", "tools"},

    # adapters: yes -> domain, system, infrastructure, adapters; decision -> shared;
    # no -> cli/tools
    "adapters": {"cli", "shared", "tools"},

    # cli: yes -> system, adapters, cli; decision/init -> domain/infrastructure/shared;
    # no -> tools
    "cli": {"domain", "infrastructure", "shared", "tools"},

    # tests: yes -> alle Projekträume. Tests sind Projektionen, keine Semantikquelle.
    "tests": set(),

    # tools: yes -> shared; no -> produktive Projekträume
    "tools": {"domain", "system", "infrastructure", "adapters", "cli"},

    # shared: yes -> shared; no -> alle anderen produktiven Projekträume
    "shared": {"domain", "system", "infrastructure", "adapters", "cli", "tools"},
}

# Klassifizierte Ausnahmen. Format:
#   "path/to/file.py": {"KB-001": "kurze Begründung"}
# Klassifizierte Ausnahmen — KANTENBEZOGEN, nicht dateibezogen.
#
# Eine Datei mit einem bekannten Bruch darf trotzdem KEINE anderen neuen Brüche
# einführen. Deshalb wird jeder Known Breach auf eine konkrete Kante bezogen:
# (source_layer, target_layer) und optional das genaue importierte Modul.
#
# Format:
#   "path/to/file.py": [
#       {
#           "id": "KB-001",
#           "source": "domain",
#           "target": "infrastructure",
#           "import": "regenbogen.infrastructure.legacy",  # optional, präzisiert
#           "reason": "Legacy-Migration; Folgeplan docs/plans/...",
#       },
#   ]
#
# Ein Import wird nur dann unterdrückt, wenn source/target (und falls angegeben
# import) exakt zu einem Eintrag passen. Alle anderen Brüche derselben Datei
# werden weiterhin gemeldet.
KNOWN_BREACHES: dict[str, list[dict[str, str]]] = {
    # "src/my_project/legacy/foo.py": [
    #     {
    #         "id": "KB-001",
    #         "source": "domain",
    #         "target": "infrastructure",
    #         "import": "my_project.infrastructure.legacy",
    #         "reason": "Legacy-Migration noch nicht abgeschlossen; Folgeplan docs/plans/...",
    #     },
    # ],
}


# ---------------------------------------------------------------------------
# Datenmodell
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ClassifiedModule:
    module: str
    layer: str | None
    is_project_internal: bool
    unclassified_reason: str | None


@dataclass(frozen=True)
class ImportFinding:
    file: Path
    source_layer: str
    imported_module: str
    target_layer: str
    line: int
    message: str
    severity: str = "ERROR"


@dataclass(frozen=True)
class UnknownLayerFinding:
    file: Path
    module: str
    line: int
    message: str
    severity: str = "ERROR"


@dataclass(frozen=True)
class PublicApiFinding:
    file: Path
    module: str
    line: int
    message: str
    severity: str = "PUBLIC_API"


Finding = ImportFinding | UnknownLayerFinding | PublicApiFinding


# ---------------------------------------------------------------------------
# Hilfsfunktionen
# ---------------------------------------------------------------------------

def iter_python_files(paths: Iterable[Path]) -> Iterable[Path]:
    for root in paths:
        if not root.exists():
            continue
        if root.is_file() and root.suffix == ".py":
            yield root
            continue
        if root.is_dir():
            for path in root.rglob("*.py"):
                if any(part.startswith(".") for part in path.parts):
                    continue
                yield path


def rel_parts_for_python_file(rel: Path) -> tuple[str, ...]:
    if rel.name == "__init__.py":
        return rel.parent.parts
    return rel.with_suffix("").parts


def is_top_level_package_init(path: Path) -> bool:
    """True fuer src/<PROJECT_PACKAGE>/__init__.py.

    Dieser Sonderfall ist bewusst: Das Top-Level-__init__ ist keine normale
    semantische Schicht. Leer ist es nur Paketmarker. Re-Exports sind
    oeffentliche API und werden separat gemeldet.
    """
    if path.name != "__init__.py":
        return False
    resolved = path.resolve()
    for root in SOURCE_ROOTS:
        try:
            rel = resolved.relative_to(root.resolve())
        except ValueError:
            continue
        return rel.parts == (PROJECT_PACKAGE, "__init__.py")
    return False


def public_api_lines_in_top_level_init(path: Path) -> list[tuple[int, str]]:
    """Meldet API-wirksame Inhalte in Top-Level-__init__.py.

    Erlaubt ohne Meldung:
      - komplett leer
      - Kommentare
      - Modul-Docstring
      - pass
      - einfache Metadaten wie __version__ = "..."

    Gemeldet werden insbesondere Imports/Re-Exports, __all__ und sonstige
    Definitionen. Das ist kein Layer-Fehler, sondern eine Public-API-Fläche.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError as exc:
        return [(exc.lineno or 0, f"Datei kann nicht geparst werden: {exc.msg}")]

    lines: list[tuple[int, str]] = []
    for node in tree.body:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) \
                and isinstance(node.value.value, str):
            continue
        if isinstance(node, ast.Pass):
            continue
        if isinstance(node, ast.Assign):
            names = [t.id for t in node.targets if isinstance(t, ast.Name)]
            if names and all(name in {"__version__", "__author__", "__license__"} for name in names):
                continue
            if "__all__" in names:
                lines.append((node.lineno, "__all__ definiert öffentliche API."))
                continue
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            lines.append((node.lineno, "Import/Re-Export im Top-Level-__init__.py ist öffentliche API."))
            continue
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            lines.append((node.lineno, "Definition im Top-Level-__init__.py ist öffentliche API."))
            continue
        lines.append((getattr(node, "lineno", 0), "Nicht-leerer Inhalt im Top-Level-__init__.py ist öffentliche API."))
    return lines


def path_to_project_module(path: Path) -> str | None:
    resolved = path.resolve()

    # Produktionscode: erwartet Paketpfade unter SOURCE_ROOT, z.B.
    # src/myproj/domain/foo.py -> myproj.domain.foo
    for root in SOURCE_ROOTS:
        try:
            rel = resolved.relative_to(root.resolve())
        except ValueError:
            continue
        parts = rel_parts_for_python_file(rel)
        if not parts:
            return None
        return ".".join(parts)

    # Tests: liegen häufig außerhalb des importierbaren Projektpakets. Für den
    # Layer-Check werden sie trotzdem als semantischer Raum myproj.tests.*
    # klassifiziert, damit die Capability-Matrix operational deckungsgleich ist.
    for root in TEST_ROOTS:
        try:
            rel = resolved.relative_to(root.resolve())
        except ValueError:
            continue
        parts = rel_parts_for_python_file(rel)
        if not parts:
            return f"{PROJECT_PACKAGE}.tests"
        return ".".join((PROJECT_PACKAGE, "tests", *parts))

    # Tools: ebenfalls meist außerhalb des Projektpakets. Sie werden als
    # myproj.tools.* klassifiziert, damit tools-Regeln geprüft werden können.
    for root in TOOLS_ROOTS:
        try:
            rel = resolved.relative_to(root.resolve())
        except ValueError:
            continue
        parts = rel_parts_for_python_file(rel)
        if not parts:
            return f"{PROJECT_PACKAGE}.tools"
        return ".".join((PROJECT_PACKAGE, "tools", *parts))

    return None


def is_system_ports_module(module: str) -> bool:
    parts = module.split(".")
    # <package>.system.ports[.*]
    return len(parts) >= 3 and parts[0] == PROJECT_PACKAGE and parts[1] == "system" and parts[2] == "ports"


def classify_module(module: str) -> ClassifiedModule:
    """
    Drei explizite Fälle — kein stilles None für zwei verschiedene Situationen:
      - extern              → layer=None, is_project_internal=False
      - intern+klassifiziert → layer=<raum>, is_project_internal=True
      - intern+NICHT klassifiziert → layer=None, is_project_internal=True, unclassified_reason gesetzt
    """
    parts = module.split(".")
    if not parts:
        return ClassifiedModule(module=module, layer=None,
                                is_project_internal=False, unclassified_reason=None)

    if parts[0] != PROJECT_PACKAGE:
        return ClassifiedModule(module=module, layer=None,
                                is_project_internal=False, unclassified_reason=None)

    if is_system_ports_module(module):
        return ClassifiedModule(module=module, layer="system.ports",
                                is_project_internal=True, unclassified_reason=None)

    for part in parts[1:]:
        layer = LAYER_BY_PACKAGE_PART.get(part)
        if layer:
            return ClassifiedModule(module=module, layer=layer,
                                    is_project_internal=True, unclassified_reason=None)

    reason = (
        f"Projektinternes Modul '{module}' enthält kein klassifizierbares Pfadsegment. "
        f"Bekannte Segmente: {sorted(LAYER_BY_PACKAGE_PART)}. "
        f"package-schema.md und LAYER_BY_PACKAGE_PART prüfen."
    )
    return ClassifiedModule(module=module, layer=None,
                            is_project_internal=True, unclassified_reason=reason)


def extract_imports(path: Path) -> list[tuple[str, int, str]]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError as exc:
        return [(f"<SYNTAX_ERROR:{exc.msg}>", exc.lineno or 0, "syntax_error")]

    imports: list[tuple[str, int, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append((alias.name, node.lineno, "absolute"))
        elif isinstance(node, ast.ImportFrom):
            if node.module is None:
                continue
            if node.level and node.level > 0:
                imports.append((node.module, node.lineno, "relative"))
            else:
                imports.append((node.module, node.lineno, "absolute"))
    return imports


def is_known_breach(path: Path, source_layer: str, target_layer: str,
                    imported_module: str) -> bool:
    """
    Prüft ob genau diese Kante als Known Breach klassifiziert ist.

    Match-Regel:
      - source und target müssen exakt passen
      - wenn der Eintrag ein 'import'-Feld hat, muss es exakt passen
      - sonst genügt source+target
    Andere Brüche derselben Datei bleiben sichtbar.
    """
    entries = KNOWN_BREACHES.get(path.as_posix())
    if not entries:
        return False
    for entry in entries:
        if entry.get("source") != source_layer:
            continue
        if entry.get("target") != target_layer:
            continue
        wanted_import = entry.get("import")
        if wanted_import and wanted_import != imported_module:
            continue
        return True
    return False


def check_file(path: Path) -> list[Finding]:
    findings: list[Finding] = []

    source_module = path_to_project_module(path)
    if source_module is None:
        findings.append(UnknownLayerFinding(
            file=path, module="<unknown>", line=0,
            message="Datei liegt außerhalb der bekannten SOURCE_ROOTS.",
        ))
        return findings

    if is_top_level_package_init(path):
        for line, message in public_api_lines_in_top_level_init(path):
            findings.append(PublicApiFinding(
                file=path, module=source_module, line=line, message=message,
            ))
        return findings

    source_classified = classify_module(source_module)
    if source_classified.unclassified_reason:
        findings.append(UnknownLayerFinding(
            file=path, module=source_module, line=0,
            message=source_classified.unclassified_reason,
        ))
        return findings
    if source_classified.layer is None:
        findings.append(UnknownLayerFinding(
            file=path, module=source_module, line=0,
            message="Quelldatei keinem semantischen Raum zugeordnet.",
        ))
        return findings

    source_layer = source_classified.layer

    for imported_module, line, import_type in extract_imports(path):
        if import_type == "syntax_error":
            findings.append(UnknownLayerFinding(
                file=path, module=imported_module, line=line,
                message="Datei kann nicht geparst werden.",
            ))
            continue

        if import_type == "relative":
            findings.append(UnknownLayerFinding(
                file=path, module=imported_module, line=line,
                message="Relativer Import: für Layer-Checks bitte absolute Imports verwenden.",
            ))
            continue

        target_classified = classify_module(imported_module)
        if not target_classified.is_project_internal:
            continue

        if target_classified.unclassified_reason:
            findings.append(UnknownLayerFinding(
                file=path, module=imported_module, line=line,
                message=target_classified.unclassified_reason,
            ))
            continue

        target_layer = target_classified.layer
        target_policy_layer = "system" if target_layer == "system.ports" else target_layer

        # Sonderregel der Matrix: infrastructure darf system.ports importieren,
        # aber kein anderes system.*.
        if source_layer == "infrastructure" and target_layer == "system.ports":
            continue

        forbidden_targets = FORBIDDEN_IMPORTS.get(source_layer, set())
        if target_policy_layer in forbidden_targets and \
                not is_known_breach(path, source_layer, target_policy_layer, imported_module):
            findings.append(ImportFinding(
                file=path, source_layer=source_layer,
                imported_module=imported_module, target_layer=target_layer,
                line=line,
                message=f"Verbotener Import: '{source_layer}' darf '{target_layer}' nicht importieren.",
            ))

    return findings


def check_config() -> list[str]:
    """Prueft ob Konfigurationsplatzhalter noch vorhanden sind.

    Die Sentinel werden dynamisch erzeugt. Dadurch bleibt diese Funktion auch
    nach einer globalen Template-Instanziierung korrekt.
    """
    errors = []
    python_package_token = placeholder_token("PYTHON_PACKAGE_NAME")
    root_tokens = [
        ("SOURCE_ROOT", SOURCE_ROOTS),
        ("TEST_ROOT", TEST_ROOTS),
        ("TOOLS_ROOT", TOOLS_ROOTS),
    ]
    if python_package_token in PROJECT_PACKAGE:
        errors.append("PROJECT_PACKAGE enthaelt Platzhalter PYTHON_PACKAGE_NAME.")
    for token_name, roots in root_tokens:
        token = placeholder_token(token_name)
        for root in roots:
            if token in str(root):
                errors.append(f"{token_name} enthaelt Platzhalter: {root}")
    return errors


def check_source_roots_exist() -> list[str]:
    """Prüft ob die konfigurierten SOURCE_ROOTS tatsächlich existieren.

    Nur sinnvoll im instanziierten Projekt — im Template sind es Platzhalter.
    """
    errors = []
    for root in SCAN_ROOTS:
        if "<" in str(root):
            continue  # Platzhalter, separat über check_config gemeldet
        if not root.exists():
            errors.append(f"Scan-Root existiert nicht: {root}")
    return errors


# ---------------------------------------------------------------------------
# Output-Modi
# ---------------------------------------------------------------------------

def print_findings_standard(findings: list[Finding]) -> None:
    for finding in findings:
        if isinstance(finding, ImportFinding):
            print(
                f"{finding.file}:{finding.line}: ERROR: {finding.message}\n"
                f"  source_layer:  {finding.source_layer}\n"
                f"  imported:      {finding.imported_module}\n"
                f"  target_layer:  {finding.target_layer}"
            )
        elif isinstance(finding, PublicApiFinding):
            print(
                f"{finding.file}:{finding.line}: PUBLIC_API: {finding.message}\n"
                f"  module: {finding.module}\n"
                f"  action: Freigabe nach AGENTS.md H9 / package-schema.md §7 prüfen"
            )
        else:
            print(
                f"{finding.file}:{finding.line}: ERROR: {finding.message}\n"
                f"  module: {finding.module}"
            )


def print_preflight(findings: list[Finding], files_checked: int) -> None:
    """
    Kompakter Agenten-Output für Preflight-Schritt P6.
    Maximale Lesbarkeit, minimale Länge.
    Markdown-Evidence bei Fehlern.
    """
    v_count = len(findings)
    if v_count == 0:
        print(f"✓ PREFLIGHT IMPORT-LAYER OK ({files_checked} Dateien geprüft)")
        known = sum(1 for _ in KNOWN_BREACHES)
        if known:
            print(f"  ({known} klassifizierte Known Breaches — bekannt, ignoriert)")
        return

    print(f"✗ PREFLIGHT IMPORT-LAYER FEHLGESCHLAGEN — {v_count} Fund(e)\n")
    has_import_error = any(isinstance(f, ImportFinding) for f in findings)
    has_unknown_error = any(isinstance(f, UnknownLayerFinding) for f in findings)
    has_public_api = any(isinstance(f, PublicApiFinding) for f in findings)
    if has_import_error or has_unknown_error:
        print("ABBRUCH: Semantische Layer-Verletzungen gefunden.")
        print("Gemäß AGENTS.md §10 HARD-Abbruch H2: Import-/Layer-Verletzung ohne klassifizierten Bruch.\n")
    elif has_public_api:
        print("ABBRUCH: Öffentliche API-Fläche berührt.")
        print("Gemäß AGENTS.md §10 H9: Public-API-Änderung braucht Freigabe.\n")
    print("Evidence (Markdown):")
    for f in findings:
        if isinstance(f, ImportFinding):
            print(f"- Datei: `{f.file}:{f.line}`")
            print(f"  Source-Layer: `{f.source_layer}`")
            print(f"  Target-Layer: `{f.target_layer}`")
            print(f"  Import: `{f.imported_module}`")
            print(f"  Befund: {f.message}")
            print("  Aktion: Import entfernen oder Known Breach klassifizieren.")
        elif isinstance(f, PublicApiFinding):
            print(f"- Datei: `{f.file}:{f.line}`")
            print(f"  Modul: `{f.module}`")
            print("  Typ: `public_api_surface`")
            print(f"  Befund: {f.message}")
            print("  Aktion: Freigabe nach H9 prüfen oder Top-Level-__init__.py leer halten.")
        else:
            print(f"- Datei: `{f.file}:{f.line}`")
            print(f"  Modul: `{f.module}`")
            print(f"  Befund: {f.message}")
            print("  Aktion: Modul klassifizieren oder package-schema.md ergänzen.")
    print("\nReferenz: AGENTS.md §4, package-schema.md")



# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Prüft Python-Imports gegen semantische Layer-Regeln."
    )
    parser.add_argument(
        "paths", nargs="*", type=Path, default=SCAN_ROOTS,
        help="Dateien oder Verzeichnisse. Default: SOURCE_ROOTS + TEST_ROOTS + TOOLS_ROOTS.",
    )
    parser.add_argument(
        "--template", action="store_true",
        help="Template-Modus: Platzhalter-Konfiguration erlaubt, Exit 0 ohne Lauf.",
    )
    parser.add_argument(
        "--preflight", action="store_true",
        help="Agenten-Modus: kompakter Output, Evidence-Format, klare Exit-Codes.",
    )
    parser.add_argument(
        "--list-known-breaches", action="store_true",
        help="Listet bekannte Brüche und beendet sich mit 0.",
    )

    args = parser.parse_args(argv)

    if args.list_known_breaches:
        if not KNOWN_BREACHES:
            print("Keine Known Breaches eingetragen.")
            return 0
        for path, breaches in KNOWN_BREACHES.items():
            print(path)
            for entry in breaches:
                bid = entry.get("id", "KB-???")
                src = entry.get("source", "?")
                tgt = entry.get("target", "?")
                imp = entry.get("import", "(jede Kante src→tgt)")
                reason = entry.get("reason", "")
                print(f"  {bid}: {src} → {tgt}  [{imp}]")
                if reason:
                    print(f"        {reason}")
        return 0

    # Template-Modus: nur Existenz und Syntax prüfen, kein Scan
    if args.template:
        print("Import-Layer-Check: TEMPLATE-MODUS")
        print("  Konfiguration enthält Platzhalter — kein Scan ausgeführt.")
        print("  Im instanziierten Projekt ohne --template ausführen.")
        config_errors = check_config()
        if not config_errors:
            print("  HINWEIS: Konfiguration enthält KEINE Platzhalter mehr —")
            print("  Box möglicherweise bereits instanziiert?")
        return 0

    # Standard-/Project-Modus
    config_errors = check_config()
    if config_errors:
        for err in config_errors:
            print(f"KONFIGURATIONSFEHLER: {err}", file=sys.stderr)
        print("Import-Layer-Check: KONFIGURATION UNVOLLSTÄNDIG (Exit 2)", file=sys.stderr)
        print("Im Template-Repository: --template verwenden.", file=sys.stderr)
        return 2

    root_errors = check_source_roots_exist()
    if root_errors:
        for err in root_errors:
            print(f"KONFIGURATIONSFEHLER: {err}", file=sys.stderr)
        print("Import-Layer-Check: SOURCE_ROOT fehlt (Exit 2)", file=sys.stderr)
        return 2

    findings: list[Finding] = []
    files_checked = 0
    for path in iter_python_files(args.paths):
        files_checked += 1
        findings.extend(check_file(path))


    if args.preflight:
        print_preflight(findings, files_checked)
        return 1 if findings else 0

    if findings:
        print_findings_standard(findings)
        print()
        print(f"Import-Layer-Check: FAILED ({len(findings)} finding(s), {files_checked} Dateien geprüft)")
        return 1

    print(f"Import-Layer-Check: OK ({files_checked} Dateien geprüft)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
