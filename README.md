# Config Migrator

**Author:** Jacques Murray

A production-grade CLI utility designed to modernize legacy JavaScript toolchain configurations. It automatically detects older configuration formats (e.g., `.eslintrc.json`, `.babelrc`) and migrates them to modern ECMAScript Module (ESM) standards (e.g., `eslint.config.js` Flat Config).

## Features

- **Safe Migration:** Implements atomic write operations with automatic `.bak` creation.
- **Strategy Pattern:** Extensible architecture allowing easy addition of new tools (WebPack, Prettier, etc.).
- **Dry Run Mode:** Preview changes without modifying the file system.
- **Type Safe:** Fully typed Python 3.13+ codebase.

## Installation

Requires Python 3.13+. We recommend using `uv` for dependency management.

```bash
# Clone the repository
git clone https://github.com/Jacques-Murray/config-migrator.git
cd config-migrator

# Create virtual environment
uv venv

# Install dependencies
uv pip install -r requirements.txt
```

## Usage

### Basic Migration

Scan a project directory and migrate detected files:

```bash
uv run config_migrator --path /path/to/legacy-project
```

### Dry Run (Safe Mode)

Simulate the migration to see what would happen without writing changes:

```bash
uv run config_migrator --path /path/to/legacy-project --dry-run
```

### Verbose Logging

Enable debug output for troubleshooting:

```bash
uv run config_migrator --path /path/to/legacy-project --verbose
```

## Development

### Running Tests

We use `pytest` for the test suite.

```bash
# Run all tests
uv run pytest

# Run with coverage report
uv run pytest --cov=src tests/
```

### Pre-commit Hooks

Ensure code quality before committing:

```bash
# Install pre-commit
uv pip install pre-commit

# Install hooks
uv run pre-commit install
```

## Architecture

The project follows strict **SOLID** principles:

- **Core:** Contains the `MigrationManager` and abstract `MigrationStrategy`.
- **Strategies:** Concrete implementations for specific tools (ESLint, Babel).
- **Utils:** `FileSystemHandler` (Safe I/O) and `JSSerializer` (Python dict to JS string).

## License

MIT License. See `LICENSE` file for details.
