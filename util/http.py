# http.py
import requests

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; MCP-Server/1.0)"
}

def get(url: str, timeout: int = 10, headers: dict = None) -> str:
    """
    Простая обёртка над requests.get
    Возвращает текст страницы или бросает исключение.
    """
    h = DEFAULT_HEADERS.copy()
    if headers:
        h.update(headers)

    resp = requests.get(url, headers=h, timeout=timeout)
    resp.raise_for_status()  # генерирует ошибку, если код != 200
    return resp.text
