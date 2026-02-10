# Export Package

This package provides functionality to export todo tasks to various formats.

## Supported Formats

- **JSON** - Structured data format
- **CSV** - Comma-separated values
- **Markdown** - Human-readable markdown format
- **HTML** - Web-ready HTML format
- **Text** - Plain text format

## Functions

### export_to_json()
Export tasks to JSON format with optional pretty printing.

```python
from export import export_to_json

tasks = [{"id": 1, "task": "Buy groceries", "priority": "high"}]
export_to_json(tasks, "tasks.json", pretty=True)
```

### export_to_csv()
Export tasks to CSV format.

```python
from export import export_to_csv

tasks = [{"id": 1, "task": "Buy groceries", "priority": "high"}]
export_to_csv(tasks, "tasks.csv")
```

### export_to_markdown()
Export tasks to Markdown format with priority sections.

```python
from export import export_to_markdown

tasks = [{"id": 1, "task": "Buy groceries", "priority": "high"}]
export_to_markdown(tasks, "tasks.md")
```

### export_to_html()
Export tasks to HTML format with styling.

```python
from export import export_to_html

tasks = [{"id": 1, "task": "Buy groceries", "priority": "high"}]
export_to_html(tasks, "tasks.html")
```

### export_to_text()
Export tasks to plain text format.

```python
from export import export_to_text

tasks = [{"id": 1, "task": "Buy groceries", "priority": "high"}]
export_to_text(tasks, "tasks.txt")
```

### export_by_format()
Auto-detect format from file extension and export.

```python
from export import export_by_format

tasks = [{"id": 1, "task": "Buy groceries", "priority": "high"}]
export_by_format(tasks, "tasks.json")  # Auto-detects JSON format
```

### create_backup()
Create a backup of tasks with timestamp.

```python
from export import create_backup

tasks = [{"id": 1, "task": "Buy groceries", "priority": "high"}]
backup_path = create_backup(tasks, backup_dir="./backups")
```

## Usage Examples

### Basic Export
```python
from export import export_to_json

tasks = [
    {"id": 1, "task": "Buy groceries", "priority": "high", "completed": False},
    {"id": 2, "task": "Write report", "priority": "medium", "completed": True}
]

# Export to JSON
export_to_json(tasks, "tasks.json")
```

### Auto-detect Format
```python
from export import export_by_format

tasks = [...]

# Format auto-detected from extension
export_by_format(tasks, "tasks.json")    # JSON
export_by_format(tasks, "tasks.csv")     # CSV
export_by_format(tasks, "tasks.md")      # Markdown
export_by_format(tasks, "tasks.html")    # HTML
export_by_format(tasks, "tasks.txt")     # Text
```

### Create Backup
```python
from export import create_backup

tasks = [...]

# Create backup with timestamp
backup_file = create_backup(tasks)
print(f"Backup created: {backup_file}")
```

## Testing

All export functions are tested in `tests/test_task_export.py`.

Run tests:
```bash
pytest tests/test_task_export.py -v
```

## Coverage

Export package has 91.41% test coverage with all major functionality tested.
