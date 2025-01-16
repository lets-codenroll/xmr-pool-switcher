import json
import os
from utils.helpers import RED, RESET, GREEN

# Path to config.json in the parent directory
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../config.json")

def load_config():
    """Load the configuration from the config.json file."""
    if not os.path.exists(CONFIG_FILE):
        print(f"{RED}Error: config.json not found at {os.path.abspath(CONFIG_FILE)}.{RESET}")
        return None
    with open(CONFIG_FILE, "r") as file:
        return json.load(file)

def save_config(config):
    """Save the updated configuration to the config.json file."""
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)
    print(f"{GREEN}Configuration saved to {os.path.abspath(CONFIG_FILE)}.{RESET}")
