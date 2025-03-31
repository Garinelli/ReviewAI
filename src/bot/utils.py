import re
import random

from src.bot.constants import LINK_PATTERN, TASK_ID_LETTERS
from src.bot.log_conf import logging

def check_link(link: str) -> bool:
    # Проверяем ссылку на WB
    logging.info(f"Начинаем обрабатывать ссылку на товар {link=}...")
    return re.fullmatch(LINK_PATTERN, link) is not None

def generate_task_id() -> str:
    logging.info("Генерируется id для таски...")
    task_id = ""
    for _ in range(8):
        task_id += random.choice(TASK_ID_LETTERS)
    logging.info(f"ID для таски сгенерирован успешно: {task_id=}")
    return task_id
