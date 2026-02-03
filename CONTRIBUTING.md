# Contributing to Todo App

Thank you for your interest in contributing to Todo App! This document provides guidelines and instructions for contributing to the project.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- git

### Setting Up Development Environment

1. **Fork and clone the repository**

```bash
git clone https://github.com/yourusername/todo-app.git
cd todo-app
```

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install development dependencies**

```bash
# Using pip with editable install (recommended)
pip install -e ".[dev]"

# Or using requirements files
pip install -r requirements-dev.txt
```

4. **Verify installation**

```bash
make test
```

## Development Workflow

### Making Changes

1. **Create a new branch**

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

2. **Make your changes**
   - Write your code
   - Add or update tests
   - Update documentation if needed

3. **Format and lint your code**

```bash
make format  # Format with black
make lint    # Check with ruff and mypy
```

4. **Run tests**

```bash
make test     # Run all tests
make coverage # Run with coverage report
```

5. **Commit your changes**

```bash
git add .
git commit -m "Brief description of your changes"
```

Follow conventional commit format:
- `feat: Add new feature`
- `fix: Fix bug`
- `docs: Update documentation`
- `test: Add or update tests`
- `refactor: Refactor code`
- `style: Format code`
- `chore: Update dependencies, build tools, etc.`

### Running Tests

```bash
# Run all tests
make test

# Run specific test file
pytest tests/test_config_manager.py

# Run with coverage
make coverage

# View coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

### Code Quality Tools

The project uses several tools to maintain code quality:

#### Black (Code Formatting)
```bash
black src/ tests/
# Or: make format
```

#### Ruff (Linting)
```bash
ruff check src/ tests/
ruff check --fix src/ tests/  # Auto-fix issues
# Or: make lint
```

#### MyPy (Type Checking)
```bash
mypy src/
```

#### Import Linter (Import Rules)
```bash
lint-imports
```

### Project Structure

```
src/
  todo_app/          # Main package
    cli.py          # CLI interface
    task_*.py       # Task-related modules
    config_manager.py  # Configuration

tests/              # Test suite
  test_*.py        # Test modules

docs/               # Documentation
scripts/            # Utility scripts
```

### Code Style Guidelines

- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions small and focused
- Maintain test coverage above 80%

#### Example Function

```python
def add_task(task: str, priority: str = "medium") -> dict:
    """
    Add a new task to the todo list.
    
    Args:
        task: The task description
        priority: Task priority (low, medium, high)
        
    Returns:
        dict: The created task object
        
    Raises:
        ValueError: If task is empty or priority is invalid
    """
    # Implementation here
    pass
```

### Writing Tests

- Write tests for all new features
- Ensure all tests pass before submitting PR
- Aim for high code coverage
- Use descriptive test names
- Use pytest fixtures for setup

#### Example Test

```python
def test_add_task_with_priority():
    """Test adding a task with a specific priority."""
    task = create_task("Buy groceries", priority="high")
    assert task["priority"] == "high"
    assert task["completed"] is False
```

## Submitting Changes

### Pull Request Process

1. **Update your branch**

```bash
git fetch origin
git rebase origin/main
```

2. **Push your changes**

```bash
git push origin feature/your-feature-name
```

3. **Create a Pull Request**
   - Go to the repository on GitHub
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template with:
     - Description of changes
     - Related issues (if any)
     - Testing performed
     - Screenshots (if applicable)

4. **Address review feedback**
   - Make requested changes
   - Push updates to the same branch
   - Respond to comments

### PR Checklist

- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commit messages are clear and descriptive
- [ ] Branch is up to date with main

## Reporting Bugs

### Before Submitting

- Check if the bug has already been reported
- Verify it's reproducible in the latest version
- Collect relevant information

### Bug Report Template

```markdown
**Description**
A clear description of the bug

**Steps to Reproduce**
1. Run command '...'
2. See error

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.11.0]
- Todo App version: [e.g., 1.0.0]

**Additional Context**
Any other relevant information
```

## Feature Requests

We welcome feature requests! Please:

1. Check if it's already been requested
2. Describe the feature and use case
3. Explain why it would be valuable
4. Provide examples if possible

## Questions?

- Open an issue with the "question" label
- Check existing documentation
- Review closed issues for similar questions

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards others

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Thank You!

Your contributions make this project better for everyone. We appreciate your time and effort! 🎉
