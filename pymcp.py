from tools.search import tool_search
from tools.fetch import tool_fetch
from tools.pyexec import tool_pyexec

TOOLS = [
    tool_search,
    tool_fetch,
    tool_pyexec,
]

if __name__ == "__main__":
    from mcp import run_server
    run_server(TOOLS)

