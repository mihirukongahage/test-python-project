"""
Tests for the CLI module.
Tests all CLI commands using Click's CliRunner.
"""

import json
import pytest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch, MagicMock
from click.testing import CliRunner

from todo_app.cli import (
    cli, load_todos, save_todos, TODO_FILE,
    add, list, complete, delete, clear, stats, search, filter, overdue
)


@pytest.fixture
def runner():
    """Create a CLI runner."""
    return CliRunner()


@pytest.fixture
def temp_todo_file(tmp_path):
    """Create a temporary todo file path."""
    return tmp_path / "test_todos.json"


@pytest.fixture
def sample_todos():
    """Sample todos for testing."""
    now = datetime.now()
    old_date = (now - timedelta(days=10)).isoformat()
    return [
        {
            "id": 1,
            "task": "Buy groceries",
            "priority": "high",
            "completed": False,
            "created_at": old_date
        },
        {
            "id": 2,
            "task": "Write documentation",
            "priority": "medium",
            "completed": False,
            "created_at": now.isoformat()
        },
        {
            "id": 3,
            "task": "Review code",
            "priority": "low",
            "completed": True,
            "created_at": now.isoformat()
        }
    ]


class TestLoadSaveTodos:
    """Tests for load_todos and save_todos functions."""

    def test_load_todos_file_exists(self, temp_todo_file, sample_todos):
        """Test loading todos when file exists."""
        with open(temp_todo_file, 'w') as f:
            json.dump(sample_todos, f)
        
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            todos = load_todos()
            assert len(todos) == 3
            assert todos[0]['task'] == "Buy groceries"

    def test_load_todos_file_not_exists(self, temp_todo_file):
        """Test loading todos when file doesn't exist."""
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            todos = load_todos()
            assert todos == []

    def test_save_todos(self, temp_todo_file, sample_todos):
        """Test saving todos to file."""
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            save_todos(sample_todos)
            
            with open(temp_todo_file, 'r') as f:
                saved = json.load(f)
            
            assert len(saved) == 3
            assert saved[0]['task'] == "Buy groceries"


class TestCliGroup:
    """Tests for the main CLI group."""

    def test_cli_help(self, runner):
        """Test CLI help message."""
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert "Simple Todo Application" in result.output


class TestAddCommand:
    """Tests for the add command."""

    def test_add_task_default_priority(self, runner, temp_todo_file):
        """Test adding a task with default priority."""
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['add', 'Test task'])
            assert result.exit_code == 0
            assert "Added task: Test task" in result.output
            assert "Priority: medium" in result.output

    def test_add_task_high_priority(self, runner, temp_todo_file):
        """Test adding a task with high priority."""
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['add', 'Urgent task', '-p', 'high'])
            assert result.exit_code == 0
            assert "Added task: Urgent task" in result.output
            assert "Priority: high" in result.output

    def test_add_task_low_priority(self, runner, temp_todo_file):
        """Test adding a task with low priority."""
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['add', 'Low priority task', '--priority', 'low'])
            assert result.exit_code == 0
            assert "Priority: low" in result.output


class TestListCommand:
    """Tests for the list command."""

    def test_list_empty(self, runner, temp_todo_file):
        """Test listing when no tasks exist."""
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['list'])
            assert result.exit_code == 0
            assert "No tasks found" in result.output

    def test_list_with_tasks(self, runner, temp_todo_file, sample_todos):
        """Test listing tasks."""
        with open(temp_todo_file, 'w') as f:
            json.dump(sample_todos, f)
        
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['list'])
            assert result.exit_code == 0
            assert "Your Todo List" in result.output
            assert "Buy groceries" in result.output
            assert "Write documentation" in result.output
            assert "Review code" in result.output

    def test_list_shows_priority_colors(self, runner, temp_todo_file, sample_todos):
        """Test that list shows different priorities."""
        with open(temp_todo_file, 'w') as f:
            json.dump(sample_todos, f)
        
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['list'])
            assert result.exit_code == 0
            assert "HIGH" in result.output
            # MEDIUM may be truncated to MEDI... in narrow terminal
            assert "MEDI" in result.output
            assert "LOW" in result.output

    def test_list_shows_status(self, runner, temp_todo_file, sample_todos):
        """Test that list shows completion status."""
        with open(temp_todo_file, 'w') as f:
            json.dump(sample_todos, f)
        
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['list'])
            assert result.exit_code == 0
            assert "Done" in result.output
            assert "Pending" in result.output


