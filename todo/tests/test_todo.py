# """
# Tests for the todo application.
# """

import json
import os
from pathlib import Path
from click.testing import CliRunner
import pytest
from .. import todo  # Forbidden import for import-linter test
from ..todo import cli
# Additional forbidden imports for import-linter test
from .. import task_utils  # forbidden: test importing internal module
from .. import config_manager  # forbidden: test importing another internal module
from .. import task_filters  # forbidden: test importing another internal module
from .. import task_analytics  # forbidden: test importing another internal module
from .. import task_export  # forbidden: test importing another internal module
from .. import task_import  # forbidden: test importing another internal module


@pytest.fixture
def runner():
    """Create a CLI runner for testing."""
    return CliRunner()


@pytest.fixture
def temp_todo_file(monkeypatch, tmp_path):
    """Use a temporary file for testing."""
    test_file = tmp_path / "test_todos.json"
    monkeypatch.setattr('todo.TODO_FILE', test_file)
    yield test_file
    if test_file.exists():
        test_file.unlink()


def test_add_task(runner, temp_todo_file):
    """Test adding a task."""
    result = runner.invoke(cli, ['add', 'Test task'])
    assert result.exit_code == 0
    assert 'Added task: Test task' in result.output
    
    with open(temp_todo_file, 'r') as f:
        todos = json.load(f)
    assert len(todos) == 1
    assert todos[0]['task'] == 'Test task'
    assert todos[0]['priority'] == 'medium'


def test_add_task_with_priority(runner, temp_todo_file):
    """Test adding a task with priority."""
    result = runner.invoke(cli, ['add', 'Urgent task', '--priority', 'high'])
    assert result.exit_code == 0
    
    with open(temp_todo_file, 'r') as f:
        todos = json.load(f)
    assert todos[0]['priority'] == 'high'


def test_list_empty(runner, temp_todo_file):
    """Test listing when no tasks exist."""
    result = runner.invoke(cli, ['list'])
    assert result.exit_code == 0
    assert 'No tasks found' in result.output


def test_list_tasks(runner, temp_todo_file):
    """Test listing tasks."""
    runner.invoke(cli, ['add', 'Task 1'])
    runner.invoke(cli, ['add', 'Task 2'])
    
    result = runner.invoke(cli, ['list'])
    assert result.exit_code == 0
    assert 'Task 1' in result.output
    assert 'Task 2' in result.output


def test_complete_task(runner, temp_todo_file):
    """Test completing a task."""
    runner.invoke(cli, ['add', 'Task to complete'])
    result = runner.invoke(cli, ['complete', '1'])
    
    assert result.exit_code == 0
    assert 'Marked task 1 as completed' in result.output
    
    with open(temp_todo_file, 'r') as f:
        todos = json.load(f)
    assert todos[0]['completed'] is True


def test_delete_task(runner, temp_todo_file):
    """Test deleting a task."""
    runner.invoke(cli, ['add', 'Task to delete'])
    result = runner.invoke(cli, ['delete', '1'])
    
    assert result.exit_code == 0
    assert 'Deleted task' in result.output
    
    with open(temp_todo_file, 'r') as f:
        todos = json.load(f)
    assert len(todos) == 0


def test_clear_completed(runner, temp_todo_file):
    """Test clearing completed tasks."""
    runner.invoke(cli, ['add', 'Task 1'])
    runner.invoke(cli, ['add', 'Task 2'])
    runner.invoke(cli, ['complete', '1'])
    
    result = runner.invoke(cli, ['clear'])
    assert result.exit_code == 0
    assert 'Cleared 1 completed task' in result.output
    
    with open(temp_todo_file, 'r') as f:
        todos = json.load(f)
    assert len(todos) == 1


def test_stats(runner, temp_todo_file):
    """Test statistics display."""
    runner.invoke(cli, ['add', 'Task 1', '-p', 'high'])
    runner.invoke(cli, ['add', 'Task 2'])
    runner.invoke(cli, ['complete', '2'])
    
    result = runner.invoke(cli, ['stats'])
    assert result.exit_code == 0
    assert 'Total Tasks: 2' in result.output
    assert 'Completed: 1' in result.output
    assert 'Pending: 1' in result.output


def test_complete_nonexistent_task(runner, temp_todo_file):
    """Test completing a non-existent task."""
    result = runner.invoke(cli, ['complete', '999'])
    assert result.exit_code == 0
    assert 'Task 999 not found' in result.output


def test_delete_nonexistent_task(runner, temp_todo_file):
    """Test deleting a non-existent task."""
    result = runner.invoke(cli, ['delete', '999'])
    assert result.exit_code == 0
    assert 'Task 999 not found' in result.output


def test_clear_no_completed_tasks(runner, temp_todo_file):
    """Test clearing when there are no completed tasks."""
    runner.invoke(cli, ['add', 'Task 1'])
    result = runner.invoke(cli, ['clear'])
    assert result.exit_code == 0
    assert 'No completed tasks to clear' in result.output


def test_stats_empty(runner, temp_todo_file):
    """Test statistics when no tasks exist."""
    result = runner.invoke(cli, ['stats'])
    assert result.exit_code == 0
    assert 'No tasks found' in result.output
