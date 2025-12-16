# pyexec.py
from mcp_api import tool
import io
import contextlib
import sys
import ast
from util.logger import log

'''def tool_pyexec(code: str):
    try:
        local_scope = {}
        output_buffer = io.StringIO()
        
        # Вариант 1: Используем системные глобальные переменные
        # Это даст доступ ко ВСЕМ модулям Python
        global_scope = {
            '__builtins__': builtins,
            '__name__': '__main__',
            '__import__': __import__,  # Ключевое: даем доступ к импорту
            '__doc__': None,
            '__package__': None,
            '__loader__': None,
            '__spec__': None,
            '__annotations__': {},
            '__file__': None,
        }
        
        # Вариант 2: Или еще проще - используем текущие глобальные переменные
        # global_scope = globals().copy()
        
        # Перехват stdout
        with contextlib.redirect_stdout(output_buffer):
            exec(code, global_scope, local_scope)
        
        output = output_buffer.getvalue()
        return {"result": local_scope, "output": output}
        
    except Exception as e:
        return {"error": str(e), "type": type(e).__name__}
'''

@tool(
    name="python",
    description="Executes Python code and returns the local scope *and* captured stdout. To see the answer, be sure to save function calls in variables or use print().",
    inputSchema={
        "type": "object",
        "properties": {
            "code": {"type": "string", "description": "Python code to execute"}
        },
        "required": ["code"]
    }
)
def tool_pyexec(code: str):
    try:
        # Шаг 1: Собираем все импорты из кода
        tree = ast.parse(code)

        # Множество импортов (базовые названия модулей)
        required_modules = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    required_modules.add(alias.name.split('.')[0])  # Только корень
            elif isinstance(node, ast.ImportFrom):
                module_name = node.module
                if module_name is not None:
                    required_modules.add(module_name.split('.')[0])

        # Шаг 2: Загружаем недостающие модули
        loaded_modules = {}
        for mod in sorted(required_modules):  # Сортируем, чтобы избежать порядка
            try:
                if mod not in sys.modules:
                    module = __import__(mod)
                    loaded_modules[mod] = module
                else:
                    loaded_modules[mod] = sys.modules[mod]
            except Exception as e:
                log(f"Error in python tool: ⚠️ Failed to load module '{mod}': {e}")

        # Шаг 3: Готовим глобальный контекст с доступом к системным модулям
        global_scope = {
            '__builtins__': __builtins__,
            '__import__': __import__,
            '__name__': '__main__',
            '__doc__': None,
            '__package__': None,
            '__loader__': None,
            '__spec__': None,
            '__annotations__': {},
            '__file__': None,
        }

        # Добавляем загруженные модули
        for name, mod in loaded_modules.items():
            global_scope[name] = mod

        # Шаг 4: Выполняем код в изолированной среде
        local_scope = {}
        output_buffer = io.StringIO()

        # Перехват stdout
        with contextlib.redirect_stdout(output_buffer):
            exec(code, global_scope, local_scope)

        output = output_buffer.getvalue()
        return {"result": local_scope, "output": output}

    except Exception as e:
        return {"error": str(e), "type": type(e).__name__}