"""
Task import module.
Provides functionality to import tasks from various formats.
"""

import json
import csv
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path


def import_from_json(filepath: str) -> Optional[List[Dict]]:
    """
    Import tasks from JSON file.
    
    Args:
        filepath: Path to input file
    
    Returns:
        List of task dictionaries if successful, None otherwise
    """
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Handle different JSON structures
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            if 'tasks' in data:
                return data['tasks']
            elif 'task_list' in data:
                return data['task_list']
        
        return None
    except (IOError, OSError, json.JSONDecodeError):
        return None


def import_from_csv(filepath: str) -> Optional[List[Dict]]:
    """
    Import tasks from CSV file.
    
    Args:
        filepath: Path to input file
    
    Returns:
        List of task dictionaries if successful, None otherwise
    """
    try:
        tasks = []
        with open(filepath, 'r', newline='') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                task = {
                    'id': int(row.get('id', 0)) if row.get('id', '').isdigit() else 0,
                    'task': row.get('task', ''),
                    'priority': row.get('priority', 'medium'),
                    'completed': row.get('completed', 'False').lower() in ['true', '1', 'yes'],
                    'created_at': row.get('created_at', datetime.now().isoformat())
                }
                tasks.append(task)
        
        return tasks if tasks else None
    except (IOError, OSError, csv.Error):
        return None


def import_from_text(filepath: str) -> Optional[List[Dict]]:
    """
    Import tasks from plain text file (simple format).
    Expected format: each line is a task, optional priority in brackets.
    Example: "[HIGH] Buy groceries"
    
    Args:
        filepath: Path to input file
    
    Returns:
        List of task dictionaries if successful, None otherwise
    """
    try:
        tasks = []
        with open(filepath, 'r') as f:
            lines = f.readlines()
        
        task_id = 1
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Parse priority
            priority = 'medium'
            if line.startswith('['):
                end_bracket = line.find(']')
                if end_bracket != -1:
                    priority_str = line[1:end_bracket].strip().lower()
                    if priority_str in ['low', 'medium', 'high']:
                        priority = priority_str
                    line = line[end_bracket + 1:].strip()
            
            # Check if completed (starts with x or ✓)
            completed = False
            if line.startswith(('x ', 'X ', '✓ ', '[x]', '[X]')):
                completed = True
                line = line.lstrip('xX✓ []').strip()
            
            task = {
                'id': task_id,
                'task': line,
                'priority': priority,
                'completed': completed,
                'created_at': datetime.now().isoformat()
            }
            tasks.append(task)
            task_id += 1
        
        return tasks if tasks else None
    except (IOError, OSError):
        return None


def import_from_markdown(filepath: str) -> Optional[List[Dict]]:
    """
    Import tasks from Markdown file (GitHub-style checkboxes).
    Expected format: - [ ] Task or - [x] Task
    
    Args:
        filepath: Path to input file
    
    Returns:
        List of task dictionaries if successful, None otherwise
    """
    try:
        tasks = []
        with open(filepath, 'r') as f:
            lines = f.readlines()
        
        task_id = 1
        current_priority = 'medium'
        
        for line in lines:
            line = line.strip()
            
            # Check for priority headers
            if line.startswith('##'):
                header = line.lstrip('#').strip().lower()
                if 'high' in header:
                    current_priority = 'high'
                elif 'low' in header:
                    current_priority = 'low'
                elif 'medium' in header:
                    current_priority = 'medium'
                continue
            
            # Parse checkbox tasks
            if line.startswith('- ['):
                completed = line[3] in ['x', 'X']
                task_text = line[6:].strip()
                
                # Remove formatting (bold, italic, etc.)
                task_text = task_text.replace('**', '').replace('*', '').replace('__', '').replace('_', '')
                
                # Extract just the task description (before any date info)
                if '(' in task_text or '[' in task_text:
                    for delimiter in [' (', ' [', ' _']:
                        if delimiter in task_text:
                            task_text = task_text.split(delimiter)[0].strip()
                            break
                
                if task_text:
                    task = {
                        'id': task_id,
                        'task': task_text,
                        'priority': current_priority,
                        'completed': completed,
                        'created_at': datetime.now().isoformat()
                    }
                    tasks.append(task)
                    task_id += 1
        
        return tasks if tasks else None
    except (IOError, OSError):
        return None


