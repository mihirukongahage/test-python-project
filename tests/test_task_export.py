"""
Tests for task_export module.
"""

import pytest
import json
import csv
from pathlib import Path
from datetime import datetime
from export.task_export import (
    export_to_json, export_to_csv, export_to_markdown,
    export_to_html, export_to_text, export_by_format, create_backup
)


@pytest.fixture
def sample_tasks():
    """Create sample tasks for testing."""
    return [
        {
            'id': 1,
            'task': 'Buy groceries',
            'priority': 'high',
            'completed': False,
            'created_at': datetime.now().isoformat()
        },
        {
            'id': 2,
            'task': 'Write report',
            'priority': 'medium',
            'completed': True,
            'created_at': datetime.now().isoformat()
        }
    ]


def test_export_to_json(sample_tasks, tmp_path):
    """Test exporting to JSON."""
    filepath = tmp_path / "tasks.json"
    result = export_to_json(sample_tasks, str(filepath))
    assert result is True
    assert filepath.exists()
    
    with open(filepath, 'r') as f:
        data = json.load(f)
    assert 'tasks' in data
    assert len(data['tasks']) == 2


def test_export_to_json_not_pretty(sample_tasks, tmp_path):
    """Test exporting to JSON without formatting."""
    filepath = tmp_path / "tasks.json"
    result = export_to_json(sample_tasks, str(filepath), pretty=False)
    assert result is True


def test_export_to_json_invalid_path(sample_tasks):
    """Test exporting to invalid path."""
    result = export_to_json(sample_tasks, "/invalid/path/tasks.json")
    assert result is False


def test_export_to_csv(sample_tasks, tmp_path):
    """Test exporting to CSV."""
    filepath = tmp_path / "tasks.csv"
    result = export_to_csv(sample_tasks, str(filepath))
    assert result is True
    assert filepath.exists()
    
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert len(rows) == 2


def test_export_to_csv_empty(tmp_path):
    """Test exporting empty list to CSV."""
    filepath = tmp_path / "tasks.csv"
    result = export_to_csv([], str(filepath))
    assert result is False


def test_export_to_markdown(sample_tasks, tmp_path):
    """Test exporting to Markdown."""
    filepath = tmp_path / "tasks.md"
    result = export_to_markdown(sample_tasks, str(filepath))
    assert result is True
    assert filepath.exists()
    
    with open(filepath, 'r') as f:
        content = f.read()
    assert '# Todo List' in content
    assert 'Buy groceries' in content


def test_export_to_markdown_invalid_date(tmp_path):
    """Test markdown export with invalid date."""
    tasks = [{'id': 1, 'task': 'Test', 'priority': 'high', 'completed': False, 'created_at': 'invalid'}]
    filepath = tmp_path / "tasks.md"
    result = export_to_markdown(tasks, str(filepath))
    assert result is True


def test_export_to_html(sample_tasks, tmp_path):
    """Test exporting to HTML."""
    filepath = tmp_path / "tasks.html"
    result = export_to_html(sample_tasks, str(filepath))
    assert result is True
    assert filepath.exists()
    
    with open(filepath, 'r') as f:
        content = f.read()
    assert '<!DOCTYPE html>' in content
    assert 'Buy groceries' in content


def test_export_to_html_invalid_date(tmp_path):
    """Test HTML export with invalid date."""
    tasks = [{'id': 1, 'task': 'Test', 'priority': 'high', 'completed': False, 'created_at': 'invalid'}]
    filepath = tmp_path / "tasks.html"
    result = export_to_html(tasks, str(filepath))
    assert result is True


def test_export_to_text(sample_tasks, tmp_path):
    """Test exporting to plain text."""
    filepath = tmp_path / "tasks.txt"
    result = export_to_text(sample_tasks, str(filepath))
    assert result is True
    assert filepath.exists()
    
    with open(filepath, 'r') as f:
        content = f.read()
    assert 'TODO LIST EXPORT' in content
    assert 'Buy groceries' in content


def test_export_to_text_invalid_date(tmp_path):
    """Test text export with invalid date."""
    tasks = [{'id': 1, 'task': 'Test', 'priority': 'high', 'completed': False, 'created_at': 'invalid'}]
    filepath = tmp_path / "tasks.txt"
    result = export_to_text(tasks, str(filepath))
    assert result is True


def test_export_by_format_json(sample_tasks, tmp_path):
    """Test export by format with JSON."""
    filepath = tmp_path / "tasks.json"
    result = export_by_format(sample_tasks, str(filepath), format='json')
    assert result is True


def test_export_by_format_auto_detect(sample_tasks, tmp_path):
    """Test export with auto-detection."""
    filepath = tmp_path / "tasks.csv"
    result = export_by_format(sample_tasks, str(filepath))
    assert result is True


def test_export_by_format_markdown(sample_tasks, tmp_path):
    """Test export by format with markdown."""
    filepath = tmp_path / "tasks.md"
    result = export_by_format(sample_tasks, str(filepath), format='markdown')
    assert result is True


def test_export_by_format_html(sample_tasks, tmp_path):
    """Test export by format with HTML."""
    filepath = tmp_path / "tasks.html"
    result = export_by_format(sample_tasks, str(filepath), format='html')
    assert result is True


def test_export_by_format_text(sample_tasks, tmp_path):
    """Test export by format with text."""
    filepath = tmp_path / "tasks.txt"
    result = export_by_format(sample_tasks, str(filepath), format='text')
    assert result is True


def test_export_by_format_invalid(sample_tasks, tmp_path):
    """Test export with invalid format."""
    filepath = tmp_path / "tasks.xyz"
    result = export_by_format(sample_tasks, str(filepath), format='invalid')
    assert result is False


def test_create_backup(sample_tasks, tmp_path):
    """Test creating a backup."""
    backup_path = create_backup(sample_tasks, backup_dir=str(tmp_path))
    assert backup_path is not None
    assert Path(backup_path).exists()


def test_create_backup_default_dir(sample_tasks):
    """Test creating backup with default directory."""
    backup_path = create_backup(sample_tasks)
    if backup_path:  # May succeed or fail depending on permissions
        assert Path(backup_path).exists()
