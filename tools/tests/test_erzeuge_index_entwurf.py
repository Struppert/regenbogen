"""Tests für erzeuge_index_entwurf.py."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
import check_agent_docs_consistency as cadc  # noqa: E402
import erzeuge_index_entwurf as eie  # noqa: E402


@pytest.fixture()
def project(tmp_path: Path) -> Path:
    (tmp_path / "src" / "pkg" / "domain").mkdir(parents=True)
    (tmp_path / "src" / "pkg" / "system").mkdir(parents=True)
    (tmp_path / "src" / "pkg" / "cli").mkdir(parents=True)
    (tmp_path / "tests" / "domain").mkdir(parents=True)
    (tmp_path / "src" / "pkg" / "domain" / "wetter.py").write_text(
        "class Wetterzustand:\n    pass\n\n\ndef _intern():\n    pass\n",
        encoding="utf-8",
    )
    (tmp_path / "src" / "pkg" / "system" / "fehler.py").write_text(
        "class NichtErreichbar(Exception):\n    pass\n\n\n"
        "class Port(Protocol):\n    pass\n\n\n"
        "class RechneUseCase:\n    pass\n",
        encoding="utf-8",
    )
    (tmp_path / "src" / "pkg" / "cli" / "main.py").write_text(
        "def main():\n    pass\n\n\ndef formatiere():\n    pass\n",
        encoding="utf-8",
    )
    (tmp_path / "tests" / "domain" / "test_wetter.py").write_text(
        "from pkg.domain.wetter import Wetterzustand\n", encoding="utf-8"
    )
    (tmp_path / "glossar-domain.md").write_text(
        "## 3. Begriffe\n\n"
        "### Wetterzustand\n\n**Projektionen:**\n- Code: src/pkg/domain/wetter.py\n\n"
        "### NurKonzept\n\n**Projektionen:**\n- Code: src/pkg/domain/wetter.py\n\n"
        "## 4. Ende\n",
        encoding="utf-8",
    )
    return tmp_path


def test_collects_public_symbols_only(project: Path):
    names = {row.name for row in eie.collect_symbols(project)}
    assert "Wetterzustand" in names
    assert "_intern" not in names


def test_space_is_derived_from_path(project: Path):
    rows = {row.name: row for row in eie.collect_symbols(project)}
    assert rows["Wetterzustand"].raum == "domain"
    assert rows["NichtErreichbar"].raum == "system"
    assert rows["main"].raum == "cli"


def test_hints_are_reading_aids(project: Path):
    rows = {row.name: row for row in eie.collect_symbols(project)}
    assert rows["NichtErreichbar"].hinweis == "Fehlerklasse"
    assert rows["Port"].hinweis == "Port/Protokoll"
    assert rows["RechneUseCase"].hinweis == "Use Case"
    assert rows["main"].hinweis == "Einstiegspunkt"


def test_glossary_links_and_concepts(project: Path):
    rows = {row.name: row for row in eie.build_rows(project)}
    assert rows["Wetterzustand"].glossar == "glossar-domain.md#Wetterzustand"
    assert rows["NurKonzept"].art == "Konzept"
    assert rows["NurKonzept"].ort == "src/pkg/domain/wetter.py"


def test_tests_are_found_by_name(project: Path):
    rows = {row.name: row for row in eie.build_rows(project)}
    assert rows["Wetterzustand"].tests == ["tests/domain/test_wetter.py"]


def test_main_writes_draft_to_tmp(project: Path):
    code = eie.main(["--root", str(project)])
    assert code == 0
    draft = project / "tmp" / "BEGRIFFSINDEX-entwurf.md"
    assert draft.exists()
    assert "ENTWURF" in draft.read_text(encoding="utf-8")


def test_main_refuses_to_write_approved_index(project: Path):
    code = eie.main(["--root", str(project), "--out", "BEGRIFFSINDEX.md"])
    assert code == 2
    assert not (project / "BEGRIFFSINDEX.md").exists()


def test_draft_is_readable_by_index_checker(project: Path):
    eie.main(["--root", str(project)])
    draft = (project / "tmp" / "BEGRIFFSINDEX-entwurf.md").read_text(encoding="utf-8")
    (project / "BEGRIFFSINDEX.md").write_text(draft, encoding="utf-8")
    findings = cadc.check_begriffsindex(project)
    assert [f.message for f in findings if f.severity == "ERROR"] == []
