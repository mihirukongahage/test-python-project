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
