import functools
import time
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    filename=f"{Path(__file__).parent.parent.parent}/py_log.log",
    filemode="w",
    format="%(asctime)s %(levelname)s %(message)s",
)


def timing_decorator(func):
    """Декоратор для замера времени выполнения функции"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"\nНачало выполнения функции '{func.__name__}'")
        start_time = time.time()

        result = func(*args, **kwargs)

        end_time = time.time()
        elapsed_time = end_time - start_time
        logging.info(
            f"Функция '{func.__name__}' выполнена за {elapsed_time:.6f} секунд\n\n"
        )
        return result

    return wrapper
