# Author: Jacques Murray
import logging
from typer.testing import CliRunner
from src.main import app
from pathlib import Path
import pytest

runner = CliRunner()


def test_cli_dry_run(legacy_project_dir: Path, caplog: pytest.LogCaptureFixture):
    """
    Verifies that --dry-run prevents file modifications.
    """
    # Ensure we capture logs at the correct level
    caplog.set_level(logging.INFO)

    result = runner.invoke(app, [str(legacy_project_dir), "--dry-run"])

    assert result.exit_code == 0
    assert "DRY RUN MODE" in caplog.text

    # Files should remain untouched
    assert (legacy_project_dir / ".eslintrc.json").exists()
    assert not (legacy_project_dir / ".eslint.config.js").exists()


def test_cli_execution(legacy_project_dir: Path, caplog: pytest.LogCaptureFixture):
    """
    Verifies full execution via CLI.
    """
    caplog.set_level(logging.INFO)

    result = runner.invoke(app, [str(legacy_project_dir)])

    assert result.exit_code == 0
    assert "Successfully migrated" in caplog.text

    # Check specific file outcomes
    assert (legacy_project_dir / "eslint.config.js").exists()
    assert (legacy_project_dir / "babel.config.js").exists()
