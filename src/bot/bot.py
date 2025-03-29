import os
import re 
import asyncio
import random

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .broker import send_message_to_broker
from .config import BOT_TOKEN
from .constants import TASK_ID_LETTERS, WELCOME_MESSAGE, START_MESSAGE
from .log_conf import logging, timing_decorator


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

semaphore = asyncio.Semaphore(5)
LINK_PATTERN = r'^https://www\.wildverries\.ru/catalog/\d+/detail\.aspx$'

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


async def send_request_status(
    user_telegram_id: int, message: str, task_id=None
) -> None:
    logging.info("Отправляем пользователю ответ по статусу...")
    await bot.send_message(chat_id=user_telegram_id, text=message)
    if not task_id is None:
        logging.info("Пытааемся отправить фотку")
        await bot.send_photo(
            chat_id=user_telegram_id, photo=FSInputFile(f"{task_id}.png")
        )
        os.remove(f"{task_id}.png")
    logging.info("Сообщения успешно отправлены ✅\n")


@dp.message(Command("start"))
async def start(message: Message):
    # Создаем inline-кнопку
    logging.info(f"Отвечаем на команду /start {message.from_user.id=}...")
    logging.info("Создаем inline-кнопку...")
    button = InlineKeyboardButton(text="Понятно ✅", callback_data="start_button")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
    logging.info("Клавиатура успешно создана")
    await message.answer(
        WELCOME_MESSAGE.format(message.from_user.first_name), reply_markup=keyboard
    )
    logging.info("Сообщение WELCOME_MESSAGE успешно отправлено ✅\n")


# Обработчик нажатия на inline-кнопку
@dp.callback_query(F.data == "start_button")
async def process_callback_button(callback_query: CallbackQuery):
    # Отправляем сообщение о том, что кнопка нажата
    logging.info(f"Обрабатываем нажатие кнопки старт {callback_query.from_user.id=}...")
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, START_MESSAGE)
    logging.info("Сообщение START_MESSAGE успешно отправлено ✅\n")


@dp.message(F.text)
async def link(message: Message):
    logging.info(
        f"Пользователь {message.from_user.id=} отправил сообщение {message.text=}"
    )
    logging.info("Запускаем проверку на ссылку...")
    if check_link(message.text) is False:
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
            # Применяем декоратор к функции
            await (timing_decorator(send_message_to_broker))(
                queue_name="parser",
                link=message.text,
                user_telegram_id=message.from_user.id,
                task_id=generate_task_id(),
            )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
