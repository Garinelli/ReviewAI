import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

from config import BOT_TOKEN
from broker import message_to_parser_queue

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def start(message: Message):
    WELCOME_MESSAGE = f"""
        Приветствуем вас, {message.from_user.first_name} {message.from_user.last_name}!\nБлагодаря этому боту, вы можете проанализировать все отзывы товарова с маркетпейлсов OZON и Wildberries, указав ссылку на товар.
    """
    await message.answer(WELCOME_MESSAGE)

@dp.message(F.text)
async def link(message: Message):
    await message.answer('Благодарим вас за использование нашего AI бота.')
    await asyncio.sleep(5)
    await message.answer('Производим сбор отзывов...')
    await message_to_parser_queue(link=message.text, user_telegram_id=message.from_user.id)

async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