def import_by_format(filepath: str, format: Optional[str] = None) -> Optional[List[Dict]]:
    """
    Import tasks using the specified format or auto-detect from file extension.
    
    Args:
        filepath: Path to input file
        format: Import format ('json', 'csv', 'md', 'txt') or None for auto-detect
    
    Returns:
        List of task dictionaries if successful, None otherwise
    """
    if format is None:
        # Auto-detect from file extension
        path = Path(filepath)
        ext = path.suffix.lower()
        format_map = {
            '.json': 'json',
            '.csv': 'csv',
            '.md': 'md',
            '.txt': 'txt'
        }
        format = format_map.get(ext, 'json')
    
    format = format.lower()
    
    if format == 'json':
        return import_from_json(filepath)
    elif format == 'csv':
        return import_from_csv(filepath)
    elif format in ['md', 'markdown']:
        return import_from_markdown(filepath)
    elif format in ['txt', 'text']:
        return import_from_text(filepath)
    else:
        return None


def merge_tasks(existing_tasks: List[Dict], imported_tasks: List[Dict], 
                strategy: str = 'append') -> List[Dict]:
    """
    Merge imported tasks with existing tasks using specified strategy.
    
    Args:
        existing_tasks: Current tasks
        imported_tasks: Tasks to import
        strategy: Merge strategy ('append', 'replace', 'skip_duplicates')
    
    Returns:
        Merged list of tasks
    """
    if strategy == 'replace':
        return imported_tasks
    
    elif strategy == 'skip_duplicates':
        merged = existing_tasks.copy()
        existing_descriptions = {t.get('task', '').lower() for t in existing_tasks}
        
        for task in imported_tasks:
            task_desc = task.get('task', '').lower()
            if task_desc not in existing_descriptions:
                merged.append(task)
                existing_descriptions.add(task_desc)
        
        return merged
    
    else:  # append (default)
        return existing_tasks + imported_tasks


def validate_imported_tasks(tasks: List[Dict]) -> tuple[List[Dict], List[str]]:
    """
    Validate imported tasks and return valid tasks and error messages.
    
    Args:
        tasks: List of imported task dictionaries
    
    Returns:
        Tuple of (valid_tasks, error_messages)
    """
    valid_tasks = []
    errors = []
    
    for i, task in enumerate(tasks, 1):
        # Check required fields
        if not isinstance(task, dict):
            errors.append(f"Task {i}: Not a valid dictionary")
            continue
        
        if 'task' not in task or not task['task']:
            errors.append(f"Task {i}: Missing or empty 'task' field")
            continue
        
        # Validate priority
        priority = task.get('priority', 'medium')
        if priority not in ['low', 'medium', 'high']:
            errors.append(f"Task {i}: Invalid priority '{priority}', using 'medium'")
            task['priority'] = 'medium'
        
        # Validate completed
        if not isinstance(task.get('completed', False), bool):
            task['completed'] = False
        
        # Validate or generate ID
        if 'id' not in task or not isinstance(task['id'], int):
            task['id'] = i
        
        # Validate or generate created_at
        if 'created_at' not in task:
            task['created_at'] = datetime.now().isoformat()
        else:
            try:
                datetime.fromisoformat(task['created_at'])
            except (ValueError, TypeError):
                errors.append(f"Task {i}: Invalid date format, using current time")
                task['created_at'] = datetime.now().isoformat()
        
        valid_tasks.append(task)
    
    return valid_tasks, errors


def restore_from_backup(backup_filepath: str) -> Optional[List[Dict]]:
    """
    Restore tasks from a backup file.
    
    Args:
        backup_filepath: Path to backup file
    
    Returns:
        List of task dictionaries if successful, None otherwise
    """
    return import_from_json(backup_filepath)
