#!/usr/bin/env python3
"""
Simple Todo Application
A terminal-based todo list manager with a beautiful CLI interface.
"""

import json
import os
from datetime import datetime
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Import new modules
from todo_app.task_filters import (
    filter_by_priority, filter_by_status, search_tasks, 
    get_overdue_tasks, sort_tasks, combine_filters
)
from todo_app.task_utils import (
    validate_task, calculate_statistics, format_date,
    create_task, get_next_task_id
)
from todo_app.config_manager import ConfigManager

console = Console()

TODO_FILE = Path.home() / ".todo_list.json"
config_manager = ConfigManager()


def load_todos():
    """Load todos from JSON file."""
    if TODO_FILE.exists():
        with open(TODO_FILE, 'r') as f:
            return json.load(f)
    return []


def save_todos(todos):
    """Save todos to JSON file."""
    with open(TODO_FILE, 'w') as f:
        json.dump(todos, f, indent=2)


@click.group()
def cli():
    """📝 Simple Todo Application - Manage your tasks efficiently!"""
    pass


@cli.command()
@click.argument('task')
@click.option('--priority', '-p', type=click.Choice(['low', 'medium', 'high']), default='medium', help='Task priority')
def add(task, priority):
    """Add a new todo task."""
    todos = load_todos()
    todo = {
        'id': len(todos) + 1,
        'task': task,
        'priority': priority,
        'completed': False,
        'created_at': datetime.now().isoformat()
    }
    todos.append(todo)
    save_todos(todos)
    console.print(f"[green]✓[/green] Added task: {task} (Priority: {priority})")


@cli.command()
def list():
    """List all todo tasks."""
    todos = load_todos()
    
    if not todos:
        console.print("[yellow]No tasks found. Add one with 'todo add <task>'[/yellow]")
        return
    
    table = Table(title="📋 Your Todo List", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="cyan", width=6)
    table.add_column("Task", style="white", width=40)
    table.add_column("Priority", width=10)
    table.add_column("Status", width=12)
    table.add_column("Created", width=20)
    
    for todo in todos:
        priority_color = {
            'low': 'green',
            'medium': 'yellow',
            'high': 'red'
        }.get(todo['priority'], 'white')
        
        status = "[green]✓ Done[/green]" if todo['completed'] else "[yellow]○ Pending[/yellow]"
        created = datetime.fromisoformat(todo['created_at']).strftime('%Y-%m-%d %H:%M')
        
        table.add_row(
            str(todo['id']),
            todo['task'],
            f"[{priority_color}]{todo['priority'].upper()}[/{priority_color}]",
            status,
            created
        )
    
    console.print(table)


@cli.command()
@click.argument('task_id', type=int)
def complete(task_id):
    """Mark a task as completed."""
    todos = load_todos()
    
    for todo in todos:
        if todo['id'] == task_id:
            todo['completed'] = True
            save_todos(todos)
            console.print(f"[green]✓[/green] Marked task {task_id} as completed!")
            return
    
    console.print(f"[red]✗[/red] Task {task_id} not found.")


@cli.command()
@click.argument('task_id', type=int)
def delete(task_id):
    """Delete a todo task."""
    todos = load_todos()
    
    for i, todo in enumerate(todos):
        if todo['id'] == task_id:
            deleted_task = todos.pop(i)
            save_todos(todos)
            console.print(f"[green]✓[/green] Deleted task: {deleted_task['task']}")
            return
    
    console.print(f"[red]✗[/red] Task {task_id} not found.")


@cli.command()
def clear():
    """Clear all completed tasks."""
    todos = load_todos()
    initial_count = len(todos)
    todos = [todo for todo in todos if not todo['completed']]
    cleared_count = initial_count - len(todos)
    
    save_todos(todos)
    
    if cleared_count > 0:
        console.print(f"[green]✓[/green] Cleared {cleared_count} completed task(s)!")
    else:
        console.print("[yellow]No completed tasks to clear.[/yellow]")


