import time
import asyncio
import json

import aio_pika

from .producer import send_message_to_broker
from src.bot.config import RABBITMQ_URL

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from selenium_stealth import stealth



MONTHS = {
    'января': '01',
    'февраля': '02',
    'марта': '03',
    'апреля': '04',
    'мая': '05',
    'июня': '06',
    'июля': '07',
    'августа': '08',
    'сентября': '09',
    'октября': 10,
    'ноября': 11,
    'декабря': 12,
}


def init_webdriver():
    # chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')

    # driver = webdriver.Chrome(options=chrome_options)

    driver = webdriver.Chrome()

    stealth(driver,
            vendor='Google Inc.',
            platform='Win32',
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine")
    return driver


def scroll_page(driver: WebDriver) -> None:
    current_height = driver.execute_script("return window.scrollY;")
    while True:
        driver.execute_script("window.scrollBy(0, 350)")
        time.sleep(0.1)
        if current_height == driver.execute_script("return window.scrollY;"):
            break
        current_height = driver.execute_script("return window.scrollY;")


def parse_user_reviews(HTML: BeautifulSoup, task_id: str) -> None:
    user_reviews = []
    reviews_date = []
    star_reviews = []
    text_len = []
    written_by_bot = []
    has_media = []
    has_answer = []
    user_review_cards = HTML.find_all('div', {'class': 'tr7_32'})
    if not user_review_cards:
        return
    for i in range(len(user_review_cards)):

        user_review = user_review_cards[i].find_all('div', {'class': 'x4p_32'})
        if user_review:
            user_review = user_review[0].text
        else:
            # Если нет текста отзыва, то переходим к следующему
            continue

        review_date = user_review_cards[i].find_all('div', {'class': 'x2p_32'})[0].text
        review_date = review_date.strip()

        review_dates = review_date.split(' ')
        if 'изменен' in review_dates:
            review_dates = review_dates[1:]
        year = review_dates[2]
        month = MONTHS[review_dates[1]]
        day = review_dates[0]
        if int(day) in range(1, 10):
            day = '0' + str(day)

        review_date = f'{year}-{month}-{day}'
        user_review = user_review.strip()
        user_review = user_review.replace('\'', '')

        has_photo = user_review_cards[i].find_all('div', {'class': 'wp0_32 pw3_32'})

        star_review = user_review_cards[i].find_all('div', {'class': 'a5d24-a a5d24-a0'})[0]
        star_review = star_review.find_all('svg')
        count_star_review = 0

        for i in range(len(star_review)):
            style = star_review[i].get('style')
            if '255' in style:
                count_star_review += 1

        # check answer
        comment_button = user_review_cards[i].find_all('button',
                                                       {'class': "p6x_32 ga121-a undefined"})
        if comment_button:
            has_answer.append(1)
        else:
            has_answer.append(0)

        user_reviews.append(user_review)
        reviews_date.append(review_date)
        star_reviews.append(count_star_review)
        text_len.append(len(user_review))
        written_by_bot.append(0)
        if has_photo:
            has_media.append(1)
        else:
            has_media.append(0)

    df = pd.DataFrame({
        'User review': user_reviews,
        'Review date': reviews_date,
        'Star review': star_reviews,
        'Text length': text_len,
        'Has media': has_media,
        'Has answer': has_answer,
        'Written by bot': written_by_bot,
    })
    df.to_csv(f'{task_id}.csv')

def get_main_page_reviews(driver: WebDriver, url: str, task_id: str) -> None:
    driver.get(url)
    time.sleep(5)
    scroll_page(driver)
    main_page_html = BeautifulSoup(driver.page_source, 'html.parser')
    parse_user_reviews(main_page_html, task_id)


async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        body = message.body.decode()
        body = json.loads(body)
        print(f"Получено сообщение: {body}")
        driver = init_webdriver()
        get_main_page_reviews(driver, body['link'], body['task_id'])
        await send_message_to_broker(queue_name='preprocessing', user_telegram_id=body['user_telegram_id'],
                                             task_id=body['task_id'])


async def message_consumer():
    connection = await aio_pika.connect(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("parser")

        await queue.consume(process_message)

        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(message_consumer())
