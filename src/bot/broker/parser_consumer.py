import json
import asyncio
import aio_pika

from parser_producer import message_to_preprocessing_queue

RABBITMQ_URL = "amqp://guest:guest@localhost/"

async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        body = message.body.decode()
        body = json.loads(body)
        print(f"Получено сообщение: {body}")
        await asyncio.sleep(2)
        await message_to_preprocessing_queue(df_name='data.csv', user_telegram_id=body['user_telegram_id'])

async def message_consumer():
    connection = await aio_pika.connect(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("parser")

        await queue.consume(process_message)

        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(message_consumer())