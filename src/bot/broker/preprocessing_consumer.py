import asyncio
import json
import string

import aio_pika
import fasttext
import nltk
import pandas as pd
import pymorphy2
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from bot_consumer import bot
from preprocessing_producer import message_to_NN_queue
from src.bot.config import RABBITMQ_URL


def tokens_to_vector(tokens, model):
    sentence = ' '.join(tokens)
    return model.get_sentence_vector(sentence)


def dataframe_preprocessing(df_name):
    df = pd.read_csv(df_name)
    df = df.copy()

    nltk.download('punkt_tab')
    nltk.download('punkt')
    nltk.download('stopwords')

    reviews = df['User review'].values

    for index, review in enumerate(reviews):
        reviews[index] = review.lower()

    for index, review in enumerate(reviews):
        tokens = word_tokenize(review)
        tokens = [word for word in tokens]
        reviews[index] = tokens

    stop_words = set(stopwords.words('russian'))
    exceptions = {
        "не", "ни", "нет", "да", "или", "и", "так", "потому", "что", "когда",
        "где", "кто", "что", "как", "зачем", "почему", "будто", "бы", "вдруг",
        "пусть", "тоже", "все", "всё", "этот", "та", "такой", "сам", "только",
        "другой", "ещё", "возможно", "почему", "впрочем", "хотя", "тем", "вместо",
        "между", "также", "тогда", "вдобавок", "после", "перед", "наоборот",
        "поэтому", "то", "тогда", "когда", "если", "даже", "включая", "совсем",
        "именно", "через", "сейчас", "когда", "будет", "для", "от", "среди"
    }

    for tokens in reviews:
        for token in tokens:
            if token in stop_words and token not in exceptions:
                tokens.remove(token)

    nltk.download('omw-1.4')

    morph = pymorphy2.MorphAnalyzer()

    for tokens in reviews:
        for index, token in enumerate(tokens):
            lemma = morph.parse(token)[0].normal_form
            tokens[index] = lemma

    df = df.drop(columns=['Unnamed: 0'])

    exceptions_punctuation = {"!", "?", "-", }

    for tokens in reviews:
        for token in tokens:
            if token in string.punctuation and token not in exceptions_punctuation:
                tokens.remove(token)

    model = fasttext.load_model('cc.ru.300.bin')

    df['User review'] = df['User review'].apply(lambda x: tokens_to_vector(x, model))

    df.to_pickle('preprocessed_df.pickle')


async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        body = message.body.decode()
        body = json.loads(body)
        print(f"Получено сообщение: {body}")
        await bot.send_message(
            chat_id=body['user_telegram_id'],
            text='💬Обрабатываем естественный язык...'
        )
        dataframe_preprocessing(body['df_name'])

        await message_to_NN_queue(df_name="preprocessed_df.pickle",
                                  user_telegram_id=body['user_telegram_id'])


async def message_consumer():
    connection = await aio_pika.connect(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("preprocessing")

        await queue.consume(process_message)

        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(message_consumer())
