"""
Pytest configuration and shared fixtures.

This file contains pytest configuration and fixtures that are
available to all test modules.
"""

import json
import pytest
from pathlib import Path


@pytest.fixture
def temp_todo_file(tmp_path):
    """Create a temporary todo file for testing."""
    todo_file = tmp_path / "test_todo.json"
    return todo_file


@pytest.fixture
def sample_tasks():
    """Provide sample tasks for testing."""
    return [
        {
            "id": 1,
            "task": "Buy groceries",
            "priority": "high",
            "completed": False,
            "created_at": "2024-01-15T10:30:00",
        },
        {
            "id": 2,
            "task": "Write documentation",
            "priority": "medium",
            "completed": False,
            "created_at": "2024-01-15T11:00:00",
        },
        {
            "id": 3,
            "task": "Review pull requests",
            "priority": "low",
            "completed": True,
            "created_at": "2024-01-14T09:00:00",
        },
    ]


@pytest.fixture
def todo_file_with_tasks(temp_todo_file, sample_tasks):
    """Create a todo file with sample tasks."""
    with open(temp_todo_file, "w") as f:
        json.dump({"tasks": sample_tasks}, f)
    return temp_todo_file
