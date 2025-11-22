from mcp_api import tool
from util.http import get

@tool(
    name="fetch",
    description="Fetches the content of a given URL.",
    inputSchema={
        "type": "object",
        "properties": {
            "url": {"type": "string", "description": "The URL to fetch"}
        },
        "required": ["url"]
    }
)
def tool_fetch(url: str):
    content = get(url)
    return {"url": url, "content": content}
