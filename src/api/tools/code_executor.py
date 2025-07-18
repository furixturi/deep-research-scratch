from api.tools.registry import register_tool


def code_handler(code: str) -> str:
    return f"Code executor stub, executed code: {code}"


# Register with explicit parameters schema
register_tool(
    name="code",
    description="Execute Python code",
    handler=code_handler,
    parameters={
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "The Python code to execute",
            }
        },
        "required": ["code"],
    },
)
