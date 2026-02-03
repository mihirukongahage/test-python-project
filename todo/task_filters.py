from datetime import datetime, timedelta
from typing import List, Dict, Optional

def filter_by_priority(tasks: List[Dict], priority: str) -> List[Dict]:
	return [task for task in tasks if task.get('priority') == priority]

def filter_by_status(tasks: List[Dict], completed: bool) -> List[Dict]:
	from . import task_utils  # Circular dependency for pydeps test
	return [task for task in tasks if task.get('completed') == completed]

def filter_by_date_range(tasks: List[Dict], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict]:
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
			continue
	return filtered

def search_tasks(tasks: List[Dict], keyword: str) -> List[Dict]:
	if not keyword:
		return tasks
	keyword_lower = keyword.lower()
	return [task for task in tasks if keyword_lower in task.get('task', '').lower()]

def get_overdue_tasks(tasks: List[Dict], days: int = 7) -> List[Dict]:
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
	priority_order = {'high': 3, 'medium': 2, 'low': 1}
	if by == 'priority':
		return sorted(tasks, key=lambda x: priority_order.get(x.get('priority', 'medium'), 2), reverse=reverse)
	elif by == 'created_at':
		return sorted(tasks, key=lambda x: x.get('created_at', ''), reverse=reverse)
	elif by == 'task':
		return sorted(tasks, key=lambda x: x.get('task', '').lower(), reverse=reverse)
	else:
		return sorted(tasks, key=lambda x: x.get('id', 0), reverse=reverse)

def get_task_by_id(tasks: List[Dict], task_id: int) -> Optional[Dict]:
	for task in tasks:
		if task.get('id') == task_id:
			return task
	return None

def combine_filters(tasks: List[Dict], priority: Optional[str] = None, completed: Optional[bool] = None, keyword: Optional[str] = None) -> List[Dict]:
	result = tasks
	if priority:
		result = filter_by_priority(result, priority)
	if completed is not None:
		result = filter_by_status(result, completed)
	if keyword:
		result = search_tasks(result, keyword)
	return result
