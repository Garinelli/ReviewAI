import os
import logging
from aiogram.types import FSInputFile
from aiogram import Bot


async def send_request_status(
    bot: Bot, user_telegram_id: int, message: str, task_id=None
) -> None:
    """Отправляет статус запроса пользователю"""
    logging.info("Отправляем пользователю ответ по статусу...")
    await bot.send_message(chat_id=user_telegram_id, text=message)
    if task_id is not None:
        logging.info("Пытаемся отправить фотку")
        await bot.send_photo(
            chat_id=user_telegram_id, photo=FSInputFile(f"{task_id}.png")
        )
        os.remove(f"{task_id}.png")
    logging.info("Сообщения успешно отправлены ✅\n")
