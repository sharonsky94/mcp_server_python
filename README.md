# MCP_server_Python – универсальный MCP сервер на Python

**MCP_server_Python** — лёгкий и универсальный сервер MCP, который позволяет добавлять инструменты для LM Studio. Поддерживает:

* Поиск и парсинг страниц
* Выполнение произвольного Python кода
* Установку Python пакетов через `pip`

## Структура проекта

```
mcp_server_python/
├── pymcp.py          # основной сервер MCP
├── README.md
├── requirements.txt  # зависимости
├── tools/            # инструменты
│   ├── fetch.py
│   ├── pyexec.py
│   ├── search.py
│   └── __init__.py
└── util/             # вспомогательные функции
    ├── http.py
    └── parser.py
```

## Установка

1. Клонируем репозиторий:

```bash
git clone https://github.com/sharonsky94/mcp_server_python.git
cd mcp_server_python
```

2. Создаём виртуальное окружение и активируем его:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Устанавливаем зависимости:

```bash
pip install -r requirements.txt
```

## Настройка LM Studio

Добавьте MCP сервер в файл:

```
/home/yourusername/.lmstudio/mcp.json
```

Пример:

```json
{
  "mcpServers": {
    "mcp-server-python": {
      "command": "/path/to/mcp_server_python/.venv/bin/python",
      "args": [
        "/path/to/mcp_server_python/pymcp.py"
      ]
    }
  }
}
```

> Обратите внимание: `"mcp-server-python"` — это имя сервера, можно менять по желанию.

## Использование инструментов

### 1. Установка Python пакета

```xml
<tool_call name="install">
requests
</tool_call>
```

### 2. Выполнение Python кода

```xml
<tool_call name="python">
x = 2 + 2
</tool_call>
```

### 3. Поиск и просмотр страниц

* Поиск: `tools/search.py`
* Загрузка страницы: `tools/fetch.py`

> Все инструменты регистрируются через декоратор `@tool` в `pymcp.py`.

## Архитектура

* Все инструменты хранятся в `tools/`, вспомогательные функции в `util/`
* MCP сервер ждёт JSON через stdin и возвращает JSON через stdout
* Можно добавлять новые инструменты просто добавляя файлы в `tools/` и регистрируя их через `@tool`
