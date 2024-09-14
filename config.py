import json
import os

CONFIG_FILE = 'config.json'

def save_config(config, profile):
    with open(f"{CONFIG_FILE}_{profile}.json", 'w') as f:
        json.dump(config, f, indent=4)

def load_config(profile):
    config_file = f"{CONFIG_FILE}_{profile}.json"
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    return {}
