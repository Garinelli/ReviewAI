import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from broker import message_to_parser_queue
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: Message):
    # Создаем inline-кнопку
    button = InlineKeyboardButton(text="Понятно ✅", callback_data="start_button")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
    WELCOME_MESSAGE = f"""
👋 Привет, {message.from_user.first_name}! Я — бот, который помогает анализировать отзывы на товары с маркетплейсов.

📊 Моя задача — предсказать, сколько отзывов могут быть накрученными (сгенерированными нейросетью). Однако важно помнить, что это всего лишь прогноз, основанный на анализе данных. Мои выводы могут быть неточными, и я не могу гарантировать 100% точность.
    """
    await message.answer(WELCOME_MESSAGE, reply_markup=keyboard)


# Обработчик нажатия на inline-кнопку
@dp.callback_query(F.data == "start_button")
async def process_callback_button(callback_query: CallbackQuery):
    # Отправляем сообщение о том, что кнопка нажата
    await bot.answer_callback_query(callback_query.id)
    text = "🔍 Чтобы начать, просто отправь мне ссылку на товар c Ozon или Wildberries. Я проанализирую отзывы и сообщу тебе результат!"
    await bot.send_message(callback_query.from_user.id, text)


@dp.message(F.text)
async def link(message: Message):
    await message.answer(
        "Благодарим вас за использование нашего AI бота.\nВаша задача отправлена в очередь!"
    )
    await asyncio.sleep(2)
    await message.answer("📝Производим сбор отзывов...")
    await message_to_parser_queue(
        link=message.text, user_telegram_id=message.from_user.id
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
