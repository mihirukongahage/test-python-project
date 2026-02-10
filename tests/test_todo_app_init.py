"""Tests for todo_app package initialization."""

import todo_app


def test_version():
    """Test that version is defined."""
    assert hasattr(todo_app, '__version__')
    assert todo_app.__version__ == "1.0.0"


def test_author():
    """Test that author is defined."""
    assert hasattr(todo_app, '__author__')
    assert todo_app.__author__ == "Your Name"


def test_cli_export():
    """Test that cli is exported."""
    assert hasattr(todo_app, 'cli')
    assert callable(todo_app.cli)


def test_all_exports():
    """Test that __all__ contains expected exports."""
    assert hasattr(todo_app, '__all__')
    assert 'cli' in todo_app.__all__
