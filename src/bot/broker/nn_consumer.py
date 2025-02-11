import asyncio
import aio_pika
from nn_producer import message_to_bot_queue

RABBITMQ_URL = "amqp://guest:guest@localhost/"

async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        print(f"Получено сообщение: {message.body.decode()}")
        await asyncio.sleep(2)
        await message_to_bot_queue(result='some text..', user_telegram_id=123)

async def message_consumer():
    connection = await aio_pika.connect(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("NN")

        await queue.consume(process_message)

        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(message_consumer())