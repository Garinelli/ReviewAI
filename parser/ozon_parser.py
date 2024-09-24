import time
import requests

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from selenium_stealth import stealth

# URLS = [
#     'https://www.ozon.ru/product/krossovki-nike-1554892756/?advert=y95DZqPAN3j-8UYEpjTB6X2aZKnIG8qKgziM-zSjFMzTgHpmLi78-tFl15nBsQmb7xJ-Feuv6p2B8xE_wLXanHEA5dILZZ9Gi4Az-jrBZGZkJmTeOswlmBDQcv5979bjqZztw1VSqkz3k6qHBnQ4YxqLUXSmVoEYbOYra6UfwBTxCTmCiDLd2Y796Mrh-n1O9Tfw-D5g-_T1Q9nWfNQWfAwxhepmpNIrEqyqsLhOHvMY3sYiiUs_-Pa1NbjaAQ8pj005M0TVMuRvUNls9ps9pW3SlQq-Jy9UOXN0-gto9KGn4eHS4ttUZe0huxpRtSEFnnF8qZM_d9Y6uznf9jRpI85kN8DhOTu8dbryKXeqT2_0wSdXPcPRlnY0tGXS5xAoPKg&avtc=1&avte=2&avts=1726751323&keywords=nike+dunk',
#     'https://www.ozon.ru/product/hudi-tvoe-985120837/?advert=s2SowocNwNPosxBHESWWJ7EBnXEDddfSMVE4Mtl91UKNQxhhaSKd_76yW2Nfw3tgzDMD_GnWi5W0ILtp1vBuG1pQeybHA0kiScywD7ynwU3mUiD8lKqf-dlU64e_LURxSFtzAlzvnNbwIiFB4sFgZR2QS8YZ7VxUI9fXDZE934eSzcNRsVE7FAVxQCnDr-KJ0G7HbfoVh58GHDM02eK6sTjmMKX9hgNUEq5tNWgNgFk7z-aE4Phia2W2xrw8zNewUB8BJadodQ9YDiX4ffHaEB9XZ6h4oaB5FdKdMOYf0pFMjLXBiXPASqMUrKoo9HMw3NQ6MrJLfij3X_90FWbYBwqz1lTu_xJnAXCquczZ5GR5YGiKq4He575T5vO2&avtc=1&avte=2&avts=1726752958&keywords=%D1%85%D1%83%D0%B4%D0%B8+%D0%BC%D1%83%D0%B6%D1%81%D0%BA%D0%BE%D0%B5',
#     'https://www.ozon.ru/product/futbolka-tvoe-bazovaya-811535281/?avtc=1&avte=2&avts=1726752963'
#     'https://www.ozon.ru/product/socks-omsa-eco-230688890/?asb=q%252FBYa7IDE3HBgdHd3tgDlcBHbMfzTwqzVggRH9IxRjY%253D&asb2=beHtbxydTGURxeLaDtfns83MzCeHhkUiaCiAu6fGKyXl0-l1JgYdbfKYAY6e2joDteuDQHgB-Bixzt85UJT1NQ&avtc=1&avte=4&avts=1726762498&keywords=%D0%BE%D0%B4%D0%B5%D0%B6%D0%B4%D0%B0',
#     'https://www.ozon.ru/product/socks-set-1243231395/?asb=DA0EIrIbVM2kDT6YrkErA82HfNrdiYJCyEElgX%252FX53Q%253D&asb2=4sFMKAHa5fHKZAyLv4X2c5-JDWTTVo4Iu2-ZfZEP4S4ZDKonYMcCYb4hcC7uRzlFczr1T0ysCzQt6ZmFZKCpDmpg-1a6Elz7zcTfhPBWkLLR-JND3eNxIHccEEGemkEYcXRnozo3_D2hdnkS8tUSUZBNEQQbKu0uqsqGTnvVBDk&avtc=1&avte=2&avts=1726762498&keywords=%D0%BE%D0%B4%D0%B5%D0%B6%D0%B4%D0%B0'
#     'https://www.ozon.ru/product/hudi-jordan-m-j-ess-flc-po-1329382759/?asb=%252FqU0QcZG6PD0xZriA2YYD2n0lSGtGofArPmDa8XX4iY%253D&asb2=dHBYcTwd59LN7_tLTd1cjyfCKhWfJSDDt4nrfJbeQe9CuHMS1pFetWyjo88TAn2r&avtc=1&avte=2&avts=1727173168&keywords=%D1%85%D1%83%D0%B4%D0%B8+jordan',
#     'https://www.ozon.ru/product/bryuki-nike-1250284627/?avtc=1&avte=2&avts=1727173193',
#     'https://www.ozon.ru/product/shokoladnye-batonchiki-snickers-krisper-4-sht-po-40-g-nuga-karamel-vozdushnyy-ris-shokolad-240122961/?advert=AL0AAeA6mNODpJtoQSWaNK7VNW2_kEpf3CoTB-ya8GkiqOVRNkbUXkiSuZKDYctuZgW_40P7KrRZjFn6fSh4hMckF47bEkQbGOflSPdZfIMIkPzOI-sx3z8p4Ac9unvfttoJrPaI-BbDcMGTZBQp8pouwxAf4C-VYjKH35rEz3UrNSD2Bwkm-FWXm2U35c4K4e4RPFR2UbUKQy1z0y0HsOjseC8IA-mFrdG_5SGjdzXEZBDoZJv-65PT_ieRsfnrh9IR2Is4Cw&avtc=1&avte=4&avts=1727173251'
# ]

