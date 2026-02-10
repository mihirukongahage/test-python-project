.PHONY: help install install-dev test coverage lint format clean build

help:
	@echo "Available commands:"
	@echo "  make install      - Install production dependencies"
	@echo "  make install-dev  - Install development dependencies"
	@echo "  make test         - Run tests"
	@echo "  make coverage     - Run tests with coverage report"
	@echo "  make lint         - Run linters (ruff)"
	@echo "  make format       - Format code with black"
	@echo "  make clean        - Remove build artifacts and cache files"
	@echo "  make build        - Build distribution packages"
	@echo "  make run          - Run the todo application"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"
	# Or if using requirements files:
	# pip install -r requirements-dev.txt

test:
	pytest -v

coverage:
	pytest --cov=src --cov-report=term-missing --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

lint:
	ruff check src/ tests/
	mypy src/

format:
	black src/ tests/
	ruff check --fix src/ tests/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf .import_linter_cache/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

build: clean
	python -m build

run:
	todo --help
