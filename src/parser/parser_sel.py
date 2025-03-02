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

    press_this_product_btn()
    sleep(2)

    scroll_down()
    sleep(2)

    feedbacks = driver.find_elements(
        By.CLASS_NAME,
        "comments__item.feedback.product-feedbacks__block-wrapper.j-feedback-slide",
    )
    print(f"Количество отзывов: {len(feedbacks)}")

    return feedbacks


def prepare_feedbacks(feedbacks: List[WebElement]) -> List[Dict]:
    """Подготавливаем данные о отзывах в виде списка словарей"""
    # (требуется работающий driver)
    comments = []
    for i, feedback in enumerate(feedbacks):
        # Дата написания отзыва
        date = feedback.find_element(
            By.CLASS_NAME, "feedback__date.hide-desktop"
        ).get_attribute("content")
        # print(date)

        # Выводим имена пользователей для визуализации обработки отзывов
        if i % 10 == 0:
            name = feedback.find_element(By.CLASS_NAME, "feedback__header").text
            print(i, name)

        rating = (
            feedback.find_element(By.CLASS_NAME, "feedback__rating-wrap")
            .find_element(By.TAG_NAME, "span")
            .get_attribute("class")[-1]
        )
        # print(f"{rating=}")

        try:
            text_html = (
                feedback.find_element(By.CLASS_NAME, "feedback__content").find_element(
                    By.CLASS_NAME, "feedback__text.j-feedback__text.show"
                )
                # .get_attribute("outerHTML")
            )
            text_html = text_html.find_elements(By.TAG_NAME, "span")[:-1:2]
            text = "\n".join([el.text for el in text_html])
        except NoSuchElementException:
            text = ""
        # print(f"{len(text)=}", text, sep="\n")

        try:
            answer_html = feedback.find_element(
                By.CLASS_NAME,
                "feedback__sellers-reply-title",
            )
        except NoSuchElementException:
            answer_html = None

        try:
            media_html = feedback.find_element(
                By.CLASS_NAME, "feedback__photos.j-feedback-photos-scroll"
            )
        except NoSuchElementException:
            media_html = None

        # print("!!", answer_html is None, media_html is None)

        comments.append(
            {
                "User review": text.replace(":", ": ").replace("\n", "\\n"),
                "Review date": date[:10],
                "Star review": int(rating),
                "Text length": len(text),
                "Has media": int(bool(media_html)),
                "Has answer": int(bool(answer_html)),
                "Written by bot": 0,
            }
        )
    # print(*comments, sep="\n")

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
