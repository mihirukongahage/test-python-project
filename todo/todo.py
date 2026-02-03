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
from .task_filters import (
	filter_by_priority, filter_by_status, search_tasks, 
	get_overdue_tasks, sort_tasks, combine_filters
)
from .task_utils import (
	validate_task, calculate_statistics, format_date,
	create_task, get_next_task_id
)
from .config_manager import ConfigManager

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
	""" Simple Todo Application - Manage your tasks efficiently!"""
	pass

# ...existing code...
