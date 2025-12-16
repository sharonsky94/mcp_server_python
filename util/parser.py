from bs4 import BeautifulSoup
import urllib.parse

def parse_ddg_lite(html: str, limit: int = 5):
    """
    Парсит страницу поиска DuckDuckGo Lite.
    Возвращает список результатов вида:
    [
        {"title": "...", "url": "..."},
        ...
    ]
    """

    soup = BeautifulSoup(html, "html.parser")
    results = []
    
    for a in soup.select("a.result-link"):
        original_url = a.get("href")
        
        # Внутри цикла после получения original_url
        if "&rut=" in original_url:
            original_url = original_url.split("&rut=")[0]

        # Если это перенаправление DuckDuckGo, извлекаем оригинальный URL
        if "/l/?uddg=" in original_url:
            # Извлекаем значение uddg
            param_start = original_url.find("uddg=") + len("uddg=")
            if param_start > 0:
                uddg_param = original_url[param_start:]
                # Декодируем URL
                try:
                    decoded_url = urllib.parse.unquote(uddg_param)
                    # Убираем возможные дополнительные параметры
                    if "?" in decoded_url:
                        decoded_url = decoded_url.split("?")[0]
                    original_url = decoded_url
                except:
                    pass
        
        title = a.get_text(strip=True)
        
        if not title or not original_url:
            continue

        results.append({
            "title": title,
            "url": original_url
        })

        if len(results) >= limit:
            break

    return results

