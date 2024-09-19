import time
from pprint import pprint

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.remote.webdriver import WebDriver

URLS = [
    'https://www.ozon.ru/product/top-calvin-klein-859907140/?avtc=1&avte=2&avts=1726735971'
]


user_reviews = dict()

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


def parse_user_reviews(HTML: BeautifulSoup) -> None:
    user_review_card = HTML.find_all('div', {'class': 'q9v_29'})
    print(len(user_review_card))
    for i in range(len(user_review_card)):
        user_name = (user_review_card[i].find_all('div', {'class': 'q4s_29'}))[0].text
        user_name = user_name.strip()

        user_review = user_review_card[i].find_all('div', {'class': 'qv4_29'})[0].text
        review_date = user_review_card[i].find_all('div', {'class': 'qv2_29'})[0].text
        review_date = review_date.strip()

        user_review = user_review.strip()
        user_review = user_review.replace('\'', '')

        star_review = user_review_card[i].find_all('div', {'class': 'a5d14-a a5d14-a0'})[0]
        star_review = star_review.find_all('svg')
        count_star_review = 0

        for i in range(len(star_review)):
            style = star_review[i].get('style')
            if '255' in style:
                count_star_review += 1

        print(user_review)
        print(review_date)
        print(count_star_review)
        print('\n')

def get_main_page_reviews(driver: WebDriver, url: str) -> None:
    driver.get(url)
    scroll_page(driver, deep=50)
    main_page_html = BeautifulSoup(driver.page_source, 'html.parser')
    parse_user_reviews(main_page_html)



if __name__ == '__main__':
    driver = init_webdriver()
    get_main_page_reviews(driver, URLS[0])
    # pprint(user_reviews)
    driver.quit()
