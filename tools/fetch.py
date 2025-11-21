from mcp import tool
from util.http import get

@tool(name="fetch")
def tool_fetch(url: str):
    content = get(url)
    return {"url": url, "content": content}

