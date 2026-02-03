"""
Task filtering and searching module.
Provides functions to filter and search tasks based on various criteria.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional


def filter_by_priority(tasks: List[Dict], priority: str) -> List[Dict]:
    """
    Filter tasks by priority level.
    
    Args:
        tasks: List of task dictionaries
        priority: Priority level ('low', 'medium', or 'high')
    
    Returns:
        List of tasks matching the priority
    """
    return [task for task in tasks if task.get('priority') == priority]


def filter_by_status(tasks: List[Dict], completed: bool) -> List[Dict]:
    """
    Filter tasks by completion status.
    
    Args:
        tasks: List of task dictionaries
        completed: True for completed tasks, False for pending tasks
    
    Returns:
        List of tasks matching the status
    """
    return [task for task in tasks if task.get('completed') == completed]


def filter_by_date_range(tasks: List[Dict], start_date: Optional[datetime] = None, 
                        end_date: Optional[datetime] = None) -> List[Dict]:
    """
    Filter tasks by creation date range.
    
    Args:
        tasks: List of task dictionaries
        start_date: Start date (inclusive), None for no start limit
        end_date: End date (inclusive), None for no end limit
    
    Returns:
        List of tasks within the date range
    """
    filtered = []
    for task in tasks:
        try:
            created_at = datetime.fromisoformat(task.get('created_at', ''))
            
            if start_date and created_at < start_date:
                continue
            if end_date and created_at > end_date:
                continue
            
            filtered.append(task)
        except (ValueError, TypeError):
            # Skip tasks with invalid dates
            continue
    
    return filtered


def search_tasks(tasks: List[Dict], keyword: str) -> List[Dict]:
    """
    Search tasks by keyword in task description.
    
    Args:
        tasks: List of task dictionaries
        keyword: Search keyword (case-insensitive)
    
    Returns:
        List of tasks containing the keyword
    """
    if not keyword:
        return tasks
    
    keyword_lower = keyword.lower()
    return [task for task in tasks if keyword_lower in task.get('task', '').lower()]


def get_overdue_tasks(tasks: List[Dict], days: int = 7) -> List[Dict]:
    """
    Get tasks that are pending and older than specified days.
    
    Args:
        tasks: List of task dictionaries
        days: Number of days threshold (default: 7)
    
    Returns:
        List of overdue pending tasks
    """
    cutoff_date = datetime.now() - timedelta(days=days)
    pending_tasks = filter_by_status(tasks, completed=False)
    
    overdue = []
    for task in pending_tasks:
        try:
            created_at = datetime.fromisoformat(task.get('created_at', ''))
            if created_at < cutoff_date:
                overdue.append(task)
        except (ValueError, TypeError):
            continue
    
    return overdue


def sort_tasks(tasks: List[Dict], by: str = 'id', reverse: bool = False) -> List[Dict]:
    """
    Sort tasks by specified field.
    
    Args:
        tasks: List of task dictionaries
        by: Field to sort by ('id', 'priority', 'created_at', 'task')
        reverse: Sort in descending order if True
    
    Returns:
        Sorted list of tasks
    """
    priority_order = {'high': 3, 'medium': 2, 'low': 1}
    
    if by == 'priority':
        return sorted(tasks, key=lambda x: priority_order.get(x.get('priority', 'medium'), 2), 
                     reverse=reverse)
    elif by == 'created_at':
        return sorted(tasks, key=lambda x: x.get('created_at', ''), reverse=reverse)
    elif by == 'task':
        return sorted(tasks, key=lambda x: x.get('task', '').lower(), reverse=reverse)
    else:  # default to id
        return sorted(tasks, key=lambda x: x.get('id', 0), reverse=reverse)


def get_task_by_id(tasks: List[Dict], task_id: int) -> Optional[Dict]:
    """
    Get a specific task by its ID.
    
    Args:
        tasks: List of task dictionaries
        task_id: ID of the task to find
    
    Returns:
        Task dictionary if found, None otherwise
    """
    for task in tasks:
        if task.get('id') == task_id:
            return task
    return None


def combine_filters(tasks: List[Dict], priority: Optional[str] = None,
                   completed: Optional[bool] = None, 
                   keyword: Optional[str] = None) -> List[Dict]:
    """
    Combine multiple filters.
    
    Args:
        tasks: List of task dictionaries
        priority: Priority filter (optional)
        completed: Status filter (optional)
        keyword: Search keyword (optional)
    
    Returns:
        List of tasks matching all specified filters
    """
    result = tasks
    
    if priority:
        result = filter_by_priority(result, priority)
    
    if completed is not None:
        result = filter_by_status(result, completed)
    
    if keyword:
        result = search_tasks(result, keyword)
    
    return result
