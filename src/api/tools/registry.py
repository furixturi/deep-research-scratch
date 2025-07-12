"""
Tool registry - separate from the main tools module to avoid circular imports.
"""

from typing import Dict, Callable, Optional, Any

tool_registry: Dict[str, Dict] = {}


def register_tool(
    name: str,
    description: str,
    handler: Callable,
    parameters: Optional[Dict] = None,
):
    """
    Register a tool with a name, description, handler function, and
    optional parameters schema.

    Args:
        name (str): The name of the tool.
        description (str): A brief description of what the tool does.
        handler (Callable): The function that implements the tool's
        functionality.
        parameters (Optional[Dict]): OpenAI-compatible parameters schema.
        If None, defaults to simple query parameter.

    Raises:
        ValueError: If a tool with the same name is already registered.
    """
    if name in tool_registry:
        raise ValueError(f"Tool '{name}' is already registered.")

    # Default parameters schema if none provided
    if parameters is None:
        parameters = {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": f"Input for the {name} tool",
                }
            },
            "required": ["query"],
        }

    tool_registry[name] = {
        "description": description,
        "handler": handler,
        "parameters": parameters,
    }

    # Debug output
    print(
        f"DEBUG: Registered tool '{name}' with description: {description}"
    )
    print(f"DEBUG: Total tools registered: {len(tool_registry)}")
