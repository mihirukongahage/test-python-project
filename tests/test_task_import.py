"""
Tests for task_import module.
"""

import pytest
import json
import csv
from pathlib import Path
from datetime import datetime
from imports.task_import import (
    import_from_json, import_from_csv, import_from_text,
    import_from_markdown, import_by_format, merge_tasks,
    validate_imported_tasks, restore_from_backup
)


@pytest.fixture
def sample_json_file(tmp_path):
    """Create a sample JSON file."""
    filepath = tmp_path / "tasks.json"
    data = {
        'tasks': [
            {'id': 1, 'task': 'Task 1', 'priority': 'high', 'completed': False, 'created_at': datetime.now().isoformat()},
            {'id': 2, 'task': 'Task 2', 'priority': 'medium', 'completed': True, 'created_at': datetime.now().isoformat()}
        ]
    }
    with open(filepath, 'w') as f:
        json.dump(data, f)
    return filepath


@pytest.fixture
def sample_csv_file(tmp_path):
    """Create a sample CSV file."""
    filepath = tmp_path / "tasks.csv"
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'task', 'priority', 'completed', 'created_at'])
        writer.writerow(['1', 'Task 1', 'high', 'True', datetime.now().isoformat()])
        writer.writerow(['2', 'Task 2', 'medium', 'False', datetime.now().isoformat()])
    return filepath


@pytest.fixture
def sample_text_file(tmp_path):
    """Create a sample text file."""
    filepath = tmp_path / "tasks.txt"
    with open(filepath, 'w') as f:
        f.write("# My Tasks\n")
        f.write("[HIGH] Buy groceries\n")
        f.write("x [MEDIUM] Write report\n")
        f.write("Call mom\n")
    return filepath


@pytest.fixture
def sample_markdown_file(tmp_path):
    """Create a sample Markdown file."""
    filepath = tmp_path / "tasks.md"
    with open(filepath, 'w') as f:
        f.write("# Todo List\n\n")
        f.write("## High Priority\n\n")
        f.write("- [ ] Buy groceries\n")
        f.write("- [x] Write report\n")
        f.write("\n## Low Priority\n\n")
        f.write("- [ ] Call mom\n")
    return filepath


def test_import_from_json_with_tasks_key(sample_json_file):
    """Test importing from JSON with 'tasks' key."""
    result = import_from_json(str(sample_json_file))
    assert result is not None
    assert len(result) == 2
    assert result[0]['task'] == 'Task 1'


def test_import_from_json_list(tmp_path):
    """Test importing from JSON that is a list."""
    filepath = tmp_path / "tasks.json"
    data = [
        {'id': 1, 'task': 'Task 1', 'priority': 'high', 'completed': False, 'created_at': datetime.now().isoformat()}
    ]
    with open(filepath, 'w') as f:
        json.dump(data, f)
    
    result = import_from_json(str(filepath))
    assert result is not None
    assert len(result) == 1


def test_import_from_json_invalid_file():
    """Test importing from non-existent file."""
    result = import_from_json("/invalid/path/tasks.json")
    assert result is None


def test_import_from_json_invalid_json(tmp_path):
    """Test importing from invalid JSON."""
    filepath = tmp_path / "invalid.json"
    with open(filepath, 'w') as f:
        f.write("invalid json {")
    
    result = import_from_json(str(filepath))
    assert result is None


def test_import_from_csv(sample_csv_file):
    """Test importing from CSV."""
    result = import_from_csv(str(sample_csv_file))
    assert result is not None
    assert len(result) == 2
    assert result[0]['task'] == 'Task 1'
    assert result[0]['completed'] is True


def test_import_from_csv_invalid_file():
    """Test importing from non-existent CSV."""
    result = import_from_csv("/invalid/path/tasks.csv")
    assert result is None


def test_import_from_text(sample_text_file):
    """Test importing from text file."""
    result = import_from_text(str(sample_text_file))
    assert result is not None
    assert len(result) >= 2  # Should have at least 2 tasks (ignoring comment)
    

def test_import_from_text_completed_tasks(sample_text_file):
    """Test importing completed tasks from text."""
    result = import_from_text(str(sample_text_file))
    completed_tasks = [t for t in result if t['completed']]
    assert len(completed_tasks) >= 1