@cli.command()
def stats():
    """Show todo statistics."""
    todos = load_todos()
    
    if not todos:
        console.print("[yellow]No tasks found.[/yellow]")
        return
    
    stats = calculate_statistics(todos)
    
    stats_text = f"""
    [bold cyan]Total Tasks:[/bold cyan] {stats['total']}
    [green]✓ Completed:[/green] {stats['completed']}
    [yellow]○ Pending:[/yellow] {stats['pending']}
    [red]! High Priority Pending:[/red] {stats['high_priority_pending']}
    [blue]Completion Rate:[/blue] {stats['completion_rate']}%
    [magenta]Average Age:[/magenta] {stats['avg_age_days']} days
    """
    
    panel = Panel(stats_text, title="📊 Todo Statistics", border_style="cyan")
    console.print(panel)


@cli.command()
@click.argument('keyword')
def search(keyword):
    """Search tasks by keyword."""
    todos = load_todos()
    
    if not todos:
        console.print("[yellow]No tasks found.[/yellow]")
        return
    
    results = search_tasks(todos, keyword)
    
    if not results:
        console.print(f"[yellow]No tasks found matching '{keyword}'[/yellow]")
        return
    
    console.print(f"[green]Found {len(results)} task(s) matching '{keyword}':[/green]\n")
    
    table = Table(title=f"🔍 Search Results: '{keyword}'", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="cyan", width=6)
    table.add_column("Task", style="white", width=40)
    table.add_column("Priority", width=10)
    table.add_column("Status", width=12)
    
    for todo in results:
        priority_color = config_manager.get_priority_color(todo['priority'])
        status = "[green]✓ Done[/green]" if todo['completed'] else "[yellow]○ Pending[/yellow]"
        
        table.add_row(
            str(todo['id']),
            todo['task'],
            f"[{priority_color}]{todo['priority'].upper()}[/{priority_color}]",
            status
        )
    
    console.print(table)


@cli.command()
@click.option('--priority', '-p', type=click.Choice(['low', 'medium', 'high']), help='Filter by priority')
@click.option('--status', '-s', type=click.Choice(['pending', 'completed']), help='Filter by status')
def filter(priority, status):
    """Filter tasks by priority and/or status."""
    todos = load_todos()
    
    if not todos:
        console.print("[yellow]No tasks found.[/yellow]")
        return
    
    completed = None if status is None else (status == 'completed')
    filtered = combine_filters(todos, priority=priority, completed=completed)
    
    if not filtered:
        console.print("[yellow]No tasks match the specified filters.[/yellow]")
        return
    
    console.print(f"[green]Found {len(filtered)} task(s):[/green]\n")
    
    table = Table(title="🔍 Filtered Tasks", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="cyan", width=6)
    table.add_column("Task", style="white", width=40)
    table.add_column("Priority", width=10)
    table.add_column("Status", width=12)
    
    for todo in filtered:
        priority_color = config_manager.get_priority_color(todo['priority'])
        status_text = "[green]✓ Done[/green]" if todo['completed'] else "[yellow]○ Pending[/yellow]"
        
        table.add_row(
            str(todo['id']),
            todo['task'],
            f"[{priority_color}]{todo['priority'].upper()}[/{priority_color}]",
            status_text
        )
    
    console.print(table)


@cli.command()
@click.option('--days', '-d', default=7, type=int, help='Days threshold (default: 7)')
def overdue(days):
    """Show overdue pending tasks."""
    todos = load_todos()
    
    if not todos:
        console.print("[yellow]No tasks found.[/yellow]")
        return
    
    overdue_tasks = get_overdue_tasks(todos, days=days)
    
    if not overdue_tasks:
        console.print(f"[green]No tasks are overdue (older than {days} days).[/green]")
        return
    
    console.print(f"[red]⚠ Found {len(overdue_tasks)} overdue task(s):[/red]\n")
    
    table = Table(title=f"⚠ Overdue Tasks (>{days} days)", show_header=True, header_style="bold red")
    table.add_column("ID", style="cyan", width=6)
    table.add_column("Task", style="white", width=40)
    table.add_column("Priority", width=10)
    table.add_column("Age (days)", width=12)
    
    for todo in overdue_tasks:
        priority_color = config_manager.get_priority_color(todo['priority'])
        from task_utils import calculate_task_age
        age = calculate_task_age(todo)
        
        table.add_row(
            str(todo['id']),
            todo['task'],
            f"[{priority_color}]{todo['priority'].upper()}[/{priority_color}]",
            str(age)
        )
    
    console.print(table)


if __name__ == '__main__':
    cli()
