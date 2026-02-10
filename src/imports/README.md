# Imports Package

This package provides functionality to import todo tasks from various formats.

## Supported Formats

- **JSON** - Structured data format
- **CSV** - Comma-separated values
- **Markdown** - Human-readable markdown format
- **Text** - Plain text format

## Functions

### import_from_json()
Import tasks from JSON files.

```python
from imports import import_from_json

tasks = import_from_json("tasks.json")
```

### import_from_csv()
Import tasks from CSV files.

```python
from imports import import_from_csv

tasks = import_from_csv("tasks.csv")
```

### import_from_text()
Import tasks from plain text files.

```python
from imports import import_from_text

tasks = import_from_text("tasks.txt")
```

### import_from_markdown()
Import tasks from Markdown files.

```python
from imports import import_from_markdown

tasks = import_from_markdown("tasks.md")
```

### import_by_format()
Auto-detect format from file extension and import.

```python
from imports import import_by_format

tasks = import_by_format("tasks.json")  # Auto-detects JSON format
```

### merge_tasks()
Merge imported tasks with existing tasks.

```python
from imports import merge_tasks

existing_tasks = [{"id": 1, "task": "Old task"}]
new_tasks = [{"id": 2, "task": "New task"}]

# Merge strategies: 'append', 'replace', 'skip_duplicates'
merged = merge_tasks(existing_tasks, new_tasks, strategy='append')
```

### validate_imported_tasks()
Validate imported tasks for correctness.

```python
from imports import validate_imported_tasks

tasks = [{"id": 1, "task": "Buy groceries"}]
valid_tasks, errors = validate_imported_tasks(tasks)
```

### restore_from_backup()
Restore tasks from a backup file.

```python
from imports import restore_from_backup

tasks = restore_from_backup("backup_2024-01-15.json")
```

## Usage Examples

### Basic Import
```python
from imports import import_from_json

# Import tasks from JSON file
tasks = import_from_json("tasks.json")
for task in tasks:
    print(f"Task: {task['task']}")
```

### Auto-detect Format
```python
from imports import import_by_format

# Format auto-detected from extension
tasks_json = import_by_format("tasks.json")    # JSON
tasks_csv = import_by_format("tasks.csv")      # CSV
tasks_md = import_by_format("tasks.md")        # Markdown
tasks_txt = import_by_format("tasks.txt")      # Text
```

### Merge with Existing Tasks
```python
from imports import import_from_json, merge_tasks

# Load existing tasks
existing_tasks = [
    {"id": 1, "task": "Existing task"}
]

# Import new tasks
imported_tasks = import_from_json("new_tasks.json")

# Merge with different strategies
merged = merge_tasks(existing_tasks, imported_tasks, strategy='append')
```

### Validate Imported Tasks
```python
from imports import import_from_json, validate_imported_tasks

# Import tasks
tasks = import_from_json("tasks.json")

# Validate
valid_tasks, errors = validate_imported_tasks(tasks)
if errors:
    print("Validation errors:", errors)
else:
    print(f"All {len(valid_tasks)} tasks are valid!")
```

### Restore from Backup
```python
from imports import restore_from_backup

# Restore from backup
tasks = restore_from_backup("backups/backup_2024-01-15_120000.json")
print(f"Restored {len(tasks)} tasks from backup")
```

## Import Formats

### JSON Format
```json
{
  "tasks": [
    {
      "id": 1,
      "task": "Buy groceries",
      "priority": "high",
      "completed": false,
      "created_at": "2024-01-15T10:30:00"
    }
  ]
}
```

### CSV Format
```csv
id,task,priority,completed,created_at
1,"Buy groceries",high,false,2024-01-15T10:30:00
```

### Text Format
```
[HIGH] Buy groceries
x [MEDIUM] Write report (completed)
Call mom
```

### Markdown Format
```markdown
# Todo List

## High Priority
- [ ] Buy groceries
- [x] Write report

## Low Priority
- [ ] Call mom
```

## Merge Strategies

- **append**: Add all imported tasks to existing list
- **replace**: Replace existing tasks with imported tasks
- **skip_duplicates**: Only add tasks that don't already exist

## Testing

All import functions are tested in `tests/test_task_import.py`.

Run tests:
```bash
pytest tests/test_task_import.py -v
```

## Coverage

Imports package has 91.33% test coverage with all major functionality tested.
