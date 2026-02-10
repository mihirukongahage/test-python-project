# Project Structure Overview

This document describes the restructured repository following Python best practices.

## Summary of Changes

The repository has been restructured from a flat layout to a professional Python package structure with proper separation of concerns.

### Key Improvements

1. **Src Layout**: Source code moved to `src/todo_app/` package
2. **Proper Package Structure**: Added `__init__.py` files for package initialization
3. **Separate Test Directory**: Tests moved to `tests/` directory
4. **Modern Configuration**: Added `pyproject.toml` for modern Python packaging
5. **Development Tools**: Added Makefile, pre-commit hooks, and CI/CD workflows
6. **Documentation**: Created comprehensive documentation and contributing guidelines
7. **Code Quality**: Configured linters, formatters, and type checkers

## Directory Structure

```
test-python-project/
├── .github/                      # GitHub-specific files
│   ├── ISSUE_TEMPLATE/          # Issue templates
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── pull_request_template.md # PR template
│   └── workflows/               # CI/CD workflows
│       └── ci.yml               # GitHub Actions CI
│
├── docs/                        # Documentation
│   ├── COVERAGE.md             # Coverage reports
│   └── README.md               # Documentation index
│
├── scripts/                     # Utility scripts
│   ├── analyze_dependencies.py # Dependency analyzer
│   ├── run_coverage.sh         # Coverage script
│   └── setup.sh                # Setup script
│
├── src/                         # Source code
│   ├── todo_app/               # Main application package
│   │   ├── __init__.py         # Package initialization
│   │   ├── cli.py              # CLI interface (renamed from todo.py)
│   │   ├── task_analytics.py   # Analytics and insights
│   │   └── task_filters.py     # Filtering and searching
│   ├── export/                 # Export functionality package
│   │   ├── __init__.py         # Export package initialization
│   │   ├── task_export.py      # Export to various formats
│   │   └── README.md           # Export documentation
│   ├── imports/                # Import functionality package
│   │   ├── __init__.py         # Import package initialization
│   │   ├── task_import.py      # Import from various formats
│   │   └── README.md           # Import documentation
│   └── utils/                  # Utility modules package
│       ├── __init__.py         # Utils package initialization
│       ├── config_manager.py   # Configuration management
│       ├── task_utils.py       # Task validation and utilities
│       └── README.md           # Utils package documentation
│
├── tests/                       # Test suite
│   ├── __init__.py             # Test package initialization
│   ├── conftest.py             # Pytest fixtures
│   ├── test_config_manager.py  # Config manager tests
│   ├── test_task_analytics.py  # Analytics tests
│   ├── test_task_export.py     # Export tests
│   ├── test_task_filters.py    # Filter tests
│   ├── test_task_import.py     # Import tests
│   └── test_task_utils.py      # Utility tests
│
├── .coveragerc                  # Coverage configuration
├── .editorconfig               # Editor configuration
├── .gitignore                  # Git ignore patterns
├── .importlinter               # Import linting rules
├── .pre-commit-config.yaml     # Pre-commit hooks
├── CHANGELOG.md                # Version history
├── CONTRIBUTING.md             # Contributing guidelines
├── LICENSE                     # MIT License
├── Makefile                    # Development tasks
├── MANIFEST.in                 # Package distribution files
├── pyproject.toml              # Modern Python project config
├── README.md                   # Project documentation
├── requirements-dev.txt        # Development dependencies
├── requirements.txt            # Production dependencies
├── setup.py                    # Backward compatibility
└── STRUCTURE.md                # This file
```

## Installation

### For Development

```bash
# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Or using requirements files
pip install -r requirements-dev.txt
```

### For Users

```bash
# Install the package
pip install -e .

# Or using requirements
pip install -r requirements.txt
```

## Usage

After installation, the package provides a `todo` command:

```bash
todo --help
todo add "Buy groceries"
todo list
```

## Development Workflow

### Quick Commands (Makefile)

```bash
make help          # Show all available commands
make install-dev   # Install development dependencies
make test          # Run tests
make coverage      # Run tests with coverage
make lint          # Run linters
make format        # Format code
make clean         # Remove build artifacts
make build         # Build distribution packages
```

### Running Tests

```bash
# Run all tests
pytest -v

# Run with coverage
pytest --cov=todo_app --cov-report=html

# Or use Makefile
make test
make coverage
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type check
mypy src/

# Or use Makefile
make format
make lint
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Run manually
pre-commit run --all-files
```

## CI/CD

GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every push and PR:

- Tests on Python 3.8, 3.9, 3.10, 3.11, 3.12
- Code formatting check (black)
- Linting (ruff)
- Type checking (mypy)
- Import structure validation (import-linter)
- Coverage reporting (Codecov)

## Configuration Files

### pyproject.toml
Modern Python project configuration including:
- Package metadata
- Dependencies
- Build system
- Tool configurations (pytest, coverage, black, ruff, mypy)
- Entry points for CLI commands

### .coveragerc
Coverage configuration:
- Source directory: `src/`
- HTML report directory: `htmlcov/`
- Exclude patterns for test files

### .importlinter
Import structure rules to maintain clean architecture

### .editorconfig
Editor configuration for consistent coding style

### .pre-commit-config.yaml
Pre-commit hooks for:
- Trailing whitespace removal
- File ending fixes
- YAML/JSON validation
- Large file detection
- Code formatting (black)
- Linting (ruff)
- Type checking (mypy)

## Dependencies

### Production
- **click**: CLI framework
- **rich**: Terminal formatting

### Development
- **pytest**: Testing framework
- **coverage**: Code coverage
- **pytest-cov**: Coverage plugin
- **black**: Code formatter
- **ruff**: Fast linter
- **mypy**: Static type checker
- **import-linter**: Import structure validation

## Package Distribution

The package is configured for distribution via PyPI:

```bash
# Build distribution packages
python -m build

# Or use Makefile
make build
```

This creates:
- Source distribution (`.tar.gz`)
- Wheel distribution (`.whl`)

## Testing Results

All 139 tests pass with 80.40% code coverage:
- 21 config manager tests
- 20 analytics tests
- 20 export tests
- 27 filter tests
- 25 import tests
- 26 utility tests

## Benefits of New Structure

1. **Maintainability**: Clear separation of source and test code
2. **Scalability**: Easy to add new modules and features
3. **Testability**: Proper test isolation and fixtures
4. **Distribution**: Ready for PyPI publication
5. **Development**: Comprehensive tooling for code quality
6. **Collaboration**: Templates and guidelines for contributors
7. **Automation**: CI/CD pipeline for continuous integration
8. **Standards**: Follows Python packaging best practices

## Migration Notes

### Import Changes

Old import style:
```python
from task_filters import filter_by_priority
from config_manager import ConfigManager
```

New import style:
```python
from todo_app.task_filters import filter_by_priority
from todo_app.config_manager import ConfigManager
```

### Command Changes

Old command:
```bash
python todo.py add "Task"
```

New command:
```bash
todo add "Task"
```

## Next Steps

Recommended improvements:
1. Add Sphinx documentation for API reference
2. Publish package to PyPI
3. Set up automated releases
4. Add more integration tests
5. Improve CLI test coverage
6. Add performance benchmarks

## Resources

- [Python Packaging Guide](https://packaging.python.org/)
- [pytest Documentation](https://docs.pytest.org/)
- [Black Documentation](https://black.readthedocs.io/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [GitHub Actions](https://docs.github.com/actions)

---

For more information, see:
- [README.md](README.md) - Project overview
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contributing guidelines
- [CHANGELOG.md](CHANGELOG.md) - Version history
