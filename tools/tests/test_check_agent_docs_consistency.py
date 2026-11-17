"""Tests für check_agent_docs_consistency.py."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import check_agent_docs_consistency as cadc  # noqa: E402

BOX_ROOT = Path(__file__).parent.parent.parent


class TestRequiredFiles:
    def test_instantiated_mode_required_files_present(self):
        missing = [
            f
            for f in cadc.required_files_for("instantiated")
            if not (BOX_ROOT / f).exists()
        ]
        assert missing == [], (
            f"Fehlende Pflichtdateien im Instantiated-Modus: {missing}"
        )

    def test_core_required_files_present(self):
        missing = [f for f in cadc.REQUIRED_FILES_CORE if not (BOX_ROOT / f).exists()]
        assert missing == [], f"Fehlende Core-Pflichtdateien: {missing}"

    def test_agent_setup_is_template_only(self):
        assert Path("AGENT-SETUP.md") in cadc.TEMPLATE_ONLY_FILES

    def test_readme_forbidden_in_template_mode(self):
        assert Path("README.md") in cadc.forbidden_files_for("template")

    def test_readme_not_forbidden_in_instantiated_mode(self):
        assert Path("README.md") not in cadc.forbidden_files_for("instantiated")


class TestRequiredTerms:
    def test_checkpoint_template_has_three_profile_terms(self):
        terms = cadc.REQUIRED_TERMS_BY_FILE.get(
            Path("docs/runs/checkpoint-template.md"), []
        )
        assert "Interaktionsprofil" in terms
        assert "Recovery-Profil" in terms
        assert "Arbeitsprofil" in terms

    def test_checkpoint_template_no_old_ausfuehrungsprofil(self):
        terms = cadc.REQUIRED_TERMS_BY_FILE.get(
            Path("docs/runs/checkpoint-template.md"), []
        )
        assert "Ausfuehrungsprofil" not in terms

    def test_sprechakt_protokoll_requires_widerrufen(self):
        terms = cadc.REQUIRED_TERMS_BY_FILE.get(Path("sprechakt-protokoll.md"), [])
        assert "widerrufen" in terms

    def test_plan_template_has_three_profile_terms(self):
        terms = cadc.REQUIRED_TERMS_BY_FILE.get(Path("docs/plans/template.md"), [])
        assert "Interaktionsprofil" in terms
        assert "Recovery-Profil" in terms
        assert "Arbeitsprofil" in terms

    def test_correspondence_protocol_is_required_and_has_core_terms(self):
        protocol = Path("korrespondenz-protokoll.md")
        assert protocol in cadc.REQUIRED_FILES_CORE
        terms = cadc.REQUIRED_TERMS_BY_FILE.get(protocol, [])
        assert "Korrespondenzsatz" in terms
        assert "Modellreview" in terms


class TestConsistencyCheckerSelfCheck:
    def test_checker_runs_green_in_instantiated_mode(self):
        result = subprocess.run(
            [sys.executable, "tools/check_agent_docs_consistency.py", "--instantiated"],
            capture_output=True,
            text=True,
            cwd=BOX_ROOT,
        )
        assert result.returncode == 0, (
            f"Consistency-Checker fehlgeschlagen:\n{result.stdout}\n{result.stderr}"
        )

    def test_checker_output_contains_ok(self):
        result = subprocess.run(
            [sys.executable, "tools/check_agent_docs_consistency.py", "--instantiated"],
            capture_output=True,
            text=True,
            cwd=BOX_ROOT,
        )
        assert "Agent-Docs-Consistency:" in result.stdout


INDEX_HEAD = (
    "| Name | Art | Raum | Ort | Test | Glossar | Status | Aliase |\n"
    "|---|---|---|---|---|---|---|---|\n"
)


def _make_root(tmp_path: Path, index_rows: str, with_header: bool = True) -> Path:
    (tmp_path / "src" / "pkg" / "domain").mkdir(parents=True)
    (tmp_path / "src" / "pkg" / "system").mkdir(parents=True)
    (tmp_path / "tests" / "domain").mkdir(parents=True)
    (tmp_path / "src" / "pkg" / "domain" / "wetter.py").write_text(
        "class Wetterzustand:\n    pass\n\n\ndef berechne():\n    return 1\n",
        encoding="utf-8",
    )
    (tmp_path / "src" / "pkg" / "system" / "use_case.py").write_text(
        "class UseCase:\n    pass\n", encoding="utf-8"
    )
    (tmp_path / "tests" / "domain" / "test_wetter.py").write_text(
        "def test_x():\n    pass\n", encoding="utf-8"
    )
    (tmp_path / "glossar-domain.md").write_text(
        "## 3. Begriffe\n\n### Wetterzustand\n", encoding="utf-8"
    )
    head = INDEX_HEAD if with_header else ""
    (tmp_path / "BEGRIFFSINDEX.md").write_text(
        "# Begriffsindex\n\n" + head + index_rows, encoding="utf-8"
    )
    return tmp_path


def _row(
    name="Wetterzustand",
    raum="domain",
    ort="`src/pkg/domain/wetter.py::Wetterzustand`",
    test="`tests/domain/test_wetter.py`",
    glossar="`glossar-domain.md#Wetterzustand`",
    aliase="",
):
    return f"| {name} | Symbol | {raum} | {ort} | {test} | {glossar} | canonical | {aliase} |\n"


def _msgs(findings, severity):
    return [f.message for f in findings if f.severity == severity]


class TestBegriffsindex:
    def test_no_index_file_means_no_findings(self, tmp_path):
        assert cadc.check_begriffsindex(tmp_path) == []

    def test_valid_index_has_no_errors_or_warnings(self, tmp_path):
        root = _make_root(tmp_path, _row())
        findings = cadc.check_begriffsindex(root)
        assert _msgs(findings, "ERROR") == []
        assert _msgs(findings, "WARN") == []

    def test_missing_path_is_error(self, tmp_path):
        root = _make_root(tmp_path, _row(ort="`src/pkg/domain/gibt_es_nicht.py`"))
        errors = _msgs(cadc.check_begriffsindex(root), "ERROR")
        assert any("gibt_es_nicht.py" in m for m in errors)

    def test_missing_symbol_is_error(self, tmp_path):
        root = _make_root(tmp_path, _row(ort="`src/pkg/domain/wetter.py::Fehlt`"))
        errors = _msgs(cadc.check_begriffsindex(root), "ERROR")
        assert any("Fehlt" in m for m in errors)

    def test_missing_test_path_is_error(self, tmp_path):
        root = _make_root(tmp_path, _row(test="`tests/domain/test_fehlt.py`"))
        errors = _msgs(cadc.check_begriffsindex(root), "ERROR")
        assert any("test_fehlt.py" in m for m in errors)

    def test_space_mismatch_is_warning_not_error(self, tmp_path):
        root = _make_root(tmp_path, _row(raum="system"))
        findings = cadc.check_begriffsindex(root)
        assert _msgs(findings, "ERROR") == []
        assert any("Raum" in m for m in _msgs(findings, "WARN"))

    def test_duplicate_names_are_warning(self, tmp_path):
        rows = _row() + _row(name="Anderes", aliase="wetterzustand")
        root = _make_root(tmp_path, rows)
        warns = _msgs(cadc.check_begriffsindex(root), "WARN")
        assert any("mehrfach" in m.lower() for m in warns)

    def test_glossar_file_missing_is_error(self, tmp_path):
        root = _make_root(tmp_path, _row(glossar="`glossar-fehlt.md#X`"))
        errors = _msgs(cadc.check_begriffsindex(root), "ERROR")
        assert any("glossar-fehlt.md" in m for m in errors)

    def test_glossar_anchor_missing_is_warning(self, tmp_path):
        root = _make_root(tmp_path, _row(glossar="`glossar-domain.md#Unbekannt`"))
        warns = _msgs(cadc.check_begriffsindex(root), "WARN")
        assert any("Unbekannt" in m for m in warns)

    def test_unindexed_public_symbols_are_info_only(self, tmp_path):
        root = _make_root(tmp_path, _row())
        findings = cadc.check_begriffsindex(root)
        infos = _msgs(findings, "INFO")
        assert any("UseCase" in m for m in infos)
        assert _msgs(findings, "ERROR") == []

    def test_index_without_table_is_warning(self, tmp_path):
        root = _make_root(tmp_path, "Nur Text, keine Tabelle.\n", with_header=False)
        warns = _msgs(cadc.check_begriffsindex(root), "WARN")
        assert warns

    def test_column_order_does_not_matter(self, tmp_path):
        root = _make_root(tmp_path, "", with_header=False)
        (root / "BEGRIFFSINDEX.md").write_text(
            "| Ort | Raum | Name |\n|---|---|---|\n"
            "| `src/pkg/domain/wetter.py::Wetterzustand` | domain | Wetterzustand |\n",
            encoding="utf-8",
        )
        findings = cadc.check_begriffsindex(root)
        assert _msgs(findings, "ERROR") == []
        assert _msgs(findings, "WARN") == []


class TestDokumentsatz:
    def test_local_documents_are_optional_not_required(self):
        # Entscheidung D3: lokale Ergaenzungen sind optional, die Pflichtliste
        # entspricht dem Template.
        for name in ("PROJEKT.md", "REGELN-UND-TOOLS.md"):
            assert Path(name) in cadc.OPTIONAL_FILES
            assert Path(name) not in cadc.REQUIRED_FILES_CORE

    def test_korrespondenz_protokoll_is_required(self):
        assert Path("korrespondenz-protokoll.md") in cadc.REQUIRED_FILES_CORE

    def test_begriffsindex_is_optional_local_file_with_level_header(self):
        assert Path("BEGRIFFSINDEX.md") in cadc.OPTIONAL_FILES
        assert Path("BEGRIFFSINDEX.md") not in cadc.REQUIRED_FILES_CORE
        assert Path("BEGRIFFSINDEX.md") in cadc.LEVEL_HEADER_FILES

    def test_real_begriffsindex_has_no_errors(self):
        findings = cadc.check_begriffsindex(BOX_ROOT)
        assert [f.message for f in findings if f.severity == "ERROR"] == []

    def test_new_core_documents_need_level_header(self):
        assert Path("PROJEKT.md") in cadc.LEVEL_HEADER_FILES
        assert Path("REGELN-UND-TOOLS.md") in cadc.LEVEL_HEADER_FILES

    def test_new_core_documents_have_required_terms(self):
        assert cadc.REQUIRED_TERMS_BY_FILE.get(Path("PROJEKT.md"))
        assert cadc.REQUIRED_TERMS_BY_FILE.get(Path("REGELN-UND-TOOLS.md"))

    def test_agents_md_keeps_safety_core_terms(self):
        terms = cadc.REQUIRED_TERMS_BY_FILE[Path("AGENTS.md")]
        for term in ("H10", "BF1", "Schreibrechte", "bindende Router"):
            assert term in terms

    def test_regeln_und_tools_keeps_all_invariants(self):
        # Entscheidung D1: die ausfuehrlichen Invarianten I1 bis I11 stehen als
        # lokale Ergaenzung in REGELN-UND-TOOLS.md.
        text = (BOX_ROOT / "REGELN-UND-TOOLS.md").read_text(encoding="utf-8")
        for n in range(1, 12):
            assert f"### I{n}." in text, f"Invariante I{n} fehlt in REGELN-UND-TOOLS.md"

    def test_abort_codes_are_defined_in_blocker_protocol(self):
        text = (BOX_ROOT / "blocker-und-abbruch-protokoll.md").read_text(
            encoding="utf-8"
        )
        for n in range(1, 11):
            assert f"H{n} " in text, f"H{n} fehlt im Abbruchprotokoll"
        for n in range(1, 7):
            assert f"SA{n}" in text, f"SA{n} fehlt im Abbruchprotokoll"

    def test_agents_md_routes_abort_code_families(self):
        text = (BOX_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        for family in ("H1-H10", "SA1-SA6", "SP1-SP7", "BF1-BF12"):
            assert family in text, f"Code-Familie {family} fehlt im Router"


KURZ_CORE = (
    "Plan-ID: PLAN-2026-01-01-x\n"
    "Plan-Version: 1\n"
    "Plan-Form: Kurz\n"
    "Mandat-ID: MD-2026-01-01-x\n"
    "Mandatstatus: aktiv\n"
    "## Ressourcenscope\n## Wirkungsscope\n## Capability-Scope\n"
)


def _write(root: Path, rel: str, text: str) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _index(rows: str) -> str:
    return (
        "# Aufgabenindex\n\n"
        "| Plan-ID | Datum | Ziel | Ergebnis | Abschlussdokument | Rückfluss-Status |\n"
        "|---|---|---|---|---|---|\n" + rows
    )


class TestKurzformImPlanCheck:
    def test_kurz_with_core_fields_has_no_error_and_no_schema_warning(
        self, tmp_path, monkeypatch
    ):
        _write(tmp_path, "docs/plans/a.md", KURZ_CORE)
        monkeypatch.chdir(tmp_path)
        findings = cadc.check_plan_and_checkpoint_instances()
        assert [f for f in findings if f.severity in ("ERROR", "WARN")] == []

    def test_kurz_missing_core_field_is_error(self, tmp_path, monkeypatch):
        _write(
            tmp_path,
            "docs/plans/a.md",
            KURZ_CORE.replace("## Capability-Scope\n", ""),
        )
        monkeypatch.chdir(tmp_path)
        findings = cadc.check_plan_and_checkpoint_instances()
        assert any(
            f.severity == "ERROR" and "Capability-Scope" in f.message for f in findings
        )

    def test_plan_without_form_and_schema_still_warns(self, tmp_path, monkeypatch):
        _write(tmp_path, "docs/plans/a.md", "Plan-ID: PLAN-x\nPlan-Version: 1\n")
        monkeypatch.chdir(tmp_path)
        findings = cadc.check_plan_and_checkpoint_instances()
        assert any("Plan-Schema-Version fehlt" in f.message for f in findings)

    def test_kurz_template_is_not_checked_as_plan(self, tmp_path, monkeypatch):
        _write(tmp_path, "docs/plans/task-kurz-template.md", "kein Plan\n")
        monkeypatch.chdir(tmp_path)
        assert cadc.check_plan_and_checkpoint_instances() == []


class TestAufgabenLebenszyklus:
    def test_nothing_present_means_no_findings(self, tmp_path):
        assert cadc.check_aufgaben_lebenszyklus(tmp_path) == []

    def test_index_with_existing_nonempty_document_is_clean(self, tmp_path):
        _write(tmp_path, "docs/abschluss/a.md", "Ergebnis.\n")
        _write(
            tmp_path,
            "docs/aufgabenindex.md",
            _index(
                "| PLAN-a | 2026-01-01 | Ziel | ok | `docs/abschluss/a.md` | LOCAL-ONLY |\n"
            ),
        )
        assert cadc.check_aufgaben_lebenszyklus(tmp_path) == []

    def test_missing_document_is_warning(self, tmp_path):
        _write(
            tmp_path,
            "docs/aufgabenindex.md",
            _index(
                "| PLAN-a | 2026-01-01 | Ziel | ok | docs/fehlt.md | LOCAL-ONLY |\n"
            ),
        )
        findings = cadc.check_aufgaben_lebenszyklus(tmp_path)
        assert [f.severity for f in findings] == ["WARN"]
        assert "fehlt oder ist leer" in findings[0].message

    def test_empty_document_is_warning(self, tmp_path):
        _write(tmp_path, "docs/abschluss/a.md", "  \n")
        _write(
            tmp_path,
            "docs/aufgabenindex.md",
            _index(
                "| PLAN-a | 2026-01-01 | Ziel | ok | docs/abschluss/a.md | LOCAL-ONLY |\n"
            ),
        )
        assert [f.severity for f in cadc.check_aufgaben_lebenszyklus(tmp_path)] == [
            "WARN"
        ]

    def test_unnamed_document_is_warning(self, tmp_path):
        _write(
            tmp_path,
            "docs/aufgabenindex.md",
            _index("| PLAN-a | 2026-01-01 | Ziel | ok | offen | LOCAL-ONLY |\n"),
        )
        findings = cadc.check_aufgaben_lebenszyklus(tmp_path)
        assert any("kein Abschlussdokument benannt" in f.message for f in findings)

    def test_content_of_document_is_not_evaluated(self, tmp_path):
        _write(tmp_path, "docs/abschluss/a.md", "x\n")
        _write(
            tmp_path,
            "docs/aufgabenindex.md",
            _index(
                "| PLAN-a | 2026-01-01 | Ziel | ok | docs/abschluss/a.md | LOCAL-ONLY |\n"
            ),
        )
        assert cadc.check_aufgaben_lebenszyklus(tmp_path) == []

    def test_kurz_plan_without_abschlussdokument_is_warning(self, tmp_path):
        _write(tmp_path, "docs/plans/a.md", KURZ_CORE)
        findings = cadc.check_aufgaben_lebenszyklus(tmp_path)
        assert any("Abschnitt 'Abschlussdokument'" in f.message for f in findings)

    def test_kurz_plan_with_abschlussdokument_is_clean(self, tmp_path):
        _write(tmp_path, "docs/plans/a.md", KURZ_CORE + "## Abschlussdokument\nPfad\n")
        assert cadc.check_aufgaben_lebenszyklus(tmp_path) == []

    def test_completed_run_with_intermediate_checkpoints_is_info(self, tmp_path):
        run = "docs/runs/RUN-x/"
        _write(tmp_path, run + "checkpoint-0001.md", "Run-Status: RUNNING\n")
        _write(tmp_path, run + "checkpoint-0002.md", "Run-Status: RUNNING\n")
        _write(
            tmp_path,
            run + "checkpoint-0003.md",
            "Run-Status: COMPLETED\nCheckpoint-Status: sealed\n",
        )
        findings = cadc.check_aufgaben_lebenszyklus(tmp_path)
        assert [f.severity for f in findings] == ["INFO"]
        assert "2 Zwischen-Checkpoints" in findings[0].message

    def test_running_run_gives_no_hint(self, tmp_path):
        run = "docs/runs/RUN-x/"
        _write(tmp_path, run + "checkpoint-0001.md", "Run-Status: RUNNING\n")
        _write(tmp_path, run + "checkpoint-0002.md", "Run-Status: RUNNING\n")
        assert cadc.check_aufgaben_lebenszyklus(tmp_path) == []
