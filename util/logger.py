# logger.py
import logging

logging.basicConfig(
    filename="pymcp.log",  # файл логов
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def log(msg):
    logging.debug(msg)