def test_import_from_text_invalid_file():
    """Test importing from non-existent text file."""
    result = import_from_text("/invalid/path/tasks.txt")
    assert result is None


def test_import_from_markdown(sample_markdown_file):
    """Test importing from Markdown."""
    result = import_from_markdown(str(sample_markdown_file))
    assert result is not None
    assert len(result) == 3
    # Check priorities are assigned based on headers
    high_priority_tasks = [t for t in result if t['priority'] == 'high']
    assert len(high_priority_tasks) >= 1


def test_import_from_markdown_invalid_file():
    """Test importing from non-existent Markdown."""
    result = import_from_markdown("/invalid/path/tasks.md")
    assert result is None


def test_import_by_format_json(sample_json_file):
    """Test import by format with JSON."""
    result = import_by_format(str(sample_json_file), format='json')
    assert result is not None


def test_import_by_format_csv(sample_csv_file):
    """Test import by format with CSV."""
    result = import_by_format(str(sample_csv_file), format='csv')
    assert result is not None


def test_import_by_format_auto_detect(sample_json_file):
    """Test import with auto-detection."""
    result = import_by_format(str(sample_json_file))
    assert result is not None


def test_import_by_format_invalid():
    """Test import with invalid format."""
    result = import_by_format("/some/file.xyz", format='invalid')
    assert result is None


def test_merge_tasks_append():
    """Test merging tasks with append strategy."""
    existing = [{'id': 1, 'task': 'Task 1'}]
    imported = [{'id': 2, 'task': 'Task 2'}]
    result = merge_tasks(existing, imported, strategy='append')
    assert len(result) == 2


def test_merge_tasks_replace():
    """Test merging tasks with replace strategy."""
    existing = [{'id': 1, 'task': 'Task 1'}]
    imported = [{'id': 2, 'task': 'Task 2'}]
    result = merge_tasks(existing, imported, strategy='replace')
    assert len(result) == 1
    assert result[0]['id'] == 2


def test_merge_tasks_skip_duplicates():
    """Test merging tasks with skip duplicates strategy."""
    existing = [{'id': 1, 'task': 'Task 1'}]
    imported = [{'id': 2, 'task': 'Task 1'}, {'id': 3, 'task': 'Task 2'}]
    result = merge_tasks(existing, imported, strategy='skip_duplicates')
    assert len(result) == 2  # Original + only new task


def test_validate_imported_tasks_valid():
    """Test validating valid tasks."""
    tasks = [
        {'id': 1, 'task': 'Task 1', 'priority': 'high', 'completed': False, 'created_at': datetime.now().isoformat()}
    ]
    valid, errors = validate_imported_tasks(tasks)
    assert len(valid) == 1
    assert len(errors) == 0


def test_validate_imported_tasks_missing_task():
    """Test validating tasks with missing task field."""
    tasks = [{'id': 1, 'priority': 'high'}]
    valid, errors = validate_imported_tasks(tasks)
    assert len(valid) == 0
    assert len(errors) == 1


def test_validate_imported_tasks_invalid_priority():
    """Test validating tasks with invalid priority."""
    tasks = [{'id': 1, 'task': 'Task 1', 'priority': 'invalid'}]
    valid, errors = validate_imported_tasks(tasks)
    assert len(valid) == 1
    assert valid[0]['priority'] == 'medium'
    assert len(errors) == 1


def test_validate_imported_tasks_invalid_date():
    """Test validating tasks with invalid date."""
    tasks = [{'id': 1, 'task': 'Task 1', 'created_at': 'invalid_date'}]
    valid, errors = validate_imported_tasks(tasks)
    assert len(valid) == 1
    assert len(errors) == 1


def test_validate_imported_tasks_not_dict():
    """Test validating non-dictionary items."""
    tasks = ['not a dict', {'id': 1, 'task': 'Valid'}]
    valid, errors = validate_imported_tasks(tasks)
    assert len(valid) == 1
    assert len(errors) == 1


def test_restore_from_backup(sample_json_file):
    """Test restoring from backup."""
    result = restore_from_backup(str(sample_json_file))
    assert result is not None
    assert len(result) == 2
