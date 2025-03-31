import logging


def check_link(link: str) -> bool:
    """Проверяет ссылку на WB"""
    logging.info(f"Начинаем обрабатывать ссылку на товар {link=}...")
    if ("wildberries.ru" in link) and ("detail.aspx" in link):
        logging.info(f"Ссылка {link} распознана WB ✅\n")
        return True
    logging.info(f"Строка {link} не распознана как ссылка на товар ❌")
    return False
