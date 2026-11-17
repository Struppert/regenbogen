#!/usr/bin/env python3
"""verdichte_aufgaben.py — Entwurf fuer die Verdichtung am Merge-Gate.

Ziel:
    Liest Plaene unter docs/plans/ und Run-Verzeichnisse unter docs/runs/ und erzeugt einen
    ENTWURF: Kandidatenliste und Zeilen fuer docs/aufgabenindex.md. Ein Mensch ergaenzt Ergebnis,
    Abschlussdokument und Rueckfluss-Status und entscheidet.

Regeln (aufgaben-lebenszyklus-protokoll.md):
    - Das Tool aendert, verschiebt und entfernt nichts im Projekt.
    - Es schreibt nur nach tmp/ (Standard: tmp/verdichtung-entwurf.md), nie nach docs/.
    - Ob ein Abschlussdokument genuegt, bewertet das Tool nicht.

Exit-Codes:
    0  Entwurf geschrieben
    2  Aufruf nicht erlaubt (Ziel liegt unter docs/)
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_OUT = Path("tmp") / "verdichtung-entwurf.md"
PLAN_TEMPLATE_NAMES = {"template.md", "task-kurz-template.md"}
_CHECKPOINT_RE = re.compile(r"^checkpoint-\d{4}\.md$")
ZUSTAND_VERDICHTBAR = ("abgeschlossen", "verworfen")


@dataclass
class PlanInfo:
    path: Path
    plan_id: str = ""
    datum: str = ""
    ziel: str = ""
    zustand: str = "unklar"
    plan_form: str = "Voll"
    size: int = 0


@dataclass
class RunInfo:
    name: str
    zwischen: list[Path] = field(default_factory=list)
    last: Path | None = None


def _field(text: str, name: str) -> str:
    match = re.search(rf"^{re.escape(name)}:\s*(.+)$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def _section_first_line(text: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\s*\n+(.*?)(?:\n\s*\n|\Z)", text, flags=re.S | re.M
    )
    if not match:
        return ""
    block = " ".join(
        line.strip() for line in match.group(1).splitlines() if line.strip()
    )
    return block[:140]


def _first_sentence(text: str, limit: int = 140) -> str:
    """Erster Satz, hoechstens `limit` Zeichen. Reine Lesehilfe fuer die Indexzeile."""
    text = " ".join(text.split())
    # Satzende: Satzzeichen direkt nach einem Wort, danach ein Grossbuchstabe oder Ende.
    match = re.match(r"(.+?\S[.!?])(?=\s+[A-ZÄÖÜ`]|\s*$)", text)
    sentence = match.group(1) if match else text
    return sentence if len(sentence) <= limit else sentence[: limit - 1].rstrip() + "…"


def classify(planstatus: str, contract: str, mandat: str) -> str:
    """abgeschlossen | verworfen | offen | unklar. Reine Lesehilfe, keine Entscheidung."""
    if planstatus == "offen":
        return "offen"
    if planstatus == "verworfen" or contract == "invalidated":
        return "verworfen"
    if contract == "completed" or planstatus == "abgeschlossen":
        return "abgeschlossen"
    if contract in ("active", "proposed") or mandat == "aktiv":
        return "offen"
    if planstatus in ("entwurf", "entscheidungsbereit"):
        return "offen"
    if mandat in ("erloschen", "abgeschlossen") and planstatus == "angenommen":
        return "abgeschlossen"
    return "unklar"


def parse_plan(path: Path) -> PlanInfo:
    text = path.read_text(encoding="utf-8")
    # Aeltere Plaene fuehren "Status:" statt "Planstatus:" und haben keine Plan-ID.
    planstatus = (_field(text, "Planstatus") or _field(text, "Status")).split(" ")[0]
    plan_id = _field(text, "Plan-ID") or f"{path.stem} (ohne Plan-ID)"
    datum = _field(text, "Datum") or (
        path.name[:10] if re.match(r"\d{4}-\d{2}-\d{2}", path.name) else ""
    )
    # Aeltere Plaene fuehren die Aufgabe als Feld "Aufgabe:" statt als Abschnitt.
    ziel = _first_sentence(
        _section_first_line(text, "Aufgabe")
        or _section_first_line(text, "Ziel")
        or _field(text, "Aufgabe")
    )
    return PlanInfo(
        path=path,
        plan_id=plan_id,
        datum=datum,
        ziel=ziel,
        zustand=classify(
            planstatus,
            _field(text, "Contract-Status"),
            _field(text, "Mandatstatus"),
        ),
        plan_form="Kurz"
        if re.search(r"^Plan-Form:\s*Kurz\b", text, flags=re.M)
        else "Voll",
        size=path.stat().st_size,
    )


def collect_plans(root: Path) -> list[PlanInfo]:
    plans_dir = root / "docs" / "plans"
    if not plans_dir.exists():
        return []
    plans = []
    for path in sorted(plans_dir.glob("*.md")):
        if path.name in PLAN_TEMPLATE_NAMES:
            continue
        plans.append(parse_plan(path))
    return plans


def collect_runs(root: Path) -> list[RunInfo]:
    runs_dir = root / "docs" / "runs"
    if not runs_dir.exists():
        return []
    runs = []
    for run_dir in sorted(p for p in runs_dir.iterdir() if p.is_dir()):
        checkpoints = sorted(
            p for p in run_dir.glob("*.md") if _CHECKPOINT_RE.match(p.name)
        )
        if len(checkpoints) < 2:
            continue
        last_text = checkpoints[-1].read_text(encoding="utf-8")
        if (
            "Run-Status: COMPLETED" in last_text
            and "Checkpoint-Status: sealed" in last_text
        ):
            runs.append(RunInfo(run_dir.name, checkpoints[:-1], checkpoints[-1]))
    return runs


def find_references(root: Path, plans: list[PlanInfo]) -> dict[str, list[str]]:
    """Dateien ausserhalb von docs/plans/ und tmp/, die einen Plan per Dateiname nennen."""
    candidates = [p for p in plans if p.zustand in ZUSTAND_VERDICHTBAR]
    found: dict[str, list[str]] = {}
    skip = (root / "docs" / "plans", root / "tmp", root / ".git", root / ".idea")
    for path in sorted(root.rglob("*.md")):
        if any(path == s or s in path.parents for s in skip):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        rel = path.relative_to(root).as_posix()
        for plan in candidates:
            # Nur der Plan selbst, nicht Dateien mit demselben Namensanfang (z. B. Sprechakte).
            if f"docs/plans/{plan.path.stem}" in text or f"{plan.path.stem}.md" in text:
                found.setdefault(plan.path.stem, []).append(rel)
    return found


def _cell(text: str) -> str:
    return text.replace("|", "/").strip() or "—"


def render_draft(root: Path, plans: list[PlanInfo], runs: list[RunInfo]) -> str:
    verdichtbar = [p for p in plans if p.zustand in ZUSTAND_VERDICHTBAR]
    offen = [p for p in plans if p.zustand not in ZUSTAND_VERDICHTBAR]
    lines = [
        "# Verdichtung (ENTWURF)",
        "",
        "> Entwurf, erzeugt von tools/verdichte_aufgaben.py. Aendert nichts im Projekt.",
        ">",
        "> Mensch prueft: Ergebnis, Abschlussdokument und Rueckfluss-Status der Indexzeilen",
        "> ergaenzen, Zeilen nach docs/aufgabenindex.md uebernehmen. Entfernen der Dateien",
        "> (Verdichtungs-Commit) braucht ein Mandat mit Dateiliste.",
        "",
        "## Indexzeilen (Entwurf)",
        "",
        "| Plan-ID | Datum | Ziel | Ergebnis | Abschlussdokument | Rückfluss-Status |",
        "|---|---|---|---|---|---|",
    ]
    for plan in verdichtbar:
        lines.append(
            f"| {_cell(plan.plan_id)} | {_cell(plan.datum)} | {_cell(plan.ziel)} "
            f"| offen ({plan.zustand}) | offen | offen |"
        )
    lines += [
        "",
        "## Kandidaten fuer das Entfernen (nach Abschlussdokument und Mandat)",
        "",
    ]
    total = 0
    for plan in verdichtbar:
        rel = plan.path.relative_to(root).as_posix()
        lines.append(f"- `{rel}` ({plan.zustand}, {plan.plan_form}, {plan.size} Bytes)")
        total += plan.size
    for run in runs:
        for checkpoint in run.zwischen:
            rel = checkpoint.relative_to(root).as_posix()
            size = checkpoint.stat().st_size
            lines.append(
                f"- `{rel}` (Zwischen-Checkpoint von {run.name}, {size} Bytes)"
            )
            total += size
    refs = find_references(root, plans)
    files = sorted({f for fs in refs.values() for f in fs})
    lines += [
        "",
        f"Summe der Kandidaten: {total / 1024:.1f} KB.",
        "",
        "## Verweise auf Kandidaten (bleiben stehen)",
        "",
        "Diese Dateien nennen Plaene per Dateiname. Versiegelte Dokumente werden nicht geaendert;",
        "die Plan-ID im Aufgabenindex loest die Verweise auf.",
        "",
        f"Betroffene Dateien: {len(files)}.",
        "",
        "## Nicht verdichten (offen oder unklar)",
        "",
    ]
    if offen:
        for plan in offen:
            rel = plan.path.relative_to(root).as_posix()
            lines.append(f"- `{rel}` ({plan.zustand})")
    else:
        lines.append("- keine")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Erzeugt einen Entwurf fuer die Verdichtung am Merge-Gate (aendert nichts)."
    )
    parser.add_argument("--root", default=".", help="Projektwurzel (Default: .)")
    parser.add_argument(
        "--out", default=str(DEFAULT_OUT), help="Zieldatei fuer den Entwurf"
    )
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    out = Path(args.out)
    target = out if out.is_absolute() else root / out
    docs = (root / "docs").resolve()
    if target.resolve() == docs or docs in target.resolve().parents:
        print("ABBRUCH: Das Tool schreibt nur Entwuerfe, nicht unter docs/.")
        return 2

    plans = collect_plans(root)
    runs = collect_runs(root)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_draft(root, plans, runs), encoding="utf-8")
    print(
        f"Entwurf geschrieben: {target} ({len(plans)} Plaene, {len(runs)} Runs mit Zwischen-Checkpoints)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
