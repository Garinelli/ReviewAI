from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from typing import List, Dict
from selenium.webdriver.remote.webelement import WebElement
import pandas as pd
from time import sleep
from pathlib import Path
from bs4 import BeautifulSoup
from typing import List, Dict


def get_feedback_link(url_product: str) -> str:
    """Получаем ссылку на страницу с отзывами"""
    feedback_link = url_product[: url_product.rfind("/")] + "/feedbacks"
    return feedback_link


def get_feedbacks_raw(driver: WebDriver, url_feedbacks: str) -> List[WebElement]:
    """Получаем все отзывы с текущей страницы"""

    def press_this_product_btn():
        """Поиск кнопки 'Этот вариант товара'"""
        try:
            # Ожидание появления кнопки с текстом "Этот вариант товара" в видимой части страницы
            button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//button[contains(text(), "Этот вариант товара")]')
                )
            )
            # button = driver.find_elements(By.CLASS_NAME, "product-feedbacks__title")
            # print(f"{len(button)=}", button[-1].get_attribute("outerHTML"))

        except TimeoutException:
            print("Ошибка при поиске кнопки: 'Этот вариант товара'")
        else:
            # Нажимаем на кнопку
            button.click()
            print("Кнопка успешно нажата!")

    def scroll_down():
        """Прокручиваем страницу вниз до тех пор, пока не достигнут конец страницы или контент не успел прогрузиться"""
        # Получение начальной высоты страницы
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Прокрутка страницы до конца
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            try:
                # Ожидание загрузки нового контента
                WebDriverWait(driver, 3).until(
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

    feedbacks = driver.find_elements(
        By.CLASS_NAME,
        "comments__item.feedback.product-feedbacks__block-wrapper",
    )
    print(f"Количество отзывов: {len(feedbacks)}")

    return feedbacks


def prepare_feedbacks(feedbacks: List[WebElement]) -> List[Dict]:
    """Подготавливаем данные о отзывах в виде списка словарей"""

    comments = []

    for i, feedback in enumerate(feedbacks):
        # Получаем HTML-код элемента и передаем его в Beautiful Soup
        feedback_html = feedback.get_attribute("outerHTML")
        soup = BeautifulSoup(feedback_html, "html.parser")

        # Дата написания отзыва
        date = soup.find("div", class_="feedback__date").text

        # Выводим имена пользователей для визуализации обработки отзывов
        if i % 10 == 0:
            name = soup.find("p", class_="feedback__header").text
            # name = name_tag.text.strip() if name_tag else "Unknown"
            print(i, name)

        # Рейтинг отзыва
        rating_tag = soup.find("div", class_="feedback__rating-wrap")
        rating = int(rating_tag.find("span")["class"][-1][-1]) if rating_tag else 0

        # Текст отзыва
        text_tag = soup.find("div", class_="feedback__content")
        if text_tag:
            text_spans = text_tag.find_all("span")[:-1:2]
            text = "\n".join([span.text.strip() for span in text_spans])
        else:
            text = ""

        # Ответ продавца
        answer_tag = soup.find("p", class_="feedback__sellers-reply-title")
        has_answer = int(answer_tag is not None)

        # Медиа (фото/видео)
        media_tag = soup.find("ul", class_="feedback__photos")
        has_media = int(media_tag is not None)

        # Добавляем отзыв в список
        comments.append(
            {
                "User review": text.replace(":", ": ").replace("\n", "\\n"),
                "Review date": date if date else "Unknown",
                "Star review": rating,
                "Text length": len(text),
                "Has media": has_media,
                "Has answer": has_answer,
                "Written by bot": 0,
            }
        )

    return comments


def main(url_product: str, out_path: str) -> None:
    """Основная функция, которая запускает парсинг отзывов и сохраняет результат в csv-файл"""

    driver = webdriver.Edge()  # Запускаем драйвер - !Обязательно!

    # Пример использования
    feedbacks = prepare_feedbacks(
        get_feedbacks_raw(driver, get_feedback_link(url_product))
    )

    driver.quit()  # Закрываем драйвер - !Обязательно!

    # Сохранение отзывов в csv-файле
    pd.DataFrame(feedbacks).to_csv(out_path, index=False)


if __name__ == "__main__":
    url = "https://www.wildberries.ru/catalog/196491327/detail.aspx"
    # url = "https://www.wildberries.ru/catalog/259046906/detail.aspx"

    main(url, f"{Path(__file__).parent}/dataframes/feedbacks_wb.csv")
