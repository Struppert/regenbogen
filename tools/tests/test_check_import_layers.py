"""Tests für check_import_layers.py."""

from __future__ import annotations

import sys
import textwrap
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
import check_import_layers as cil  # noqa: E402


@pytest.fixture()
def src_root(tmp_path: Path) -> Path:
    root = tmp_path / "src"
    root.mkdir()
    return root


@pytest.fixture()
def test_root(tmp_path: Path) -> Path:
    root = tmp_path / "tests"
    root.mkdir()
    return root


def _write(path: Path, code: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(code), encoding="utf-8")
    return path


class TestRelativeImports:
    def test_relative_import_in_source_produces_finding(self, tmp_path, monkeypatch):
        # A relative import in non-test source should be flagged.
        # SOURCE_ROOTS must point to src/ so modules resolve as mypkg.domain.foo.
        src = tmp_path / "src"
        pkg = src / "mypkg"
        pkg.mkdir(parents=True)
        (pkg / "__init__.py").write_text("")
        domain = pkg / "domain"
        domain.mkdir()
        (domain / "__init__.py").write_text("")
        module = _write(
            domain / "foo.py",
            """\
            from .helpers import bar
        """,
        )

        monkeypatch.setattr(cil, "SOURCE_ROOTS", [src])
        monkeypatch.setattr(cil, "TEST_ROOTS", [tmp_path / "tests"])
        monkeypatch.setattr(cil, "TOOLS_ROOTS", [])
        monkeypatch.setattr(cil, "SCAN_ROOTS", [src, tmp_path / "tests"])
        monkeypatch.setattr(cil, "PROJECT_PACKAGE", "mypkg")

        findings = cil.check_file(module)
        messages = [f.message for f in findings]
        assert any("Relativer Import" in m for m in messages)

    def test_relative_import_in_tests_no_finding(self, tmp_path, monkeypatch):
        # A relative import in tests/ must NOT produce a finding (package-schema.md allows it).
        src = tmp_path / "src"
        tests = tmp_path / "tests"
        tests.mkdir()
        (tests / "__init__.py").write_text("")
        module = _write(
            tests / "test_foo.py",
            """\
            from .helpers import something
        """,
        )

        monkeypatch.setattr(cil, "SOURCE_ROOTS", [src])
        monkeypatch.setattr(cil, "TEST_ROOTS", [tests])
        monkeypatch.setattr(cil, "TOOLS_ROOTS", [])
        monkeypatch.setattr(cil, "SCAN_ROOTS", [src, tests])
        monkeypatch.setattr(cil, "PROJECT_PACKAGE", "mypkg")

        findings = cil.check_file(module)
        relative_findings = [f for f in findings if "Relativer Import" in f.message]
        assert relative_findings == []


class TestLayerViolation:
    def test_domain_importing_infrastructure_is_violation(self, tmp_path, monkeypatch):
        # SOURCE_ROOTS points to src/ so modules resolve as mypkg.domain.foo etc.
        src = tmp_path / "src"
        pkg = src / "mypkg"
        (pkg / "domain").mkdir(parents=True)
        (pkg / "infrastructure").mkdir(parents=True)
        (pkg / "__init__.py").write_text("")
        (pkg / "domain" / "__init__.py").write_text("")
        (pkg / "infrastructure" / "__init__.py").write_text("")

        module = _write(
            pkg / "domain" / "foo.py",
            """\
            import mypkg.infrastructure.db
        """,
        )

        monkeypatch.setattr(cil, "SOURCE_ROOTS", [src])
        monkeypatch.setattr(cil, "TEST_ROOTS", [])
        monkeypatch.setattr(cil, "TOOLS_ROOTS", [])
        monkeypatch.setattr(cil, "SCAN_ROOTS", [src])
        monkeypatch.setattr(cil, "PROJECT_PACKAGE", "mypkg")

        findings = cil.check_file(module)
        assert any(isinstance(f, cil.ImportFinding) for f in findings)


class TestCheckConfig:
    def test_detects_placeholder_in_project_package(self, monkeypatch):
        monkeypatch.setattr(cil, "PROJECT_PACKAGE", "<PYTHON_PACKAGE_NAME>")
        errors = cil.check_config()
        assert errors

    def test_no_errors_with_real_values(self, monkeypatch):
        monkeypatch.setattr(cil, "PROJECT_PACKAGE", "mypkg")
        monkeypatch.setattr(cil, "SOURCE_ROOTS", [Path("src/mypkg")])
        monkeypatch.setattr(cil, "TEST_ROOTS", [Path("tests")])
        monkeypatch.setattr(cil, "TOOLS_ROOTS", [Path("tools")])
        # check_config checks if roots exist on disk, so we skip that part
        # by only checking that the placeholder sentinel is not found.
        errors = cil.check_config()
        sentinel_errors = [e for e in errors if "PYTHON_PACKAGE_NAME" in e]
        assert sentinel_errors == []
