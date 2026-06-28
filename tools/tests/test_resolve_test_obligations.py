"""Tests für resolve_test_obligations.py."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
import resolve_test_obligations as rto  # noqa: E402


def _classify(rel: str) -> rto.FileObligations:
    return rto.classify_path(Path(rel))


def _hard_stop(rel: str) -> bool:
    return _classify(rel).hard_stop


def _reasons(rel: str) -> list[str]:
    return [ob.reason for ob in _classify(rel).obligations]


class TestAgentDocs:
    @pytest.mark.parametrize(
        "name",
        [
            "AGENTS.md",
            "AGENT-SETUP.md",
            "BROWNFIELD-MIGRATION.md",
            "glossar-domain.md",
            "glossar-system.md",
            "glossar-meta.md",
            "ausfuehrungsmandat-protokoll.md",
            "sprechakt-protokoll.md",
            "regelmatrix.md",
            "test-obligations.md",
        ],
    )
    def test_root_agent_docs_classified(self, name):
        result = _classify(name)
        assert not result.hard_stop
        reasons = _reasons(name)
        assert any("Agenten-Dokument" in r for r in reasons)

    def test_agent_docs_requires_human(self):
        result = _classify("AGENTS.md")
        assert any(ob.requires_human for ob in result.obligations)


class TestNormativeDocPaths:
    @pytest.mark.parametrize(
        "path",
        [
            "docs/plans/template.md",
            "docs/runs/checkpoint-template.md",
        ],
    )
    def test_normative_template_not_plain_docs(self, path):
        result = _classify(path)
        assert not result.hard_stop
        reasons = [ob.reason for ob in result.obligations]
        assert any("Normatives Box-Artefakt" in r for r in reasons)

    def test_normative_template_requires_human(self):
        result = _classify("docs/plans/template.md")
        assert any(ob.requires_human for ob in result.obligations)


class TestKnownRootFiles:
    def test_changelog_not_hard_stop(self):
        assert not _hard_stop("CHANGELOG.md")

    def test_readme_not_hard_stop(self):
        assert not _hard_stop("README.md")

    def test_changelog_no_agent_check(self):
        result = _classify("CHANGELOG.md")
        checks = set()
        for ob in result.obligations:
            checks |= ob.checks
        assert "agent-docs-consistency" not in checks


class TestPackagingFiles:
    @pytest.mark.parametrize(
        "name",
        [
            "pyproject.toml",
            "setup.py",
            "requirements.txt",
            "requirements-dev.txt",
        ],
    )
    def test_packaging_hard_stop(self, name):
        assert _hard_stop(name)

    def test_packaging_requires_human(self):
        result = _classify("pyproject.toml")
        assert any(ob.requires_human for ob in result.obligations)


class TestUnknownFiles:
    def test_unknown_root_file_is_hard_stop(self):
        # A root-level file that isn't in AGENT_DOCS or KNOWN_ROOT_FILES
        # should produce a hard stop.
        assert _hard_stop("some-random-file.md")

    def test_agent_doc_nested_not_classified_as_agent_doc(self):
        # AGENTS.md at depth > 1 is not a root agent doc.
        result = _classify("subdir/AGENTS.md")
        reasons = [ob.reason for ob in result.obligations]
        assert not any("Agenten-Dokument" in r for r in reasons)
