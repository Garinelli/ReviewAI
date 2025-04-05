from functools import partial, reduce
from datetime import datetime, timedelta
from time import sleep
from typing import List, Dict
import asyncio
import json

import aio_pika
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium_stealth import stealth

from src.bot.broker.producer import send_message_to_broker
from src.bot.config import RABBITMQ_URL
from src.bot.constants import MONTHS, KEYWORDS, CLASS_NAME

def init_webdriver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=chrome_options)

    stealth(
        driver,
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
    )
    return driver

def get_feedback_link(url_product: str) -> str:
    """Получаем ссылку на страницу с отзывами"""
    feedback_link = url_product[: url_product.rfind("/")] + "/feedbacks"
    return feedback_link

def get_feedbacks_raw(driver: WebDriver, url_feedbacks: str) -> List[WebElement]:
    """Получаем все отзывы с текущей страницы"""

    def press_this_product_btn():
        """Поиск кнопки 'Этот вариант товара'"""
        try:
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//button[contains(text(), "Этот вариант товара")]')
                )
            )
        except TimeoutException:
            print("Ошибка при поиске кнопки: 'Этот вариант товара'")
        else:
            button.click()
            print("Кнопка успешно нажата!")

    def scroll_down():
        """Прокручиваем страницу вниз до тех пор, пока не достигнут конец страницы или контент не успел прогрузиться"""
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                # Ожидание загрузки нового контента
                WebDriverWait(driver, 10).until(
                    lambda d: d.execute_script("return document.body.scrollHeight")
                    > last_height
                )
            except TimeoutException:
                print("Конец страницы достигнут или контент не успел прогрузиться!")
                break
            # Получение новой высоты страницы | Обновление последней высоты страницы
            last_height = driver.execute_script("return document.body.scrollHeight")

    # Открытие сайта
    driver.get(url_feedbacks)
    sleep(3)
    driver.get(url_feedbacks)

    press_this_product_btn()
    sleep(2)

    scroll_down()
    sleep(2)

    html_code = driver.page_source

    return html_code

def conv_date(date_time: str):
    """Преобразование даты в формат datetime"""
    date_list = date_time.split(", ")[0].split()
    if len(date_list) == 1:
        now = datetime.now()
        new_date = now - timedelta(days=int(date_list[0] == "Вчера"))
        date_list = [f"{new_date.day}", f"{new_date.month}", f"{new_date.year}"]
        # Преобразуем строку в объект datetime
        date_obj = datetime.strptime(" ".join(date_list), r"%d %m %Y")
    else:
        date_list[1] = MONTHS[date_list[1]]
        if len(date_list) == 2:
            date_list.append(f"{datetime.now().year}")
        # Преобразуем строку в объект datetime
        date_obj = datetime.strptime(" ".join(date_list), r"%d %B %Y")

    # Форматируем дату в нужный формат
    formatted_date = date_obj.strftime(r"%Y-%m-%d")
    return formatted_date

def parse_reviews(feedbacks) -> list:
    reviews = []

    for i, feedback in enumerate(feedbacks):
        # Дата написания отзыва
        date_time = feedback.find("div", class_="feedback__date").text
        date = conv_date(date_time)

        # Выводим имена пользователей для визуализации обработки отзывов
        if i % 10 == 0:
            name = feedback.find("p", class_="feedback__header").text
            print(i, name)

        # Рейтинг отзыва
        rating_tag = feedback.find("div", class_="feedback__rating-wrap")
        rating = int(rating_tag.find("span")["class"][-1][-1]) if rating_tag else 0

        # Текст отзыва
        review_pros = feedback.find("span", class_=f"{CLASS_NAME} {CLASS_NAME}-pro")
        review_cons = feedback.find("span", class_=f"{CLASS_NAME} {CLASS_NAME}-con")
        review_comments = feedback.select_one(f'span[class="{CLASS_NAME}"]')

        review = (review_pros, review_cons, review_comments)

        # Случай, когда у отзыва нет текста
        if not any(review):
            continue

        text = " ".join(
            [
                str(item.text).strip().removeprefix(word)
                for item, word in zip(review, KEYWORDS)
                if item
            ]
        )
        print(f'{text = }\n')
        # Это вариант может быть быстрее, но менее читаем
        # text = " ".join(
        #     [
        #         item.find_all(string=True, recursive=False)[-1].strip()
        #         for item in review
        #         if item
        #     ]
        # )

        # Медиа (фото/видео)
        media_tag = feedback.find("ul", class_="feedback__photos")
        has_media = int(media_tag is not None)

        # Добавляем отзыв в список
        reviews.append(
            {
                "User review": text.replace("\n", " "),
                "Review date": date,
                "Star review": rating,
                "Has media": has_media,
            }
        ) 
    return reviews

def prepare_feedbacks(html_code: str) -> List[Dict]:
    """Подготавливаем данные о отзывах в виде списка словарей"""
    soup = BeautifulSoup(html_code, "html.parser")
    feedbacks = soup.find_all(
        "li", class_="comments__item feedback product-feedbacks__block-wrapper"
    )
    print(f"Количество отзывов: {len(feedbacks)}")

    reviews = parse_reviews(feedbacks)
    
    return reviews

def parser_feedbacks(url_product, driver, task_id) -> None:
    """Основная функция, которая запускает парсинг отзывов и сохраняет результат в csv-файл"""
    # Пример использования
    feedbacks = prepare_feedbacks(
        get_feedbacks_raw(driver, get_feedback_link(url_product))
    )

    driver.quit()  # Закрываем драйвер - !Обязательно!

    # Сохранение отзывов в csv-файле
    pd.DataFrame(feedbacks).to_csv(f"{task_id}.csv")

async def process_message(message: aio_pika.IncomingMessage, driver: WebDriver):
    async with message.process():
        body = message.body.decode()
        body = json.loads(body)
        print(f"Получено сообщение: {body}")
        parser_feedbacks(body["link"], driver, body["task_id"])
        await send_message_to_broker(
            queue_name="preprocessing",
            user_telegram_id=body["user_telegram_id"],
            task_id=body["task_id"],
        )

async def message_consumer(driver: WebDriver):
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=5)
        queue = await channel.declare_queue("parser")

        await queue.consume(partial(process_message, driver=driver))

        try:
            await asyncio.Future()
        finally:
            await connection.close()

if __name__ == "__main__":
    DRIVER = init_webdriver()
    asyncio.run(message_consumer(DRIVER))
