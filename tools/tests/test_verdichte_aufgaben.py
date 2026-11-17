"""Tests für verdichte_aufgaben.py."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
import verdichte_aufgaben as va  # noqa: E402


def _plan(
    root: Path, name: str, status: str, contract: str = "", mandat: str = ""
) -> Path:
    body = (
        f"# Plan\n\nPlan-ID: PLAN-{name}\nPlan-Version: 1\nPlanstatus: {status}\n"
        f"Datum: 2026-01-01\n"
    )
    if contract:
        body += f"Contract-Status: {contract}\n"
    if mandat:
        body += f"Mandatstatus: {mandat}\n"
    body += "\n## Aufgabe\n\nEtwas Wichtiges tun | mit Pipe.\n\n## Weiter\n"
    path = root / "docs" / "plans" / f"2026-01-01-{name}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    return path


@pytest.mark.parametrize(
    ("planstatus", "contract", "mandat", "expected"),
    [
        ("angenommen", "completed", "erloschen", "abgeschlossen"),
        ("abgeschlossen", "", "", "abgeschlossen"),
        ("verworfen", "invalidated", "erloschen", "verworfen"),
        ("angenommen", "active", "aktiv", "offen"),
        ("entwurf", "", "nicht erteilt", "offen"),
        ("angenommen", "", "erloschen", "abgeschlossen"),
        ("irgendwas", "", "", "unklar"),
    ],
)
def test_classify(planstatus, contract, mandat, expected):
    assert va.classify(planstatus, contract, mandat) == expected


def test_collect_plans_skips_templates(tmp_path):
    _plan(tmp_path, "a", "angenommen", "completed")
    (tmp_path / "docs" / "plans" / "template.md").write_text("Plan-ID: PLAN-t\n")
    (tmp_path / "docs" / "plans" / "task-kurz-template.md").write_text(
        "Plan-ID: PLAN-k\n"
    )
    assert [p.plan_id for p in va.collect_plans(tmp_path)] == ["PLAN-a"]


def test_draft_lists_closed_plans_and_keeps_open_ones_apart(tmp_path):
    _plan(tmp_path, "fertig", "angenommen", "completed")
    _plan(tmp_path, "laeuft", "angenommen", "active", "aktiv")
    text = va.render_draft(tmp_path, va.collect_plans(tmp_path), [])
    rows, _, rest = text.partition("## Kandidaten")
    assert "PLAN-fertig" in rows
    assert "PLAN-laeuft" not in rows
    assert "PLAN-laeuft" not in rest.split("## Nicht verdichten")[0]
    assert "2026-01-01-laeuft.md" in rest.split("## Nicht verdichten")[1]


def test_pipe_in_goal_does_not_break_table(tmp_path):
    _plan(tmp_path, "fertig", "angenommen", "completed")
    text = va.render_draft(tmp_path, va.collect_plans(tmp_path), [])
    row = next(line for line in text.splitlines() if line.startswith("| PLAN-fertig"))
    assert row.count("|") == 7


def test_intermediate_checkpoints_only_when_run_completed(tmp_path):
    run = tmp_path / "docs" / "runs" / "RUN-a"
    run.mkdir(parents=True)
    (run / "checkpoint-0001.md").write_text("Run-Status: RUNNING\n")
    (run / "checkpoint-0002.md").write_text(
        "Run-Status: COMPLETED\nCheckpoint-Status: sealed\n"
    )
    runs = va.collect_runs(tmp_path)
    assert len(runs) == 1
    assert [p.name for p in runs[0].zwischen] == ["checkpoint-0001.md"]
    open_run = tmp_path / "docs" / "runs" / "RUN-b"
    open_run.mkdir()
    (open_run / "checkpoint-0001.md").write_text("Run-Status: RUNNING\n")
    (open_run / "checkpoint-0002.md").write_text("Run-Status: RUNNING\n")
    assert [r.name for r in va.collect_runs(tmp_path)] == ["RUN-a"]


def test_main_writes_only_to_tmp_and_changes_nothing(tmp_path):
    plan = _plan(tmp_path, "fertig", "angenommen", "completed")
    before = plan.read_text()
    assert va.main(["--root", str(tmp_path)]) == 0
    assert (tmp_path / "tmp" / "verdichtung-entwurf.md").exists()
    assert plan.read_text() == before


def test_main_refuses_target_under_docs(tmp_path):
    _plan(tmp_path, "fertig", "angenommen", "completed")
    assert va.main(["--root", str(tmp_path), "--out", "docs/aufgabenindex.md"]) == 2
    assert not (tmp_path / "docs" / "aufgabenindex.md").exists()


def test_legacy_plan_without_plan_id_is_recognized(tmp_path):
    path = tmp_path / "docs" / "plans" / "2026-06-12-alt.md"
    path.parent.mkdir(parents=True)
    path.write_text(
        "# Plan: Alt\n\nStatus: abgeschlossen\n\n## Aufgabe\n\nAlte Aufgabe.\n"
    )
    plans = va.collect_plans(tmp_path)
    assert len(plans) == 1
    assert plans[0].plan_id.endswith("(ohne Plan-ID)")
    assert plans[0].datum == "2026-06-12"
    assert plans[0].zustand == "abgeschlossen"


def test_legacy_open_status_stays_open(tmp_path):
    path = tmp_path / "docs" / "plans" / "2026-06-21-offen.md"
    path.parent.mkdir(parents=True)
    path.write_text("Status: offen (Eingabe fuer das Template)\n\n## Aufgabe\n\nX.\n")
    assert va.collect_plans(tmp_path)[0].zustand == "offen"


def test_references_to_candidates_are_counted_but_nothing_is_changed(tmp_path):
    plan = _plan(tmp_path, "fertig", "angenommen", "completed")
    ref = tmp_path / "bericht.md"
    ref.write_text("Siehe docs/plans/2026-01-01-fertig.md\n")
    other = tmp_path / "anderes.md"
    other.write_text("kein Verweis\n")
    plans = va.collect_plans(tmp_path)
    refs = va.find_references(tmp_path, plans)
    assert refs == {"2026-01-01-fertig": ["bericht.md"]}
    text = va.render_draft(tmp_path, plans, [])
    assert "Betroffene Dateien: 1." in text
    assert ref.read_text() == "Siehe docs/plans/2026-01-01-fertig.md\n"
    assert plan.exists()


def test_open_plans_are_not_counted_as_candidates(tmp_path):
    _plan(tmp_path, "laeuft", "angenommen", "active", "aktiv")
    (tmp_path / "bericht.md").write_text("2026-01-01-laeuft\n")
    assert va.find_references(tmp_path, va.collect_plans(tmp_path)) == {}


def test_files_with_same_name_prefix_are_not_references(tmp_path):
    _plan(tmp_path, "fertig", "angenommen", "completed")
    (tmp_path / "sprechakt.md").write_text(
        "Sprechakt 2026-01-01-fertig-entscheidungen.md\n"
    )
    assert va.find_references(tmp_path, va.collect_plans(tmp_path)) == {}


def test_legacy_inline_aufgabe_field_is_used_as_goal(tmp_path):
    path = tmp_path / "docs" / "plans" / "2026-06-12-alt.md"
    path.parent.mkdir(parents=True)
    path.write_text(
        "# Plan: Alt\n\nStatus: abgeschlossen\nAufgabe: Tkinter-GUI als zweiter Einstiegspunkt\n"
    )
    assert (
        va.collect_plans(tmp_path)[0].ziel == "Tkinter-GUI als zweiter Einstiegspunkt"
    )


def test_goal_is_first_sentence_and_limited(tmp_path):
    path = tmp_path / "docs" / "plans" / "2026-06-12-lang.md"
    path.parent.mkdir(parents=True)
    path.write_text(
        "Status: abgeschlossen\n\n## Aufgabe\n\nErster Satz. Zweiter Satz folgt hier.\n"
    )
    assert va.collect_plans(tmp_path)[0].ziel == "Erster Satz."
    assert va._first_sentence("a" * 300).endswith("…")
    assert len(va._first_sentence("a" * 300)) == 140


def test_dot_inside_command_does_not_end_the_sentence():
    text = "Den Altbestand mit `ruff format --check . --exclude tmp` bereinigen. Danach pruefen."
    assert (
        va._first_sentence(text)
        == "Den Altbestand mit `ruff format --check . --exclude tmp` bereinigen."
    )
