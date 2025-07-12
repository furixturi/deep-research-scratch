from typing import Dict, Callable, List, Optional, Any
from api.tools.registry import tool_registry


def get_available_tools() -> Dict[str, str]:
    """
    Get a dictionary of available tools with their descriptions.

    Returns:
        Dict[str, str]: A dictionary where keys are tool names and
        values are their descriptions.
    """
    return {
        name: data["description"]
        for name, data in tool_registry.items()
    }


def get_tools_openai_format() -> List[Dict]:
    """
    Convert internal tools to OpenAI tool format.

    Returns:
        List[Dict]: List of tools in OpenAI format for API calls.
    """
    openai_tools = []
    for tool_name, tool_data in tool_registry.items():
        openai_tools.append(
            {
                "type": "function",
                "function": {
                    "name": tool_name,
                    "description": tool_data["description"],
                    "parameters": tool_data["parameters"],
                },
            }
        )
    return openai_tools


def execute_tool(tool_name: str, tool_args: Dict[str, Any]) -> str:
    """
    Execute a tool with the given arguments.

    Args:
        tool_name (str): The name of the tool to execute.
        tool_args (Dict[str, Any]): The arguments to pass to the tool.

    Returns:
        str: The result from the tool execution.

    Raises:
        ValueError: If the tool is not registered.
    """
    if tool_name not in tool_registry:
        raise ValueError(f"Tool '{tool_name}' is not registered.")

    handler = tool_registry[tool_name]["handler"]

    # For tools that expect a single argument, try to extract it
    # Otherwise, pass the full arguments dict
    try:
        # Try to call with unpacked arguments first
        return handler(**tool_args)
    except TypeError:
        # If that fails, try with a single argument
        # This handles legacy tools that expect a single string parameter
        if len(tool_args) == 1:
            return handler(next(iter(tool_args.values())))
        else:
            # If multiple args but handler doesn't support **kwargs,
            # pass the whole dict
            return handler(tool_args)


# Import tools to register them - clean and explicit
from api.tools import search
from api.tools import code_executor
