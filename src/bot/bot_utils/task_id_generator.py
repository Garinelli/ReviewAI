import random
import logging
from src.bot.constants import TASK_ID_LETTERS


def generate_task_id() -> str:
    """Генерирует ID для задачи"""
    logging.info("Генерируется id для таски...")
    task_id = ""
    for _ in range(8):
        task_id += random.choice(TASK_ID_LETTERS)
    logging.info(f"ID для таски сгенерирован успешно: {task_id=}")
    return task_id
