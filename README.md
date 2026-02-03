# 📝 Todo Application

A comprehensive and beautiful terminal-based todo list manager built with Python, featuring advanced analytics, import/export capabilities, and extensive testing.

## Features

### Core Functionality
- ✅ Add tasks with priority levels (low, medium, high)
- 📋 List all tasks with beautiful formatting
- ✓ Mark tasks as completed
- 🗑️ Delete individual tasks
- 🧹 Clear all completed tasks
- 📊 View statistics about your tasks
- 💾 Persistent storage using JSON

### Advanced Features
- 🔍 **Search**: Find tasks by keywords
- 🎯 **Filter**: Filter tasks by priority, status, or date range
- ⏰ **Overdue**: View tasks past their due date
- 📈 **Analytics**: Advanced insights and productivity metrics
- 📥 **Import**: Import tasks from JSON, CSV, Text, and Markdown files
- 📤 **Export**: Export tasks to JSON, CSV, Markdown, HTML, and Text formats
- ⚙️ **Configuration**: Customizable settings and preferences
- 📊 **Enhanced Statistics**: Detailed analytics and reporting

## Installation

1. Clone or download this project
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Commands

#### Add a task

```bash
python todo.py add "Buy groceries"
python todo.py add "Finish project report" --priority high
python todo.py add "Call mom" -p low
```

#### List all tasks

```bash
python todo.py list
```

#### Mark a task as completed

```bash
python todo.py complete 1
```

#### Delete a task

```bash
python todo.py delete 2
```

#### Clear all completed tasks

```bash
python todo.py clear
```

#### View statistics

```bash
python todo.py stats
```

### Advanced Commands

#### Search for tasks

```bash
python todo.py search "project"
```

#### Filter tasks

```bash
# Filter by priority
python todo.py filter --priority high

# Filter by status
python todo.py filter --status pending

# Filter by date range
python todo.py filter --start-date 2024-01-01 --end-date 2024-12-31
```

#### View overdue tasks

```bash
python todo.py overdue
```

#### View analytics

```bash
python todo.py analytics
```

#### Import tasks

```bash
# Import from JSON
python todo.py import tasks.json --format json

# Import from CSV
python todo.py import tasks.csv --format csv

# Auto-detect format
python todo.py import tasks.json
```

#### Export tasks

```bash
# Export to JSON
python todo.py export tasks.json --format json

# Export to CSV
python todo.py export tasks.csv --format csv

# Export to HTML
python todo.py export tasks.html --format html
```

#### Configuration

```bash
# View current configuration
python todo.py config show

# Set configuration values
python todo.py config set theme dark
python todo.py config set default_priority medium

# Reset to defaults
python todo.py config reset
```

### Get help

```bash
python todo.py --help
python todo.py add --help
python todo.py filter --help
```

## Project Structure

```
├── todo.py                 # Main CLI application
├── task_filters.py         # Task filtering and searching
├── task_utils.py           # Task validation and utilities
├── task_analytics.py       # Advanced analytics and insights
├── task_export.py          # Export functionality
├── task_import.py          # Import functionality
├── config_manager.py       # Configuration management
├── test_*.py              # Comprehensive test suite
└── requirements.txt       # Python dependencies
```

## Dependencies

- **click**: Beautiful command-line interface creation
- **rich**: Rich terminal formatting and colors
- **pytest**: Testing framework (for development)
- **coverage**: Code coverage measurement
- **pytest-cov**: Coverage plugin for pytest

## Testing & Coverage

### Run Tests

```bash
# Run all tests
pytest -v

# Run specific test file
pytest test_todo.py -v

# Run with coverage
pytest --cov=. --cov-report=html
```

### Run Coverage Analysis

```bash
# Quick method using the script
./run_coverage.sh

# Or manually
coverage run -m pytest
coverage report -m
coverage html  # Generate HTML report
```

### View Coverage Report

- **Terminal**: `coverage report -m`
- **HTML**: Open `htmlcov/index.html` in your browser

Current coverage: **87.88%** ✅ (151 tests passing)

## Data Storage

Tasks are stored in `~/.todo_list.json` in your home directory.

Configuration is stored in `~/.todo_config.json`.

## Example Session

```bash
$ python todo.py add "Write documentation" -p high
✓ Added task: Write documentation (Priority: high)

$ python todo.py add "Review pull requests" -p medium
✓ Added task: Review pull requests (Priority: medium)

$ python todo.py list
┏━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┓
┃ ID   ┃ Task                   ┃ Priority ┃ Status     ┃ Created            ┃
┡━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━┩
│ 1    │ Write documentation    │ HIGH     │ ○ Pending  │ 2024-01-15 10:30   │
│ 2    │ Review pull requests   │ MEDIUM   │ ○ Pending  │ 2024-01-15 10:31   │
└──────┴────────────────────────┴──────────┴────────────┴────────────────────┘

$ python todo.py complete 1
✓ Marked task 1 as completed!

$ python todo.py stats
╭────────── 📊 Todo Statistics ───────────╮
│                                         │
│     Total Tasks: 2                      │
│     ✓ Completed: 1                      │
│     ○ Pending: 1                        │
│     ! High Priority Pending: 0          │
│                                         │
╰─────────────────────────────────────────╯

$ python todo.py analytics
╭──────────── 📈 Task Analytics ────────────╮
│                                           │
│ Productivity Score: 85.5/100              │
│ Tasks Completed Today: 1                  │
│ Average Completion Time: 2.3 days         │
│ Current Streak: 3 days                    │
│                                           │
│ Priority Distribution:                    │
│   • High: 40%                             │
│   • Medium: 35%                           │
│   • Low: 25%                              │
│                                           │
│ Top Bottlenecks:                          │
│   1. Documentation tasks (2.1 days avg)   │
│   2. Review tasks (1.8 days avg)          │
│                                           │
╰───────────────────────────────────────────╯
```

## Import/Export Formats

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
# My Tasks
[HIGH] Buy groceries
x [MEDIUM] Write report
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

## License

MIT License - Feel free to use and modify!