URLS = [
    'https://www.ozon.ru/product/hoodie-jordan-1329382759/?asb=%252FqU0QcZG6PD0xZriA2YYD2n0lSGtGofArPmDa8XX4iY%253D&asb2=dHBYcTwd59LN7_tLTd1cjyfCKhWfJSDDt4nrfJbeQe9CuHMS1pFetWyjo88TAn2r&avtc=1&avte=2&avts=1727173168&keywords=%D1%85%D1%83%D0%B4%D0%B8+jordan',
    'https://www.ozon.ru/product/komplekt-futbolok-hugo-1607528917/?avtc=1&avte=2&avts=1727174466',
    'https://www.ozon.ru/product/komplekt-noskov-hugo-1474326144/?avtc=1&avte=2&avts=1727174474',
    'https://www.ozon.ru/product/prorezinennyy-chehol-broscorp-dlya-apple-iphone-13-epl-ayfon-13-s-soft-touch-pokrytiem-i-mikrofibroy-380844736/?advert=AL0A0p6I0eK085rFIkyOT-seqC_iTBpxhk-naZZDp3hDcmGtWzoylH9TBhzvp-yvPbmbx5JifpCp8tBorjX4QAPzfDL66GeQjZFUgJEjPoqjIMto48KyqNLZTWXfxq29Ww4t8waXnTNwqPV2w5A7hLdsB1LWmABWwWO1JXCxKAdjivKZuynI8yMBr70qIVDqZA4h9GBUHhJRK4k7E9Cb84ta-KQpSBq0Vvy2uQ2U7nWDuonwuuCYH_Q61uoEMQy_tnanJ8E8XAKCjVLrsZwELpTNoZzSeWcs_0RyBo3OassczrMilWTf8a_jNwx1yf2lPMGNL-IQt1tXquKDkWONo7KVpfz6FFF7x_a0NPdQOmePqM7d7en7L8CyL3rimrjBWyT4YA7C2wCGRo_rV7QxyLh3cE-ng8Y_SRKaabRU7iw&avtc=1&avte=2&avts=1727174490&keywords=%D1%87%D0%B5%D1%85%D0%BE%D0%BB+%D0%BD%D0%B0+%D0%B0%D0%B9%D1%84%D0%BE%D0%BD+13',
    'https://www.ozon.ru/product/chehol-na-ayfon-13-iphone-13-magsave-zelenyy-1601768702/?advert=AL0AK-SX0lKxmc_a0IM_ZjI5Cw9fUTm41Y0sPGfq7rgkfDQoQRUKMTbjmXVBTXZKKgdGzWmtFuwy08g2iqEq1RajD7dtS6etwDSQJTZ8IhPz8eYbpLlwhD3lccS73QKky5ZS5_IO3IypNWpNsTkULOljpxVPcsIMgW_UB2PicBc631dtu9om4cY8zqP4DL1s_TacTysRooWfR71quN2VxeRqxRsLU9XdUxL59H61kFiyQLE6AaH5texo4Sr403uTdMprdQaH32TogO8VtFUFsfoyu9hjuvMrjF7m74cxjElvZqtHJwY9FalwS7fAHXmUIIymInaF_FjG-gexEA1Ux-efye1xn6A93G55Mmz-5jeVUQ4aP_Jjl-AhBdhWGkBfSxLhPwC8AzeHtWDM3zUJe0V9Fs-XmSLfykbgTxtWm5qLttCsIYxRoVP6-g&avtc=1&avte=2&avts=1727174490&keywords=%D1%87%D0%B5%D1%85%D0%BE%D0%BB+%D0%BD%D0%B0+%D0%B0%D0%B9%D1%84%D0%BE%D0%BD+13',
    'https://www.ozon.ru/product/bryuki-sportivnye-nike-w-nsw-style-flc-hr-pant-os-749284686/?advert=AL0ANJPLfLNyJ2l1MGh3FLNnRlzCiURdX2j-5UXxJNEMoZJWMZrW60ME9-hpxafZ6VTJe5FHFXOFe13XdYzTi7DjimVdEAVf1PlIwiupaOe5zXIdU6_-0Di4gv0SqSv8KIOKzAU2lIsls3HX53EETuISw7qIL5ZD-Q8fJS2KFw2iuDvglxfmTaWtYcSBOMcd8JH4KMusFmCJTu3c5X55I8G0Ucd6x7GYz2xhIANmkMvWt5y3lrRsdfJulnWERH8A9SwO5zN2ttMijZ4KvKNiNlDJSAHj4v7CCxWpJLjze8GDYWzCcgaSJEb2xNYSsXpbvZ9W1Ufh5JxNIF6Ywrelo7D1XOaPHrPFgpmYtol9UpKKzmCXQPO4BlM9kSzdj_bG96rwDnbOhLMP-lxnW8qsxjQJiZ7U2BQ&avtc=1&avte=2&avts=1727174550&keywords=%D0%B1%D1%80%D1%8E%D0%BA%D0%B8+%D0%BD%D0%B0%D0%B9%D0%BA',
    'https://www.ozon.ru/product/kurtka-1250536745/?advert=AL0A6XaQ7GL9Ew1g334rMNRCkVVXSwpOUB5wTByNjX24kXt4CrluSYo9SzNsw3vrT1XeV73c_yMqc1mjXuxp4ge77eJPDXaIh16b5oYwXhf17w2g-R8OWTFxJt7sdErpls35DcsLE_PlfDzON19PanLo6r74JC1QxJmIAwSOIru6xhJUSeCKdlJW_wV50Ub-7Ag20SEWG8rL98rEWgKUOYhPl54EPRrblDJiwF1TkhtUdpowNP6Sp7VA9rH5s1rGEKcBwRbRxUBsE7Xxyb4tt_hFlMD2PySex51RrpZEaBLoOMi1n0DBo8GU-IS5F-zS_c8JUr-Fn3x-I75CCmN7ULK6acQAsEhe5murvhIo0e74S66zhT-VMZRb-V-hf4nLOxKqzaV2D2SllYHjbRhh_tH3sktYoSSPscT1&avtc=1&avte=2&avts=1727174573&keywords=%D0%BA%D1%83%D1%80%D1%82%D0%BA%D0%B0+%D0%B7%D0%B8%D0%BC%D0%BD%D1%8F%D1%8F',
    'https://www.ozon.ru/product/kostyum-sportivnyy-1425140298/?avtc=1&avte=2&avts=1727174575'
]

