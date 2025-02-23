import asyncio
import json

import aio_pika

from src.bot.config import RABBITMQ_URL


async def message_to_NN_queue(df_name: str, user_telegram_id: int):
    conn = await aio_pika.connect(RABBITMQ_URL)

    async with conn:
        channel = await conn.channel()
        await channel.declare_queue("NN")

        body_ = json.dumps({
            "df_name": df_name,
            "user_telegram_id": user_telegram_id,
        })

        await channel.default_exchange.publish(
            aio_pika.Message(body=body_.encode("utf-8")),
            routing_key="NN"
        )

        print("[INFO] MESSAGE HAS BEEN PUBLISHED TO NN QUEUE")


if __name__ == "__main__":
    asyncio.run(message_to_NN_queue("http://example.com", 123456))
