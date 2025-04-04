import json
import aio_pika

from src.bot.config import RABBITMQ_URL

async def send_message_to_broker(**kwargs):
    connection = await aio_pika.connect_robust(RABBITMQ_URL)

    async with connection:
        channel = await connection.channel()
        await channel.declare_queue(kwargs['queue_name'])

        body_ = json.dumps(kwargs)

        await channel.default_exchange.publish(
            aio_pika.Message(body=body_.encode("utf-8")),
            routing_key=kwargs['queue_name']
        )

        print(f"[INFO] MESSAGE HAS BEEN PUBLISHED TO {kwargs['queue_name']} QUEUE")

