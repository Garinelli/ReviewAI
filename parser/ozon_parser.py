import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium_stealth import stealth

URLS = [
    'https://www.ozon.ru/product/top-calvin-klein-859907140/?avtc=1&avte=2&avts=1726735971',
    'https://www.ozon.ru/product/krossovki-nike-1554892756/?advert=y95DZqPAN3j-8UYEpjTB6X2aZKnIG8qKgziM-zSjFMzTgHpmLi78-tFl15nBsQmb7xJ-Feuv6p2B8xE_wLXanHEA5dILZZ9Gi4Az-jrBZGZkJmTeOswlmBDQcv5979bjqZztw1VSqkz3k6qHBnQ4YxqLUXSmVoEYbOYra6UfwBTxCTmCiDLd2Y796Mrh-n1O9Tfw-D5g-_T1Q9nWfNQWfAwxhepmpNIrEqyqsLhOHvMY3sYiiUs_-Pa1NbjaAQ8pj005M0TVMuRvUNls9ps9pW3SlQq-Jy9UOXN0-gto9KGn4eHS4ttUZe0huxpRtSEFnnF8qZM_d9Y6uznf9jRpI85kN8DhOTu8dbryKXeqT2_0wSdXPcPRlnY0tGXS5xAoPKg&avtc=1&avte=2&avts=1726751323&keywords=nike+dunk',
    'https://www.ozon.ru/product/hudi-tvoe-985120837/?advert=s2SowocNwNPosxBHESWWJ7EBnXEDddfSMVE4Mtl91UKNQxhhaSKd_76yW2Nfw3tgzDMD_GnWi5W0ILtp1vBuG1pQeybHA0kiScywD7ynwU3mUiD8lKqf-dlU64e_LURxSFtzAlzvnNbwIiFB4sFgZR2QS8YZ7VxUI9fXDZE934eSzcNRsVE7FAVxQCnDr-KJ0G7HbfoVh58GHDM02eK6sTjmMKX9hgNUEq5tNWgNgFk7z-aE4Phia2W2xrw8zNewUB8BJadodQ9YDiX4ffHaEB9XZ6h4oaB5FdKdMOYf0pFMjLXBiXPASqMUrKoo9HMw3NQ6MrJLfij3X_90FWbYBwqz1lTu_xJnAXCquczZ5GR5YGiKq4He575T5vO2&avtc=1&avte=2&avts=1726752958&keywords=%D1%85%D1%83%D0%B4%D0%B8+%D0%BC%D1%83%D0%B6%D1%81%D0%BA%D0%BE%D0%B5',
    'https://www.ozon.ru/product/futbolka-tvoe-bazovaya-811535281/?avtc=1&avte=2&avts=1726752963'
]

user_names = []
user_reviews = []
reviews_date = []
star_reviews = []


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
    if not user_review_card:
        return
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

        user_names.append(user_name)
        user_reviews.append(user_review)
        reviews_date.append(review_date)
        star_reviews.append(count_star_review)


def get_main_page_reviews(driver: WebDriver, url: str) -> None:
    time.sleep(5)
    driver.get(url)
    scroll_page(driver, deep=120)
    main_page_html = BeautifulSoup(driver.page_source, 'html.parser')
    parse_user_reviews(main_page_html)


def main():
    driver = init_webdriver()
    for i in range(len(URLS)):
        get_main_page_reviews(driver, URLS[i])
    df = pd.DataFrame({
        'User name': user_names,
        'User review': user_reviews,
        'Review date': reviews_date,
        'Star review': star_reviews
    })
    df.to_csv('dataframe.csv')


if __name__ == '__main__':
    main()
