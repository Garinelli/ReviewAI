import asyncio
import logging
from asyncio import Semaphore
from aiogram import Dispatcher, F
from aiogram.types import Message
from src.bot.broker import send_message_to_broker
from src.bot.log_conf import timing_decorator


def setup_link_handler(
    dp: Dispatcher,
    semaphore: Semaphore,
    check_link_func: callable,
    generate_task_id_func: callable,
):
    @dp.message(F.text)
    async def link(message: Message):
        logging.info(
            f"Пользователь {message.from_user.id=} отправил сообщение {message.text=}"
        )
        logging.info("Запускаем проверку на ссылку...")
        if not check_link_func(message.text):
            await message.reply(
                "Это не совсем то, что мне нужно(\nОтправьте ссылку на главную страницу товара!"
            )
            logging.info(
                f"Отправлено сообщение о том, что ссылка не распознана {message.from_user.id=}\n"
            )
        else:
            async with semaphore:
                await message.answer(
                    "Благодарим вас за использование нашего AI бота.\nВаша задача отправлена в очередь!"
                )
                await asyncio.sleep(2)
                logging.info(
                    "Ссылка распознана, отправляем сообщение о начале сбора отзывов..."
                )
                await message.answer("📝Производим сбор отзывов...")
                # await (timing_decorator(send_message_to_broker))(
                #     queue_name="parser",
                #     link=message.text,
                #     user_telegram_id=message.from_user.id,
                #     task_id=generate_task_id_func(),
                # )
