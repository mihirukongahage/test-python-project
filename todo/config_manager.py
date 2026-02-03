import json
import copy
from pathlib import Path
from typing import Dict, Any, Optional

DEFAULT_CONFIG = {
	'todo_file': str(Path.home() / ".todo_list.json"),
	'display': {
		'table_style': 'default',
		'show_timestamps': True,
		'date_format': '%Y-%m-%d %H:%M',
		'colors': {
			'low': 'green',
			'medium': 'yellow',
			'high': 'red'
		}
	},
	'behavior': {
		'auto_id_reindex': False,
		'confirm_delete': False,
		'default_priority': 'medium',
		'archive_completed': False,
		'overdue_threshold_days': 7
	}
}

class ConfigManager:
	def __init__(self, config_file: Optional[Path] = None):
		self.config_file = config_file or Path.home() / ".todo_config.json"
		self.config = self.load_config()
	def load_config(self) -> Dict[str, Any]:
		if self.config_file.exists():
			try:
				with open(self.config_file, 'r') as f:
					loaded = json.load(f)
					return self._merge_configs(copy.deepcopy(DEFAULT_CONFIG), loaded)
			except (json.JSONDecodeError, IOError):
				return copy.deepcopy(DEFAULT_CONFIG)
		return copy.deepcopy(DEFAULT_CONFIG)
	def save_config(self) -> bool:
		try:
			with open(self.config_file, 'w') as f:
				json.dump(self.config, f, indent=2)
			return True
		except IOError:
			return False
	def get(self, key: str, default: Any = None) -> Any:
		keys = key.split('.')
		value = self.config
		for k in keys:
			if isinstance(value, dict) and k in value:
				value = value[k]
			else:
				return default
		return value
	def set(self, key: str, value: Any) -> None:
		keys = key.split('.')
		config = self.config
		for k in keys[:-1]:
			if k not in config or not isinstance(config[k], dict):
				config[k] = {}
			config = config[k]
		config[keys[-1]] = value
	def reset_to_defaults(self) -> None:
		self.config = copy.deepcopy(DEFAULT_CONFIG)
	def get_todo_file(self) -> Path:
		return Path(self.get('todo_file', str(Path.home() / ".todo_list.json")))
	def get_priority_color(self, priority: str) -> str:
		return self.get(f'display.colors.{priority}', 'white')
	def get_date_format(self) -> str:
		return self.get('display.date_format', '%Y-%m-%d %H:%M')
	def get_default_priority(self) -> str:
		return self.get('behavior.default_priority', 'medium')
	def should_confirm_delete(self) -> bool:
		return self.get('behavior.confirm_delete', False)
	def get_overdue_threshold(self) -> int:
		return self.get('behavior.overdue_threshold_days', 7)
	def _merge_configs(self, base: Dict, override: Dict) -> Dict:
		result = base.copy()
		for key, value in override.items():
			if key in result and isinstance(result[key], dict) and isinstance(value, dict):
				result[key] = self._merge_configs(result[key], value)
			else:
				result[key] = value
		return result
