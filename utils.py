# utils.py

import json
import os


def load_config(file_path):
    """Loads config settings from a JSON file."""
    if not os.path.exists(file_path):
        print(f"Config file {file_path} not found.")
        return {}
    with open(file_path, 'r') as file:
        return json.load(file)


def save_config(config, file_path):
    """Saves config settings to a JSON file."""
    with open(file_path, 'w') as file:
        json.dump(config, file, indent=4)


def format_message(sender, message):
    """Formats a message for display."""
    return f"{sender}: {message}"


def log_message(message):
    print(message)  


# Example Implementation
if __name__ == "__main__":
    config = load_config("config.json")
    if not config:
        config = {"host": "localhost", "port": 12345}
        save_config(config, "config.json")

    print("Configuration loaded:", config)
