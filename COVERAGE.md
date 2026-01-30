# Code Coverage Report

## Summary

- **Total Coverage**: 93.68% ✅
- **Total Statements**: 95
- **Missed Statements**: 6
- **Test Cases**: 8 (all passing)

## Coverage Breakdown

### Covered ✅
- ✓ Adding tasks (with and without priority)
- ✓ Listing tasks (empty and with tasks)
- ✓ Completing tasks (happy path)
- ✓ Deleting tasks (happy path)
- ✓ Clearing completed tasks (when tasks exist)
- ✓ Showing statistics (when tasks exist)
- ✓ File I/O operations (load/save)
- ✓ Task creation and management

### Missing Coverage (6 lines) ⚠️

The following edge cases are not currently tested:

1. **Line 110** - `complete` command error handling
   ```python
   console.print(f"[red]✗[/red] Task {task_id} not found.")
   ```
   - Scenario: Trying to complete a non-existent task

2. **Line 126** - `delete` command error handling
   ```python
   console.print(f"[red]✗[/red] Task {task_id} not found.")
   ```
   - Scenario: Trying to delete a non-existent task

3. **Line 142** - `clear` command when nothing to clear
   ```python
   console.print("[yellow]No completed tasks to clear.[/yellow]")
   ```
   - Scenario: Running clear when no completed tasks exist

4. **Lines 151-152** - `stats` command with empty todo list
   ```python
   console.print("[yellow]No tasks found.[/yellow]")
   return
   ```
   - Scenario: Running stats when no tasks exist

5. **Line 172** - Main entry point
   ```python
   cli()
   ```
   - Standard Python idiom, not critical to test

## How to Run Coverage

### Option 1: Using the coverage script
```bash
./run_coverage.sh
```

### Option 2: Using pytest-cov
```bash
pytest --cov=todo --cov-report=term-missing --cov-report=html test_todo.py
```

### Option 3: Using coverage directly
```bash
coverage run -m pytest test_todo.py
coverage report -m
coverage html
```

## View HTML Report

Open the detailed HTML report in your browser:
```bash
xdg-open htmlcov/index.html
```

Or navigate directly to: `htmlcov/index.html`

## Improving Coverage

To reach 100% coverage, add these test cases to `test_todo.py`:

1. Test completing a non-existent task (should show error)
2. Test deleting a non-existent task (should show error)
3. Test clearing when no completed tasks exist
4. Test stats command with empty todo list

These are all error handling and edge cases that would make the test suite more robust.
