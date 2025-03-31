import asyncio
from aiogram import Bot, Dispatcher

from src.bot.bot_utils.link_checker import check_link
from src.bot.bot_utils.task_id_generator import generate_task_id

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
