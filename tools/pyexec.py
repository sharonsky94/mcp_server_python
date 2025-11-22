from mcp_api import tool

@tool(
    name="python",
    description="Executes Python code and returns the local scope.",
    inputSchema={
        "type": "object",
        "properties": {
            "code": {"type": "string", "description": "Python code to execute"}
        },
        "required": ["code"]
    }
)
def tool_pyexec(code: str):
    try:
        local_scope = {}
        exec(code, {}, local_scope)
        return {"result": local_scope}
    except Exception as e:
        return {"error": str(e)}
