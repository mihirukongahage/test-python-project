# Utils Package

This package contains utility modules that provide reusable functionality for the todo application.

## Modules

### task_utils.py

Core utility functions for task management:

- **validate_task()** - Validate task structure and data
- **calculate_statistics()** - Calculate statistics from task list
- **format_date()** - Format datetime objects for display
- **create_task()** - Create a new task object
- **get_next_task_id()** - Get the next available task ID
- **format_task_description()** - Format task descriptions for display
- **calculate_task_age()** - Calculate how long a task has existed
- **get_priority_score()** - Get numeric score for priority level
- **reindex_tasks()** - Reindex task IDs sequentially
- **is_overdue()** - Check if a task is overdue
- **export_tasks_to_dict()** - Export tasks to dictionary format
- **import_tasks_from_dict()** - Import tasks from dictionary format

### config_manager.py

Configuration management for the application:

- **ConfigManager** class - Manages application configuration
  - Load/save configuration files
  - Get/set configuration values
  - Reset to defaults
  - Helper methods for common config values

- **DEFAULT_CONFIG** - Default configuration dictionary

## Usage

### Importing from Utils

```python
# Import specific functions
from utils.task_utils import validate_task, create_task
from utils.config_manager import ConfigManager

# Or import from package
from utils import validate_task, ConfigManager
```

### Example: Using Task Utils

```python
from utils.task_utils import create_task, validate_task

# Create a new task
task = create_task("Buy groceries", priority="high")

# Validate the task
is_valid, error = validate_task(task)
if is_valid:
    print("Task is valid!")
else:
    print(f"Invalid task: {error}")
```

### Example: Using Config Manager

```python
from utils.config_manager import ConfigManager

# Initialize config manager
config = ConfigManager()

# Get configuration value
date_format = config.get("display.date_format")

# Set configuration value
config.set("theme", "dark")
config.save()

# Get priority color
color = config.get_priority_color("high")
```

## Design Principles

1. **Reusability**: Functions are designed to be used across multiple modules
2. **Single Responsibility**: Each function has a clear, focused purpose
3. **Type Safety**: Functions include type hints where appropriate
4. **Error Handling**: Proper error handling and validation
5. **Documentation**: All functions include docstrings

## Testing

All utility functions have corresponding tests in the `tests/` directory:

- `tests/test_task_utils.py` - Tests for task utility functions
- `tests/test_config_manager.py` - Tests for configuration management

Run tests:
```bash
pytest tests/test_task_utils.py -v
pytest tests/test_config_manager.py -v
```

## Dependencies

- **pathlib** - File path handling
- **json** - JSON serialization
- **datetime** - Date and time handling
- **typing** - Type hints

No external dependencies required.
