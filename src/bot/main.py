import asyncio
from aiogram import Bot, Dispatcher
# from aiogram.filters import Command
# from aiogram.types import Message, CallbackQuery

import imports_conf  # ОБЯЗАТЕЛЬНО ДЛЯ VS CODE

from src.bot.bot_utils.link_checker import check_link
from src.bot.bot_utils.task_id_generator import generate_task_id

# from src.bot.bot_utils.status_sender import send_request_status
from src.bot.handlers.start_handler import setup_start_handlers
from src.bot.handlers.link_handler import setup_link_handler
from src.bot.config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
semaphore = asyncio.Semaphore(5)

setup_start_handlers(dp, bot)
setup_link_handler(dp, semaphore, check_link, generate_task_id)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
