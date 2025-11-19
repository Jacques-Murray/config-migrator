# Author: Jacques Murray
import pytest
import json
from pathlib import Path


@pytest.fixture
def legacy_project_dir(tmp_path: Path) -> Path:
    """
    Creates a temporary directory structure simulating a legacy project
    populated with older config files.
    """
    project_root = tmp_path / "legacy_project"
    project_root.mkdir()

    # Create a dummy .eslintrc.json
    eslint_data = {
        "env": {"browser": True, "es2021": True},
        "extends": "eslint:recommended",
        "rules": {"semi": ["error", "always"]},
    }
    (project_root / ".eslintrc.json").write_text(json.dumps(eslint_data))

    # Create a dummy .babelrc
    babel_data = {
        "presets": ["@babel/preset-env"],
        "plugins": ["@babel/plugin-transform-runtime"],
    }
    (project_root / ".babelrc").write_text(json.dumps(babel_data))

    return project_root
