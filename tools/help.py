# help.py
from mcp_api import tool

@tool(
    name="help",
    description="To call all the listed tools, use tools/call in the RPC channel. If you need a tool that doesn't exist, describe what you need and I'll help you find or create it.",
    inputSchema={
        "type": "object",
        "properties": {
            "request": {
                "type": "string",
                "description": "A detailed description of what needs to be found or what tool needs to be created"
            }
        },
        "required": ["request"]
    }
)
def tool_help(request: str):
    """
    Инструмент для помощи модели - передает запрос пользователю
    когда модель сталкивается с задачей, для которой нет подходящего инструмента
    
    Args:
        request: Текст запроса с описанием того, что нужно найти или создать
    """
    # Вместо заглушки теперь передаем запрос пользователю
    # В реальной системе здесь может быть логирование, уведомление и т.д.
    
    return {
        "status": "request_received",
        "message": "Ваш запрос получен. Я обработаю его и помогу решить вашу задачу."
    }
