import json
import asyncio
import aio_pika

from aiogram import Bot
bot = Bot(token="qwe")


RABBITMQ_URL = "amqp://guest:guest@localhost/"

async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        body = message.body.decode()
        body = json.loads(body)
        result_message = f'Количество накрученных отзывов: {body["result"]}'
        await bot.send_message(
            chat_id=body['user_telegram_id'],
            text='Результат получен...'
        )
        await asyncio.sleep(5)
        await bot.send_message(body['user_telegram_id'], result_message)
        print(f"Получено сообщение: {body}")


async def message_consumer():
    connection = await aio_pika.connect(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("bot")

        await queue.consume(process_message)

        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(message_consumer())