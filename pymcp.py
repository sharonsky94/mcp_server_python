# pymcp.py
from mcp_api import TOOLS, send_response
import sys
import json
from tools import search, fetch, pyexec, install  # noqa: F401
from util.logger import log

def run_server():
    for line in sys.stdin:
        if not line.strip():
            continue
        log(f"Received: {line.strip()}")
        try:
            req = json.loads(line)
        except Exception as e:
            log(f"Invalid JSON: {e}")
            send_response(None, error=f"Invalid JSON: {e}")
            continue

        req_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})

        if method == "initialize":
            # Для capabilities.tools - объект
            # LM Studio ожидает объект tools с name+description+inputSchema
            tools_obj = {}
            for key, meta in TOOLS.items():
                tools_obj[meta["name"]] = {
                    "description": meta["description"],
                    "inputSchema": meta["inputSchema"]
                }

            send_response(req_id, result={
                "protocolVersion": "2025-06-18",
                "serverInfo": {
                    "name": "mcp-server-python",
                    "version": "0.1.0"
                },
                "capabilities": {
                    "tools": tools_obj
                }
            })
            continue

        # ИСПРАВЛЕНИЕ: Обрабатываем tools/call вместо callTool
        if method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})

            if tool_name not in TOOLS:
                log(f"Unknown tool: {tool_name}")
                send_response(req_id, error=f"Unknown tool: {tool_name}")
                continue

            try:
                log(f"Calling tool {tool_name} with arguments {arguments}")
                result = TOOLS[tool_name]["func"](**arguments)
                log(f"Tool {tool_name} returned {result}")
                # Формат ответа для tools/call
                send_response(req_id, result={
                    "content": [
                        {
                            "type": "text", 
                            "text": str(result)
                        }
                    ]
                })
            except Exception as e:
                log(f"Tool {tool_name} raised {e}")
                send_response(req_id, error=str(e))
            continue
        
        if method == "notifications/initialized":
            # Просто подтверждаем уведомление, ничего не делаем
            send_response(None, result={"status": "ok"})
            continue

        if method == "tools/list":
            # Для tools/list - массив (как в оригинальной версии)
            tools_info = []
            for key, meta in TOOLS.items():
                tools_info.append({
                    "name": meta["name"],
                    "description": meta["description"],
                    "inputSchema": meta["inputSchema"]
                })

            send_response(req_id, result={"tools": tools_info})
            continue

        # Добавляем обработку неизвестных методов
        if method and method.startswith("notifications/"):
            # Игнорируем неизвестные уведомления
            send_response(None, result={"status": "ok"})
            continue

        send_response(req_id, error=f"Unknown method: {method}")

if __name__ == "__main__":
    run_server()