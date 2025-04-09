import json
import aio_pika
from aio_pika import Connection
from aio_pika.pool import Pool

from src.bot.config import RABBITMQ_URL
from src.bot.log_conf import logging

# Пул соединений
connection_pool: Pool[Connection] = Pool(
    lambda: aio_pika.connect(RABBITMQ_URL, heartbeat=60, timeout=10), max_size=10
)


async def send_message_to_broker(**kwargs) -> None:
    async with connection_pool.acquire() as connection:
        channel = await connection.channel()

        await channel.declare_queue(kwargs["queue_name"], durable=True, exclusive=False)

        await channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(kwargs).encode("utf-8"),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key=kwargs["queue_name"],
        )

        logging.info(
            f"[INFO] MESSAGE HAS BEEN PUBLISHED TO {kwargs['queue_name']} QUEUE. task_id = {kwargs['task_id']}"
        )
