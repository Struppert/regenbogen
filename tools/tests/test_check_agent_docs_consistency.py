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
