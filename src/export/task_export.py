"""
Task export module.
Provides functionality to export tasks in various formats.
"""

import json
import csv
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path


def export_to_json(tasks: List[Dict], filepath: str, pretty: bool = True) -> bool:
    """
    Export tasks to JSON file.
    
    Args:
        tasks: List of task dictionaries
        filepath: Path to output file
        pretty: Whether to format JSON with indentation
    
    Returns:
        True if successful, False otherwise
    """
    try:
        export_data = {
            'export_date': datetime.now().isoformat(),
            'total_tasks': len(tasks),
            'tasks': tasks
        }
        
        with open(filepath, 'w') as f:
            if pretty:
                json.dump(export_data, f, indent=2)
            else:
                json.dump(export_data, f)
        
        return True
    except (IOError, OSError):
        return False


def export_to_csv(tasks: List[Dict], filepath: str) -> bool:
    """
    Export tasks to CSV file.
    
    Args:
        tasks: List of task dictionaries
        filepath: Path to output file
    
    Returns:
        True if successful, False otherwise
    """
    if not tasks:
        return False
    
    try:
        fieldnames = ['id', 'task', 'priority', 'completed', 'created_at']
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for task in tasks:
                row = {key: task.get(key, '') for key in fieldnames}
                writer.writerow(row)
        
        return True
    except (IOError, OSError):
        return False


def export_to_markdown(tasks: List[Dict], filepath: str) -> bool:
    """
    Export tasks to Markdown file.
    
    Args:
        tasks: List of task dictionaries
        filepath: Path to output file
    
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(filepath, 'w') as f:
            f.write("# Todo List\n\n")
            f.write(f"*Exported: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n")
            
            # Group by priority
            for priority in ['high', 'medium', 'low']:
                priority_tasks = [t for t in tasks if t.get('priority') == priority]
                if priority_tasks:
                    f.write(f"## {priority.capitalize()} Priority\n\n")
                    
                    for task in priority_tasks:
                        checkbox = '[x]' if task.get('completed', False) else '[ ]'
                        created = task.get('created_at', '')
                        try:
                            date_obj = datetime.fromisoformat(created)
                            date_str = date_obj.strftime('%Y-%m-%d')
                        except (ValueError, TypeError):
                            date_str = 'N/A'
                        
                        f.write(f"- {checkbox} **{task.get('task', '')}** _{date_str}_\n")
                    
                    f.write("\n")
        
        return True
    except (IOError, OSError):
        return False


def export_to_html(tasks: List[Dict], filepath: str) -> bool:
    """
    Export tasks to HTML file.
    
    Args:
        tasks: List of task dictionaries
        filepath: Path to output file
    
    Returns:
        True if successful, False otherwise
    """
    try:
        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Todo List Export</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }
        .task {
            background: white;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .task.completed {
            opacity: 0.6;
            text-decoration: line-through;
        }
        .priority-high { border-left: 5px solid #f44336; }
        .priority-medium { border-left: 5px solid #ff9800; }
        .priority-low { border-left: 5px solid #4CAF50; }
        .badge {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 12px;
            font-weight: bold;
        }
        .badge-high { background-color: #f44336; color: white; }
        .badge-medium { background-color: #ff9800; color: white; }
        .badge-low { background-color: #4CAF50; color: white; }
        .badge-completed { background-color: #2196F3; color: white; }
        .date {
            color: #666;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <h1>📝 Todo List</h1>
    <p><em>Exported: """ + datetime.now().strftime('%Y-%m-%d %H:%M') + """</em></p>
    <p><strong>Total Tasks:</strong> """ + str(len(tasks)) + """</p>
"""
        
        for task in tasks:
            priority = task.get('priority', 'medium')
            completed = task.get('completed', False)
            task_desc = task.get('task', '')
            created = task.get('created_at', '')
            
            try:
                date_obj = datetime.fromisoformat(created)
                date_str = date_obj.strftime('%Y-%m-%d %H:%M')
            except (ValueError, TypeError):
                date_str = 'N/A'
            
            completed_class = ' completed' if completed else ''
            
            html_content += f"""
    <div class="task priority-{priority}{completed_class}">
        <div>
            <span class="badge badge-{priority}">{priority.upper()}</span>
            {' <span class="badge badge-completed">COMPLETED</span>' if completed else ''}
        </div>
        <h3>{task_desc}</h3>
        <p class="date">Created: {date_str}</p>
    </div>
"""
        
        html_content += """
</body>
</html>
"""
        
        with open(filepath, 'w') as f:
            f.write(html_content)
        
        return True
    except (IOError, OSError):
        return False


def export_to_text(tasks: List[Dict], filepath: str) -> bool:
    """
    Export tasks to plain text file.
    
    Args:
        tasks: List of task dictionaries
        filepath: Path to output file
    
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(filepath, 'w') as f:
            f.write("=" * 60 + "\n")
            f.write("TODO LIST EXPORT\n")
            f.write("=" * 60 + "\n")
            f.write(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"Total Tasks: {len(tasks)}\n")
            f.write("=" * 60 + "\n\n")
            
            for task in tasks:
                status = "✓" if task.get('completed', False) else "○"
                priority = task.get('priority', 'medium').upper()
                task_desc = task.get('task', '')
                created = task.get('created_at', '')
                
                try:
                    date_obj = datetime.fromisoformat(created)
                    date_str = date_obj.strftime('%Y-%m-%d')
                except (ValueError, TypeError):
                    date_str = 'N/A'
                
                f.write(f"[{status}] [{priority}] {task_desc}\n")
                f.write(f"    Created: {date_str}\n")
                f.write("-" * 60 + "\n\n")
        
        return True
    except (IOError, OSError):
        return False


def export_by_format(tasks: List[Dict], filepath: str, format: Optional[str] = None) -> bool:
    """
    Export tasks using the specified format or auto-detect from file extension.
    
    Args:
        tasks: List of task dictionaries
        filepath: Path to output file
        format: Export format ('json', 'csv', 'md', 'html', 'txt') or None for auto-detect
    
    Returns:
        True if successful, False otherwise
    """
    if format is None:
        # Auto-detect from file extension
        path = Path(filepath)
        ext = path.suffix.lower()
        format_map = {
            '.json': 'json',
            '.csv': 'csv',
            '.md': 'md',
            '.html': 'html',
            '.htm': 'html',
            '.txt': 'txt'
        }
        format = format_map.get(ext, 'json')
    
    format = format.lower()
    
    if format == 'json':
        return export_to_json(tasks, filepath)
    elif format == 'csv':
        return export_to_csv(tasks, filepath)
    elif format in ['md', 'markdown']:
        return export_to_markdown(tasks, filepath)
    elif format in ['html', 'htm']:
        return export_to_html(tasks, filepath)
    elif format in ['txt', 'text']:
        return export_to_text(tasks, filepath)
    else:
        return False


def create_backup(tasks: List[Dict], backup_dir: Optional[str] = None) -> Optional[str]:
    """
    Create a backup of tasks with timestamp.
    
    Args:
        tasks: List of task dictionaries
        backup_dir: Directory to store backup (default: current directory)
    
    Returns:
        Path to backup file if successful, None otherwise
    """
    if backup_dir is None:
        backup_dir = Path.home() / ".todo_backups"
    else:
        backup_dir = Path(backup_dir)
    
    try:
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = backup_dir / f"todo_backup_{timestamp}.json"
        
        if export_to_json(tasks, str(backup_file)):
            return str(backup_file)
        return None
    except (IOError, OSError):
        return None
