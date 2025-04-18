import os
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from src.bot.broker import send_message_to_broker
from src.bot.config import BOT_TOKEN
from src.bot.constants import (WELCOME_MESSAGE, START_MESSAGE, SUBMITTING_TASK_MESSAGE, 
                               BAD_LINK_MESSAGE, FEEDBACK_ENTER_MESSAGE, FEEDBACK_THANK_YOU_MESSAGE,
                               PRODUCT_LINK)
from src.bot.log_conf import logging, timing_decorator
from src.bot.utils import link_validation, generate_task_id, is_article
from src.bot.db import insert_feedback, create_tables, delete_tables


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


class CreateFeedback(StatesGroup):
    command_entered = State() 


async def send_review_graph(user_telegram_id: int, task_id: str) -> None:
    logging.info("Пытааемся отправить фотку")
    await bot.send_photo(
            chat_id=user_telegram_id, photo=FSInputFile(f"{task_id}.png")
        )
    os.remove(f"{task_id}.png")


async def send_request_status(
    user_telegram_id: int, message: str, task_id: str=None
) -> None:
    logging.info("Отправляем пользователю ответ по статусу...")
    await bot.send_message(chat_id=user_telegram_id, text=message)

    if task_id is not None:
        await send_review_graph(user_telegram_id, task_id)
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


@dp.message(Command("feedback"))
async def start_feedback(message: Message, state: FSMContext):
    await message.answer(FEEDBACK_ENTER_MESSAGE)
    await state.set_state(CreateFeedback.command_entered)


@dp.message(CreateFeedback.command_entered, F.text)
async def upload_feedback(message: Message, state: FSMContext):
    insert_feedback(message.text)
    await message.answer(FEEDBACK_THANK_YOU_MESSAGE)
    await state.clear()


@dp.message(F.text)
async def link(message: Message):
    logging.info(
        f"Пользователь {message.from_user.id=} отправил сообщение {message.text=}"
    )
    logging.info("Запускаем проверку на ссылку...")

    if link_validation(message.text) is not False:
        link = message.text
    elif is_article(message.text) is not False:
        link = PRODUCT_LINK.format(message.text)
    else:   
        await message.reply(BAD_LINK_MESSAGE)
        logging.info(
            f"Отправлено сообщение о том, что ссылка не распознана {message.from_user.id=}\n"
        )
        return 
    
    task_id = generate_task_id()
    await message.answer(SUBMITTING_TASK_MESSAGE.format(task_id))
    await asyncio.sleep(1)
    logging.info(
        "Ссылка распознана, отправляем сообщение о начале сбора отзывов..."
    )
    # Применяем декоратор к функции
    await (timing_decorator(send_message_to_broker))(
        queue_name="parser",
        link=link,
        user_telegram_id=message.from_user.id,
        task_id=task_id,
    )


async def main():
    # delete_tables()
    # create_tables()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
