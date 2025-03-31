import logging
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram import Bot, Dispatcher, F
from ..constants import WELCOME_MESSAGE, START_MESSAGE

# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
#     from src.bot.main import Bot


def setup_start_handlers(dp: Dispatcher, bot: Bot):
    @dp.message(Command("start"))
    async def start(message):
        logging.info(f"Отвечаем на команду /start {message.from_user.id=}...")
        logging.info("Создаем inline-кнопку...")
        button = InlineKeyboardButton(text="Понятно ✅", callback_data="start_button")
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
        logging.info("Клавиатура успешно создана")
        await message.answer(
            WELCOME_MESSAGE.format(message.from_user.first_name), reply_markup=keyboard
        )
        logging.info("Сообщение WELCOME_MESSAGE успешно отправлено ✅\n")

    @dp.callback_query(F.data == "start_button")
    async def process_callback_button(callback_query):
        logging.info(
            f"Обрабатываем нажатие кнопки старт {callback_query.from_user.id=}..."
        )
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, START_MESSAGE)
        logging.info("Сообщение START_MESSAGE успешно отправлено ✅\n")
