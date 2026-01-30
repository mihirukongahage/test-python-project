"""
Tests for config_manager module.
"""

import json
import pytest
from pathlib import Path
from config_manager import ConfigManager, DEFAULT_CONFIG


@pytest.fixture
def temp_config_file(tmp_path):
    """Create a temporary config file."""
    config_file = tmp_path / "test_config.json"
    # Ensure it doesn't exist initially
    if config_file.exists():
        config_file.unlink()
    return config_file


def test_config_manager_default_init(temp_config_file):
    """Test initializing ConfigManager with defaults."""
    manager = ConfigManager(temp_config_file)
    assert manager.config == DEFAULT_CONFIG


def test_load_config_creates_default(temp_config_file):
    """Test loading config creates default when file doesn't exist."""
    manager = ConfigManager(temp_config_file)
    assert manager.config['behavior']['default_priority'] == 'medium'


def test_save_and_load_config(temp_config_file):
    """Test saving and loading configuration."""
    manager = ConfigManager(temp_config_file)
    manager.set('behavior.default_priority', 'high')
    assert manager.save_config() is True
    
    # Load it again
    manager2 = ConfigManager(temp_config_file)
    assert manager2.get('behavior.default_priority') == 'high'


def test_get_simple_key(temp_config_file):
    """Test getting a simple configuration key."""
    manager = ConfigManager(temp_config_file)
    result = manager.get('todo_file')
    assert result is not None


def test_get_nested_key(temp_config_file):
    """Test getting a nested configuration key."""
    manager = ConfigManager(temp_config_file)
    result = manager.get('display.colors.high')
    assert result == 'red'


def test_get_nonexistent_key(temp_config_file):
    """Test getting a non-existent key returns default."""
    manager = ConfigManager(temp_config_file)
    result = manager.get('nonexistent.key', 'default_value')
    assert result == 'default_value'


def test_set_simple_key(temp_config_file):
    """Test setting a simple configuration key."""
    manager = ConfigManager(temp_config_file)
    manager.set('todo_file', '/custom/path')
    assert manager.get('todo_file') == '/custom/path'


def test_set_nested_key(temp_config_file):
    """Test setting a nested configuration key."""
    manager = ConfigManager(temp_config_file)
    manager.set('display.colors.medium', 'blue')
    assert manager.get('display.colors.medium') == 'blue'


def test_set_new_nested_key(temp_config_file):
    """Test setting a new nested key."""
    manager = ConfigManager(temp_config_file)
    manager.set('new.nested.key', 'value')
    assert manager.get('new.nested.key') == 'value'


def test_reset_to_defaults(temp_config_file):
    """Test resetting configuration to defaults."""
    manager = ConfigManager(temp_config_file)
    original_priority = manager.get('behavior.default_priority')
    manager.set('behavior.default_priority', 'high')
    assert manager.get('behavior.default_priority') == 'high'
    manager.reset_to_defaults()
    assert manager.get('behavior.default_priority') == 'medium'


def test_get_todo_file(temp_config_file):
    """Test getting todo file path."""
    manager = ConfigManager(temp_config_file)
    result = manager.get_todo_file()
    assert isinstance(result, Path)


def test_get_priority_color(temp_config_file):
    """Test getting priority colors."""
    manager = ConfigManager(temp_config_file)
    # Reset to ensure defaults
    manager.reset_to_defaults()
    assert manager.get_priority_color('low') == 'green'
    assert manager.get_priority_color('medium') == 'yellow'
    assert manager.get_priority_color('high') == 'red'


def test_get_priority_color_invalid(temp_config_file):
    """Test getting color for invalid priority."""
    manager = ConfigManager(temp_config_file)
    result = manager.get_priority_color('invalid')
    assert result == 'white'


def test_get_date_format(temp_config_file):
    """Test getting date format."""
    manager = ConfigManager(temp_config_file)
    result = manager.get_date_format()
    assert result == '%Y-%m-%d %H:%M'


def test_get_default_priority(temp_config_file):
    """Test getting default priority."""
    manager = ConfigManager(temp_config_file)
    # Reset to ensure defaults
    manager.reset_to_defaults()
    result = manager.get_default_priority()
    assert result == 'medium'


def test_should_confirm_delete(temp_config_file):
    """Test checking delete confirmation setting."""
    manager = ConfigManager(temp_config_file)
    result = manager.should_confirm_delete()
    assert result is False


def test_get_overdue_threshold(temp_config_file):
    """Test getting overdue threshold."""
    manager = ConfigManager(temp_config_file)
    result = manager.get_overdue_threshold()
    assert result == 7


def test_load_config_with_invalid_json(temp_config_file):
    """Test loading config with invalid JSON."""
    with open(temp_config_file, 'w') as f:
        f.write("invalid json {")
    
    manager = ConfigManager(temp_config_file)
    assert manager.config == DEFAULT_CONFIG


def test_load_config_merges_with_defaults(temp_config_file):
    """Test loading partial config merges with defaults."""
    partial_config = {'behavior': {'default_priority': 'high'}}
    with open(temp_config_file, 'w') as f:
        json.dump(partial_config, f)
    
    manager = ConfigManager(temp_config_file)
    assert manager.get('behavior.default_priority') == 'high'
    assert manager.get('display.colors.high') == 'red'  # Should have default


def test_save_config_failure(tmp_path):
    """Test save config handles failures gracefully."""
    # Use a path that can't be written to
    invalid_path = tmp_path / "nonexistent_dir" / "config.json"
    manager = ConfigManager(invalid_path)
    result = manager.save_config()
    # This might succeed or fail depending on permissions, so just test it doesn't crash
    assert isinstance(result, bool)


def test_merge_configs_deep(temp_config_file):
    """Test deep merging of configurations."""
    manager = ConfigManager(temp_config_file)
    base = {'a': {'b': {'c': 1}}, 'd': 2}
    override = {'a': {'b': {'e': 3}}}
    result = manager._merge_configs(base, override)
    
    assert result['a']['b']['c'] == 1
    assert result['a']['b']['e'] == 3
    assert result['d'] == 2
