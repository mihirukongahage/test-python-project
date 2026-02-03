"""
Task analytics module.
Provides advanced analytics and insights for task management.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from collections import defaultdict


def calculate_completion_trend(tasks: List[Dict], days: int = 7) -> Dict[str, int]:
    """
    Calculate completion trend over the last N days.
    
    Args:
        tasks: List of task dictionaries
        days: Number of days to analyze (default: 7)
    
    Returns:
        Dictionary with dates and completion counts
    """
    trend = defaultdict(int)
    cutoff_date = datetime.now() - timedelta(days=days)
    
    for task in tasks:
        if not task.get('completed', False):
            continue
        
        try:
            created_at = datetime.fromisoformat(task.get('created_at', ''))
            if created_at >= cutoff_date:
                date_key = created_at.strftime('%Y-%m-%d')
                trend[date_key] += 1
        except (ValueError, TypeError):
            continue
    
    return dict(trend)


def get_productivity_score(tasks: List[Dict]) -> float:
    """
    Calculate a productivity score based on task completion and priorities.
    
    Args:
        tasks: List of task dictionaries
    
    Returns:
        Productivity score (0-100)
    """
    if not tasks:
        return 0.0
    
    total_score = 0
    max_possible_score = 0
    
    priority_weights = {'low': 1, 'medium': 2, 'high': 3}
    
    for task in tasks:
        priority = task.get('priority', 'medium')
        weight = priority_weights.get(priority, 2)
        max_possible_score += weight
        
        if task.get('completed', False):
            total_score += weight
    
    if max_possible_score == 0:
        return 0.0
    
    return round((total_score / max_possible_score) * 100, 2)


def analyze_task_distribution(tasks: List[Dict]) -> Dict[str, Dict[str, int]]:
    """
    Analyze the distribution of tasks by priority and status.
    
    Args:
        tasks: List of task dictionaries
    
    Returns:
        Dictionary with distribution statistics
    """
    distribution = {
        'by_priority': {'low': 0, 'medium': 0, 'high': 0},
        'by_status': {'pending': 0, 'completed': 0},
        'by_priority_status': {
            'high_pending': 0,
            'high_completed': 0,
            'medium_pending': 0,
            'medium_completed': 0,
            'low_pending': 0,
            'low_completed': 0
        }
    }
    
    for task in tasks:
        priority = task.get('priority', 'medium')
        completed = task.get('completed', False)
        
        # Count by priority
        if priority in distribution['by_priority']:
            distribution['by_priority'][priority] += 1
        
        # Count by status
        status = 'completed' if completed else 'pending'
        distribution['by_status'][status] += 1
        
        # Count by combined priority and status
        key = f"{priority}_{'completed' if completed else 'pending'}"
        if key in distribution['by_priority_status']:
            distribution['by_priority_status'][key] += 1
    
    return distribution


def get_time_to_complete(tasks: List[Dict]) -> Dict[str, float]:
    """
    Calculate average time to complete tasks by priority.
    
    Args:
        tasks: List of task dictionaries
    
    Returns:
        Dictionary with average days to complete by priority
    """
    completion_times = {
        'low': [],
        'medium': [],
        'high': [],
        'overall': []
    }
    
    for task in tasks:
        if not task.get('completed', False):
            continue
        
        try:
            created_at = datetime.fromisoformat(task.get('created_at', ''))
            # Assume completion time is now for simplicity
            completion_time = datetime.now()
            days_to_complete = (completion_time - created_at).days
            
            priority = task.get('priority', 'medium')
            completion_times[priority].append(days_to_complete)
            completion_times['overall'].append(days_to_complete)
        except (ValueError, TypeError):
            continue
    
    # Calculate averages
    averages = {}
    for priority, times in completion_times.items():
        if times:
            averages[priority] = round(sum(times) / len(times), 2)
        else:
            averages[priority] = 0.0
    
    return averages


def identify_bottlenecks(tasks: List[Dict], threshold_days: int = 14) -> List[Dict]:
    """
    Identify tasks that might be bottlenecks (old pending tasks).
    
    Args:
        tasks: List of task dictionaries
        threshold_days: Days threshold for considering a task a bottleneck
    
    Returns:
        List of bottleneck tasks with additional metadata
    """
    bottlenecks = []
    cutoff_date = datetime.now() - timedelta(days=threshold_days)
    
    for task in tasks:
        if task.get('completed', False):
            continue
        
        try:
            created_at = datetime.fromisoformat(task.get('created_at', ''))
            if created_at < cutoff_date:
                age = (datetime.now() - created_at).days
                bottlenecks.append({
                    'task': task,
                    'age_days': age,
                    'urgency_score': calculate_urgency_score(task, age)
                })
        except (ValueError, TypeError):
            continue
    
    # Sort by urgency score
    bottlenecks.sort(key=lambda x: x['urgency_score'], reverse=True)
    return bottlenecks


def calculate_urgency_score(task: Dict, age_days: int) -> float:
    """
    Calculate urgency score for a task.
    
    Args:
        task: Task dictionary
        age_days: Age of the task in days
    
    Returns:
        Urgency score
    """
    priority_scores = {'low': 1, 'medium': 2, 'high': 3}
    priority = task.get('priority', 'medium')
    priority_score = priority_scores.get(priority, 2)
    
    # Combine priority and age
    urgency = (priority_score * 10) + (age_days * 0.5)
    return round(urgency, 2)


def get_priority_transition_matrix(tasks: List[Dict]) -> Dict[str, int]:
    """
    Analyze how tasks are distributed across priorities.
    
    Args:
        tasks: List of task dictionaries
    
    Returns:
        Dictionary with priority counts and percentages
    """
    if not tasks:
        return {
            'low': {'count': 0, 'percentage': 0},
            'medium': {'count': 0, 'percentage': 0},
            'high': {'count': 0, 'percentage': 0}
        }
    
    counts = {'low': 0, 'medium': 0, 'high': 0}
    
    for task in tasks:
        priority = task.get('priority', 'medium')
        if priority in counts:
            counts[priority] += 1
    
    total = len(tasks)
    result = {}
    for priority, count in counts.items():
        result[priority] = {
            'count': count,
            'percentage': round((count / total) * 100, 2) if total > 0 else 0
        }
    
    return result


def calculate_velocity(tasks: List[Dict], period_days: int = 7) -> Dict[str, float]:
    """
    Calculate task completion velocity (tasks per day).
    
    Args:
        tasks: List of task dictionaries
        period_days: Period to analyze (default: 7 days)
    
    Returns:
        Dictionary with velocity metrics
    """
    cutoff_date = datetime.now() - timedelta(days=period_days)
    completed_in_period = 0
    created_in_period = 0
    
    for task in tasks:
        try:
            created_at = datetime.fromisoformat(task.get('created_at', ''))
            
            if created_at >= cutoff_date:
                created_in_period += 1
                if task.get('completed', False):
                    completed_in_period += 1
        except (ValueError, TypeError):
            continue
    
    velocity = completed_in_period / period_days if period_days > 0 else 0
    creation_rate = created_in_period / period_days if period_days > 0 else 0
    
    return {
        'tasks_completed': completed_in_period,
        'tasks_created': created_in_period,
        'completion_velocity': round(velocity, 2),
        'creation_rate': round(creation_rate, 2),
        'net_velocity': round(velocity - creation_rate, 2)
    }


def generate_insights(tasks: List[Dict]) -> List[str]:
    """
    Generate actionable insights based on task analysis.
    
    Args:
        tasks: List of task dictionaries
    
    Returns:
        List of insight strings
    """
    insights = []
    
    if not tasks:
        insights.append("No tasks found. Start by adding some tasks!")
        return insights
    
    # Calculate various metrics
    distribution = analyze_task_distribution(tasks)
    productivity = get_productivity_score(tasks)
    bottlenecks = identify_bottlenecks(tasks)
    velocity = calculate_velocity(tasks)
    
    # Generate insights
    if productivity < 30:
        insights.append(f"⚠️ Low productivity score ({productivity}%). Focus on completing high-priority tasks.")
    elif productivity > 80:
        insights.append(f"🎉 Excellent productivity score ({productivity}%)! Keep up the great work!")
    
    high_pending = distribution['by_priority_status']['high_pending']
    if high_pending > 3:
        insights.append(f"🔴 You have {high_pending} high-priority pending tasks. Consider tackling these first.")
    
    if bottlenecks:
        insights.append(f"⏰ Found {len(bottlenecks)} potential bottlenecks. Oldest task is {bottlenecks[0]['age_days']} days old.")
    
    if velocity['net_velocity'] < 0:
        insights.append(f"📈 You're creating tasks faster than completing them (net: {velocity['net_velocity']} tasks/day).")
    
    pending_count = distribution['by_status']['pending']
    completed_count = distribution['by_status']['completed']
    if pending_count > completed_count * 2:
        insights.append(f"📋 Large backlog: {pending_count} pending vs {completed_count} completed tasks.")
    
    if not insights:
        insights.append("✅ Everything looks good! Keep maintaining your tasks.")
    
    return insights


def get_weekly_summary(tasks: List[Dict]) -> Dict:
    """
    Generate a comprehensive weekly summary.
    
    Args:
        tasks: List of task dictionaries
    
    Returns:
        Dictionary with weekly summary metrics
    """
    velocity = calculate_velocity(tasks, period_days=7)
    trend = calculate_completion_trend(tasks, days=7)
    productivity = get_productivity_score(tasks)
    distribution = analyze_task_distribution(tasks)
    insights = generate_insights(tasks)
    
    return {
        'period': 'Last 7 days',
        'velocity': velocity,
        'completion_trend': trend,
        'productivity_score': productivity,
        'distribution': distribution,
        'insights': insights,
        'generated_at': datetime.now().isoformat()
    }
