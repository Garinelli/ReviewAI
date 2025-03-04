import json
import asyncio

import aio_pika

from src.bot.config import RABBITMQ_URL

async def message_to_preprocessing_queue(user_telegram_id: int, task_id: str):
    conn = await aio_pika.connect(RABBITMQ_URL)

    async with conn:
        channel = await conn.channel()
        await channel.declare_queue("preprocessing")

        body = json.dumps({
            "user_telegram_id": user_telegram_id,
            "task_id": task_id
        })

        await channel.default_exchange.publish(
            aio_pika.Message(body=body.encode("utf-8")),
            routing_key="preprocessing"
        )

        print("[INFO] MESSAGE HAS BEEN PUBLISHED TO preprocessing QUEUE")


if __name__ == "__main__":
    asyncio.run(message_to_preprocessing_queue("http://example.com", 123456))