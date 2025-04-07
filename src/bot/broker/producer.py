import json
import aio_pika

from src.bot.config import RABBITMQ_URL
from src.bot.log_conf import logging

async def send_message_to_broker(**kwargs):
    conn = await aio_pika.connect(RABBITMQ_URL)

    async with conn:
        channel = await conn.channel()
        await channel.declare_queue(kwargs['queue_name'])

        body_ = json.dumps(kwargs)

        await channel.default_exchange.publish(
            aio_pika.Message(body=body_.encode("utf-8")),
            routing_key=kwargs['queue_name']
        )

        logging.info(f"[INFO] MESSAGE HAS BEEN PUBLISHED TO {kwargs['queue_name']} QUEUE. task_id = {kwargs['task_id']}")
