from tools import register_tool

def code_handler(code: str) -> str:
    return f"Code executor stub, executed code: {code}"

register_tool(
    name="code",
    description="Execute Python code",
    handler=code_handler
)