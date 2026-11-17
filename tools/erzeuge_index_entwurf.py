#!/usr/bin/env python3
"""erzeuge_index_entwurf.py — Entwurf fuer BEGRIFFSINDEX.md erzeugen.

Ziel:
    Erzeugt einen ENTWURF des Begriffsindex als menschenlesbare Markdown-Tabelle.
    Ein Mensch prueft den Entwurf, streicht nicht semantisch relevante Zeilen,
    ergaenzt Aliase und gibt ihn frei. Erst danach entsteht BEGRIFFSINDEX.md.

Regeln:
    - Das Tool schreibt nie nach BEGRIFFSINDEX.md (kein automatisches Schreiben
      des freigegebenen Index).
    - Standardziel ist tmp/BEGRIFFSINDEX-entwurf.md.
    - Die Spalte "Hinweis" ist eine Lesehilfe. Sie entscheidet nichts und
      wird bei der Freigabe entfernt.

Exit-Codes:
    0  Entwurf geschrieben
    2  Aufruf nicht erlaubt (z. B. Ziel ist der freigegebene Index)
"""

from __future__ import annotations

import argparse
import ast
import re
from dataclasses import dataclass, field
from pathlib import Path

APPROVED_INDEX = "BEGRIFFSINDEX.md"
DEFAULT_OUT = Path("tmp") / "BEGRIFFSINDEX-entwurf.md"
GLOSSAR_FILES = (
    ("glossar-domain.md", "domain"),
    ("glossar-system.md", "system"),
)
SPACES = ("domain", "system", "infrastructure", "adapters", "cli")
_PATH_RE = re.compile(r"(?:src|tests|tools)/[\w/.\-]+\.py")


@dataclass
class IndexRow:
    name: str
    art: str
    raum: str
    ort: str = ""
    tests: list[str] = field(default_factory=list)
    glossar: str = ""
    hinweis: str = ""


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def space_of(path: str) -> str:
    parts = Path(path).parts
    if parts and parts[0] in ("tests", "tools"):
        return parts[0]
    if len(parts) >= 3 and parts[0] == "src" and parts[2] in SPACES:
        return parts[2]
    return ""


def _base_names(node: ast.ClassDef) -> list[str]:
    names: list[str] = []
    for base in node.bases:
        if isinstance(base, ast.Name):
            names.append(base.id)
        elif isinstance(base, ast.Attribute):
            names.append(base.attr)
    return names


def _hint_for(node: ast.ClassDef | ast.FunctionDef, rel_path: str) -> str:
    space = space_of(rel_path)
    if isinstance(node, ast.ClassDef):
        bases = _base_names(node)
        if any("Exception" in b or "Error" in b for b in bases):
            return "Fehlerklasse"
        if "Protocol" in bases:
            return "Port/Protokoll"
        if node.name.endswith("UseCase"):
            return "Use Case"
        return "Typ"
    if space == "cli" and node.name == "main":
        return "Einstiegspunkt"
    if space == "cli":
        return "Oberflaeche, Hilfsfunktion?"
    return "Funktion, Relevanz pruefen"


def collect_symbols(root: Path) -> list[IndexRow]:
    rows: list[IndexRow] = []
    src_root = root / "src"
    if not src_root.exists():
        return rows
    for py_file in sorted(src_root.rglob("*.py")):
        if py_file.name == "__init__.py":
            continue
        rel = py_file.relative_to(root).as_posix()
        tree = ast.parse(_read(py_file))
        for node in tree.body:
            if not isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                continue
            if node.name.startswith("_"):
                continue
            rows.append(
                IndexRow(
                    name=node.name,
                    art="Symbol",
                    raum=space_of(rel),
                    ort=f"{rel}::{node.name}",
                    hinweis=_hint_for(node, rel),
                )
            )
    return rows


