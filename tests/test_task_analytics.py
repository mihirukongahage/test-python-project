"""
Tests for task_analytics module.
"""

import pytest
from datetime import datetime, timedelta
from todo_app.task_analytics import (
    calculate_completion_trend, get_productivity_score, analyze_task_distribution,
    get_time_to_complete, identify_bottlenecks, calculate_urgency_score,
    get_priority_transition_matrix, calculate_velocity, generate_insights,
    get_weekly_summary
)


@pytest.fixture
def sample_tasks():
    """Create sample tasks for testing."""
    now = datetime.now()
    return [
        {
            'id': 1,
            'task': 'Task 1',
            'priority': 'high',
            'completed': True,
            'created_at': (now - timedelta(days=10)).isoformat()
        },
        {
            'id': 2,
            'task': 'Task 2',
            'priority': 'medium',
            'completed': False,
            'created_at': (now - timedelta(days=5)).isoformat()
        },
        {
            'id': 3,
            'task': 'Task 3',
            'priority': 'low',
            'completed': True,
            'created_at': (now - timedelta(days=2)).isoformat()
        },
        {
            'id': 4,
            'task': 'Task 4',
            'priority': 'high',
            'completed': False,
            'created_at': (now - timedelta(days=15)).isoformat()
        }
    ]


def test_calculate_completion_trend(sample_tasks):
    """Test calculating completion trend."""
    result = calculate_completion_trend(sample_tasks, days=14)
    assert isinstance(result, dict)


def test_calculate_completion_trend_invalid_date():
    """Test completion trend with invalid dates."""
    tasks = [{'id': 1, 'completed': True, 'created_at': 'invalid'}]
    result = calculate_completion_trend(tasks)
    assert result == {}


def test_get_productivity_score_empty():
    """Test productivity score with empty list."""
    result = get_productivity_score([])
    assert result == 0.0


def test_get_productivity_score(sample_tasks):
    """Test calculating productivity score."""
    score = get_productivity_score(sample_tasks)
    assert isinstance(score, float)
    assert 0 <= score <= 100


def test_analyze_task_distribution(sample_tasks):
    """Test analyzing task distribution."""
    result = analyze_task_distribution(sample_tasks)
    assert 'by_priority' in result
    assert 'by_status' in result
    assert 'by_priority_status' in result
    assert result['by_priority']['high'] == 2
    assert result['by_status']['completed'] == 2


def test_analyze_task_distribution_empty():
    """Test distribution with empty list."""
    result = analyze_task_distribution([])
    assert result['by_priority']['low'] == 0


def test_get_time_to_complete(sample_tasks):
    """Test calculating time to complete."""
    result = get_time_to_complete(sample_tasks)
    assert 'overall' in result
    assert 'high' in result
    assert isinstance(result['overall'], float)


def test_get_time_to_complete_no_completed():
    """Test time to complete with no completed tasks."""
    tasks = [{'id': 1, 'completed': False, 'created_at': datetime.now().isoformat()}]
    result = get_time_to_complete(tasks)
    assert result['overall'] == 0.0


def test_identify_bottlenecks(sample_tasks):
    """Test identifying bottleneck tasks."""
    result = identify_bottlenecks(sample_tasks, threshold_days=10)
    assert isinstance(result, list)
    assert len(result) >= 1  # At least one old pending task


def test_identify_bottlenecks_no_old_tasks():
    """Test bottlenecks with no old tasks."""
    now = datetime.now()
    tasks = [{
        'id': 1,
        'task': 'New task',
        'completed': False,
        'created_at': now.isoformat()
    }]
    result = identify_bottlenecks(tasks, threshold_days=7)
    assert result == []


def test_calculate_urgency_score():
    """Test calculating urgency score."""
    task = {'priority': 'high'}
    score = calculate_urgency_score(task, age_days=10)
    assert isinstance(score, float)
    assert score > 0


def test_calculate_urgency_score_low_priority():
    """Test urgency score with low priority."""
    task = {'priority': 'low'}
    score = calculate_urgency_score(task, age_days=5)
    assert score < calculate_urgency_score({'priority': 'high'}, age_days=5)


def test_get_priority_transition_matrix_empty():
    """Test priority matrix with empty list."""
    result = get_priority_transition_matrix([])
    assert result['low']['count'] == 0
    assert result['low']['percentage'] == 0


