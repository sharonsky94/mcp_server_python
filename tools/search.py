from mcp import tool
from util.http import get
from util.parser import parse_ddg_lite

@tool(name="search")
def tool_search(query: str, limit: int = 5):
    html = get("https://lite.duckduckgo.com/lite/?q=" + query)
    items = parse_ddg_lite(html, limit)
    return items

