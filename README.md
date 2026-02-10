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

### From Source

1. Clone or download this project
2. Install the package:

```bash
# Install for development (editable mode)
pip install -e ".[dev]"

# Or install just the package
pip install -e .

# Or using traditional requirements files
pip install -r requirements.txt        # Production dependencies
pip install -r requirements-dev.txt    # Development dependencies
```

### Using pip (when published)

```bash
pip install todo-app
```

## Usage

### Basic Commands

#### Add a task

```bash
todo add "Buy groceries"
todo add "Finish project report" --priority high
todo add "Call mom" -p low
```

#### List all tasks

```bash
todo list
```

#### Mark a task as completed

```bash
todo complete 1
```

#### Delete a task

```bash
todo delete 2
```

#### Clear all completed tasks

```bash
todo clear
```

#### View statistics

```bash
todo stats
```

### Advanced Commands

#### Search for tasks

```bash
todo search "project"
```

#### Filter tasks

```bash
# Filter by priority
todo filter --priority high

# Filter by status
todo filter --status pending

# Filter by date range
todo filter --start-date 2024-01-01 --end-date 2024-12-31
```

#### View overdue tasks

```bash
todo overdue
```

#### View analytics

```bash
todo analytics
```

#### Import tasks

```bash
# Import from JSON
todo import tasks.json --format json

# Import from CSV
todo import tasks.csv --format csv

# Auto-detect format
todo import tasks.json
```

#### Export tasks

```bash
# Export to JSON
todo export tasks.json --format json

# Export to CSV
todo export tasks.csv --format csv

# Export to HTML
todo export tasks.html --format html
```

#### Configuration

```bash
# View current configuration
todo config show

# Set configuration values
todo config set theme dark
todo config set default_priority medium

# Reset to defaults
todo config reset
```

### Get help

```bash
todo --help
todo add --help
todo filter --help
```

## Project Structure

```
test-python-project/
├── src/
│   ├── todo_app/              # Main application package
│   │   ├── __init__.py
│   │   ├── cli.py             # Main CLI application
│   │   ├── task_filters.py    # Task filtering and searching
│   │   ├── task_analytics.py  # Advanced analytics and insights
│   ├── export/                # Export functionality
│   │   ├── __init__.py
│   │   ├── task_export.py     # Export to various formats
│   │   └── README.md
│   ├── imports/               # Import functionality
│   │   ├── __init__.py
│   │   ├── task_import.py     # Import from various formats
│   │   └── README.md
│   └── utils/                 # Utility modules
│       ├── __init__.py
│       ├── task_utils.py      # Task validation and utilities
│       ├── config_manager.py  # Configuration management
│       └── README.md
├── tests/                     # Test suite
│   ├── __init__.py
│   ├── test_config_manager.py
│   ├── test_task_analytics.py
│   ├── test_task_export.py
│   ├── test_task_filters.py
│   ├── test_task_import.py
│   └── test_task_utils.py
├── scripts/                   # Utility scripts
│   ├── run_coverage.sh
│   └── setup.sh
├── docs/                      # Documentation
│   └── COVERAGE.md
├── pyproject.toml            # Modern Python project configuration
├── setup.py                  # Backward compatibility
├── requirements.txt          # Production dependencies
├── requirements-dev.txt      # Development dependencies
├── Makefile                  # Common development tasks
├── LICENSE                   # MIT License
├── README.md                 # This file
├── .gitignore               # Git ignore patterns
├── .coveragerc              # Coverage configuration
└── .importlinter            # Import linting rules
```

## Dependencies

- **click**: Beautiful command-line interface creation
- **rich**: Rich terminal formatting and colors
- **pytest**: Testing framework (for development)
- **coverage**: Code coverage measurement
- **pytest-cov**: Coverage plugin for pytest

## Development

### Quick Start with Makefile

The project includes a Makefile for common development tasks:

```bash
make help          # Show all available commands
make install-dev   # Install with development dependencies
make test          # Run tests
make coverage      # Run tests with coverage report
make lint          # Run linters
make format        # Format code with black
make clean         # Remove build artifacts
make build         # Build distribution packages
```

### Testing & Coverage

#### Run Tests

```bash
# Using Makefile (recommended)
make test

# Or directly with pytest
pytest -v

# Run specific test file
pytest tests/test_config_manager.py -v

# Run with coverage
make coverage
# Or: pytest --cov=todo_app --cov-report=html
```

#### Run Coverage Analysis

```bash
# Quick method using Makefile
make coverage

# Or using the script
./scripts/run_coverage.sh

# Or manually
coverage run -m pytest
coverage report -m
coverage html  # Generate HTML report
```

#### View Coverage Report

- **Terminal**: `coverage report -m`
- **HTML**: Open `htmlcov/index.html` in your browser

Current coverage: **87.88%** ✅ (151 tests passing)

### Code Quality

The project uses several tools to maintain code quality:

- **black**: Code formatting
- **ruff**: Fast Python linter
- **mypy**: Static type checking
- **import-linter**: Enforce import boundaries
- **pytest**: Testing framework
- **coverage**: Code coverage measurement

Run all quality checks:

```bash
make format  # Format code
make lint    # Run linters
make test    # Run tests
```

## Data Storage

Tasks are stored in `~/.todo_list.json` in your home directory.

Configuration is stored in `~/.todo_config.json`.

## Example Session

```bash
$ todo add "Write documentation" -p high
✓ Added task: Write documentation (Priority: high)

$ todo add "Review pull requests" -p medium
✓ Added task: Review pull requests (Priority: medium)

$ todo list
┏━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┓
┃ ID   ┃ Task                   ┃ Priority ┃ Status     ┃ Created            ┃
┡━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━┩
│ 1    │ Write documentation    │ HIGH     │ ○ Pending  │ 2024-01-15 10:30   │
│ 2    │ Review pull requests   │ MEDIUM   │ ○ Pending  │ 2024-01-15 10:31   │
└──────┴────────────────────────┴──────────┴────────────┴────────────────────┘

$ todo complete 1
✓ Marked task 1 as completed!

$ todo stats
╭────────── 📊 Todo Statistics ───────────╮
│                                         │
│     Total Tasks: 2                      │
│     ✓ Completed: 1                      │
│     ○ Pending: 1                        │
│     ! High Priority Pending: 0          │
│                                         │
╰─────────────────────────────────────────╯

$ todo analytics
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
