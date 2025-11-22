# mcp_api.py
import sys
import json
from typing import Callable, Dict
from util.logger import log

# теперь словарь инструментов хранит словарь с метаданными
TOOLS: Dict[str, dict] = {}

def tool(name: str = None, description: str = "", inputSchema: dict = None):
    """
    Декоратор для регистрации инструмента с описанием.
    inputSchema — словарь JSON Schema для аргументов.
    """
    def decorator(func: Callable):
        key = name or func.__name__
        TOOLS[key] = {
            "func": func,
            "name": key,
            "description": description,
            "inputSchema": inputSchema or {}
        }
        return func
    return decorator

def send_response(out_id, result=None, error=None):
    """JSON-RPC 2.0 ответ"""
    msg = {"jsonrpc": "2.0", "id": out_id}
    if error is not None:
        msg["error"] = {"message": str(error)}
    else:
        msg["result"] = result
    s = json.dumps(msg, ensure_ascii=False)
    log(f"Sent: {s}")
    sys.stdout.write(json.dumps(msg, ensure_ascii=False) + "\n")
    sys.stdout.flush()
