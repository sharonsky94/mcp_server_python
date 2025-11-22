from mcp_api import tool
from util.http import get
from util.parser import parse_ddg_lite

@tool(
    name="search",
    description="Performs a DuckDuckGo Lite search and returns the results.",
    inputSchema={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Search query"},
            "limit": {"type": "integer", "description": "Maximum number of results", "default": 5}
        },
        "required": ["query"]
    }
)
def tool_search(query: str, limit: int = 5):
    html = get("https://lite.duckduckgo.com/lite/?q=" + query)
    items = parse_ddg_lite(html, limit)
    return items
