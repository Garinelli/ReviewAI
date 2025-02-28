import json
import asyncio

import aio_pika
from src.bot.config import RABBITMQ_URL


async def message_to_parser_queue(link: str, user_telegram_id: int):
    conn = await aio_pika.connect(RABBITMQ_URL)

    async with conn:
        channel = await conn.channel()
        await channel.declare_queue("parser")

        body_ = json.dumps({
            "link": link,
            "user_telegram_id": user_telegram_id,
        })

        await channel.default_exchange.publish(
            aio_pika.Message(body=body_.encode("utf-8")),
            routing_key="parser"
        )

        print("[INFO] MESSAGE HAS BEEN PUBLISHED TO PARSER QUEUE")

