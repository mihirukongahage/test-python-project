"""
Tests for task_utils module.
"""

import pytest
from datetime import datetime, timedelta
from todo_app.task_utils import (
    validate_task, format_task_description, calculate_task_age,
    get_priority_score, calculate_statistics, reindex_tasks,
    create_task, format_date, is_overdue, get_next_task_id,
    export_tasks_to_dict, import_tasks_from_dict
)


@pytest.fixture
def valid_task():
    """Create a valid task for testing."""
    return {
        'id': 1,
        'task': 'Test task',
        'priority': 'medium',
        'completed': False,
        'created_at': datetime.now().isoformat()
    }


@pytest.fixture
def sample_tasks():
    """Create sample tasks for testing."""
    now = datetime.now()
    return [
        {
            'id': 1,
            'task': 'Task 1',
            'priority': 'high',
            'completed': False,
            'created_at': (now - timedelta(days=10)).isoformat()
        },
        {
            'id': 2,
            'task': 'Task 2',
            'priority': 'medium',
            'completed': True,
            'created_at': (now - timedelta(days=5)).isoformat()
        },
        {
            'id': 3,
            'task': 'Task 3',
            'priority': 'low',
            'completed': False,
            'created_at': (now - timedelta(days=2)).isoformat()
        }
    ]


def test_validate_task_valid(valid_task):
    """Test validating a valid task."""
    is_valid, error = validate_task(valid_task)
    assert is_valid is True
    assert error is None


def test_validate_task_missing_field():
    """Test validating task with missing field."""
    task = {'id': 1, 'task': 'Test'}
    is_valid, error = validate_task(task)
    assert is_valid is False
    assert 'Missing required field' in error


def test_validate_task_invalid_id():
    """Test validating task with invalid ID."""
    task = {
        'id': 'not_an_int',
        'task': 'Test',
        'priority': 'medium',
        'completed': False,
        'created_at': datetime.now().isoformat()
    }
    is_valid, error = validate_task(task)
    assert is_valid is False
    assert 'ID must be an integer' in error


def test_validate_task_empty_description():
    """Test validating task with empty description."""
    task = {
        'id': 1,
        'task': '   ',
        'priority': 'medium',
        'completed': False,
        'created_at': datetime.now().isoformat()
    }
    is_valid, error = validate_task(task)
    assert is_valid is False
    assert 'non-empty string' in error


def test_validate_task_invalid_priority():
    """Test validating task with invalid priority."""
    task = {
        'id': 1,
        'task': 'Test',
        'priority': 'invalid',
        'completed': False,
        'created_at': datetime.now().isoformat()
    }
    is_valid, error = validate_task(task)
    assert is_valid is False
    assert 'Priority must be' in error


def test_validate_task_invalid_completed():
    """Test validating task with invalid completed field."""
    task = {
        'id': 1,
        'task': 'Test',
        'priority': 'medium',
        'completed': 'not_bool',
        'created_at': datetime.now().isoformat()
    }
    is_valid, error = validate_task(task)
    assert is_valid is False
    assert 'Completed must be a boolean' in error


def test_validate_task_invalid_date():
    """Test validating task with invalid date."""
    task = {
        'id': 1,
        'task': 'Test',
        'priority': 'medium',
        'completed': False,
        'created_at': 'invalid_date'
    }
    is_valid, error = validate_task(task)
    assert is_valid is False
    assert 'Invalid created_at' in error


def test_format_task_description_short():
    """Test formatting short task description."""
    result = format_task_description("Short task", max_length=50)
    assert result == "Short task"


def test_format_task_description_long():
    """Test formatting long task description."""
    long_task = "A" * 100
    result = format_task_description(long_task, max_length=50)
    assert len(result) == 50
    assert result.endswith("...")


def test_calculate_task_age(valid_task):
    """Test calculating task age."""
    age = calculate_task_age(valid_task)
    assert age == 0  # Created just now


def test_calculate_task_age_old():
    """Test calculating age of old task."""
    old_date = datetime.now() - timedelta(days=10)
    task = {'created_at': old_date.isoformat()}
    age = calculate_task_age(task)
    assert age == 10


def test_calculate_task_age_invalid():
    """Test calculating age with invalid date."""
    task = {'created_at': 'invalid'}
    age = calculate_task_age(task)
    assert age == -1