class TestCompleteCommand:
    """Tests for the complete command."""

    def test_complete_existing_task(self, runner, temp_todo_file, sample_todos):
        """Test completing an existing task."""
        with open(temp_todo_file, 'w') as f:
            json.dump(sample_todos, f)
        
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['complete', '1'])
            assert result.exit_code == 0
            assert "Marked task 1 as completed" in result.output

    def test_complete_nonexistent_task(self, runner, temp_todo_file, sample_todos):
        """Test completing a non-existent task."""
        with open(temp_todo_file, 'w') as f:
            json.dump(sample_todos, f)
        
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['complete', '999'])
            assert result.exit_code == 0
            assert "Task 999 not found" in result.output


class TestDeleteCommand:
    """Tests for the delete command."""

    def test_delete_existing_task(self, runner, temp_todo_file, sample_todos):
        """Test deleting an existing task."""
        with open(temp_todo_file, 'w') as f:
            json.dump(sample_todos, f)
        
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['delete', '1'])
            assert result.exit_code == 0
            assert "Deleted task: Buy groceries" in result.output

    def test_delete_nonexistent_task(self, runner, temp_todo_file, sample_todos):
        """Test deleting a non-existent task."""
        with open(temp_todo_file, 'w') as f:
            json.dump(sample_todos, f)
        
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['delete', '999'])
            assert result.exit_code == 0
            assert "Task 999 not found" in result.output


class TestClearCommand:
    """Tests for the clear command."""

    def test_clear_completed_tasks(self, runner, temp_todo_file, sample_todos):
        """Test clearing completed tasks."""
        with open(temp_todo_file, 'w') as f:
            json.dump(sample_todos, f)
        
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['clear'])
            assert result.exit_code == 0
            assert "Cleared 1 completed task(s)" in result.output

    def test_clear_no_completed_tasks(self, runner, temp_todo_file):
        """Test clearing when no completed tasks exist."""
        todos = [
            {
                "id": 1,
                "task": "Pending task",
                "priority": "medium",
                "completed": False,
                "created_at": datetime.now().isoformat()
            }
        ]
        with open(temp_todo_file, 'w') as f:
            json.dump(todos, f)
        
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['clear'])
            assert result.exit_code == 0
            assert "No completed tasks to clear" in result.output


class TestStatsCommand:
    """Tests for the stats command."""

    def test_stats_empty(self, runner, temp_todo_file):
        """Test stats when no tasks exist."""
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['stats'])
            assert result.exit_code == 0
            assert "No tasks found" in result.output

    def test_stats_with_tasks(self, runner, temp_todo_file, sample_todos):
        """Test stats with tasks."""
        with open(temp_todo_file, 'w') as f:
            json.dump(sample_todos, f)
        
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['stats'])
            assert result.exit_code == 0
            assert "Todo Statistics" in result.output
            assert "Total Tasks" in result.output
            assert "Completed" in result.output
            assert "Pending" in result.output


class TestSearchCommand:
    """Tests for the search command."""

    def test_search_empty_todos(self, runner, temp_todo_file):
        """Test search when no tasks exist."""
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['search', 'test'])
            assert result.exit_code == 0
            assert "No tasks found" in result.output

    def test_search_found(self, runner, temp_todo_file, sample_todos):
        """Test search with matching results."""
        with open(temp_todo_file, 'w') as f:
            json.dump(sample_todos, f)
        
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['search', 'groceries'])
            assert result.exit_code == 0
            assert "Found 1 task(s)" in result.output
            assert "Buy groceries" in result.output

    def test_search_not_found(self, runner, temp_todo_file, sample_todos):
        """Test search with no matching results."""
        with open(temp_todo_file, 'w') as f:
            json.dump(sample_todos, f)
        
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['search', 'nonexistent'])
            assert result.exit_code == 0
            assert "No tasks found matching 'nonexistent'" in result.output

    def test_search_case_insensitive(self, runner, temp_todo_file, sample_todos):
        """Test case-insensitive search."""
        with open(temp_todo_file, 'w') as f:
            json.dump(sample_todos, f)
        
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['search', 'GROCERIES'])
            assert result.exit_code == 0
            assert "Found 1 task(s)" in result.output


