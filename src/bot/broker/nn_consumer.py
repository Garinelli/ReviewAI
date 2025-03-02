import os 
import asyncio
import json
from pathlib import Path

import aio_pika
import numpy as np
import pandas as pd
import tensorflow as tf

from .bot_consumer import bot
from .nn_producer import message_to_bot_queue

from src.bot.config import RABBITMQ_URL

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def nn_predict(df_name):
    df = pd.read_pickle(df_name)

    model = tf.keras.models.load_model(BASE_DIR / 'ml/Models/fasttext_model_gru.h5')
    all_reviews_count = len(df)

    written_by_bot = 0

    fake_reviews_id = []

    for index, row in df.iterrows():
        review = row["User review"]
        star_review = row["Star review"]
        text_len = row["Text length"]
        has_media = row["Has media"]
        has_answer = row["Has answer"]

        tensor_vector = tf.convert_to_tensor([review], dtype=tf.float32)
        second_tensor = np.array([[star_review, text_len, has_media, has_answer]])
        second_tensor = tf.convert_to_tensor(second_tensor, dtype=tf.float32)

        prediction = model.predict([tensor_vector, second_tensor])

        if prediction[0][0] < prediction[0][1]:
            written_by_bot += 1
            fake_reviews_id.append(index)

    percent_result = round((written_by_bot / all_reviews_count) * 100, 1)

    return all_reviews_count, written_by_bot, percent_result, fake_reviews_id 


async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        body = message.body.decode()
        body = json.loads(body)
        csv_df_name = f"body['df_name'].split('.')[0].csv"

        print(f"Получено сообщение: {body}")
        await bot.send_message(
            chat_id=body['user_telegram_id'],
            text='🎯Искусственный интеллект предсказывает результат...'
        )

        result_predict = nn_predict(body['df_name'])
        result_message = f'🔍Всего было выявлено отзывов: {result_predict[0]}\n⚠️Количество накрученных отзывов: {result_predict[1]}\n📈В процентах: {result_predict[2]}'

        os.remove(body['df_name'])
        os.remove(csv_df_name)

        await message_to_bot_queue(result=result_message, user_telegram_id=body['user_telegram_id'])


async def message_consumer():
    connection = await aio_pika.connect(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("NN")

        await queue.consume(process_message)

        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(message_consumer())
