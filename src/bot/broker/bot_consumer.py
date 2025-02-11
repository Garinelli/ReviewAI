import asyncio
import aio_pika

RABBITMQ_URL = "amqp://guest:guest@localhost/"

async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        print(f"Получено сообщение: {message.body.decode()}")

async def message_consumer():
    connection = await aio_pika.connect(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("bot")

        await queue.consume(process_message)

        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(message_consumer())