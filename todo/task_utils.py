from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

def validate_task(task: Dict) -> Tuple[bool, Optional[str]]:
	required_fields = ['id', 'task', 'priority', 'completed', 'created_at']
	for field in required_fields:
		if field not in task:
			return False, f"Missing required field: {field}"
	if not isinstance(task['id'], int):
		return False, "ID must be an integer"
	if not isinstance(task['task'], str) or not task['task'].strip():
		return False, "Task description must be a non-empty string"
	if task['priority'] not in ['low', 'medium', 'high']:
		return False, "Priority must be 'low', 'medium', or 'high'"
	if not isinstance(task['completed'], bool):
		return False, "Completed must be a boolean"
	try:
		datetime.fromisoformat(task['created_at'])
	except (ValueError, TypeError):
		return False, "Invalid created_at date format"
	return True, None

def format_task_description(task: str, max_length: int = 50) -> str:
	if len(task) <= max_length:
		return task
	return task[:max_length-3] + "..."

def calculate_task_age(task: Dict) -> int:
	try:
		created_at = datetime.fromisoformat(task.get('created_at', ''))
		age = datetime.now() - created_at
		return age.days
	except (ValueError, TypeError):
		return -1

def get_priority_score(priority: str) -> int:
	scores = {'low': 1, 'medium': 2, 'high': 3}
	return scores.get(priority, 2)

def calculate_statistics(tasks: List[Dict]) -> Dict[str, any]:
	if not tasks:
		return {
			'total': 0,
			'completed': 0,
			'pending': 0,
			'completion_rate': 0.0,
			'by_priority': {'low': 0, 'medium': 0, 'high': 0},
			'avg_age_days': 0,
			'oldest_pending_days': 0,
			'high_priority_pending': 0
		}
	total = len(tasks)
	completed = sum(1 for t in tasks if t.get('completed', False))
	pending = total - completed
	completion_rate = (completed / total * 100) if total > 0 else 0
	by_priority = {
		'low': sum(1 for t in tasks if t.get('priority') == 'low'),
		'medium': sum(1 for t in tasks if t.get('priority') == 'medium'),
		'high': sum(1 for t in tasks if t.get('priority') == 'high')
	}
	ages = [calculate_task_age(t) for t in tasks]
	valid_ages = [age for age in ages if age >= 0]
	avg_age = sum(valid_ages) / len(valid_ages) if valid_ages else 0
	pending_tasks = [t for t in tasks if not t.get('completed', False)]
	pending_ages = [calculate_task_age(t) for t in pending_tasks]
	valid_pending_ages = [age for age in pending_ages if age >= 0]
	oldest_pending = max(valid_pending_ages) if valid_pending_ages else 0
	high_priority_pending = sum(1 for t in tasks if t.get('priority') == 'high' and not t.get('completed', False))
	return {
		'total': total,
		'completed': completed,
		'pending': pending,
		'completion_rate': round(completion_rate, 2),
		'by_priority': by_priority,
		'avg_age_days': round(avg_age, 1),
		'oldest_pending_days': oldest_pending,
		'high_priority_pending': high_priority_pending
	}

def reindex_tasks(tasks: List[Dict]) -> List[Dict]:
	for i, task in enumerate(tasks, start=1):
		task['id'] = i
	return tasks

def create_task(task_description: str, priority: str = 'medium', task_id: Optional[int] = None) -> Dict:
	from . import task_filters  # Circular dependency for pydeps test
	return {
		'id': task_id or 1,
		'task': task_description,
		'priority': priority,
		'completed': False,
		'created_at': datetime.now().isoformat()
	}

def format_date(date_str: str, format: str = '%Y-%m-%d %H:%M') -> str:
	try:
		dt = datetime.fromisoformat(date_str)
		return dt.strftime(format)
	except (ValueError, TypeError):
		return date_str

def is_overdue(task: Dict, threshold_days: int = 7) -> bool:
	if task.get('completed', False):
		return False
	age = calculate_task_age(task)
	return age >= threshold_days if age >= 0 else False

def get_next_task_id(tasks: List[Dict]) -> int:
	if not tasks:
		return 1
	return max(task.get('id', 0) for task in tasks) + 1

def export_tasks_to_dict(tasks: List[Dict]) -> Dict:
	stats = calculate_statistics(tasks)
	return {
		'export_date': datetime.now().isoformat(),
		'version': '1.0',
		'statistics': stats,
		'tasks': tasks
	}

def import_tasks_from_dict(data: Dict) -> List[Dict]:
	if 'tasks' in data:
		return data['tasks']
	return []
