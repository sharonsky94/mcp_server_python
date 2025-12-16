from typing import Dict, Any
import requests
from io import BytesIO
from pdfminer.high_level import extract_text as pdf_extract_text
from util.logger import log
from mcp_api import tool
from util.http import get
from bs4 import BeautifulSoup
import chardet
from typing import Optional

@tool(
    name="fetch",
    description="Fetch and extract plain text from web pages or PDF files.",
    inputSchema={
        "type": "object",
        "properties": {
            "url": {
                "type": "string", 
                "description": "The URL to fetch",
                "format": "uri"
            }
        },
        "required": ["url"],
        "additionalProperties": False
    }
)
def tool_fetch(url: str) -> Dict[str, Any]:
    """
    Fetch and extract plain text from web pages or PDF files.
    
    Now supports:
    - HTML web pages
    - PDF files with text layer
    """
       # Валидация URL (базовая проверка)
    if not url or not isinstance(url, str):
        log(f"Invalid URL provided: {url}")
        return {"error": "Invalid URL format"}
    
    # Проверка на стандартные схемы
    if not url.lower().startswith(('http://', 'https://')):
        log(f"URL may be invalid (missing http/https): {url}")
    
    try:
        log(f"Fetching resource: {url}")
        
        # Определяем тип контента
        content_type = _detect_content_type(url)
        
        if 'application/pdf' in content_type or url.lower().endswith('.pdf'):
            # Обрабатываем PDF
            return _fetch_and_extract_pdf(url)
        else:
            # Старая логика для HTML
            return _fetch_html_page(url)
    
    except Exception as e:
        log(f"Fatal error: {str(e)}")
        return {"error": f"Failed to fetch and process content: {str(e)}"}

def _detect_content_type(url: str) -> str:
    """Detect content type of the URL."""
    try:
        response = requests.head(url, timeout=10)
        content_type = response.headers.get('Content-Type', '')
        log(f"Detected content type: {content_type}")
        return content_type
    except Exception as e:
        log(f"Error detecting content type: {str(e)}")
        return ""

def _fetch_and_extract_pdf(url: str) -> Dict[str, Any]:
    """Fetch and extract text from PDF file."""
    try:
        response = requests.get(url, stream=True, timeout=30)
        
        if response.status_code != 200:
            return {"error": f"HTTP error {response.status_code}"}
        
        # Читаем содержимое как байты
        pdf_content = response.content
        
        # Используем BytesIO для передачи в pdfminer
        with BytesIO(pdf_content) as pdf_file:
            try:
                # Извлекаем текст из PDF
                text = pdf_extract_text(pdf_file, codec='utf-8')
                
                # Очищаем текст от лишних пробелов и переносов
                lines = [line.strip() for line in text.split('\n') if line.strip()]
                cleaned_text = '\n'.join(lines)
                
                log(f"PDF extracted successfully. Text length: {len(cleaned_text)}")
                
                return {
                    "url": url,
                    "text": cleaned_text,
                    "metadata": {
                        "file_type": "pdf",
                        "content_length": len(pdf_content),
                        "text_extraction_method": "pdfminer"
                    }
                }
            except Exception as e:
                return {"error": f"PDF extraction failed: {str(e)}"}
    
    except Exception as e:
        return {"error": f"PDF fetch failed: {str(e)}"}