class TestFilterCommand:
    """Tests for the filter command."""

    def test_filter_empty_todos(self, runner, temp_todo_file):
        """Test filter when no tasks exist."""
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['filter'])
            assert result.exit_code == 0
            assert "No tasks found" in result.output

    def test_filter_by_priority(self, runner, temp_todo_file, sample_todos):
        """Test filtering by priority."""
        with open(temp_todo_file, 'w') as f:
            json.dump(sample_todos, f)
        
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['filter', '-p', 'high'])
            assert result.exit_code == 0
            assert "Found 1 task(s)" in result.output
            assert "Buy groceries" in result.output

    def test_filter_by_status_pending(self, runner, temp_todo_file, sample_todos):
        """Test filtering by pending status."""
        with open(temp_todo_file, 'w') as f:
            json.dump(sample_todos, f)
        
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['filter', '-s', 'pending'])
            assert result.exit_code == 0
            assert "Found 2 task(s)" in result.output

    def test_filter_by_status_completed(self, runner, temp_todo_file, sample_todos):
        """Test filtering by completed status."""
        with open(temp_todo_file, 'w') as f:
            json.dump(sample_todos, f)
        
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['filter', '-s', 'completed'])
            assert result.exit_code == 0
            assert "Found 1 task(s)" in result.output
            assert "Review code" in result.output

    def test_filter_combined(self, runner, temp_todo_file, sample_todos):
        """Test filtering by both priority and status."""
        with open(temp_todo_file, 'w') as f:
            json.dump(sample_todos, f)
        
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['filter', '-p', 'high', '-s', 'pending'])
            assert result.exit_code == 0
            assert "Found 1 task(s)" in result.output
            assert "Buy groceries" in result.output

    def test_filter_no_match(self, runner, temp_todo_file, sample_todos):
        """Test filter with no matching results."""
        with open(temp_todo_file, 'w') as f:
            json.dump(sample_todos, f)
        
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['filter', '-p', 'high', '-s', 'completed'])
            assert result.exit_code == 0
            assert "No tasks match the specified filters" in result.output


class TestOverdueCommand:
    """Tests for the overdue command."""

    def test_overdue_empty_todos(self, runner, temp_todo_file):
        """Test overdue when no tasks exist."""
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['overdue'])
            assert result.exit_code == 0
            assert "No tasks found" in result.output

    def test_overdue_with_old_tasks(self, runner, temp_todo_file, sample_todos):
        """Test overdue with old pending tasks."""
        with open(temp_todo_file, 'w') as f:
            json.dump(sample_todos, f)
        
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['overdue', '-d', '7'])
            assert result.exit_code == 0
            assert "Found 1 overdue task(s)" in result.output
            assert "Buy groceries" in result.output

    def test_overdue_no_old_tasks(self, runner, temp_todo_file):
        """Test overdue when no tasks are overdue."""
        todos = [
            {
                "id": 1,
                "task": "Recent task",
                "priority": "medium",
                "completed": False,
                "created_at": datetime.now().isoformat()
            }
        ]
        with open(temp_todo_file, 'w') as f:
            json.dump(todos, f)
        
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['overdue', '-d', '7'])
            assert result.exit_code == 0
            assert "No tasks are overdue" in result.output

    def test_overdue_custom_days(self, runner, temp_todo_file, sample_todos):
        """Test overdue with custom days threshold."""
        with open(temp_todo_file, 'w') as f:
            json.dump(sample_todos, f)
        
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['overdue', '--days', '5'])
            assert result.exit_code == 0
            assert "overdue" in result.output.lower()


class TestMainEntry:
    """Tests for the main entry point."""

    def test_main_entry(self, runner):
        """Test that cli can be invoked with --help."""
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert "Simple Todo Application" in result.output

    def test_main_module_execution(self, runner, temp_todo_file):
        """Test the __main__ block execution."""
        import runpy
        import sys
        
        # Test that the module can be run as __main__
        # We mock sys.argv to pass --help
        original_argv = sys.argv
        try:
            sys.argv = ['todo_app.cli', '--help']
            # This will raise SystemExit(0) on success
            try:
                runpy.run_module('todo_app.cli', run_name='__main__')
            except SystemExit as e:
                # --help causes SystemExit(0)
                assert e.code == 0
        finally:
            sys.argv = original_argv
