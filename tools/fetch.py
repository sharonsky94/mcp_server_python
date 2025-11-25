from mcp_api import tool
from util.http import get
from bs4 import BeautifulSoup

@tool(
    name="fetch",
    description="Fetches web page content and returns only plain text (without HTML tags).",
    inputSchema={
        "type": "object",
        "properties": {
            "url": {"type": "string", "description": "The URL to fetch"}
        },
        "required": ["url"]
    }
)
def tool_fetch(url: str):
    html = get(url)
    
    # Парсим HTML и извлекаем чистый текст
    soup = BeautifulSoup(html, "html.parser")
    plain_text = soup.get_text(separator='\n', strip=True)
    
    return {"url": url, "text": plain_text}

