# 📝 Todo Application

A simple and beautiful terminal-based todo list manager built with Python.

## Features

- ✅ Add tasks with priority levels (low, medium, high)
- 📋 List all tasks with beautiful formatting
- ✓ Mark tasks as completed
- 🗑️ Delete individual tasks
- 🧹 Clear all completed tasks
- 📊 View statistics about your tasks
- 💾 Persistent storage using JSON

## Installation

1. Clone or download this project
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Add a task

```bash
python todo.py add "Buy groceries"
python todo.py add "Finish project report" --priority high
python todo.py add "Call mom" -p low
```

### List all tasks

```bash
python todo.py list
```

### Mark a task as completed

```bash
python todo.py complete 1
```

### Delete a task

```bash
python todo.py delete 2
```

### Clear all completed tasks

```bash
python todo.py clear
```

### View statistics

```bash
python todo.py stats
```

### Get help

```bash
python todo.py --help
python todo.py add --help
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
pytest test_todo.py -v
```

### Run Coverage Analysis

```bash
# Quick method using the script
./run_coverage.sh

# Or manually
coverage run -m pytest test_todo.py
coverage report -m
coverage html  # Generate HTML report
```

### View Coverage Report

- **Terminal**: `coverage report -m`
- **HTML**: Open `htmlcov/index.html` in your browser

Current coverage: **93.68%** ✅

## Data Storage

Tasks are stored in `~/.todo_list.json` in your home directory.

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
```

## License

MIT License - Feel free to use and modify!