user_names = []
user_reviews = []
reviews_date = []
star_reviews = []
text_len = []
written_by_bot = []



def init_webdriver():
    # chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    #
    # driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Chrome()
    stealth(driver,
            vendor='Google Inc.',
            platform='Win32',
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine")
    return driver


def scroll_page(driver: WebDriver, deep: int) -> None:
    for _ in range(deep):
        driver.execute_script("window.scrollBy(0, 350)")
        time.sleep(0.1)


def parse_user_reviews(HTML: BeautifulSoup) -> None:
    user_review_card = HTML.find_all('div', {'class': 'q0w_29'})
    if not user_review_card:
        return
    for i in range(len(user_review_card)):
        user_name = ((user_review_card[i].find_all('div', {'class': 's5q_29'}))[0]).text

        user_name = user_name.strip()

        if user_name == "Пользователь предпочёл скрыть свои данные":
            user_name = 'No data'

        user_review = user_review_card[i].find_all('div', {'class': 'vq5_29'})
        if user_review:
            user_review = user_review[0].text
        else:
            user_review = 'No data'

        review_date = user_review_card[i].find_all('div', {'class': 'vq3_29'})[0].text
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
        text_len.append(len(user_review))
        written_by_bot.append(0)


def get_main_page_reviews(driver: WebDriver, url: str) -> None:
    # request = requests.get(url)
    #
    # if request.status_code != 200:
    #     return

    driver.get(url)
    time.sleep(5)
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
        'Star review': star_reviews,
        'Text length': text_len
    })
    df.to_csv('dataframe.csv')


if __name__ == '__main__':
    main()
