# Author: Jacques Murray
from pathlib import Path
from src.strategies.eslint import ESLintStrategy
from src.strategies.babel import BabelStrategy


class TestESLintStrategy:
    def test_detect(self, legacy_project_dir: Path):
        strategy = ESLintStrategy()
        files = strategy.detect(legacy_project_dir)
        assert len(files) == 1
        assert files[0].name == ".eslintrc.json"

    def test_migrate(self, legacy_project_dir: Path):
        strategy = ESLintStrategy()
        target_file = legacy_project_dir / ".eslintrc.json"

        strategy.migrate(target_file)

        # Assert old file is gone (or backed up)
        assert not target_file.exists()
        assert (legacy_project_dir / ".eslintrc.json.bak").exists()

        # Assert new file exists
        new_file = legacy_project_dir / "eslint.config.js"
        assert new_file.exists()

        content = new_file.read_text()
        assert "export default" in content
        assert "rules" in content
        assert "semi" in content


class TestBabelStrategy:
    def test_detect(self, legacy_project_dir: Path):
        strategy = BabelStrategy()
        files = strategy.detect(legacy_project_dir)
        assert len(files) == 1
        assert files[0].name == ".babelrc"

    def test_migrate(self, legacy_project_dir: Path):
        strategy = BabelStrategy()
        target_file = legacy_project_dir / ".babelrc"

        strategy.migrate(target_file)

        # Assert old file is gone (or backed up)
        assert not target_file.exists()
        assert (legacy_project_dir / ".babelrc.bak").exists()

        # Assert new file exists
        new_file = legacy_project_dir / "babel.config.js"
        assert new_file.exists()

        content = new_file.read_text()
        assert "export default" in content
        assert "@babel/preset-env" in content
