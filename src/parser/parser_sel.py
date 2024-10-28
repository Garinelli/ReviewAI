from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


def get_feedback_link(url):
    driver = webdriver.Chrome()  # Используем Chrome, вы можете выбрать другой браузер
    driver.get(url)

    # Прокручиваем страницу вниз до тех пор, пока элемент не будет найден
    while True:
        try:
            # Пытаемся найти элемент
            feedback_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".btn-base.comments__btn-all")
                )
            )

            # Если элемент найден, выходим из цикла
            print("НАШЕЛ!!!!!")
            break
        except Exception:
            # Прокручиваем страницу вниз
            print("НЕ НААШЕЛ!!!")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")

    # Получаем ссылку из элемента
    feedback_link = feedback_button.get_attribute("href")

    driver.quit()

    return feedback_link


# Пример использования
url = "https://www.wildberries.ru/catalog/243062249/detail.aspx"
link = get_feedback_link(url)
print(f"Ссылка на все отзывы: {link}")
