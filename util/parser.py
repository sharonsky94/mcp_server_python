from bs4 import BeautifulSoup

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

    # В DDG Lite результаты лежат в таблице, ссылки в <a class="result-link">
    for a in soup.select("a.result-link"):
        title = a.get_text(strip=True)
        url = a.get("href")

        if not title or not url:
            continue

        results.append({
            "title": title,
            "url": url
        })

        if len(results) >= limit:
            break

    return results
