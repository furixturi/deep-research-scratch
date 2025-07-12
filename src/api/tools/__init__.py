from typing import Dict, Callable, List

tool_registry : Dict[str, Callable] = {}

def register_tool(name: str, description: str, handler: Callable):
    """
    Register a tool with a name, description, and handler function.
    
    Args:
        name (str): The name of the tool.
        description (str): A brief description of what the tool does.
        handler (Callable): The function that implements the tool's functionality.

    Raises:
        ValueError: If a tool with the same name is already registered.
    """
    if name in tool_registry:
        raise ValueError(f"Tool '{name}' is already registered.")
    
    tool_registry[name] = {
        "description": description,
        "handler": handler
    }

def get_available_tools() -> Dict[str, str]:
    """
    Get a dictionary of available tools with their descriptions.
    
    Returns:
        Dict[str, str]: A dictionary where keys are tool names and values are their descriptions.
    """
    return {name: data["description"] for name, data in tool_registry.items()}

def get_tool_handler(name: str) -> Callable:    
    """
    Get the handler function for a registered tool.
    
    Args:
        name (str): The name of the tool.
        
    Returns:
        Callable: The handler function for the tool.
        
    Raises:
        ValueError: If the tool is not registered.
    """
    if not name in tool_registry:
        raise ValueError(f"Tool '{name}' is not registered.")
    
    return tool_registry[name]["handler"]

def get_openai_tools() -> List[Dict]:
    """
    Convert internal tools to OpenAI tool format.
    
    Returns:
        List[Dict]: List of tools in OpenAI format for API calls.
    """
    openai_tools = []
    for tool_name, description in get_available_tools().items():
        openai_tools.append({
            "type": "function",
            "function": {
                "name": tool_name,
                "description": description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The input query for the tool"
                        }
                    },
                    "required": ["query"]
                }
            }
        })
    return openai_tools