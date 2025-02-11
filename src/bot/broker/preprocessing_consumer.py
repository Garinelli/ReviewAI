import json
import asyncio
import aio_pika

from preprocessing_producer import message_to_NN_queue
from bot_consumer import bot
RABBITMQ_URL = "amqp://guest:guest@localhost/"

async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        body = message.body.decode()
        body = json.loads(body)
        print(f"Получено сообщение: {body}")
        await bot.send_message(
            chat_id=body['user_telegram_id'],
            text='Обрабатываем естественный язык...'
        )
        await asyncio.sleep(5)
        await message_to_NN_queue(df_name=body['df_name'], user_telegram_id=body['user_telegram_id'])

async def message_consumer():
    connection = await aio_pika.connect(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("preprocessing")

        await queue.consume(process_message)

        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(message_consumer())