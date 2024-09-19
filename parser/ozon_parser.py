import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.remote.webdriver import WebDriver

URLS = [
    'https://www.ozon.ru/product/top-calvin-klein-859907140/?avtc=1&avte=2&avts=1726735971'
]


def init_webdriver():
    driver = webdriver.Chrome()
    stealth(driver,
            vendor='Google Inc.',
            platform='Win32',
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine")
    return driver


def scroll_page(driver: WebDriver, deep: int) -> None:
    for _ in range(deep):
        driver.execute_script("window.scrollBy(0, 100)")
        time.sleep(0.1)


def get_mainpage_cards(driver: WebDriver, url: str) -> None:
    driver.get(url)
    scroll_page(driver, deep=50)
    main_page_html = BeautifulSoup(driver.page_source, 'html.parser')

    content = main_page_html.find_all('div', {"class": "q4s_29"})
    for i in range(len(content)):
        user_name = content[i].text
        user_name = user_name.replace(' ', '')
        print(f'{user_name = }')


if __name__ == '__main__':
    driver = init_webdriver()
    get_mainpage_cards(driver, URLS[0])
    driver.quit()
