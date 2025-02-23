import json
import asyncio

import aio_pika

from src.bot.config import RABBITMQ_URL

async def message_to_bot_queue(result: str, user_telegram_id: int):
    conn = await aio_pika.connect(RABBITMQ_URL)

    async with conn:
        channel = await conn.channel()
        await channel.declare_queue("bot")

        body_ = json.dumps({
            "result": result,
            "user_telegram_id": user_telegram_id,
        })

        await channel.default_exchange.publish(
            aio_pika.Message(body=body_.encode("utf-8")),
            routing_key="bot"
        )

        print("[INFO] MESSAGE HAS BEEN PUBLISHED TO bot QUEUE")

if __name__ == "__main__":
    asyncio.run(message_to_bot_queue("http://example.com", 123456))