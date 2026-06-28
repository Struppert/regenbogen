"""Tests für instantiate_project_box.py im instanziierten Projektkontext."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "instantiate"))
from instantiate_project_box import (  # noqa: E402
    Replacement,
    build_replacements,
    derive_python_package_name,
    instantiate_checks,
    replacement_map,
    validate_python_package_name,
)


class TestReplacement:
    def test_token_builds_angle_bracket_placeholder(self):
        repl = Replacement("SOURCE_ROOT", "src")
        assert repl.token == "<SOURCE_ROOT>"


class TestDerivePythonPackageName:
    def test_normalizes_display_name(self):
        assert derive_python_package_name("Regenbogen App") == "regenbogen_app"

    def test_replaces_invalid_characters(self):
        assert derive_python_package_name("Regenbogen-App!") == "regenbogen_app"


class TestValidatePythonPackageName:
    def test_accepts_valid_name(self):
        assert validate_python_package_name("regenbogen") == "regenbogen"

    def test_rejects_uppercase_name(self):
        with pytest.raises(SystemExit):
            validate_python_package_name("Regenbogen")

    def test_rejects_keyword(self):
        with pytest.raises(SystemExit):
            validate_python_package_name("class")


class TestBuildReplacements:
    def test_uses_defaults_for_standard_commands(self):
        args = argparse.Namespace(
            project_display_name="Regenbogen",
            python_package_name=None,
            source_root="src",
            test_root="tests",
            docs_root="docs",
            tools_root="tools",
            import_layer_check_cmd=None,
            python_lint_cmd=None,
            python_format_check_cmd=None,
            python_typecheck_cmd=None,
            python_test_cmd=None,
            full_validation_cmd=None,
        )

        replacements = build_replacements(args)
        values = replacement_map(replacements)

        assert values["PYTHON_PACKAGE_NAME"] == "regenbogen"
        assert values["IMPORT_LAYER_CHECK_CMD"] == (
            "python tools/check_import_layers.py --preflight src tests tools"
        )
        assert values["PYTHON_TEST_CMD"] == "python -m pytest"

    def test_respects_explicit_package_name(self):
        args = argparse.Namespace(
            project_display_name="Regenbogen",
            python_package_name="regenbogen_alt",
            source_root="src",
            test_root="tests",
            docs_root="docs",
            tools_root="tools",
            import_layer_check_cmd="custom import check",
            python_lint_cmd="custom lint",
            python_format_check_cmd="custom format",
            python_typecheck_cmd="custom typecheck",
            python_test_cmd="custom test",
            full_validation_cmd="custom full",
        )

        replacements = build_replacements(args)
        values = replacement_map(replacements)

        assert values["PYTHON_PACKAGE_NAME"] == "regenbogen_alt"
        assert values["PYTHON_LINT_CMD"] == "custom lint"
        assert values["FULL_VALIDATION_CMD"] == "custom full"


class TestInstantiateChecks:
    def test_expands_root_placeholders(self):
        commands = [
            "python tool.py <SOURCE_ROOT> <TEST_ROOT> <TOOLS_ROOT>",
        ]
        values = {
            "SOURCE_ROOT": "src",
            "TEST_ROOT": "tests",
            "TOOLS_ROOT": "tools",
        }

        assert instantiate_checks(commands, values) == [
            "python tool.py src tests tools"
        ]
