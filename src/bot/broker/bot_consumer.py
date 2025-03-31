import asyncio
import json

import aio_pika

from src.bot.config import RABBITMQ_URL
from src.bot.bot import send_request_status


async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        body = message.body.decode()
        body = json.loads(body)
        result_message = body["result"]
        await send_request_status(
            body['user_telegram_id'],
            '✅Результат получен...'
        )
        await asyncio.sleep(3)
        await send_request_status(body['user_telegram_id'], result_message, body['task_id'])
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