import os 
import asyncio
import json
from pathlib import Path

import aio_pika
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt

from src.bot.config import RABBITMQ_URL
from src.bot.bot import send_request_status
from .producer import send_message_to_broker



BASE_DIR = Path(__file__).resolve().parent.parent.parent
model = tf.keras.models.load_model(BASE_DIR / 'ml/Models/fasttext_model_gru.h5')


def nn_predict(task_id):
    df = pd.read_pickle(f'{task_id}.pickle')

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

        print(f"Получено сообщение: {body}")
        await send_request_status(
            body['user_telegram_id'],
            '🎯Искусственный интеллект предсказывает результат...'
        )

        df = pd.read_csv(f'{body["task_id"]}.csv')

        result_predict = nn_predict(body['task_id'])
        result_message = f'🔍Всего было выявлено отзывов: {result_predict[0]}\n⚠️Количество накрученных отзывов: {result_predict[1]}\n📈В процентах: {result_predict[2]}\n💬Выявленные отзывы:\n'

        fake_reviews_id = result_predict[3]
        fake_reviews = ""

        for index, id in enumerate(fake_reviews_id):
            if index >= 5:
                break
            fake_reviews += f"{index + 1}. {df.loc[df['Unnamed: 0'] == id, 'User review'].values[0]}\n"

        result_message += fake_reviews

        star_reviews = list(df['Star review'].values)
        plt.plot(star_reviews, marker='o', linestyle='-', color='b', label='Оценки')

        plt.xlabel('Номер отзыва')
        plt.ylabel('Оценка')
        plt.title('Динамика отзывов')
        plt.yticks([1, 2, 3, 4, 5])
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend()
        plt.savefig(f'{body["task_id"]}.png', dpi=300, bbox_inches='tight')
        plt.close()

        os.remove(f'{body["task_id"]}.csv')
        os.remove(f'{body["task_id"]}.pickle')

        await send_message_to_broker(queue_name='bot',
                                     result=result_message, user_telegram_id=body['user_telegram_id'],
                                     task_id=body['task_id'])


async def message_consumer():
    connection = await aio_pika.connect(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("NN")

        await queue.consume(process_message)

        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(message_consumer())
