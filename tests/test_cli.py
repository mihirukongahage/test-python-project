"""
Tests for the CLI module.
Covers all CLI commands and their functionality.
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
    """Create a CLI runner for testing."""
    return CliRunner()


@pytest.fixture
def temp_todo_file(tmp_path):
    """Create a temporary todo file path."""
    return tmp_path / "test_todo.json"


@pytest.fixture
def sample_todos():
    """Provide sample todos for testing."""
    return [
        {
            "id": 1,
            "task": "Buy groceries",
            "priority": "high",
            "completed": False,
            "created_at": datetime.now().isoformat()
        },
        {
            "id": 2,
            "task": "Write documentation",
            "priority": "medium",
            "completed": False,
            "created_at": datetime.now().isoformat()
        },
        {
            "id": 3,
            "task": "Review pull requests",
            "priority": "low",
            "completed": True,
            "created_at": datetime.now().isoformat()
        }
    ]


@pytest.fixture
def old_todos():
    """Provide old todos for overdue testing."""
    old_date = (datetime.now() - timedelta(days=10)).isoformat()
    return [
        {
            "id": 1,
            "task": "Old pending task",
            "priority": "high",
            "completed": False,
            "created_at": old_date
        },
        {
            "id": 2,
            "task": "Recent task",
            "priority": "medium",
            "completed": False,
            "created_at": datetime.now().isoformat()
        }
    ]


class TestLoadTodos:
    """Tests for load_todos function."""

    def test_load_todos_file_exists(self, temp_todo_file, sample_todos):
        """Test loading todos when file exists."""
        with open(temp_todo_file, 'w') as f:
            json.dump(sample_todos, f)
        
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            todos = load_todos()
            assert len(todos) == 3
            assert todos[0]['task'] == "Buy groceries"

    def test_load_todos_file_not_exists(self, tmp_path):
        """Test loading todos when file doesn't exist."""
        non_existent_file = tmp_path / "non_existent.json"
        
        with patch('todo_app.cli.TODO_FILE', non_existent_file):
            todos = load_todos()
            assert todos == []


class TestSaveTodos:
    """Tests for save_todos function."""

    def test_save_todos(self, temp_todo_file, sample_todos):
        """Test saving todos to file."""
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            save_todos(sample_todos)
        
        with open(temp_todo_file, 'r') as f:
            saved_todos = json.load(f)
        
        assert len(saved_todos) == 3
        assert saved_todos[0]['task'] == "Buy groceries"


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

    def test_list_shows_all_priorities(self, runner, temp_todo_file, sample_todos):
        """Test that list shows tasks with all priority levels."""
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

    def test_stats_with_tasks(self, runner, temp_todo_file, sample_todos):
        """Test showing statistics with tasks."""
        with open(temp_todo_file, 'w') as f:
            json.dump(sample_todos, f)
        
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['stats'])
            assert result.exit_code == 0
            assert "Todo Statistics" in result.output
            assert "Total Tasks" in result.output
            assert "Completed" in result.output
            assert "Pending" in result.output

    def test_stats_empty(self, runner, temp_todo_file):
        """Test showing statistics when no tasks exist."""
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['stats'])
            assert result.exit_code == 0
            assert "No tasks found" in result.output


class TestSearchCommand:
    """Tests for the search command."""

    def test_search_found(self, runner, temp_todo_file, sample_todos):
        """Test searching for existing tasks."""
        with open(temp_todo_file, 'w') as f:
            json.dump(sample_todos, f)
        
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['search', 'groceries'])
            assert result.exit_code == 0
            assert "Found 1 task(s)" in result.output
            assert "Buy groceries" in result.output

    def test_search_not_found(self, runner, temp_todo_file, sample_todos):
        """Test searching for non-existing tasks."""
        with open(temp_todo_file, 'w') as f:
            json.dump(sample_todos, f)
        
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['search', 'nonexistent'])
            assert result.exit_code == 0
            assert "No tasks found matching 'nonexistent'" in result.output

    def test_search_empty_list(self, runner, temp_todo_file):
        """Test searching when no tasks exist."""
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['search', 'anything'])
            assert result.exit_code == 0
            assert "No tasks found" in result.output

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

    def test_filter_combined(self, runner, temp_todo_file, sample_todos):
        """Test filtering by both priority and status."""
        with open(temp_todo_file, 'w') as f:
            json.dump(sample_todos, f)
        
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['filter', '-p', 'high', '-s', 'pending'])
            assert result.exit_code == 0
            assert "Found 1 task(s)" in result.output

    def test_filter_no_match(self, runner, temp_todo_file, sample_todos):
        """Test filtering with no matching tasks."""
        with open(temp_todo_file, 'w') as f:
            json.dump(sample_todos, f)
        
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['filter', '-p', 'high', '-s', 'completed'])
            assert result.exit_code == 0
            assert "No tasks match the specified filters" in result.output

    def test_filter_empty_list(self, runner, temp_todo_file):
        """Test filtering when no tasks exist."""
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['filter', '-p', 'high'])
            assert result.exit_code == 0
            assert "No tasks found" in result.output


