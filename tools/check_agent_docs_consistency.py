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
    Path("docs/runs/checkpoint-template.md"),
]

# AGENT-SETUP.md ist ein Template-Artefakt:
#   Template-Modus:     Pflichtdatei (erklärt die Instanziierung).
#   Instantiated-Modus: NICHT Pflicht. Soll nach docs/ verschoben oder entfernt sein.
#                       Wird im instanziierten Projekt nicht auf Platzhalter geprüft.
TEMPLATE_ONLY_FILES = [
    Path("AGENT-SETUP.md"),
    Path(".agent-box-template.md"),
]

CURRENT_DOCUMENTATION_FILES: list[Path] = []

LEVEL_HEADER_FILES = [
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
    Path("docs/runs/checkpoint-template.md"),
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
        "bindende Router",
        "Task-Schnitt",
        "Schreibrechte",
        "Fast-Path",
        "Governance-Ausloeser",
        "Ausfuehrungsbreite",
        "Blosse Teilbarkeit ist kein Schnittgrund",
        "package-schema.md",
        "BROWNFIELD-MIGRATION.md",
        "blocker-und-abbruch-protokoll.md",
        "ausfuehrungsmandat-protokoll.md",
        "migration-bridges.md",
        "erfahrungsbericht-protokoll.md",
        "glossar-domain.md",
        "glossar-meta.md",
        "H10",
        "BF1",
        ".agent-box/adoption.md",
    ],
    Path("AGENT-SETUP.md"): [
        "Template-Zustand",
        "Projekt-Zustand",
        "Instanziierung",
        "Platzhalter",
        "AGENTS.md",
    ],
    Path("BROWNFIELD-MIGRATION.md"): [
        "Brownfield",
        "Datei-Aktionsmatrix",
        "Migrationsevidence",
        ".agent-box/migrations",
        "Baseline",
        "--force",
        "Bestehendes Python-Projekt",
        "Bestehendes Box-Projekt",
        "Observed State",
        "Accepted Local Truth",
        "Accepted Alternative",
        "Migration Candidate",
        "Legacy Defect",
        "Known Breach",
        "Discover",
        "Describe",
        "Decide",
        ".agent-box/adoption.md",
        "unboxed-to",
        "BF-Abbruch",
        "Accepted-Alternative-Kandidat",
        "Herkunftsmarker",
        "Aktuelle Box-Version",
        "Baseline-Anker",
        "Lokale Divergenz gegen Baseline-Anker",
        "Merge-Richtung",
        "Drei-Wege-Merge",
        "Migrationsmandat",
        "Zielmodellentscheidung",
        "WG-MUTATION",
        "Vorlaeufige Brownfield-Governance-Evidence",
        "dokumentierend, nicht normativ",
        "Zurueckgestellte Provenienzmechanismen",
        "Konformitaet",
        "ausfuehrungsmandat-protokoll.md",
        "BF1",
        "BF2",
        "BF3",
        "BF4",
        "BF5",
        "BF6",
        "BF7",
        "BF8",
        "BF9",
        "BF10",
        "BF11",
        "BF12",
    ],
    Path("blocker-und-abbruch-protokoll.md"): [
        "H1",
        "H10",
        "SA1",
        "SA6",
        "Abbruch-Evidence",
        "Wiedereinstieg",
        "Pendeln",
        "Stagnation",
        "Anti-Zeno",
        ".agent-box/evidence/erfahrungsberichte",
    ],
    Path("ausfuehrungsmandat-protokoll.md"): [
        "ANALYSE",
        "PLAN",
        "AUSFUEHRUNG",
        "Ausfuehrungsmandat",
        "WG-MUTATION",
        "Mandatstatus",
        "Plan-Version",
        "Delta-Freigabe",
        "Wirkungsgate",
        "diagnostische Wirkung",
        "normative Wirkung",
        "projekt-transformative Wirkung",
        "Direktauftrag",
        "Mandatsgrundlage",
        "Grundlagen-Version",
    ],
    Path("package-schema.md"): [
        "domain",
        "system",
        "infrastructure",
        "adapters",
        "Capability",
        "Known Breaches",
        "LAYER_BY_PACKAGE_PART",
        "decision",
    ],
    Path("preflight-checkliste.md"): [
        "AGENTS.md",
        "package-schema.md",
        "Import",
        "Testpflicht",
        "Schreibrechte",
        "glossar-README.md",
        "Autonomieregel",
        "PF-AGENTS",
        "PF-SCHREIBEN",
        "PF-PLAN",
        "WG-MUTATION",
    ],
    Path("task-schnitt.md"): [
        "Semantic Working Set",
        "SWS",
        "T1",
        "T2",
        "T3",
        "T4",
        "T5",
        "Binding",
    ],
    Path("sprechakt-protokoll.md"): [
        "Sprechakt",
        "SP0",
        "SP1",
        "SP2",
        "SP7",
        "docs/sprechakte",
        "offen",
        "festgelegt",
        "abgelehnt",
        "superseded",
        "widerrufen",
        "Ausfuehrungsmandat",
    ],
    Path("regelmatrix.md"): [
        "Autoritaetsmodell",
        "AGENTS.md",
        "package-schema.md",
        "Widerspruch",
        "grundsatz.md",
        "BF",
        "blocker-und-abbruch-protokoll.md",
        "ausfuehrungsmandat-protokoll.md",
        "beschreibbar",
        "freigegeben",
    ],
    Path("test-obligations.md"): [
        "Testpflicht",
        "domain",
        "system",
        "infrastructure",
        "adapters",
    ],
    Path("migration-bridges.md"): [
        "legacy-bridge",
        "do-not-touch-mechanically",
        "canonical",
        "SP6",
        "BR-",
    ],
    Path("erfahrungsbericht-protokoll.md"): [
        "E1",
        "E2",
        "E3",
        "E4",
        "E5",
        ".agent-box/evidence/erfahrungsberichte",
        "learning-matrix",
        "Vorgeschlagene Musterkennung",
    ],
    Path("grundsatz.md"): [
        "Reifizierung",
        "Plausibilität",
        "Projektionen",
        "Autonomieregel",
        "Glossar",
        "Sprechakt",
        "Abbruch",
    ],
    Path("glossar-domain.md"): [
        "Kompetenzfrage",
        "Invarianten",
        "Projektionen",
        "Migrationsstatus",
        "SP7",
        "domain",
    ],
    Path("glossar-system.md"): [
        "Kompetenzfrage",
        "Invarianten",
        "Projektionen",
        "Migrationsstatus",
        "system",
        "SP7",
    ],
    Path("glossar-meta.md"): [
        "Kompetenzfrage",
        "Invarianten",
        "Projektionen",
        "Migrationsstatus",
        "meta",
        "SP7",
        "Agenten-Box",
        "Instanziierungs-Sprechakt",
        "Semantic Working Set",
        "Observed State",
        "Accepted Local Truth",
        "Legacy Defect",
        "Migrationsevidence",
        "BF-Code",
        "widerrufen",
    ],
    Path("glossar-README.md"): [
        "Ladeprotokoll",
        "glossar-domain.md",
        "glossar-system.md",
        "glossar-meta.md",
        "migration-bridges.md",
        "SP7",
        "T1",
        "Autonomieregel",
    ],
    Path(".agent-box-template.md"): [
        "Box-Version",
        "Markdown only",
        "Box-Artefakte",
        "Ersetzungsziele des Instanziierungswerkzeugs",
        "Instanziierungsnachweis",
        ".agent-box/instantiation.md",
        ".agent-box/adoption.md",
        "tools/check_agent_docs_consistency.py",
        "grundsatz.md",
        ".agent-box-template.md",
        "ausfuehrungsmandat-protokoll.md",
        "docs/runs/checkpoint-template.md",
    ],
    Path("docs/plans/template.md"): [
        "Planstatus:",
        "Aufgabe",
        "Betroffene Räume",
        "Testpflicht",
        "Abbruchbedingungen",
        "Abschlusskriterien",
        "Erfahrungsbericht",
        "erfahrungsbericht-protokoll.md",
        "Auslöser geprüft",
        "Bericht erforderlich",
        "Plan-ID",
        "Plan-Version",
        "Plan-Schema-Version",
        "Mandat-ID",
        "Mandatstatus",
        "Mandatsgrundlage",
        "Grundlagen-Version",
        "Freigegebener Scope",
        "Contract-ID",
        "Contract-Status",
        "Run-ID",
        "Priming-Revision",
        "Repository-Vertragsrevision",
        "Plan-Revision",
        "Scope-ID",
        "Scope-Version",
        "Authorization-Revision",
        "Base-Snapshot",
        "Interaktionsprofil",
        "Recovery-Profil",
        "Arbeitsprofil",
        "Ressourcenscope",
        "Wirkungsscope",
        "Capability-Scope",
        "Explizit erlaubte Wirkungen",
        "Abgeleitete Wirkungen",
        "Verbotene Wirkungen",
    ],
    Path("docs/runs/checkpoint-template.md"): [
        "Run-ID",
        "Contract-ID",
        "Plan-ID",
        "Plan-Revision",
        "Mandat-ID",
        "Mandatstatus",
        "Priming-Revision",
        "Repository-Vertragsrevision",
        "Base-Snapshot",
        "Interaktionsprofil",
        "Recovery-Profil",
        "Arbeitsprofil",
        "Checkpoint-Nr",
        "Vorgaenger-Checkpoint",
        "Zeitpunkt-UTC",
        "Run-Status:",
        "Checkpoint-Status:",
        "Aktueller HEAD",
        "Letzter sicherer Snapshot",
        "Worktree-State",
        "Dirty paths",
        "Recovery artifact",
        "Recovery status",
        "Naechster zulaessiger Schritt",
    ],
}

