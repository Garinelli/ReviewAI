import asyncio
import json
import string
from pathlib import Path

import aio_pika
import fasttext
import nltk
import pandas as pd
import pymorphy2
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from src.bot.config import RABBITMQ_URL
from src.bot.bot_utils.status_sender import send_request_status
from src.bot.main import bot
from src.bot.broker.producer import send_message_to_broker
from src.bot.log_conf import logging

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

nltk.download('omw-1.4')
nltk.download('punkt_tab')
nltk.download('punkt')
nltk.download('stopwords')

model_path = str(BASE_DIR / 'models/cc.ru.300.bin')
model = fasttext.load_model(model_path)

exceptions = {
    "не", "ни", "нет", "да", "или", "и", "так", "потому", "что", "когда",
    "где", "кто", "что", "как", "зачем", "почему", "будто", "бы", "вдруг",
    "пусть", "тоже", "все", "всё", "этот", "та", "такой", "сам", "только",
    "другой", "ещё", "возможно", "почему", "впрочем", "хотя", "тем", "вместо",
    "между", "также", "тогда", "вдобавок", "после", "перед", "наоборот",
    "поэтому", "то", "тогда", "когда", "если", "даже", "включая", "совсем",
    "именно", "через", "сейчас", "когда", "будет", "для", "от", "среди"
}

exceptions_punctuation = {"!", "?", "-", }

stop_words = set(stopwords.words('russian'))

morph = pymorphy2.MorphAnalyzer()
    
def tokens_to_vector(tokens, model):
    sentence = ' '.join(tokens)
    return model.get_sentence_vector(sentence)

def get_tokens(reviews):
    for index, review in enumerate(reviews):
        tokens = word_tokenize(review)
        tokens = [word for word in tokens]
        reviews[index] = tokens
    return reviews

def remove_stop_words(reviews):
    for tokens in reviews:
        for token in tokens:
            if token in stop_words and token not in exceptions:
                tokens.remove(token)
    
def lemma_preporation(reviews):
    for tokens in reviews:
        for index, token in enumerate(tokens):
            lemma = morph.parse(token)[0].normal_form
            tokens[index] = lemma

def remove_punctuation(reviews):    
    for tokens in reviews:
        for token in tokens:
            if token in string.punctuation and token not in exceptions_punctuation:
                tokens.remove(token)

async def dataframe_preprocessing(task_id):
    df = pd.read_csv(f'{task_id}.csv').drop(columns=['Unnamed: 0'])
    df = df.copy()

    reviews = df['User review'].values

    for index, review in enumerate(reviews):
        reviews[index] = review.lower()

    reviews = get_tokens(reviews)
    remove_stop_words(reviews)
    lemma_preporation(reviews)
    remove_punctuation(reviews)

    df['User review'] = df['User review'].apply(lambda x: tokens_to_vector(x, model))
    df.to_pickle(f'{task_id}.pickle')

async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        body = message.body.decode()
        body = json.loads(body)

        logging.info(f"Получено сообщение: {body}. queue_name = {body['queue_name']}")
        print(f"Получено сообщение: {body}")

        await send_request_status(
            bot,
            body['user_telegram_id'],
            '💬Обрабатываем естественный язык...'
        )
        await dataframe_preprocessing(body['task_id'])

        await send_message_to_broker(queue_name='NN', task_id=body['task_id'],
                                  user_telegram_id=body['user_telegram_id'])

async def message_consumer():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=5)
        queue = await channel.declare_queue("preprocessing")

        await queue.consume(process_message)

        try:
            await asyncio.Future()
        finally:
            await connection.close()

if __name__ == "__main__":
    asyncio.run(message_consumer())