def test_get_priority_transition_matrix(sample_tasks):
    """Test getting priority transition matrix."""
    result = get_priority_transition_matrix(sample_tasks)
    assert 'low' in result
    assert 'count' in result['low']
    assert 'percentage' in result['low']
    assert result['high']['count'] == 2


def test_calculate_velocity(sample_tasks):
    """Test calculating task velocity."""
    result = calculate_velocity(sample_tasks, period_days=30)
    assert 'tasks_completed' in result
    assert 'tasks_created' in result
    assert 'completion_velocity' in result
    assert isinstance(result['completion_velocity'], float)


def test_calculate_velocity_zero_period():
    """Test velocity with zero period."""
    result = calculate_velocity([], period_days=0)
    assert result['completion_velocity'] == 0


def test_generate_insights_empty():
    """Test generating insights with empty list."""
    result = generate_insights([])
    assert isinstance(result, list)
    assert len(result) > 0


def test_generate_insights(sample_tasks):
    """Test generating insights."""
    result = generate_insights(sample_tasks)
    assert isinstance(result, list)
    assert len(result) > 0
    assert all(isinstance(insight, str) for insight in result)


def test_get_weekly_summary(sample_tasks):
    """Test getting weekly summary."""
    result = get_weekly_summary(sample_tasks)
    assert 'period' in result
    assert 'velocity' in result
    assert 'productivity_score' in result
    assert 'insights' in result
    assert result['period'] == 'Last 7 days'


def test_get_weekly_summary_empty():
    """Test weekly summary with empty list."""
    result = get_weekly_summary([])
    assert 'insights' in result
    assert len(result['insights']) > 0


# Additional tests to improve coverage for lines 67, 145-146, 186-187, 272-273, 311, 313, 317, 328, 331

def test_get_time_to_complete_invalid_date():
    """Test time to complete with invalid date format (covers lines 145-146)."""
    tasks = [
        {'id': 1, 'completed': True, 'created_at': 'invalid-date'},
        {'id': 2, 'completed': True, 'created_at': None},
        {'id': 3, 'completed': True, 'created_at': 12345},  # Not a string
    ]
    result = get_time_to_complete(tasks)
    assert result['overall'] == 0.0


def test_identify_bottlenecks_invalid_date():
    """Test identify bottlenecks with invalid date format (covers lines 186-187)."""
    tasks = [
        {'id': 1, 'completed': False, 'created_at': 'not-a-date'},
        {'id': 2, 'completed': False, 'created_at': None},
        {'id': 3, 'completed': False},  # Missing created_at
    ]
    result = identify_bottlenecks(tasks, threshold_days=1)
    assert result == []


def test_calculate_velocity_invalid_date():
    """Test calculate velocity with invalid date format (covers lines 272-273)."""
    tasks = [
        {'id': 1, 'completed': True, 'created_at': 'bad-date'},
        {'id': 2, 'completed': False, 'created_at': None},
    ]
    result = calculate_velocity(tasks, period_days=7)
    assert result['tasks_completed'] == 0
    assert result['tasks_created'] == 0


def test_generate_insights_low_productivity():
    """Test generate insights with low productivity score (covers line 311)."""
    now = datetime.now()
    # Create tasks where very few are completed (productivity < 30%)
    tasks = [
        {'id': 1, 'priority': 'high', 'completed': False, 'created_at': (now - timedelta(days=1)).isoformat()},
        {'id': 2, 'priority': 'high', 'completed': False, 'created_at': (now - timedelta(days=1)).isoformat()},
        {'id': 3, 'priority': 'high', 'completed': False, 'created_at': (now - timedelta(days=1)).isoformat()},
        {'id': 4, 'priority': 'medium', 'completed': False, 'created_at': (now - timedelta(days=1)).isoformat()},
        {'id': 5, 'priority': 'low', 'completed': True, 'created_at': (now - timedelta(days=1)).isoformat()},
    ]
    result = generate_insights(tasks)
    assert any('Low productivity' in insight for insight in result)


