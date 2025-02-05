import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

from config import BOT_TOKEN
from broker import send_link_message

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
    await message.answer('Задача отправлена в очередь')

async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
