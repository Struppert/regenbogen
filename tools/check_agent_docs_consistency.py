#!/usr/bin/env python3
"""
check_agent_docs_consistency.py — Konsistenzcheck für Agentendokumente.

Modi:
  --template      Box im Template-Repository (Platzhalter erlaubt, BR-001-Beispiel
                  erlaubt, Glossar darf leer sein). Default wenn nicht angegeben.
  --instantiated  Box im Zielprojekt nach Instanziierung. Platzhalter sind ERROR.
                  Bridge-Beispiel sollte ersetzt sein. Glossar darf leer sein
                  beim Projektstart, aber nicht nach erstem Sprechakt.
  --preflight     Agenten-Modus mit kurzem Output und Exit-Code.

Exit-Codes:
  0  Keine Errors
  1  Errors gefunden
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


# ---------------------------------------------------------------------------
# Konfiguration
# ---------------------------------------------------------------------------

# Dateien die in JEDEM Modus Pflicht sind (operativer Kern).
REQUIRED_FILES_CORE = [
    Path("AGENTS.md"),
    Path("BROWNFIELD-MIGRATION.md"),
    Path("blocker-und-abbruch-protokoll.md"),
    Path("ausfuehrungsmandat-protokoll.md"),
    Path("package-schema.md"),
    Path("preflight-checkliste.md"),
    Path("task-schnitt.md"),
    Path("sprechakt-protokoll.md"),
    Path("regelmatrix.md"),
    Path("test-obligations.md"),
    Path("migration-bridges.md"),
    Path("erfahrungsbericht-protokoll.md"),
    Path("grundsatz.md"),
    Path("glossar-domain.md"),
    Path("glossar-system.md"),
    Path("glossar-meta.md"),
    Path("glossar-README.md"),
    Path("docs/plans/template.md"),
]

# AGENT-SETUP.md ist ein Template-Artefakt:
#   Template-Modus:     Pflichtdatei (erklärt die Instanziierung).
#   Instantiated-Modus: NICHT Pflicht. Soll nach docs/ verschoben oder entfernt sein.
#                       Wird im instanziierten Projekt nicht auf Platzhalter geprüft.
TEMPLATE_ONLY_FILES = [
    Path("AGENT-SETUP.md"),
    Path(".agent-box-template.md"),
]

# Rückwärtskompatibler Alias — einige Hilfsfunktionen iterieren noch hierüber.
REQUIRED_FILES = REQUIRED_FILES_CORE + TEMPLATE_ONLY_FILES


def required_files_for(mode: str) -> list[Path]:
    if mode == "instantiated":
        return list(REQUIRED_FILES_CORE)
    return REQUIRED_FILES_CORE + TEMPLATE_ONLY_FILES


# README-Regel ist modusabhängig:
#   Template-Modus:     Box darf KEIN README.md enthalten (würde Zielprojekt-README belegen).
#   Instantiated-Modus: Zielprojekt DARF ein eigenes README.md haben — kein Verbot.
def forbidden_files_for(mode: str) -> list[Path]:
    if mode == "instantiated":
        return []
    return [Path("README.md")]

OPTIONAL_FILES = [
    Path("learning-matrix.md"),
]

REQUIRED_TERMS_BY_FILE: dict[Path, list[str]] = {
    Path("AGENTS.md"): [
        "bindender Router", "Task-Schnitt", "Schreibrechte",
        "Fast-Path", "Governance-Ausloeser", "Ausfuehrungsbreite",
        "Blosse Teilbarkeit ist kein Schnittgrund",
        "package-schema.md", "BROWNFIELD-MIGRATION.md",
        "blocker-und-abbruch-protokoll.md", "ausfuehrungsmandat-protokoll.md",
        "migration-bridges.md", "erfahrungsbericht-protokoll.md",
        "glossar-domain.md", "glossar-meta.md",
        "H10", "BF1", ".agent-box/adoption.md",
    ],
    Path("AGENT-SETUP.md"): [
        "Template-Zustand", "Projekt-Zustand",
        "Instanziierung", "Platzhalter",
        "AGENTS.md",
    ],
    Path("BROWNFIELD-MIGRATION.md"): [
        "Brownfield", "Datei-Aktionsmatrix", "Migrationsevidence",
        ".agent-box/migrations", "Baseline", "--force",
        "Bestehendes Python-Projekt", "Bestehendes Box-Projekt",
        "Observed State", "Accepted Local Truth", "Legacy Defect",
        "Known Breach", "Discover", "Describe", "Decide",
        ".agent-box/adoption.md", "unboxed-to", "BF-Abbruch",
        "Accepted-Alternative-Kandidat", "Herkunftsmarker",
        "Aktuelle Box-Version", "Baseline-Anker",
        "Lokale Divergenz gegen Baseline-Anker", "Merge-Richtung",
        "Drei-Wege-Merge", "Migrationsmandat",
        "ausfuehrungsmandat-protokoll.md",
    ],
    Path("blocker-und-abbruch-protokoll.md"): [
        "H1", "H10", "SA1", "SA6", "Abbruch-Evidence",
        "Wiedereinstieg", "Pendeln", "Stagnation", "Anti-Zeno",
        "tmp/erfahrungsberichte",
    ],
    Path("ausfuehrungsmandat-protokoll.md"): [
        "ANALYSE", "PLAN", "AUSFUEHRUNG", "Ausfuehrungsmandat",
        "WG-AUSFUEHRUNG", "Mandatstatus", "Plan-Version", "Delta-Freigabe",
        "Wirkungsgate",
    ],
    Path("package-schema.md"): [
        "domain", "system", "infrastructure", "adapters",
        "Capability", "Known Breaches", "LAYER_BY_PACKAGE_PART", "decision",
    ],
    Path("preflight-checkliste.md"): [
        "PF-ROUTER", "AGENTS.md", "package-schema.md",
        "Import", "Testpflicht", "Schreibrechte",
        "glossar-README.md", "Autonomieregel",
    ],
    Path("task-schnitt.md"): [
        "Semantic Working Set", "SWS",
        "T1", "T2", "Binding",
    ],
    Path("sprechakt-protokoll.md"): [
        "Sprechakt", "SP0", "SP1", "SP2", "SP7", "docs/sprechakte",
        "offen", "festgelegt", "abgelehnt", "superseded", "widerrufen",
        "Ausfuehrungsmandat",
    ],
    Path("regelmatrix.md"): [
        "Autoritaetsmodell", "AGENTS.md",
        "package-schema.md", "Widerspruch", "grundsatz.md", "BF",
        "blocker-und-abbruch-protokoll.md", "ausfuehrungsmandat-protokoll.md",
        "beschreibbar", "freigegeben",
    ],
    Path("test-obligations.md"): [
        "Testpflicht", "domain", "system", "infrastructure", "adapters",
    ],
    Path("migration-bridges.md"): [
        "legacy-bridge", "do-not-touch-mechanically",
        "canonical", "SP6", "BR-",
    ],
    Path("erfahrungsbericht-protokoll.md"): [
        "E1", "E2", "E3", "E4", "E5", "tmp/erfahrungsberichte", "learning-matrix",
        "Vorgeschlagene Musterkennung",
    ],
    Path("grundsatz.md"): [
        "Reifizierung", "Plausibilität", "Projektionen",
        "Autonomieregel", "Glossar", "Sprechakt", "Abbruch",
    ],
    Path("glossar-domain.md"): [
        "Kompetenzfrage", "Invarianten", "Projektionen",
        "Migrationsstatus", "SP7", "domain",
    ],
    Path("glossar-system.md"): [
        "Kompetenzfrage", "Invarianten", "Projektionen",
        "Migrationsstatus", "system", "SP7",
    ],
    Path("glossar-meta.md"): [
        "Kompetenzfrage", "Invarianten", "Projektionen",
        "Migrationsstatus", "meta", "SP7",
        "Agenten-Box", "Instanziierungs-Sprechakt",
        "Semantic Working Set", "Observed State",
        "Accepted Local Truth", "Legacy Defect",
        "Migrationsevidence", "BF-Code", "widerrufen",
    ],
    Path("glossar-README.md"): [
        "Ladeprotokoll", "glossar-domain.md", "glossar-system.md",
        "glossar-meta.md", "migration-bridges.md", "SP7", "T1", "Autonomieregel",
    ],
    Path(".agent-box-template.md"): [
        "Box-Version", "Markdown only", "Box-Artefakte",
        "Ersetzungsziele des Instanziierungswerkzeugs",
        "Instanziierungsnachweis", ".agent-box/instantiation.md",
        ".agent-box/adoption.md", "tools/check_agent_docs_consistency.py",
        "grundsatz.md", ".agent-box-template.md",
        "ausfuehrungsmandat-protokoll.md",
    ],
    Path("docs/plans/template.md"): [
        "Planstatus:", "Aufgabe", "Betroffene Räume", "Testpflicht",
        "Abbruchbedingungen", "Abschlusskriterien",
        "Erfahrungsbericht", "erfahrungsbericht-protokoll.md",
        "Auslöser geprüft", "Bericht erforderlich",
        "Plan-ID", "Plan-Version", "Mandatstatus", "Freigegebener Scope",
    ],
}

COUPLING_HINTS: dict[str, list[str]] = {
    ".agent-box-template.md": [
        "tools/instantiate/instantiate_project_box.py", "AGENT-SETUP.md",
        "tools/instantiate/README.md",
    ],
    "docs/plans/template.md": [
        "AGENTS.md", "preflight-checkliste.md", "sprechakt-protokoll.md",
        "test-obligations.md", "erfahrungsbericht-protokoll.md",
        "ausfuehrungsmandat-protokoll.md",
    ],
    "AGENTS.md": [
        "preflight-checkliste.md", "task-schnitt.md",
        "sprechakt-protokoll.md", "regelmatrix.md",
        "blocker-und-abbruch-protokoll.md", "ausfuehrungsmandat-protokoll.md",
        "migration-bridges.md", "erfahrungsbericht-protokoll.md",
        "grundsatz.md", "glossar-README.md", "BROWNFIELD-MIGRATION.md",
    ],
    "package-schema.md": [
        "AGENTS.md", "test-obligations.md",
        "tools/check_import_layers.py",
        "glossar-domain.md", "glossar-system.md", "glossar-meta.md",
    ],
    "grundsatz.md": ["AGENTS.md", "glossar-README.md", "regelmatrix.md"],
    "glossar-domain.md": [
        "AGENTS.md", "glossar-README.md", "package-schema.md", "migration-bridges.md",
    ],
    "glossar-system.md": [
        "AGENTS.md", "glossar-README.md", "package-schema.md", "migration-bridges.md",
    ],
    "glossar-meta.md": [
        "AGENTS.md", "glossar-README.md", "migration-bridges.md",
    ],
    "glossar-README.md": [
        "AGENTS.md", "glossar-domain.md", "glossar-system.md", "glossar-meta.md",
        "preflight-checkliste.md",
    ],
    "migration-bridges.md": [
        "AGENTS.md", "sprechakt-protokoll.md", "package-schema.md",
        "glossar-domain.md", "glossar-system.md", "glossar-meta.md",
    ],
    "erfahrungsbericht-protokoll.md": ["AGENTS.md", "learning-matrix.md"],
    "learning-matrix.md": ["erfahrungsbericht-protokoll.md", "AGENTS.md"],
    "preflight-checkliste.md": [
        "AGENTS.md", "regelmatrix.md", "glossar-README.md",
        "blocker-und-abbruch-protokoll.md", "ausfuehrungsmandat-protokoll.md",
    ],
    "task-schnitt.md": [
        "AGENTS.md", "preflight-checkliste.md", "sprechakt-protokoll.md",
    ],
    "sprechakt-protokoll.md": [
        "AGENTS.md", "task-schnitt.md", "preflight-checkliste.md",
        "migration-bridges.md", "blocker-und-abbruch-protokoll.md",
        "ausfuehrungsmandat-protokoll.md",
    ],
    "test-obligations.md": [
        "AGENTS.md", "preflight-checkliste.md", "tools/resolve_test_obligations.py",
    ],
    "regelmatrix.md": [
        "AGENTS.md", "grundsatz.md", "blocker-und-abbruch-protokoll.md",
        "ausfuehrungsmandat-protokoll.md",
    ],
    "ausfuehrungsmandat-protokoll.md": [
        "AGENTS.md", "preflight-checkliste.md", "regelmatrix.md",
        "docs/plans/template.md", "sprechakt-protokoll.md",
        "BROWNFIELD-MIGRATION.md",
    ],
    "blocker-und-abbruch-protokoll.md": [
        "AGENTS.md", "preflight-checkliste.md", "regelmatrix.md",
        "tools/check_import_layers.py", "tools/check_agent_docs_consistency.py",
    ],
    "BROWNFIELD-MIGRATION.md": [
        "AGENTS.md", "AGENT-SETUP.md",
        "regelmatrix.md", "ausfuehrungsmandat-protokoll.md",
        "tools/instantiate/instantiate_project_box.py",
    ],
    "tools/check_import_layers.py": [
        "package-schema.md", "AGENTS.md", "test-obligations.md", "preflight-checkliste.md",
    ],
    "tools/resolve_test_obligations.py": [
        "test-obligations.md", "AGENTS.md", "erfahrungsbericht-protokoll.md",
    ],
    "tools/check_agent_docs_consistency.py": [
        "AGENTS.md", "regelmatrix.md", "grundsatz.md",
    ],
}

def placeholder_token(name: str) -> str:
    """Return a template token without embedding the token literal in checker code.

    Wichtig: Diese Funktion darf nicht durch einen naiven Template-Replace
    zerstoert werden. Deshalb steht im Checker-Code bewusst kein zusammenhaengendes
    Literal wie <PYTHON_PACKAGE_NAME>. Sonst wuerde eine globale Instanziierung auch die
    Sentinel-Liste veraendern und der instanziierte Checker wuerde reale
    Projektwerte faelschlich als offene Platzhalter melden.
    """
    return "<" + name + ">"


PLACEHOLDER_TOKENS = [
    placeholder_token("PROJECT_DISPLAY_NAME"),
    placeholder_token("PYTHON_PACKAGE_NAME"),
    placeholder_token("SOURCE_ROOT"),
    placeholder_token("TEST_ROOT"),
    placeholder_token("DOCS_ROOT"),
    placeholder_token("TOOLS_ROOT"),
    placeholder_token("IMPORT_LAYER_CHECK_CMD"),
    placeholder_token("PYTHON_LINT_CMD"),
    placeholder_token("PYTHON_FORMAT_CHECK_CMD"),
    placeholder_token("PYTHON_TYPECHECK_CMD"),
    placeholder_token("PYTHON_TEST_CMD"),
    placeholder_token("FULL_VALIDATION_CMD"),
]


# ---------------------------------------------------------------------------
# Datenmodell
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Finding:
    severity: str  # "ERROR" | "WARN" | "INFO"
    path: Path
    message: str


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_required_files(mode: str) -> list[Finding]:
    findings: list[Finding] = []
    for path in required_files_for(mode):
        if not path.exists():
            findings.append(Finding("ERROR", path, "Pflichtdatei fehlt."))
    for path in OPTIONAL_FILES:
        if not path.exists():
            findings.append(Finding("INFO", path,
                "Optionale Datei fehlt (empfohlen nach erster Session)."))
    # README-Regel ist modusabhängig (siehe forbidden_files_for).
    for path in forbidden_files_for(mode):
        if path.exists():
            findings.append(Finding("ERROR", path,
                "Im Template-Modus darf die Box kein README.md enthalten. "
                "README.md gehört dem Template-Repository oder dem Zielprojekt. "
                "Box-Anleitung steht in AGENT-SETUP.md."))
    # Hinweis im instanziierten Projekt: AGENT-SETUP.md sollte verschoben/entfernt sein.
    if mode == "instantiated" and Path("AGENT-SETUP.md").exists():
        findings.append(Finding("WARN", Path("AGENT-SETUP.md"),
            "AGENT-SETUP.md ist ein Template-Artefakt. Nach Instanziierung nach "
            "docs/agent-box-instantiation.md verschieben oder entfernen."))
    return findings


def check_required_terms() -> list[Finding]:
    findings: list[Finding] = []
    for path, terms in REQUIRED_TERMS_BY_FILE.items():
        if not path.exists():
            continue
        text = read_text(path)
        for term in terms:
            if term not in text:
                findings.append(Finding("ERROR", path,
                    f"Pflichtbegriff fehlt: {term!r}"))
    return findings


def check_project_state_marker(mode: str) -> list[Finding]:
    """Im Projektmodus muss genau ein Herkunftsmarker existieren.

    Greenfield-Projekte besitzen .agent-box/instantiation.md.
    Brownfield-adoptierte Projekte besitzen .agent-box/adoption.md.
    Beide zugleich oder keiner von beiden sind ein Zustandsfehler.
    """
    findings: list[Finding] = []
    if mode != "instantiated":
        return findings

    instantiation = Path(".agent-box/instantiation.md")
    adoption = Path(".agent-box/adoption.md")
    has_instantiation = instantiation.exists()
    has_adoption = adoption.exists()

    if has_instantiation == has_adoption:
        if has_instantiation:
            findings.append(Finding("ERROR", Path(".agent-box"),
                "Projektzustand unklar: .agent-box/instantiation.md und "
                ".agent-box/adoption.md existieren beide. Genau ein Marker ist erlaubt."))
        else:
            findings.append(Finding("ERROR", Path(".agent-box"),
                "Projektzustandsmarker fehlt: erwartet genau eine Datei aus "
                ".agent-box/instantiation.md oder .agent-box/adoption.md."))
        return findings

    if has_instantiation:
        text = read_text(instantiation)
        for term in ["Box-Name:", "Box-Version:"]:
            if term not in text:
                findings.append(Finding("ERROR", instantiation,
                    f"Pflichtfeld fehlt: {term}"))

    if has_adoption:
        text = read_text(adoption)
        for term in ["Status: active", "Aufnahmetyp: brownfield", "Box-Name:", "Box-Version:"]:
            if term not in text:
                findings.append(Finding("ERROR", adoption,
                    f"Pflichtfeld fehlt: {term}"))

    return findings


def check_placeholders(mode: str) -> list[Finding]:
    """
    mode='template'     → Platzhalter erwartet, WARN nur wenn KEINE Platzhalter
                          in Dateien wo welche erwartet sind (z.B. AGENTS.md)
    mode='instantiated' → Platzhalter sind immer ERROR
    """
    findings: list[Finding] = []
    if mode == "instantiated":
        # AGENT-SETUP.md ist Template-Artefakt — im instanziierten Projekt
        # nicht mehr Pflicht und nicht auf Platzhalter zu prüfen.
        check_files = [p for p in (REQUIRED_FILES_CORE + OPTIONAL_FILES)]
        for path in check_files:
            if not path.exists():
                continue
            text = read_text(path)
            for token in PLACEHOLDER_TOKENS:
                if token in text:
                    findings.append(Finding("ERROR", path,
                        f"Nicht ersetzter Platzhalter: {token}"))
    else:  # template
        # Im Template ist alles ok, solange Dokumente sich erkennen lassen.
        # Wir prüfen nur ob AGENTS.md überhaupt PROJECT_DISPLAY_NAME/PYTHON_PACKAGE_NAME-Platzhalter erwähnt,
        # sonst ist es kein Template mehr.
        agents = Path("AGENTS.md")
        if agents.exists():
            text = read_text(agents)
            display_name_token = placeholder_token("PROJECT_DISPLAY_NAME")
            package_name_token = placeholder_token("PYTHON_PACKAGE_NAME")
            if display_name_token not in text or package_name_token not in text:
                findings.append(Finding("INFO", agents,
                    "AGENTS.md enthaelt keinen PROJECT_DISPLAY_NAME/PYTHON_PACKAGE_NAME-Platzhalter. "
                    "Box moeglicherweise schon instanziiert? Dann --instantiated verwenden."))
    return findings


def check_strandjunction_residues(mode: str) -> list[Finding]:
    """Prüft ob StrandJunction-Reste in der generischen Box stehen."""
    findings: list[Finding] = []
    forbidden_residues = [
        "strandjunction", "libstrandjunction",
        "failure.source", "condition.source",
        "FactStore",
        "OperationStrand", "CallContext",
        "graph::", "namespace strand",
    ]
    severity = "ERROR" if mode == "instantiated" else "WARN"
    all_files = REQUIRED_FILES + OPTIONAL_FILES
    for path in all_files:
        if not path.exists():
            continue
        text = read_text(path)
        for residue in forbidden_residues:
            if residue in text:
                findings.append(Finding(severity, path,
                    f"StrandJunction-Rest gefunden: {residue!r}. "
                    f"Diese Box ist generisch — projektspezifische Begriffe entfernen."))
    return findings


def check_layer_config_sync() -> list[Finding]:
    findings: list[Finding] = []
    checker_path = Path("tools/check_import_layers.py")
    if not checker_path.exists():
        return findings
    standard_layers = ["domain", "system", "infrastructure",
                       "adapters", "cli", "shared", "tools", "tests"]
    checker_text = read_text(checker_path)
    for layer in standard_layers:
        if f'"{layer}"' not in checker_text and f"'{layer}'" not in checker_text:
            findings.append(Finding("WARN", checker_path,
                f"Raum '{layer}' nicht als String-Literal in LAYER_BY_PACKAGE_PART gefunden."))
    return findings


def _section_lines(lines: list[str], section_heading: str) -> list[str]:
    """Return lines inside a top-level Markdown section.

    The start line is included; the next `## ` heading ends the section.
    """
    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == section_heading)
    except StopIteration:
        return []
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## "):
            end = i
            break
    return lines[start:end]


def check_glossar_consistency(mode: str) -> list[Finding]:
    """
    Erkennt reale Glossar-Einträge zuverlässig.

    Ein Eintrag ist ein "### <Begriff>"-Heading im Abschnitt "## 3. Begriffe".
    Platzhalter wie "### <Begriff>" (mit spitzen Klammern) zählen nicht als realer Eintrag.

    Template:     leere Glossare → INFO.
    Instantiated: leere Glossare → WARN (Projektstart ok, nach erstem Sprechakt nicht).
    """
    findings: list[Finding] = []
    for glossar in [
        Path("glossar-domain.md"),
        Path("glossar-system.md"),
        Path("glossar-meta.md"),
    ]:
        if not glossar.exists():
            continue
        lines = read_text(glossar).splitlines()
        begriffe_lines = _section_lines(lines, "## 3. Begriffe")

        # Reale Einträge: "### " Heading im Begriffe-Abschnitt,
        # aber kein Platzhalter "### <...>".
        real_entries = [
            line for line in begriffe_lines
            if line.startswith("### ") and "<" not in line
        ]

        if not real_entries:
            severity = "INFO" if mode == "template" else "WARN"
            if glossar.name == "glossar-meta.md":
                findings.append(Finding(severity, glossar,
                    "Keine Meta-Glossar-Einträge im Abschnitt '## 3. Begriffe' gefunden. "
                    "glossar-meta.md muss die Agenten-Metabegriffe enthalten."))
            else:
                findings.append(Finding(severity, glossar,
                    "Keine Glossar-Einträge im Abschnitt '## 3. Begriffe' gefunden. "
                    "Erster projektspezifischer Eintrag entsteht durch Sprechakt SP1 (Domain) "
                    "oder SP2 (System). Eintragsformat: '### <Begriffsname>'."))
    return findings


def check_migration_bridges(mode: str) -> list[Finding]:
    findings: list[Finding] = []
    bridges_path = Path("migration-bridges.md")
    if not bridges_path.exists():
        return findings

    agents_path = Path("AGENTS.md")
    if agents_path.exists():
        text = read_text(agents_path)
        if "migration-bridges.md" not in text:
            findings.append(Finding("ERROR", agents_path,
                "AGENTS.md verweist nicht auf migration-bridges.md."))

    bridges_text = read_text(bridges_path)
    if "BR-001" not in bridges_text and "BR-" not in bridges_text:
        severity = "INFO" if mode == "template" else "WARN"
        findings.append(Finding(severity, bridges_path,
            "Keine Bridge-Einträge (BR-NNN) gefunden."))

    # Im instanziierten Projekt: Beispiel-Eintrag sollte ersetzt sein
    if mode == "instantiated" and "legacy_customer_id" in bridges_text:
        findings.append(Finding("ERROR", bridges_path,
            "Generisches Beispiel 'legacy_customer_id' steht noch drin — "
            "durch projektspezifische Bridges ersetzen oder entfernen."))
    return findings


def check_erfahrungsbericht_protokoll() -> list[Finding]:
    findings: list[Finding] = []
    eb_path = Path("erfahrungsbericht-protokoll.md")
    if not eb_path.exists():
        return findings
    agents_path = Path("AGENTS.md")
    if agents_path.exists():
        text = read_text(agents_path)
        if "erfahrungsbericht" not in text.lower():
            findings.append(Finding("WARN", agents_path,
                "AGENTS.md erwähnt keine Erfahrungsberichte."))
    return findings


def check_markdown_fences() -> list[Finding]:
    """Findet unbalancierte Markdown-Code-Fences in operativen Dokumenten."""
    findings: list[Finding] = []
    for path in REQUIRED_FILES + OPTIONAL_FILES:
        if not path.exists() or path.suffix != ".md":
            continue
        count = read_text(path).count("```")
        if count % 2 != 0:
            findings.append(Finding("ERROR", path,
                f"Unbalancierte Markdown-Code-Fences: {count} Vorkommen von ``` ."))
    return findings


def check_legacy_sprechakt_ids() -> list[Finding]:
    """Verhindert die alte Kollision: drei disjunkte Code-Familien.

    HARD-Abbruch:  H-Codes (H1 aufwaerts)
    SOFT-Abbruch:  SA-Codes (frueher nackte S-Codes — kollidierte mit Sprechakt)
    Sprechakt:     SP-Codes

    Gefangen werden veraltete Sprechakt- und SOFT-Schreibweisen
    ohne SA- bzw. SP-Praefix in den jeweiligen Kontexten.
    """
    findings: list[Finding] = []
    sprechakt_patterns = [
        re.compile(r"Sprechakt S[1-7]\b"),
        re.compile(r"Sprechakt-Klasse:\s*S(?!P)(?!A)"),
        re.compile(r"Sprechakt-Klassen S[1-7]"),
    ]
    # SOFT-Abbruch-Codes muessen SA heissen. Ein nacktes S<n> in einer Zeile
    # mit SOFT-Kontext ist veraltet.
    soft_pattern = re.compile(r"\bS[1-6]\b")
    soft_context = re.compile(r"SOFT|Test rot|Lint rot|Typecheck rot|Build-/Installationsfehler")

    for path in REQUIRED_FILES + OPTIONAL_FILES + list(Path("tools").glob("*.py")):
        if not path.exists():
            continue
        text = read_text(path)
        is_markdown = path.suffix == ".md"
        for line_no, line in enumerate(text.splitlines(), start=1):
            if any(p.search(line) for p in sprechakt_patterns):
                findings.append(Finding("ERROR", path,
                    f"Veraltete Sprechakt-ID in Zeile {line_no}: Sprechakte heißen SP1..SP7."))
            # SOFT-Heuristik nur in Markdown: Tool-Quelltext enthält die Muster
            # naturgemäß als Regex-Literale und Meldungstexte.
            if is_markdown and soft_pattern.search(line) and soft_context.search(line) \
                    and "SA" not in line and "SP" not in line:
                findings.append(Finding("ERROR", path,
                    f"Veraltete SOFT-Abbruch-ID in Zeile {line_no}: SOFT-Abbrüche heißen SA1..SA6."))
    return findings


def check_experience_trigger_sync() -> list[Finding]:
    """Prüft, ob E1..E5 im Erfahrungsbericht-Protokoll und Tool sichtbar sind."""
    findings: list[Finding] = []
    required = ["E1", "E2", "E3", "E4", "E5"]
    for path in [Path("erfahrungsbericht-protokoll.md")]:
        if not path.exists():
            continue
        text = read_text(path)
        for trigger in required:
            if trigger not in text:
                findings.append(Finding("ERROR", path,
                    f"Erfahrungsbericht-Trigger fehlt: {trigger}"))
    tool = Path("tools/resolve_test_obligations.py")
    if tool.exists():
        text = read_text(tool)
        for trigger in required:
            if trigger not in text:
                findings.append(Finding("ERROR", tool,
                    f"Erfahrungsbericht-Trigger fehlt im Selfcheck-Output: {trigger}"))
    return findings


def check_reference_integrity() -> list[Finding]:
    """Prueft einfache, aber operative Referenzdrift."""
    findings: list[Finding] = []
    historical_files = {Path("CHANGELOG.md"), Path("tutorial.md")}
    allowed_compact_context = "frueheres `AGENTS-COMPACT.md`"

    scan_files = REQUIRED_FILES + OPTIONAL_FILES + list(Path("tools").glob("*.py"))
    for path in scan_files:
        if not path.exists():
            continue
        text = read_text(path)
        if path not in historical_files and "AGENTS-COMPACT.md" in text \
                and allowed_compact_context not in text:
            findings.append(Finding("ERROR", path,
                "Aktiver Verweis auf entfernte Datei AGENTS-COMPACT.md."))

        if re.search(r"AGENTS\.md\s*(§|Abschnitt)\s*\d+", text):
            findings.append(Finding("ERROR", path,
                "Instabile numerische Referenz auf AGENTS.md gefunden. "
                "Stattdessen zuständiges Dokument oder Abschnittstitel nennen."))

    return findings


def check_coupling_hints(changed_files: list[str]) -> list[Finding]:
    findings: list[Finding] = []
    if not changed_files:
        return findings
    changed_set = {Path(p).as_posix() for p in changed_files}
    for changed in sorted(changed_set):
        hints = COUPLING_HINTS.get(changed, [])
        for coupled in hints:
            if coupled not in changed_set:
                findings.append(Finding("WARN", Path(changed),
                    f"Änderung an '{changed}' → '{coupled}' prüfen (Inhalt, nicht Präsenz)."))
    return findings


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def print_findings(findings: list[Finding]) -> None:
    for f in findings:
        print(f"{f.path}: {f.severity}: {f.message}")


def print_preflight(findings: list[Finding], mode: str) -> None:
    errors = [f for f in findings if f.severity == "ERROR"]
    warnings = [f for f in findings if f.severity == "WARN"]
    if not errors:
        print(f"✓ PREFLIGHT DOCS-CONSISTENCY OK (Modus: {mode})")
        print("  Struktureller Check bestanden — kein Beweis inhaltlicher Konsistenz.")
        if warnings:
            print(f"  ({len(warnings)} Warnungen — keine Blocker)")
        return
    print(f"✗ PREFLIGHT DOCS-CONSISTENCY FEHLGESCHLAGEN — {len(errors)} Fehler (Modus: {mode})\n")
    print("ABBRUCH: Agentendokumente inkonsistent.")
    print("Gemäß blocker-und-abbruch-protokoll.md H3.\n")
    print("Evidence:")
    for f in errors:
        print(f"  {f.path}: {f.message}")
    if warnings:
        print(f"\nWarnungen ({len(warnings)}):")
        for f in warnings:
            print(f"  {f.path}: {f.message}")



def has_error(findings: list[Finding]) -> bool:
    return any(f.severity == "ERROR" for f in findings)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Prüft Konsistenz der Agentendokumente."
    )
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("--template", action="store_const",
        dest="mode", const="template",
        help="Template-Modus (Default): Platzhalter erlaubt, leere Glossare ok.")
    mode_group.add_argument("--instantiated", action="store_const",
        dest="mode", const="instantiated",
        help="Projekt-Modus: Platzhalter sind ERROR, Bridge-Beispiel sollte ersetzt sein.")
    parser.add_argument("--strict-placeholders", action="store_true",
        help="(Legacy) Platzhalter als ERROR statt WARN — entspricht --instantiated.")
    parser.add_argument("--changed-file", action="append", default=[], dest="changed_file",
        help="Geänderte Datei für Kopplungshinweise.")
    parser.add_argument("--preflight", action="store_true",
        help="Kompakter Agenten-Output.")

    args = parser.parse_args(argv)

    # Modus bestimmen
    mode = args.mode or ("instantiated" if args.strict_placeholders else "template")

    findings: list[Finding] = []
    findings.extend(check_required_files(mode))
    findings.extend(check_required_terms())
    findings.extend(check_project_state_marker(mode))
    findings.extend(check_placeholders(mode))
    findings.extend(check_strandjunction_residues(mode))
    findings.extend(check_layer_config_sync())
    findings.extend(check_glossar_consistency(mode))
    findings.extend(check_migration_bridges(mode))
    findings.extend(check_erfahrungsbericht_protokoll())
    findings.extend(check_markdown_fences())
    findings.extend(check_legacy_sprechakt_ids())
    findings.extend(check_experience_trigger_sync())
    findings.extend(check_reference_integrity())
    findings.extend(check_coupling_hints(args.changed_file))


    if args.preflight:
        print_preflight(findings, mode)
        return 1 if has_error(findings) else 0

    if findings:
        print_findings(findings)
        print()

    if has_error(findings):
        print(f"Agent-Docs-Consistency: FAILED (Modus: {mode})")
        return 1
    if any(f.severity == "WARN" for f in findings):
        print(f"Agent-Docs-Consistency: WARNINGS (Modus: {mode})")
        return 0
    print(f"Agent-Docs-Consistency: OK (Modus: {mode})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