def test_generate_insights_high_productivity():
    """Test generate insights with high productivity score (covers line 313)."""
    now = datetime.now()
    # Create tasks where most are completed (productivity > 80%)
    tasks = [
        {'id': 1, 'priority': 'high', 'completed': True, 'created_at': (now - timedelta(days=1)).isoformat()},
        {'id': 2, 'priority': 'high', 'completed': True, 'created_at': (now - timedelta(days=1)).isoformat()},
        {'id': 3, 'priority': 'medium', 'completed': True, 'created_at': (now - timedelta(days=1)).isoformat()},
        {'id': 4, 'priority': 'low', 'completed': True, 'created_at': (now - timedelta(days=1)).isoformat()},
    ]
    result = generate_insights(tasks)
    assert any('Excellent productivity' in insight for insight in result)


def test_generate_insights_many_high_priority_pending():
    """Test generate insights with many high-priority pending tasks (covers line 317)."""
    now = datetime.now()
    # Create more than 3 high-priority pending tasks
    tasks = [
        {'id': 1, 'priority': 'high', 'completed': False, 'created_at': (now - timedelta(days=1)).isoformat()},
        {'id': 2, 'priority': 'high', 'completed': False, 'created_at': (now - timedelta(days=1)).isoformat()},
        {'id': 3, 'priority': 'high', 'completed': False, 'created_at': (now - timedelta(days=1)).isoformat()},
        {'id': 4, 'priority': 'high', 'completed': False, 'created_at': (now - timedelta(days=1)).isoformat()},
        {'id': 5, 'priority': 'medium', 'completed': True, 'created_at': (now - timedelta(days=1)).isoformat()},
    ]
    result = generate_insights(tasks)
    assert any('high-priority pending tasks' in insight for insight in result)


def test_generate_insights_large_backlog():
    """Test generate insights with large backlog (covers line 328)."""
    now = datetime.now()
    # Create scenario where pending > completed * 2
    tasks = [
        {'id': 1, 'priority': 'medium', 'completed': True, 'created_at': (now - timedelta(days=1)).isoformat()},
        {'id': 2, 'priority': 'medium', 'completed': False, 'created_at': (now - timedelta(days=1)).isoformat()},
        {'id': 3, 'priority': 'medium', 'completed': False, 'created_at': (now - timedelta(days=1)).isoformat()},
        {'id': 4, 'priority': 'medium', 'completed': False, 'created_at': (now - timedelta(days=1)).isoformat()},
        {'id': 5, 'priority': 'medium', 'completed': False, 'created_at': (now - timedelta(days=1)).isoformat()},
    ]
    result = generate_insights(tasks)
    assert any('Large backlog' in insight for insight in result)


def test_generate_insights_everything_good():
    """Test generate insights when everything looks good (covers line 331)."""
    now = datetime.now()
    # Create a balanced scenario:
    # - productivity between 30-80% (not low, not high)
    # - no high-priority pending tasks (high_pending <= 3)
    # - no bottlenecks (tasks not older than 14 days)
    # - net_velocity >= 0 (completed >= created in period)
    # - no large backlog (pending <= completed * 2)
    # 
    # To achieve net_velocity >= 0, all tasks created in period must be completed
    # To achieve productivity between 30-80%, we need some pending tasks (but created outside period)
    tasks = [
        # Tasks created in period (last 7 days) - all completed
        {'id': 1, 'priority': 'medium', 'completed': True, 'created_at': (now - timedelta(days=1)).isoformat()},
        {'id': 2, 'priority': 'medium', 'completed': True, 'created_at': (now - timedelta(days=1)).isoformat()},
        # Tasks created outside period (older than 7 days) - some pending
        {'id': 3, 'priority': 'low', 'completed': False, 'created_at': (now - timedelta(days=10)).isoformat()},
    ]
    # productivity = (2*2) / (2*2 + 1*1) * 100 = 4/5 * 100 = 80% - exactly 80, not > 80
    # high_pending = 0
    # bottlenecks = 0 (task 3 is 10 days old, threshold is 14)
    # net_velocity = 2/7 - 2/7 = 0 (only 2 tasks created in period, both completed)
    # pending = 1, completed = 2, so pending (1) <= completed * 2 (4) - no backlog
    result = generate_insights(tasks)
    assert any('Everything looks good' in insight for insight in result)


def test_get_productivity_score_zero_max_score():
    """Test productivity score edge case (attempts to cover line 67)."""
    # This tests the edge case where max_possible_score could be 0
    # In practice, this is unreachable because weight defaults to 2
    # But we test with an empty-like scenario
    result = get_productivity_score([])
    assert result == 0.0