def test_get_priority_score():
    """Test getting priority scores."""
    assert get_priority_score('low') == 1
    assert get_priority_score('medium') == 2
    assert get_priority_score('high') == 3
    assert get_priority_score('invalid') == 2  # Default


def test_calculate_statistics_empty():
    """Test calculating statistics for empty list."""
    stats = calculate_statistics([])
    assert stats['total'] == 0
    assert stats['completed'] == 0
    assert stats['pending'] == 0
    assert stats['completion_rate'] == 0.0


def test_calculate_statistics(sample_tasks):
    """Test calculating statistics."""
    stats = calculate_statistics(sample_tasks)
    assert stats['total'] == 3
    assert stats['completed'] == 1
    assert stats['pending'] == 2
    assert stats['completion_rate'] == 33.33
    assert stats['by_priority']['high'] == 1
    assert stats['by_priority']['medium'] == 1
    assert stats['by_priority']['low'] == 1
    assert stats['high_priority_pending'] == 1
    assert stats['oldest_pending_days'] == 10


def test_reindex_tasks(sample_tasks):
    """Test reindexing tasks."""
    tasks = [{'id': 5, 'task': 'A'}, {'id': 10, 'task': 'B'}, {'id': 3, 'task': 'C'}]
    result = reindex_tasks(tasks)
    assert result[0]['id'] == 1
    assert result[1]['id'] == 2
    assert result[2]['id'] == 3


def test_create_task():
    """Test creating a new task."""
    task = create_task('New task', priority='high', task_id=5)
    assert task['id'] == 5
    assert task['task'] == 'New task'
    assert task['priority'] == 'high'
    assert task['completed'] is False
    assert 'created_at' in task


def test_create_task_default_priority():
    """Test creating task with default priority."""
    task = create_task('New task')
    assert task['priority'] == 'medium'


def test_format_date_valid():
    """Test formatting valid date."""
    date_str = datetime(2024, 1, 15, 10, 30).isoformat()
    result = format_date(date_str, '%Y-%m-%d')
    assert result == '2024-01-15'


def test_format_date_invalid():
    """Test formatting invalid date."""
    result = format_date('invalid_date')
    assert result == 'invalid_date'


def test_is_overdue_true():
    """Test checking if task is overdue."""
    old_date = datetime.now() - timedelta(days=10)
    task = {'completed': False, 'created_at': old_date.isoformat()}
    assert is_overdue(task, threshold_days=7) is True


def test_is_overdue_false():
    """Test checking if task is not overdue."""
    recent_date = datetime.now() - timedelta(days=3)
    task = {'completed': False, 'created_at': recent_date.isoformat()}
    assert is_overdue(task, threshold_days=7) is False


def test_is_overdue_completed():
    """Test that completed tasks are never overdue."""
    old_date = datetime.now() - timedelta(days=10)
    task = {'completed': True, 'created_at': old_date.isoformat()}
    assert is_overdue(task, threshold_days=7) is False


def test_is_overdue_invalid_date():
    """Test overdue check with invalid date."""
    task = {'completed': False, 'created_at': 'invalid'}
    assert is_overdue(task) is False


def test_get_next_task_id_empty():
    """Test getting next ID from empty list."""
    assert get_next_task_id([]) == 1


def test_get_next_task_id(sample_tasks):
    """Test getting next task ID."""
    next_id = get_next_task_id(sample_tasks)
    assert next_id == 4


def test_export_tasks_to_dict(sample_tasks):
    """Test exporting tasks."""
    result = export_tasks_to_dict(sample_tasks)
    assert 'export_date' in result
    assert 'version' in result
    assert 'statistics' in result
    assert 'tasks' in result
    assert len(result['tasks']) == 3


def test_import_tasks_from_dict(sample_tasks):
    """Test importing tasks."""
    exported = export_tasks_to_dict(sample_tasks)
    imported = import_tasks_from_dict(exported)
    assert len(imported) == len(sample_tasks)


def test_import_tasks_from_dict_invalid():
    """Test importing from invalid data."""
    result = import_tasks_from_dict({'invalid': 'data'})
    assert result == []


def test_calculate_statistics_with_invalid_dates():
    """Test statistics calculation with invalid dates."""
    tasks = [
        {
            'id': 1,
            'task': 'Task',
            'priority': 'high',
            'completed': False,
            'created_at': 'invalid_date'
        }
    ]
    stats = calculate_statistics(tasks)
    assert stats['total'] == 1
    assert stats['avg_age_days'] == 0
