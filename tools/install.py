import subprocess
from mcp_api import tool
import sys

@tool(
    name="install",
    description="Installs a Python package using pip.",
    inputSchema={
        "type": "object",
        "properties": {
            "package": {"type": "string", "description": "Name of the Python package to install"}
        },
        "required": ["package"]
    }
)
def tool_install(package: str):
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", package],
        capture_output=True, text=True
    )
    return {"stdout": result.stdout, "stderr": result.stderr, "code": result.returncode}
