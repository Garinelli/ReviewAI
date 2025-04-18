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
from src.bot.constants import RESULT_MESSAGE
from src.bot.broker.producer import send_message_to_broker
from src.bot.log_conf import logging

BASE_DIR = Path(__file__).resolve().parent.parent.parent
model = tf.keras.models.load_model(BASE_DIR / "ml/Models/fasttext_model_gru.h5")  # pylint: disable=E1101:no-member


def nn_predict(task_id):
    df = pd.read_pickle(f"{task_id}.pickle")
    all_reviews_count = len(df)
    written_by_bot = 0
    fake_reviews_id = []

    for index, row in df.iterrows():
        review = row["User review"]
        star_review = row["Star review"]
        has_media = row["Has media"]

        review_vector = tf.convert_to_tensor([review], dtype=tf.float32)
        num_tensor = np.array([[star_review, has_media]])
        num_tensor = tf.convert_to_tensor(num_tensor, dtype=tf.float32)

        prediction = model.predict([review_vector, num_tensor])
        if prediction[0][0] < prediction[0][1]:
            written_by_bot += 1
            fake_reviews_id.append(index)

    percent_result = round((written_by_bot / all_reviews_count) * 100, 1)

    return all_reviews_count, written_by_bot, percent_result, fake_reviews_id


def create_review_star_graphic(star_reviews: list[int], task_id: str):
    plt.plot(star_reviews, color="#A344FA", label="Оценки")
    plt.ylabel("Оценка")
    plt.title("Динамика отзывов")
    plt.yticks([1, 2, 3, 4, 5])
    plt.gca().set_xticks([]) 
    plt.savefig(f"{task_id}.png", dpi=300, bbox_inches="tight")
    plt.close()


def get_result_message(result_predict: tuple, task_id: str) -> str:
    df = pd.read_csv(f"{task_id}.csv")
    # Дифференцирование временного ряда
    df["Star review"] = df["Star review"].diff()
    result_message = RESULT_MESSAGE.format(
        result_predict[0], result_predict[1], result_predict[2]
    )

    fake_reviews_id = result_predict[3]

    if fake_reviews_id:
        fake_reviews = "Выявленные отзывы:\n"
        for index, review_id in enumerate(fake_reviews_id):
            if index >= 5:
                break
            fake_reviews += f"{index + 1}. {df.loc[df['Unnamed: 0'] == review_id, 'User review'].values[0]}\n"

        result_message += fake_reviews
    
    star_reviews = list(df["Star review"].values)
    create_review_star_graphic(star_reviews, task_id)

    return result_message


async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        body = message.body.decode()
        body = json.loads(body)

        logging.info(f"Получено сообщение: {body}. queue_name = {body['queue_name']}")
        print(f"Получено сообщение: {body}")
        
        await send_request_status(
            body["user_telegram_id"],
            "🎯Искусственный интеллект предсказывает результат...",
        )

        result_predict = await asyncio.to_thread(nn_predict, body["task_id"])
        result_message = get_result_message(result_predict, body['task_id'])

        os.remove(f"{body['task_id']}.csv")
        os.remove(f"{body['task_id']}.pickle")

        await send_message_to_broker(
            queue_name="bot",
            result=result_message,
            user_telegram_id=body["user_telegram_id"],
            task_id=body["task_id"],
        )


async def message_consumer():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=5)
        queue = await channel.declare_queue("NN", durable=True)

        await queue.consume(process_message)

        try:
            await asyncio.Future()
        finally:
            await connection.close()


if __name__ == "__main__":
    asyncio.run(message_consumer())
