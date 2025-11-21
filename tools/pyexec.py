from mcp import tool

@tool(name="python")
def tool_pyexec(code: str):
    try:
        local_scope = {}
        exec(code, {}, local_scope)
        return {"result": local_scope}
    except Exception as e:
        return {"error": str(e)}