def _fetch_html_page(url: str) -> Dict[str, Any]:
    """Old HTML fetching logic - keep this for web pages."""
    try:
        response = get(url)
        
        if response is None:
            return {"error": "Empty response"}
        
        html_content = _decode_response(response)
        if html_content is None:
            return {"error": "Failed to decode content"}
        
        plain_text = _extract_plain_text(html_content)
        
        # Проверяем, не пустой ли результат
        if not plain_text or plain_text.isspace():
            log(f"Extracted text is empty for URL: {url}")
            return {"url": url, "text": "", "warning": "No text content found"}
        
        # Логируем успех
        log(f"Successfully fetched and extracted text from {url}")
        log(f"Text length: {len(plain_text)} characters")
        
        return {
            "url": url,
            "text": plain_text,
            "metadata": {
                "text_length": len(plain_text),
                "character_encoding": html_content.encoding if hasattr(html_content, 'encoding') else 'unknown'
            }
        }
    
    except ConnectionError as e:
        log(f"Connection error fetching {url}: {str(e)}")
        return {"error": f"Connection error: {str(e)}"}
    
    except TimeoutError as e:
        log(f"Timeout error fetching {url}: {str(e)}")
        return {"error": f"Request timeout: {str(e)}"}
    
    except Exception as e:
        log(f"Unexpected error fetching {url}")
        return {"error": f"Failed to fetch page: {str(e)}"}

# Не забудьте добавить необходимые пакеты в зависимости
# Можете использовать tool "install" для установки:
# - pdfminer.six
# - python-magic (для лучшей детекции типов)

def _decode_response(response) -> Optional[str]:
    """
    Декодирует ответ в строку с автоматическим определением кодировки.
    
    Args:
        response: Ответ от HTTP-запроса
        
    Returns:
        Декодированная строка или None при ошибке
    """
    try:
        # Если уже строка
        if isinstance(response, str):
            return response
        
        # Если bytes - определяем кодировку
        elif isinstance(response, bytes):
            # Используем chardet для определения кодировки
            detected = chardet.detect(response)
            encoding = detected.get('encoding', 'utf-8')
            confidence = detected.get('confidence', 0)
            
            log(f"Detected encoding: {encoding} (confidence: {confidence:.2f})")
            
            # Список кодировок для попытки
            encodings_to_try = []
            
            # Используем обнаруженную кодировку, если уверенность высокая
            if confidence > 0.7 and encoding:
                encodings_to_try.append(encoding)
            
            # Добавляем наиболее распространенные кодировки
            encodings_to_try.extend(['utf-8', 'latin-1', 'cp1251', 'cp1252', 'iso-8859-1'])
            
            # Убираем дубликаты
            encodings_to_try = list(dict.fromkeys(encodings_to_try))
            
            # Пробуем декодировать
            for enc in encodings_to_try:
                try:
                    decoded = response.decode(enc, errors='strict')
                    log(f"Successfully decoded using {enc}")
                    return decoded
                except (UnicodeDecodeError, LookupError) as e:
                    log(f"Failed to decode with {enc}: {e}")
                    continue
            
            # Если все попытки не удались, используем replace
            log("All decoding attempts failed, using errors='replace'")
            return response.decode('utf-8', errors='replace')
        
        else:
            # Если другой тип, преобразуем в строку
            return str(response)
    
    except Exception as e:
        log(f"Error decoding response: {str(e)}")
        return None


def _extract_plain_text(html_content: str) -> str:
    """
    Извлекает чистый текст из HTML с дополнительной очисткой.
    
    Args:
        html_content: HTML строка
        
    Returns:
        Очищенный текст
    """
    try:
        # Используем более устойчивый парсер
        soup = BeautifulSoup(html_content, 'lxml')
        
        # Удаляем скрипты и стили
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Получаем текст с разделителями
        text = soup.get_text(separator='\n', strip=True)
        
        # Дополнительная очистка: удаляем лишние пустые строки
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Объединяем обратно с одним переносом строки между абзацами
        cleaned_text = '\n'.join(lines)
        
        return cleaned_text
    
    except Exception as e:
        log(f"Error extracting text: {str(e)}")
        # Если BeautifulSoup не работает, попробуем простую очистку
        try:
            # Базовая очистка HTML тегов (очень простая, на крайний случай)
            import re
            cleaned = re.sub(r'<[^>]+>', '\n', html_content)
            cleaned = re.sub(r'\n\s*\n+', '\n', cleaned)
            return cleaned.strip()
        except Exception:
            return html_content
