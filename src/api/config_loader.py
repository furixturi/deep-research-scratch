import yaml
import os

def load_default_config():
    config_path = os.path.join(os.path.dirname(__file__), 'default_config.yaml')
    if not os.path.exists(config_path):
        return {}
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)
    
## Example loaded config
# {
#   "models": {
#     "supported": {
#       "aoai": ["gpt-4o", "gpt-4", "o3"],
#       "openai": ["gpt-4o", "gpt-4", "gpt-3.5-turbo"]
#     },
#     "default": {
#       "provider": "aoai",
#       "model": "gpt-4o"
#     },
#     "single_agent": {
#       "provider": "aoai",
#       "model": "gpt-4o"
#     },
#     "planner_agent": {
#       "provider": "aoai",
#       "model": "o3"
#     },
#     "search_agent": {
#       "provider": "aoai",
#       "model": "gpt-4o"
#     }
#   },
#   "agent_type": "single_agent",
#   "tools": {
#     "search": {
#       "description": "Search the web for information"
#     },
#     "code": {
#       "description": "Execute Python code"
#     }
#   }
# }