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

console = Console()

TODO_FILE = Path.home() / ".todo_list.json"


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
    
    total = len(todos)
    completed = sum(1 for t in todos if t['completed'])
    pending = total - completed
    
    high_priority = sum(1 for t in todos if t['priority'] == 'high' and not t['completed'])
    
    stats_text = f"""
    [bold cyan]Total Tasks:[/bold cyan] {total}
    [green]✓ Completed:[/green] {completed}
    [yellow]○ Pending:[/yellow] {pending}
    [red]! High Priority Pending:[/red] {high_priority}
    """
    
    panel = Panel(stats_text, title="📊 Todo Statistics", border_style="cyan")
    console.print(panel)


if __name__ == '__main__':
    cli()