COUPLING_HINTS: dict[str, list[str]] = {
    ".agent-box-template.md": [
        "tools/instantiate/instantiate_project_box.py",
        "AGENT-SETUP.md",
        "tools/instantiate/README.md",
    ],
    "docs/plans/template.md": [
        "AGENTS.md",
        "preflight-checkliste.md",
        "sprechakt-protokoll.md",
        "test-obligations.md",
        "erfahrungsbericht-protokoll.md",
        "ausfuehrungsmandat-protokoll.md",
    ],
    "AGENTS.md": [
        "preflight-checkliste.md",
        "task-schnitt.md",
        "sprechakt-protokoll.md",
        "regelmatrix.md",
        "blocker-und-abbruch-protokoll.md",
        "ausfuehrungsmandat-protokoll.md",
        "migration-bridges.md",
        "erfahrungsbericht-protokoll.md",
        "grundsatz.md",
        "glossar-README.md",
        "BROWNFIELD-MIGRATION.md",
    ],
    "package-schema.md": [
        "AGENTS.md",
        "test-obligations.md",
        "tools/check_import_layers.py",
        "glossar-domain.md",
        "glossar-system.md",
        "glossar-meta.md",
    ],
    "grundsatz.md": ["AGENTS.md", "glossar-README.md", "regelmatrix.md"],
    "glossar-domain.md": [
        "AGENTS.md",
        "glossar-README.md",
        "package-schema.md",
        "migration-bridges.md",
    ],
    "glossar-system.md": [
        "AGENTS.md",
        "glossar-README.md",
        "package-schema.md",
        "migration-bridges.md",
    ],
    "glossar-meta.md": [
        "AGENTS.md",
        "glossar-README.md",
        "migration-bridges.md",
    ],
    "glossar-README.md": [
        "AGENTS.md",
        "glossar-domain.md",
        "glossar-system.md",
        "glossar-meta.md",
        "preflight-checkliste.md",
    ],
    "migration-bridges.md": [
        "AGENTS.md",
        "sprechakt-protokoll.md",
        "package-schema.md",
        "glossar-domain.md",
        "glossar-system.md",
        "glossar-meta.md",
    ],
    "erfahrungsbericht-protokoll.md": ["AGENTS.md", "learning-matrix.md"],
    "learning-matrix.md": ["erfahrungsbericht-protokoll.md", "AGENTS.md"],
    "preflight-checkliste.md": [
        "AGENTS.md",
        "regelmatrix.md",
        "glossar-README.md",
        "blocker-und-abbruch-protokoll.md",
        "ausfuehrungsmandat-protokoll.md",
    ],
    "task-schnitt.md": [
        "AGENTS.md",
        "preflight-checkliste.md",
        "sprechakt-protokoll.md",
    ],
    "sprechakt-protokoll.md": [
        "AGENTS.md",
        "task-schnitt.md",
        "preflight-checkliste.md",
        "migration-bridges.md",
        "blocker-und-abbruch-protokoll.md",
        "ausfuehrungsmandat-protokoll.md",
    ],
    "test-obligations.md": [
        "AGENTS.md",
        "preflight-checkliste.md",
        "tools/resolve_test_obligations.py",
        "package-schema.md",
    ],
    "regelmatrix.md": [
        "AGENTS.md",
        "grundsatz.md",
        "blocker-und-abbruch-protokoll.md",
        "ausfuehrungsmandat-protokoll.md",
        "preflight-checkliste.md",
    ],
    "ausfuehrungsmandat-protokoll.md": [
        "AGENTS.md",
        "preflight-checkliste.md",
        "regelmatrix.md",
        "docs/plans/template.md",
        "sprechakt-protokoll.md",
        "BROWNFIELD-MIGRATION.md",
    ],
    "blocker-und-abbruch-protokoll.md": [
        "AGENTS.md",
        "preflight-checkliste.md",
        "regelmatrix.md",
        "tools/check_import_layers.py",
        "tools/check_agent_docs_consistency.py",
    ],
    "BROWNFIELD-MIGRATION.md": [
        "AGENTS.md",
        "AGENT-SETUP.md",
        "regelmatrix.md",
        "ausfuehrungsmandat-protokoll.md",
        "tools/instantiate/instantiate_project_box.py",
    ],
    "tools/check_import_layers.py": [
        "package-schema.md",
        "AGENTS.md",
        "test-obligations.md",
        "preflight-checkliste.md",
    ],
    "tools/resolve_test_obligations.py": [
        "test-obligations.md",
        "AGENTS.md",
        "erfahrungsbericht-protokoll.md",
    ],
    "tools/check_agent_docs_consistency.py": [
        "AGENTS.md",
        "regelmatrix.md",
        "grundsatz.md",
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
            findings.append(
                Finding(
                    "INFO",
                    path,
                    "Optionale Datei fehlt (empfohlen nach erster Session).",
                )
            )
    # README-Regel ist modusabhängig (siehe forbidden_files_for).
    for path in forbidden_files_for(mode):
        if path.exists():
            findings.append(
                Finding(
                    "ERROR",
                    path,
                    "Im Template-Modus darf die Box kein README.md enthalten. "
                    "README.md gehört dem Template-Repository oder dem Zielprojekt. "
                    "Box-Anleitung steht in AGENT-SETUP.md.",
                )
            )
    # Hinweis im instanziierten Projekt: AGENT-SETUP.md sollte verschoben/entfernt sein.
    if mode == "instantiated" and Path("AGENT-SETUP.md").exists():
        findings.append(
            Finding(
                "WARN",
                Path("AGENT-SETUP.md"),
                "AGENT-SETUP.md ist ein Template-Artefakt. Nach Instanziierung nach "
                "docs/agent-box-instantiation.md verschieben oder entfernen.",
            )
        )
    return findings


def check_required_terms(mode: str) -> list[Finding]:
    findings: list[Finding] = []
    for path, terms in REQUIRED_TERMS_BY_FILE.items():
        if mode == "instantiated" and path in TEMPLATE_ONLY_FILES:
            continue
        if not path.exists():
            continue
        text = read_text(path)
        for term in terms:
            if term not in text:
                findings.append(
                    Finding("ERROR", path, f"Pflichtbegriff fehlt: {term!r}")
                )
    return findings


def check_level_headers() -> list[Finding]:
    findings: list[Finding] = []
    required = ["Ebene:", "Rolle:", "Autoritative Frage:", "Nicht zustaendig fuer:"]
    allowed_levels = {"PRIMING", "REPOSITORY", "PLAN/RUN", "MIXED-TRANSITION"}
    for path in LEVEL_HEADER_FILES:
        if not path.exists():
            continue
        text = read_text(path)
        head = "\n".join(text.splitlines()[:12])
        for term in required:
            if term not in head:
                findings.append(
                    Finding(
                        "ERROR",
                        path,
                        f"Ebenenkopf unvollstaendig: {term} fehlt im Dokumentkopf.",
                    )
                )
        match = re.search(r"^>\s*Ebene:\s*(.+)$", head, flags=re.MULTILINE)
        if match:
            value = match.group(1).strip()
            if value not in allowed_levels:
                findings.append(
                    Finding("ERROR", path, f"Ungueltiger Ebenenwert: {value}.")
                )
    return findings


def check_plan_and_checkpoint_instances() -> list[Finding]:
    findings: list[Finding] = []
    # Pflichtfelder fuer Plaene mit Plan-Schema-Version: v0.3.7+
    # Aeltere Plaene (ohne Plan-Schema-Version) werden nur auf Kernfelder geprueft.
    plan_required_core = [
        "Plan-ID:",
        "Plan-Version:",
        "Mandat-ID:",
        "Mandatstatus:",
        "Ressourcenscope",
        "Wirkungsscope",
        "Capability-Scope",
    ]
    plan_required_v037 = [
        "Plan-Schema-Version:",
        "Contract-ID:",
        "Contract-Status:",
        "Run-ID:",
        "Priming-Revision:",
        "Repository-Vertragsrevision:",
        "Plan-Revision:",
        "Scope-ID:",
        "Scope-Version:",
        "Authorization-Revision:",
        "Base-Snapshot:",
        "Interaktionsprofil:",
        "Recovery-Profil:",
        "Arbeitsprofil:",
        "Mandatsrevision:",
    ]
    for path in Path("docs/plans").glob("*.md"):
        if path.name == "template.md":
            continue
        text = read_text(path)
        m = re.search(r"^Plan-Schema-Version:\s*(\S+)", text, flags=re.MULTILINE)
        schema_version = m.group(1).strip() if m else None
        if schema_version is None:
            findings.append(
                Finding(
                    "WARN",
                    path,
                    "Plan-Schema-Version fehlt. Aeltere Plaene werden nur auf Kernfelder geprueft. "
                    "Fuer vollstaendige Pruefung Plan-Schema-Version: v0.3.7 ergaenzen.",
                )
            )
            continue
        required = plan_required_core + plan_required_v037
        for term in required:
            if term not in text:
                findings.append(
                    Finding("ERROR", path, f"Planinstanz-Pflichtfeld fehlt: {term}")
                )

    checkpoint_required = [
        "Run-ID:",
        "Contract-ID:",
        "Plan-ID:",
        "Plan-Revision:",
        "Mandat-ID:",
        "Mandatstatus:",
        "Checkpoint-Nr:",
        "Run-Status:",
        "Checkpoint-Status:",
        "Aktueller HEAD:",
        "Letzter sicherer Snapshot:",
        "Worktree-State:",
        "Dirty paths:",
        "Recovery artifact:",
        "Recovery status:",
        "Naechster zulaessiger Schritt:",
    ]
    checkpoint_filename_re = re.compile(r"^checkpoint-\d{4}\.md$")
    run_root = Path("docs/runs")
    if run_root.exists():
        for path in run_root.rglob("*.md"):
            if not checkpoint_filename_re.match(path.name):
                continue
            text = read_text(path)
            for term in checkpoint_required:
                if term not in text:
                    findings.append(
                        Finding("ERROR", path, f"Checkpoint-Pflichtfeld fehlt: {term}")
                    )
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
            findings.append(
                Finding(
                    "ERROR",
                    Path(".agent-box"),
                    "Projektzustand unklar: .agent-box/instantiation.md und "
                    ".agent-box/adoption.md existieren beide. Genau ein Marker ist erlaubt.",
                )
            )
        else:
            findings.append(
                Finding(
                    "ERROR",
                    Path(".agent-box"),
                    "Projektzustandsmarker fehlt: erwartet genau eine Datei aus "
                    ".agent-box/instantiation.md oder .agent-box/adoption.md.",
                )
            )
        return findings

    if has_instantiation:
        text = read_text(instantiation)
        for term in ["Box-Name:", "Box-Version:"]:
            if term not in text:
                findings.append(
                    Finding("ERROR", instantiation, f"Pflichtfeld fehlt: {term}")
                )
        valid_statuses = {
            "active",
            "unverified",
            "failed",
            "pending",
            "verification-failed",
            "festgelegt",
        }
        status_match = re.search(r"^Status:\s*(\S+)", text, flags=re.MULTILINE)
        if status_match:
            status = status_match.group(1)
            if status not in valid_statuses:
                findings.append(
                    Finding(
                        "ERROR",
                        instantiation,
                        f"Ungueltiger Instanziierungsstatus: {status!r}. "
                        f"Erlaubt: {', '.join(sorted(valid_statuses))}",
                    )
                )
        else:
            findings.append(Finding("ERROR", instantiation, "Status-Feld fehlt."))

    if has_adoption:
        text = read_text(adoption)
        for term in [
            "Status: active",
            "Aufnahmetyp: brownfield",
            "Box-Name:",
            "Box-Version:",
            "Zielmodellentscheidung:",
            "Migrationsmandat:",
            "Mandat-ID:",
            "Mandatsgrundlage:",
            "Grundlagen-ID:",
            "Grundlagen-Version:",
            "Scope:",
        ]:
            if term not in text:
                findings.append(
                    Finding("ERROR", adoption, f"Pflichtfeld fehlt: {term}")
                )

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
                    findings.append(
                        Finding("ERROR", path, f"Nicht ersetzter Platzhalter: {token}")
                    )
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
                findings.append(
                    Finding(
                        "INFO",
                        agents,
                        "AGENTS.md enthaelt keinen PROJECT_DISPLAY_NAME/PYTHON_PACKAGE_NAME-Platzhalter. "
                        "Box moeglicherweise schon instanziiert? Dann --instantiated verwenden.",
                    )
                )
    return findings


def check_strandjunction_residues(mode: str) -> list[Finding]:
    """Prüft ob StrandJunction-Reste in der generischen Box stehen."""
    findings: list[Finding] = []
    forbidden_residues = [
        "strandjunction",
        "libstrandjunction",
        "failure.source",
        "condition.source",
        "FactStore",
        "OperationStrand",
        "CallContext",
        "graph::",
        "namespace strand",
    ]
    severity = "ERROR" if mode == "instantiated" else "WARN"
    all_files = REQUIRED_FILES + OPTIONAL_FILES
    for path in all_files:
        if not path.exists():
            continue
        text = read_text(path)
        for residue in forbidden_residues:
            if residue in text:
                findings.append(
                    Finding(
                        severity,
                        path,
                        f"StrandJunction-Rest gefunden: {residue!r}. "
                        f"Diese Box ist generisch — projektspezifische Begriffe entfernen.",
                    )
                )
    return findings


def check_layer_config_sync() -> list[Finding]:
    findings: list[Finding] = []
    checker_path = Path("tools/check_import_layers.py")
    if not checker_path.exists():
        return findings
    standard_layers = [
        "domain",
        "system",
        "infrastructure",
        "adapters",
        "cli",
        "shared",
        "tools",
        "tests",
    ]
    checker_text = read_text(checker_path)
    for layer in standard_layers:
        if f'"{layer}"' not in checker_text and f"'{layer}'" not in checker_text:
            findings.append(
                Finding(
                    "WARN",
                    checker_path,
                    f"Raum '{layer}' nicht als String-Literal in LAYER_BY_PACKAGE_PART gefunden.",
                )
            )
    return findings


def _section_lines(lines: list[str], section_heading: str) -> list[str]:
    """Return lines inside a top-level Markdown section.

    The start line is included; the next `## ` heading ends the section.
    """
    try:
        start = next(
            i for i, line in enumerate(lines) if line.strip() == section_heading
        )
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
            line
            for line in begriffe_lines
            if line.startswith("### ") and "<" not in line
        ]

        if not real_entries:
            severity = "INFO" if mode == "template" else "WARN"
            if glossar.name == "glossar-meta.md":
                findings.append(
                    Finding(
                        severity,
                        glossar,
                        "Keine Meta-Glossar-Einträge im Abschnitt '## 3. Begriffe' gefunden. "
                        "glossar-meta.md muss die Agenten-Metabegriffe enthalten.",
                    )
                )
            else:
                findings.append(
                    Finding(
                        severity,
                        glossar,
                        "Keine Glossar-Einträge im Abschnitt '## 3. Begriffe' gefunden. "
                        "Erster projektspezifischer Eintrag entsteht durch Sprechakt SP1 (Domain) "
                        "oder SP2 (System). Eintragsformat: '### <Begriffsname>'.",
                    )
                )
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
            findings.append(
                Finding(
                    "ERROR",
                    agents_path,
                    "AGENTS.md verweist nicht auf migration-bridges.md.",
                )
            )

    bridges_text = read_text(bridges_path)
    if "BR-001" not in bridges_text and "BR-" not in bridges_text:
        severity = "INFO" if mode == "template" else "WARN"
        findings.append(
            Finding(severity, bridges_path, "Keine Bridge-Einträge (BR-NNN) gefunden.")
        )

    # Im instanziierten Projekt: Beispiel-Eintrag sollte ersetzt sein
    if mode == "instantiated" and "legacy_customer_id" in bridges_text:
        findings.append(
            Finding(
                "ERROR",
                bridges_path,
                "Generisches Beispiel 'legacy_customer_id' steht noch drin — "
                "durch projektspezifische Bridges ersetzen oder entfernen.",
            )
        )
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
            findings.append(
                Finding(
                    "WARN", agents_path, "AGENTS.md erwähnt keine Erfahrungsberichte."
                )
            )
    return findings


def check_markdown_fences() -> list[Finding]:
    """Findet unbalancierte Markdown-Code-Fences in operativen Dokumenten."""
    findings: list[Finding] = []
    for path in REQUIRED_FILES + OPTIONAL_FILES:
        if not path.exists() or path.suffix != ".md":
            continue
        count = read_text(path).count("```")
        if count % 2 != 0:
            findings.append(
                Finding(
                    "ERROR",
                    path,
                    f"Unbalancierte Markdown-Code-Fences: {count} Vorkommen von ``` .",
                )
            )
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
    soft_context = re.compile(
        r"SOFT|Test rot|Lint rot|Typecheck rot|Build-/Installationsfehler"
    )

    for path in REQUIRED_FILES + OPTIONAL_FILES + list(Path("tools").glob("*.py")):
        if not path.exists():
            continue
        text = read_text(path)
        is_markdown = path.suffix == ".md"
        for line_no, line in enumerate(text.splitlines(), start=1):
            if any(p.search(line) for p in sprechakt_patterns):
                findings.append(
                    Finding(
                        "ERROR",
                        path,
                        f"Veraltete Sprechakt-ID in Zeile {line_no}: Sprechakte heißen SP1..SP7.",
                    )
                )
            # SOFT-Heuristik nur in Markdown: Tool-Quelltext enthält die Muster
            # naturgemäß als Regex-Literale und Meldungstexte.
            if (
                is_markdown
                and soft_pattern.search(line)
                and soft_context.search(line)
                and "SA" not in line
                and "SP" not in line
            ):
                findings.append(
                    Finding(
                        "ERROR",
                        path,
                        f"Veraltete SOFT-Abbruch-ID in Zeile {line_no}: SOFT-Abbrüche heißen SA1..SA6.",
                    )
                )
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
                findings.append(
                    Finding(
                        "ERROR", path, f"Erfahrungsbericht-Trigger fehlt: {trigger}"
                    )
                )
    tool = Path("tools/resolve_test_obligations.py")
    if tool.exists():
        text = read_text(tool)
        for trigger in required:
            if trigger not in text:
                findings.append(
                    Finding(
                        "ERROR",
                        tool,
                        f"Erfahrungsbericht-Trigger fehlt im Selfcheck-Output: {trigger}",
                    )
                )
    return findings


def check_reference_integrity(mode: str) -> list[Finding]:
    """Prueft einfache, aber operative Referenzdrift."""
    findings: list[Finding] = []
    historical_files = {Path("CHANGELOG.md")}
    allowed_compact_context = "frueheres `AGENTS-COMPACT.md`"

    scan_files = (
        required_files_for(mode)
        + OPTIONAL_FILES
        + CURRENT_DOCUMENTATION_FILES
        + list(Path("tools").glob("*.py"))
        + [
            path
            for path in Path("tools").glob("*/*.py")
            if "tools/instantiate/" not in path.as_posix()
        ]
    )
    for path in scan_files:
        if not path.exists():
            continue
        text = read_text(path)
        if (
            path not in historical_files
            and "AGENTS-COMPACT.md" in text
            and allowed_compact_context not in text
        ):
            findings.append(
                Finding(
                    "ERROR",
                    path,
                    "Aktiver Verweis auf entfernte Datei AGENTS-COMPACT.md.",
                )
            )

        unstable_agents_ref = (
            r"(?:`AGENTS\.md`|AGENTS\.md|\[[^\]]*AGENTS\.md[^\]]*\]\([^)]+\))"
            r"\s*(?:§|Abschnitt)\s*\d+"
        )
        if re.search(unstable_agents_ref, text):
            findings.append(
                Finding(
                    "ERROR",
                    path,
                    "Instabile numerische Referenz auf AGENTS.md gefunden. "
                    "Stattdessen zuständiges Dokument oder Abschnittstitel nennen.",
                )
            )

        old_pf_pattern = (
            r"(?<![A-Z])\bP[1-9]\b"
            r"|(?<![A-Z])\bP" + "10" + r"\b"
            r"|P" + "1[–-]P" + "9"
            r"|P" + "1[–-]P" + "10"
        )
        if path not in historical_files and re.search(old_pf_pattern, text):
            findings.append(
                Finding(
                    "ERROR",
                    path,
                    "Positionsabhaengige Preflight-Referenz gefunden. "
                    "Kanonisch sind semantische PF-* IDs.",
                )
            )

    return findings


def check_pf_id_integrity(mode: str) -> list[Finding]:
    """Prueft stabile Preflight-IDs und aktive Referenzen darauf."""
    findings: list[Finding] = []
    preflight = Path("preflight-checkliste.md")
    if not preflight.exists():
        return findings

    preflight_text = read_text(preflight)
    defined = re.findall(
        r"^##\s+\d+\.\s+(PF-[A-Z]+(?:-[A-Z]+)*)\s+—\s+(.+)$",
        preflight_text,
        flags=re.MULTILINE,
    )
    ids = [item[0] for item in defined]
    id_set = set(ids)

    if not ids:
        findings.append(
            Finding("ERROR", preflight, "Keine kanonischen PF-* Definitionen gefunden.")
        )
        return findings

    for pf_id in sorted(id_set):
        if ids.count(pf_id) > 1:
            findings.append(
                Finding("ERROR", preflight, f"PF-* Eintrag mehrfach definiert: {pf_id}")
            )

    for pf_id, title in defined:
        if not title.strip():
            findings.append(
                Finding("ERROR", preflight, f"PF-* Eintrag ohne Titel: {pf_id}")
            )

    fast_path_match = re.search(r"Fast-Path:\*\*\s*([^\n]+)", preflight_text)
    if fast_path_match:
        fast_path_ids = set(
            re.findall(r"PF-[A-Z]+(?:-[A-Z]+)*", fast_path_match.group(1))
        )
        for pf_id in sorted(fast_path_ids - id_set):
            findings.append(
                Finding(
                    "ERROR",
                    preflight,
                    f"Fast-Path referenziert unbekannten PF-* Eintrag: {pf_id}",
                )
            )

    shortform_match = re.search(
        r"## 2\. Kurzform\s+```text\n(.*?)\n```", preflight_text, flags=re.DOTALL
    )
    if shortform_match:
        shortform_ids = set(
            re.findall(
                r"^((?:PF-[A-Z]+(?:-[A-Z]+)*))\s+",
                shortform_match.group(1),
                flags=re.MULTILINE,
            )
        )
        for pf_id in sorted(id_set - shortform_ids):
            findings.append(
                Finding("ERROR", preflight, f"PF-* Eintrag fehlt in Kurzform: {pf_id}")
            )
        for pf_id in sorted(shortform_ids - id_set):
            findings.append(
                Finding(
                    "ERROR",
                    preflight,
                    f"Kurzform enthaelt unbekannten PF-* Eintrag: {pf_id}",
                )
            )
    else:
        findings.append(
            Finding(
                "ERROR", preflight, "Kurzform-Block fuer PF-* Eintraege nicht gefunden."
            )
        )

    historical_files = {Path("CHANGELOG.md")}
    scan_files = (
        required_files_for(mode)
        + OPTIONAL_FILES
        + CURRENT_DOCUMENTATION_FILES
        + list(Path("tools").glob("*.py"))
        + [
            path
            for path in Path("tools").glob("*/*.py")
            if "tools/instantiate/" not in path.as_posix()
        ]
    )
    for path in scan_files:
        if not path.exists() or path in historical_files:
            continue
        text = read_text(path)
        for pf_id in sorted(set(re.findall(r"PF-[A-Z]+(?:-[A-Z]+)*", text))):
            if pf_id == "PF-ID":
                continue
            if pf_id not in id_set:
                findings.append(
                    Finding(
                        "ERROR", path, f"Unbekannter PF-* Eintrag referenziert: {pf_id}"
                    )
                )

    return findings


def check_plan_checkpoint_enums() -> list[Finding]:
    """Validiert Enum-Felder in Plan- und Checkpoint-Instanzen. (#29)"""
    findings: list[Finding] = []

    VALID_CONTRACT_STATUS = {
        "proposed",
        "active",
        "invalidated",
        "completed",
        "aborted",
    }
    VALID_INTERAKTIONSPROFIL = {"interaktiv", "autonom"}
    VALID_RECOVERY_PROFIL = {"normal", "overnight"}
    VALID_ARBEITSPROFIL = {"feature", "brownfield-migration", "governance-migration"}
    VALID_MANDATSTATUS = {"nicht erteilt", "aktiv", "widerrufen", "erloschen"}
    VALID_RUN_STATUS = {
        "PREPARED",
        "RUNNING",
        "PAUSED",
        "BLOCKED",
        "ABORTED",
        "COMPLETED",
    }
    VALID_CHECKPOINT_STATUS = {"draft", "sealed"}
    VALID_WORKTREE_STATE = {"clean", "dirty", "detached"}
    VALID_RECOVERY_STATUS = {"unsecured", "secured", "restored"}

    def single_val(text: str, field: str) -> str | None:
        """Gibt den Wert zurück, falls er kein | enthält (noch nicht ausgefüllte Felder überspringen)."""
        m = re.search(rf"^{re.escape(field)}:\s*(.+)$", text, flags=re.MULTILINE)
        if not m:
            return None
        val = m.group(1).strip()
        if "|" in val or val == "—":
            return None
        return val

    for path in Path("docs/plans").glob("*.md"):
        if path.name == "template.md":
            continue
        text = read_text(path)
        if "Plan-Schema-Version:" not in text:
            continue
        checks = [
            ("Contract-Status", VALID_CONTRACT_STATUS),
            ("Interaktionsprofil", VALID_INTERAKTIONSPROFIL),
            ("Recovery-Profil", VALID_RECOVERY_PROFIL),
            ("Arbeitsprofil", VALID_ARBEITSPROFIL),
        ]
        for field, valid in checks:
            val = single_val(text, field)
            if val is not None and val not in valid:
                findings.append(
                    Finding(
                        "ERROR",
                        path,
                        f"Ungueltiger {field}-Wert: {val!r}. Erlaubt: {sorted(valid)}",
                    )
                )
        # Mandatstatus: "nicht erteilt" enthält Leerzeichen
        m = re.search(r"^Mandatstatus:\s*(.+)$", text, flags=re.MULTILINE)
        if m:
            val = m.group(1).strip()
            if "|" not in val and val != "—" and val not in VALID_MANDATSTATUS:
                findings.append(
                    Finding(
                        "ERROR",
                        path,
                        f"Ungueltiger Mandatstatus: {val!r}. Erlaubt: {sorted(VALID_MANDATSTATUS)}",
                    )
                )

    checkpoint_filename_re = re.compile(r"^checkpoint-\d{4}\.md$")
    run_root = Path("docs/runs")
    if run_root.exists():
        for path in run_root.rglob("*.md"):
            if not checkpoint_filename_re.match(path.name):
                continue
            text = read_text(path)
            cp_checks = [
                ("Run-Status", VALID_RUN_STATUS),
                ("Checkpoint-Status", VALID_CHECKPOINT_STATUS),
                ("Worktree-State", VALID_WORKTREE_STATE),
            ]
            for field, valid in cp_checks:
                val = single_val(text, field)
                if val is not None and val not in valid:
                    findings.append(
                        Finding(
                            "ERROR",
                            path,
                            f"Ungueltiger {field}-Wert: {val!r}. Erlaubt: {sorted(valid)}",
                        )
                    )
            rs = single_val(text, "Recovery status")
            if rs is not None and rs not in VALID_RECOVERY_STATUS:
                findings.append(
                    Finding(
                        "ERROR",
                        path,
                        f"Ungueltiger Recovery-Status: {rs!r}. Erlaubt: {sorted(VALID_RECOVERY_STATUS)}",
                    )
                )

    return findings


def check_dash_in_autonomous_plans() -> list[Finding]:
    """— ist in autonomen/overnight-Laeufen fuer Pflichtfelder verboten. (#9)"""
    findings: list[Finding] = []
    dash_forbidden_fields = ["Contract-ID", "Run-ID", "Base-Snapshot"]
    for path in Path("docs/plans").glob("*.md"):
        if path.name == "template.md":
            continue
        text = read_text(path)
        if "Plan-Schema-Version:" not in text:
            continue
        interaktionsprofil = ""
        recovery_profil = ""
        m = re.search(r"^Interaktionsprofil:\s*(\S+)", text, flags=re.MULTILINE)
        if m:
            interaktionsprofil = m.group(1).strip()
        m = re.search(r"^Recovery-Profil:\s*(\S+)", text, flags=re.MULTILINE)
        if m:
            recovery_profil = m.group(1).strip()
        if interaktionsprofil not in {"autonom"} and recovery_profil not in {
            "overnight"
        }:
            continue
        for field in dash_forbidden_fields:
            m = re.search(rf"^{re.escape(field)}:\s*—\s*$", text, flags=re.MULTILINE)
            if m:
                findings.append(
                    Finding(
                        "ERROR",
                        path,
                        f"{field} darf fuer autonome/overnight-Laeufe nicht '—' sein.",
                    )
                )
    return findings


def check_plan_checkpoint_not_template_copy() -> list[Finding]:
    """Erkennt Planinstanzen, die noch Vorlagenreste enthalten. (#31)"""
    findings: list[Finding] = []
    template_indicators = [
        "PLAN-YYYY-MM-DD-",
        "CONTRACT-YYYY-MM-DD-",
        "RUN-YYYY-MM-DD-",
        "SCOPE-YYYY-MM-DD-",
        "MD-YYYY-MM-DD-",
    ]
    for path in Path("docs/plans").glob("*.md"):
        if path.name == "template.md":
            continue
        text = read_text(path)
        if "Plan-Schema-Version:" not in text:
            continue
        for indicator in template_indicators:
            if indicator in text:
                findings.append(
                    Finding(
                        "ERROR",
                        path,
                        f"Planinstanz enthaelt Vorlagenreste: {indicator!r} ist nicht ausgefuellt.",
                    )
                )
                break

    checkpoint_filename_re = re.compile(r"^checkpoint-\d{4}\.md$")
    run_root = Path("docs/runs")
    if run_root.exists():
        for path in run_root.rglob("*.md"):
            if not checkpoint_filename_re.match(path.name):
                continue
            text = read_text(path)
            for indicator in template_indicators:
                if indicator in text:
                    findings.append(
                        Finding(
                            "ERROR",
                            path,
                            f"Checkpoint enthaelt Vorlagenreste: {indicator!r}.",
                        )
                    )
                    break
    return findings


def check_plan_instance_level() -> list[Finding]:
    """Plan-Instanzen muessen Ebene: PLAN/RUN haben, nicht REPOSITORY. (#32)"""
    findings: list[Finding] = []
    for path in Path("docs/plans").glob("*.md"):
        if path.name == "template.md":
            continue
        text = read_text(path)
        if "Plan-Schema-Version:" not in text:
            continue
        head = "\n".join(text.splitlines()[:12])
        m = re.search(r"^>\s*Ebene:\s*(.+)$", head, flags=re.MULTILINE)
        if m:
            level = m.group(1).strip()
            if level != "PLAN/RUN":
                findings.append(
                    Finding(
                        "ERROR",
                        path,
                        f"Planinstanz hat falsche Ebene: {level!r}. Erwartet: PLAN/RUN.",
                    )
                )
        elif "> Ebene:" not in head:
            findings.append(
                Finding(
                    "WARN",
                    path,
                    "Planinstanz hat keinen Ebenenkopf (Ebene: PLAN/RUN erwartet).",
                )
            )
    return findings


def check_plan_checkpoint_crossrefs() -> list[Finding]:
    """Contract-ID und Plan-ID muessen in Plan und zugehoerigen Checkpoints uebereinstimmen. (#30)"""
    findings: list[Finding] = []
    checkpoint_filename_re = re.compile(r"^checkpoint-\d{4}\.md$")
    run_root = Path("docs/runs")
    if not run_root.exists():
        return findings

    for run_dir in run_root.iterdir():
        if not run_dir.is_dir():
            continue
        checkpoints = [
            p for p in run_dir.glob("*.md") if checkpoint_filename_re.match(p.name)
        ]
        if not checkpoints:
            continue
        cp_contracts: set[str] = set()
        cp_plans: set[str] = set()
        for cp_path in checkpoints:
            text = read_text(cp_path)
            m = re.search(r"^Contract-ID:\s*(\S+)", text, flags=re.MULTILINE)
            if m and m.group(1) != "—":
                cp_contracts.add(m.group(1).strip())
            m = re.search(r"^Plan-ID:\s*(\S+)", text, flags=re.MULTILINE)
            if m and m.group(1) != "—":
                cp_plans.add(m.group(1).strip())
        if len(cp_contracts) > 1:
            findings.append(
                Finding(
                    "ERROR",
                    run_dir,
                    f"Checkpoints im Run-Verzeichnis haben unterschiedliche Contract-IDs: {cp_contracts}",
                )
            )
        if len(cp_plans) > 1:
            findings.append(
                Finding(
                    "ERROR",
                    run_dir,
                    f"Checkpoints im Run-Verzeichnis haben unterschiedliche Plan-IDs: {cp_plans}",
                )
            )

        contract_id = next(iter(cp_contracts), None)
        plan_id = next(iter(cp_plans), None)
        if plan_id:
            for plan_path in Path("docs/plans").glob("*.md"):
                if plan_path.name == "template.md":
                    continue
                text = read_text(plan_path)
                m = re.search(r"^Plan-ID:\s*(\S+)", text, flags=re.MULTILINE)
                if m and m.group(1).strip() == plan_id:
                    if contract_id:
                        m2 = re.search(
                            r"^Contract-ID:\s*(\S+)", text, flags=re.MULTILINE
                        )
                        plan_contract = m2.group(1).strip() if m2 else None
                        if (
                            plan_contract
                            and plan_contract != "—"
                            and plan_contract != contract_id
                        ):
                            findings.append(
                                Finding(
                                    "ERROR",
                                    plan_path,
                                    f"Plan.Contract-ID ({plan_contract!r}) stimmt nicht mit "
                                    f"Checkpoint.Contract-ID ({contract_id!r}) ueberein.",
                                )
                            )
                    break
    return findings


def check_template_mode_clean(mode: str) -> list[Finding]:
    """Im Template-Modus duerfen keine Instanziierungsmarker existieren. (#35)"""
    findings: list[Finding] = []
    if mode != "template":
        return findings
    for marker in [Path(".agent-box/instantiation.md"), Path(".agent-box/adoption.md")]:
        if marker.exists():
            findings.append(
                Finding(
                    "WARN",
                    marker,
                    "Instanziierungsmarker im Template-Modus gefunden. "
                    "Box ist moeglicherweise bereits instanziiert — dann --instantiated verwenden.",
                )
            )
    return findings


def check_instantiate_tool_residue(mode: str) -> list[Finding]:
    """Im instanziierten Projekt: tools/instantiate/ ist kein normales Werkzeug. (#36)"""
    findings: list[Finding] = []
    if mode != "instantiated":
        return findings
    tool = Path("tools/instantiate/instantiate_project_box.py")
    if tool.exists() and Path(".agent-box/instantiation.md").exists():
        findings.append(
            Finding(
                "INFO",
                tool,
                "tools/instantiate/ ist nach der Instanziierung kein aktives Agentenwerkzeug. "
                "Erneuter Aufruf ist verboten (tools/instantiate/README.md Regel).",
            )
        )
    return findings


def check_version_consistency(mode: str) -> list[Finding]:
    """Prüft ob BOX_VERSION in Tool, Manifest und Tutorial übereinstimmen."""
    findings: list[Finding] = []
    if mode == "instantiated":
        return findings
    tool_path = Path("tools/instantiate/instantiate_project_box.py")
    manifest_path = Path(".agent-box-template.md")
    tutorial_path = Path("tutorial.md")

    version: str | None = None
    if tool_path.exists():
        m = re.search(
            r'^BOX_VERSION\s*=\s*"(v[^"]+)"', read_text(tool_path), flags=re.MULTILINE
        )
        if m:
            version = m.group(1)

    if version is None:
        return findings

    if manifest_path.exists():
        if f"Box-Version: {version}" not in read_text(manifest_path):
            findings.append(
                Finding(
                    "ERROR",
                    manifest_path,
                    f"Box-Version stimmt nicht mit {tool_path}: erwartet {version!r}.",
                )
            )

    if tutorial_path.exists():
        if f"box-python {version}" not in read_text(tutorial_path):
            findings.append(
                Finding(
                    "WARN",
                    tutorial_path,
                    f"Tutorial-Versionszeile stimmt moeglicherweise nicht mit {version!r} ueberein.",
                )
            )

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
                findings.append(
                    Finding(
                        "WARN",
                        Path(changed),
                        f"Änderung an '{changed}' → '{coupled}' prüfen (Inhalt, nicht Präsenz).",
                    )
                )
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
    print(
        f"✗ PREFLIGHT DOCS-CONSISTENCY FEHLGESCHLAGEN — {len(errors)} Fehler (Modus: {mode})\n"
    )
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
    mode_group.add_argument(
        "--template",
        action="store_const",
        dest="mode",
        const="template",
        help="Template-Modus (Default): Platzhalter erlaubt, leere Glossare ok.",
    )
    mode_group.add_argument(
        "--instantiated",
        action="store_const",
        dest="mode",
        const="instantiated",
        help="Projekt-Modus: Platzhalter sind ERROR, Bridge-Beispiel sollte ersetzt sein.",
    )
    parser.add_argument(
        "--strict-placeholders",
        action="store_true",
        help="(Legacy) Platzhalter als ERROR statt WARN — entspricht --instantiated.",
    )
    parser.add_argument(
        "--changed-file",
        action="append",
        default=[],
        dest="changed_file",
        help="Geänderte Datei für Kopplungshinweise.",
    )
    parser.add_argument(
        "--preflight", action="store_true", help="Kompakter Agenten-Output."
    )

    args = parser.parse_args(argv)

    # Modus bestimmen
    mode = args.mode or ("instantiated" if args.strict_placeholders else "template")

    findings: list[Finding] = []
    findings.extend(check_required_files(mode))
    findings.extend(check_required_terms(mode))
    findings.extend(check_level_headers())
    findings.extend(check_plan_and_checkpoint_instances())
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
    findings.extend(check_reference_integrity(mode))
    findings.extend(check_pf_id_integrity(mode))
    findings.extend(check_version_consistency(mode))
    findings.extend(check_plan_checkpoint_enums())
    findings.extend(check_dash_in_autonomous_plans())
    findings.extend(check_plan_checkpoint_not_template_copy())
    findings.extend(check_plan_instance_level())
    findings.extend(check_plan_checkpoint_crossrefs())
    findings.extend(check_template_mode_clean(mode))
    findings.extend(check_instantiate_tool_residue(mode))
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