def collect_glossary_entries(root: Path) -> list[tuple[str, str, str, list[str]]]:
    """Liefert (name, glossar-datei, glossar-raum, im Eintrag genannte Pfade)."""
    entries: list[tuple[str, str, str, list[str]]] = []
    for glossar_file, glossar_space in GLOSSAR_FILES:
        path = root / glossar_file
        if not path.exists():
            continue
        text = _read(path)
        marker = "## 3. Begriffe"
        if marker not in text:
            continue
        section = text.split(marker, 1)[1]
        section = re.split(r"^## ", section, maxsplit=1, flags=re.MULTILINE)[0]
        for block in re.split(r"^### ", section, flags=re.MULTILINE)[1:]:
            name = block.splitlines()[0].strip()
            if not name or "<" in name:
                continue
            entries.append((name, glossar_file, glossar_space, _PATH_RE.findall(block)))
    return entries


def find_tests(root: Path, name: str, test_texts: dict[str, str]) -> list[str]:
    pattern = re.compile(rf"\b{re.escape(name)}\b")
    found = [rel for rel, text in test_texts.items() if pattern.search(text)]
    return sorted(found)[:3]


def build_rows(root: Path) -> list[IndexRow]:
    rows = collect_symbols(root)
    by_name = {row.name: row for row in rows}

    for name, glossar_file, glossar_space, paths in collect_glossary_entries(root):
        link = f"{glossar_file}#{name}"
        if name in by_name:
            by_name[name].glossar = link
            by_name[name].hinweis = "im Glossar; " + by_name[name].hinweis
            continue
        src_paths = [p for p in paths if p.startswith("src/")]
        ort = src_paths[0] if src_paths else ""
        rows.append(
            IndexRow(
                name=name,
                art="Konzept",
                raum=glossar_space,
                ort=ort,
                glossar=link,
                hinweis="im Glossar; Konzept ohne eigenes Symbol",
            )
        )

    test_texts: dict[str, str] = {}
    tests_root = root / "tests"
    if tests_root.exists():
        for test_file in sorted(tests_root.rglob("test_*.py")):
            test_texts[test_file.relative_to(root).as_posix()] = _read(test_file)
    for row in rows:
        row.tests = find_tests(root, row.name, test_texts)
    return rows


def render_draft(rows: list[IndexRow]) -> str:
    lines = [
        "# Begriffsindex (ENTWURF)",
        "",
        "> Entwurf, erzeugt von tools/erzeuge_index_entwurf.py. Nicht freigegeben.",
        ">",
        "> Mensch prueft: Zeilen ohne semantische Relevanz streichen, Aliase und",
        "> Raum ergaenzen, Spalte 'Hinweis' entfernen. Danach als BEGRIFFSINDEX.md",
        "> ablegen. Das Tool schreibt den freigegebenen Index nie selbst.",
        "",
        "| Name | Art | Raum | Ort | Test | Glossar | Status | Aliase | Hinweis |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        ort = f"`{row.ort}`" if row.ort else "—"
        tests = ", ".join(f"`{t}`" for t in row.tests) or "—"
        glossar = f"`{row.glossar}`" if row.glossar else "—"
        lines.append(
            f"| {row.name} | {row.art} | {row.raum or '—'} | {ort} | {tests} "
            f"| {glossar} | canonical |  | {row.hinweis} |"
        )
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Erzeugt einen Entwurf fuer BEGRIFFSINDEX.md (nur Entwurf)."
    )
    parser.add_argument("--root", default=".", help="Projektwurzel (Default: .)")
    parser.add_argument(
        "--out", default=str(DEFAULT_OUT), help="Zieldatei fuer den Entwurf"
    )
    args = parser.parse_args(argv)

    root = Path(args.root)
    out = Path(args.out)
    if out.name == APPROVED_INDEX:
        print(
            f"ABBRUCH: {APPROVED_INDEX} ist der freigegebene Index. "
            "Das Tool schreibt nur Entwuerfe."
        )
        return 2

    rows = build_rows(root)
    target = out if out.is_absolute() else root / out
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_draft(rows), encoding="utf-8")
    print(f"Entwurf geschrieben: {target} ({len(rows)} Zeilen)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
