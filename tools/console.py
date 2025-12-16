# console.py
from mcp_api import tool
import subprocess
from typing import Dict

@tool(
    name="console",
    description="Executes shell commands with error handling. Each invocation is a separate script, so the entire command chain must be written at once. Example: 'mkdir -p test_dir && cd test_dir && touch file.txt'.",
    inputSchema={
        "type": "object",
        "properties": {
            "command": {"type": "string", "description": "Shell command to execute"}
        },
        "required": ["command"]
    }
)
def tool_console(command: str) -> Dict[str, str]:
    """
    Executes shell commands with error handling and preserves cd transitions.
    
    Args:
        command (str): Shell command string (e.g., 'cd dir && mkdir -p src')

    Returns:
        dict: Output of the command, current directory after execution
    """
    try:
        # Выполняем команду с shell=True для поддержки &&, || и т.д.
        result = subprocess.run(
            command,
            shell=True,  # Важно! Для работы with &&, ||, pipe и др.
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            cwd='.',
            timeout=30
        )
   
        return {
            "output": result.stdout,
            "current_directory": "/home/d/.lmstudio/extensions/plugins/mcp/mcp-server-python/"
        }

    except FileNotFoundError:
        return {"error": "Command not found. Please check the command name."}
    except PermissionError:
        return {"error": "Permission denied. Cannot execute this command."}
    except subprocess.TimeoutExpired:
        return {"error": "Command timed out after 30 seconds"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

