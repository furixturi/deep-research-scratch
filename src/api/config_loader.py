import yaml
import os

def load_default_config():
    config_path = os.path.join(os.path.dirname(__file__), 'default_config.yaml')
    if not os.path.exists(config_path):
        return {}
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)