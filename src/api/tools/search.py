from api.tools import register_tool

def search_handler(query: str) -> str:
    """
    Simulate a search tool that returns a fixed response.
    
    Args:
        query (str): The search query.
        
    Returns:
        str: A simulated search result.
    """
    return f"Simulated search result for query: {query}"

register_tool(
    name="search",
    description="Search the web for information",
    handler=search_handler
)