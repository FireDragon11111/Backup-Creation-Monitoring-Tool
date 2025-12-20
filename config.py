import json
import os

CONFIG_FILE = 'config.json'

DEFAULT_CONFIG = {
    'backup_frequency': 'Daily',
    'backup_time': '00:00',
    'backup_day_of_week': 'Sunday',
    'backup_day_of_month': "1",  # stored as a string to match calendar output
    'zip_files_kept': 3,
    'interval_days': 0,
    'interval_hours': 0,
    'interval_minutes': 0,
    'interval_seconds': 0,
    'source_dir': '',
    'dest_dir': '',
    'sub_dirs': [],
    'monitoring_state': False
}

def sanitize_config(config):
    sanitized = {}
    for key, default in DEFAULT_CONFIG.items():
        value = config.get(key, default)
        # For numeric defaults, try converting the value to an integer
        if isinstance(default, int):
            try:
                sanitized[key] = int(value) if value != "" else default
            except (ValueError, TypeError):
                sanitized[key] = default
        # For string defaults, use the value if it is not empty
        elif isinstance(default, str):
            sanitized[key] = value if value else default
        # For lists, ensure the value is a list
        elif isinstance(default, list):
            sanitized[key] = value if isinstance(value, list) else default
        # For booleans or other types, use the value directly
        else:
            sanitized[key] = value
    return sanitized

def save_config(config, profile):
    with open(f"{CONFIG_FILE}_{profile}.json", 'w') as f:
        json.dump(config, f, indent=4)

def load_config(profile):
    config_file = f"{CONFIG_FILE}_{profile}.json"
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            return sanitize_config(config)
        except Exception as e:
            # If loading fails, return a copy of the default configuration.
            return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()