class TestOverdueCommand:
    """Tests for the overdue command."""

    def test_overdue_with_old_tasks(self, runner, temp_todo_file, old_todos):
        """Test showing overdue tasks."""
        with open(temp_todo_file, 'w') as f:
            json.dump(old_todos, f)
        
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['overdue'])
            assert result.exit_code == 0
            assert "Found 1 overdue task(s)" in result.output
            assert "Old pending task" in result.output

    def test_overdue_no_old_tasks(self, runner, temp_todo_file, sample_todos):
        """Test when no tasks are overdue."""
        with open(temp_todo_file, 'w') as f:
            json.dump(sample_todos, f)
        
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['overdue'])
            assert result.exit_code == 0
            assert "No tasks are overdue" in result.output

    def test_overdue_custom_days(self, runner, temp_todo_file, old_todos):
        """Test overdue with custom days threshold."""
        with open(temp_todo_file, 'w') as f:
            json.dump(old_todos, f)
        
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['overdue', '-d', '5'])
            assert result.exit_code == 0
            assert "overdue" in result.output.lower()

    def test_overdue_empty_list(self, runner, temp_todo_file):
        """Test overdue when no tasks exist."""
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            result = runner.invoke(cli, ['overdue'])
            assert result.exit_code == 0
            assert "No tasks found" in result.output


class TestMainEntry:
    """Tests for the main entry point."""

    def test_main_entry(self, runner):
        """Test that CLI can be invoked with help."""
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert "Simple Todo Application" in result.output


class TestIntegration:
    """Integration tests for CLI workflow."""

    def test_add_list_complete_workflow(self, runner, temp_todo_file):
        """Test complete workflow: add, list, complete, delete."""
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            # Add a task
            result = runner.invoke(cli, ['add', 'Integration test task', '-p', 'high'])
            assert result.exit_code == 0
            assert "Added task" in result.output
            
            # List tasks
            result = runner.invoke(cli, ['list'])
            assert result.exit_code == 0
            assert "Integration test task" in result.output
            
            # Complete the task
            result = runner.invoke(cli, ['complete', '1'])
            assert result.exit_code == 0
            assert "Marked task 1 as completed" in result.output
            
            # Clear completed tasks
            result = runner.invoke(cli, ['clear'])
            assert result.exit_code == 0
            assert "Cleared 1 completed task(s)" in result.output

    def test_multiple_tasks_workflow(self, runner, temp_todo_file):
        """Test workflow with multiple tasks."""
        with patch('todo_app.cli.TODO_FILE', temp_todo_file):
            # Add multiple tasks
            runner.invoke(cli, ['add', 'Task 1', '-p', 'high'])
            runner.invoke(cli, ['add', 'Task 2', '-p', 'medium'])
            runner.invoke(cli, ['add', 'Task 3', '-p', 'low'])
            
            # List all tasks
            result = runner.invoke(cli, ['list'])
            assert "Task 1" in result.output
            assert "Task 2" in result.output
            assert "Task 3" in result.output
            
            # Filter by priority
            result = runner.invoke(cli, ['filter', '-p', 'high'])
            assert "Task 1" in result.output
            
            # Search
            result = runner.invoke(cli, ['search', 'Task 2'])
            assert "Task 2" in result.output
            
            # Stats
            result = runner.invoke(cli, ['stats'])
            assert "Total Tasks" in result.output
            assert "3" in result.output


class TestMainBlock:
    """Tests for the __main__ block execution."""

    def test_main_block_execution(self):
        """Test that the __main__ block calls cli() when executed as main module."""
        import runpy
        import sys
        
        # Mock sys.argv to simulate running with --help to avoid interactive mode
        original_argv = sys.argv
        sys.argv = ['cli.py', '--help']
        
        try:
            # Run the module as __main__ - this will execute line 298
            runpy.run_module('todo_app.cli', run_name='__main__', alter_sys=True)
        except SystemExit as e:
            # Click exits with code 0 after showing help
            assert e.code == 0
        finally:
            sys.argv = original_argv
