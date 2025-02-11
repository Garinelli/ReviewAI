import json
import asyncio
import aio_pika
from nn_producer import message_to_bot_queue
from bot_consumer import bot

RABBITMQ_URL = "amqp://guest:guest@localhost/"

async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        body = message.body.decode()
        body = json.loads(body)
        print(f"Получено сообщение: {body}")
        await bot.send_message(
            chat_id=body['user_telegram_id'],
            text='Искуственный интелект предсказывает результат...'
        )
        await asyncio.sleep(5)
        await message_to_bot_queue(result='5%', user_telegram_id=body['user_telegram_id'])


async def message_consumer():
    connection = await aio_pika.connect(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("NN")

        await queue.consume(process_message)

        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(message_consumer())