"""
Tests for task_filters module.
"""

import pytest
from datetime import datetime, timedelta
from todo_app.task_filters import (
    filter_by_priority, filter_by_status, filter_by_date_range,
    search_tasks, get_overdue_tasks, sort_tasks, get_task_by_id,
    combine_filters
)


@pytest.fixture
def sample_tasks():
    """Create sample tasks for testing."""
    now = datetime.now()
    return [
        {
            'id': 1,
            'task': 'Buy groceries',
            'priority': 'high',
            'completed': False,
            'created_at': (now - timedelta(days=10)).isoformat()
        },
        {
            'id': 2,
            'task': 'Write documentation',
            'priority': 'medium',
            'completed': True,
            'created_at': (now - timedelta(days=5)).isoformat()
        },
        {
            'id': 3,
            'task': 'Review code',
            'priority': 'high',
            'completed': False,
            'created_at': (now - timedelta(days=2)).isoformat()
        },
        {
            'id': 4,
            'task': 'Call client',
            'priority': 'low',
            'completed': False,
            'created_at': now.isoformat()
        }
    ]


def test_filter_by_priority_high(sample_tasks):
    """Test filtering by high priority."""
    result = filter_by_priority(sample_tasks, 'high')
    assert len(result) == 2
    assert all(t['priority'] == 'high' for t in result)


def test_filter_by_priority_medium(sample_tasks):
    """Test filtering by medium priority."""
    result = filter_by_priority(sample_tasks, 'medium')
    assert len(result) == 1
    assert result[0]['priority'] == 'medium'


def test_filter_by_priority_low(sample_tasks):
    """Test filtering by low priority."""
    result = filter_by_priority(sample_tasks, 'low')
    assert len(result) == 1
    assert result[0]['priority'] == 'low'


def test_filter_by_status_pending(sample_tasks):
    """Test filtering pending tasks."""
    result = filter_by_status(sample_tasks, completed=False)
    assert len(result) == 3
    assert all(not t['completed'] for t in result)


def test_filter_by_status_completed(sample_tasks):
    """Test filtering completed tasks."""
    result = filter_by_status(sample_tasks, completed=True)
    assert len(result) == 1
    assert result[0]['completed'] is True


def test_filter_by_date_range_with_start(sample_tasks):
    """Test filtering by date range with start date."""
    start_date = datetime.now() - timedelta(days=6)
    result = filter_by_date_range(sample_tasks, start_date=start_date)
    assert len(result) == 3


def test_filter_by_date_range_with_end(sample_tasks):
    """Test filtering by date range with end date."""
    end_date = datetime.now() - timedelta(days=3)
    result = filter_by_date_range(sample_tasks, end_date=end_date)
    assert len(result) == 2


def test_filter_by_date_range_both(sample_tasks):
    """Test filtering by date range with both start and end."""
    start_date = datetime.now() - timedelta(days=6)
    end_date = datetime.now() - timedelta(days=1)
    result = filter_by_date_range(sample_tasks, start_date=start_date, end_date=end_date)
    assert len(result) == 2


def test_filter_by_date_range_invalid_date():
    """Test filtering with invalid date in task."""
    tasks = [{'id': 1, 'task': 'Test', 'created_at': 'invalid-date'}]
    result = filter_by_date_range(tasks)
    assert len(result) == 0


def test_search_tasks_found(sample_tasks):
    """Test searching tasks with matching keyword."""
    result = search_tasks(sample_tasks, 'code')
    assert len(result) == 1
    assert result[0]['task'] == 'Review code'


def test_search_tasks_case_insensitive(sample_tasks):
    """Test case-insensitive search."""
    result = search_tasks(sample_tasks, 'WRITE')
    assert len(result) == 1
    assert result[0]['task'] == 'Write documentation'


def test_search_tasks_not_found(sample_tasks):
    """Test searching with no matches."""
    result = search_tasks(sample_tasks, 'xyz')
    assert len(result) == 0


def test_search_tasks_empty_keyword(sample_tasks):
    """Test searching with empty keyword."""
    result = search_tasks(sample_tasks, '')
    assert len(result) == len(sample_tasks)


def test_get_overdue_tasks(sample_tasks):
    """Test getting overdue tasks."""
    result = get_overdue_tasks(sample_tasks, days=7)
    assert len(result) == 1
    assert result[0]['id'] == 1


def test_get_overdue_tasks_custom_threshold(sample_tasks):
    """Test getting overdue tasks with custom threshold."""
    result = get_overdue_tasks(sample_tasks, days=3)
    assert len(result) == 1


def test_get_overdue_tasks_invalid_date():
    """Test overdue tasks with invalid dates."""
    tasks = [{'id': 1, 'task': 'Test', 'completed': False, 'created_at': 'invalid'}]
    result = get_overdue_tasks(tasks)
    assert len(result) == 0


def test_sort_tasks_by_id(sample_tasks):
    """Test sorting by ID."""
    shuffled = [sample_tasks[2], sample_tasks[0], sample_tasks[3], sample_tasks[1]]
    result = sort_tasks(shuffled, by='id')
    assert [t['id'] for t in result] == [1, 2, 3, 4]


def test_sort_tasks_by_priority(sample_tasks):
    """Test sorting by priority."""
    result = sort_tasks(sample_tasks, by='priority', reverse=True)
    priorities = [t['priority'] for t in result]
    assert priorities[0] in ['high', 'high']
    assert priorities[-1] == 'low'


def test_sort_tasks_by_created_at(sample_tasks):
    """Test sorting by creation date."""
    result = sort_tasks(sample_tasks, by='created_at')
    # Oldest first
    assert result[0]['id'] == 1
    assert result[-1]['id'] == 4


def test_sort_tasks_by_task_name(sample_tasks):
    """Test sorting by task name."""
    result = sort_tasks(sample_tasks, by='task')
    assert result[0]['task'] == 'Buy groceries'


def test_get_task_by_id_found(sample_tasks):
    """Test getting task by ID."""
    result = get_task_by_id(sample_tasks, 2)
    assert result is not None
    assert result['id'] == 2
    assert result['task'] == 'Write documentation'


def test_get_task_by_id_not_found(sample_tasks):
    """Test getting non-existent task."""
    result = get_task_by_id(sample_tasks, 999)
    assert result is None


def test_combine_filters_all(sample_tasks):
    """Test combining all filters."""
    result = combine_filters(sample_tasks, priority='high', completed=False, keyword='groceries')
    assert len(result) == 1
    assert result[0]['id'] == 1


def test_combine_filters_priority_only(sample_tasks):
    """Test combining with priority filter only."""
    result = combine_filters(sample_tasks, priority='high')
    assert len(result) == 2


def test_combine_filters_none(sample_tasks):
    """Test combining with no filters."""
    result = combine_filters(sample_tasks)
    assert len(result) == len(sample_tasks)
