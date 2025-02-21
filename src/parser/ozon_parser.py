import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium_stealth import stealth

URLS = [
    'https://www.ozon.ru/product/kurtka-1250536745/?advert=AL0A6XaQ7GL9Ew1g334rMNRCkVVXSwpOUB5wTByNjX24kXt4CrluSYo9SzNsw3vrT1XeV73c_yMqc1mjXuxp4ge77eJPDXaIh16b5oYwXhf17w2g-R8OWTFxJt7sdErpls35DcsLE_PlfDzON19PanLo6r74JC1QxJmIAwSOIru6xhJUSeCKdlJW_wV50Ub-7Ag20SEWG8rL98rEWgKUOYhPl54EPRrblDJiwF1TkhtUdpowNP6Sp7VA9rH5s1rGEKcBwRbRxUBsE7Xxyb4tt_hFlMD2PySex51RrpZEaBLoOMi1n0DBo8GU-IS5F-zS_c8JUr-Fn3x-I75CCmN7ULK6acQAsEhe5murvhIo0e74S66zhT-VMZRb-V-hf4nLOxKqzaV2D2SllYHjbRhh_tH3sktYoSSPscT1&avtc=1&avte=2&avts=1727174573&keywords=%D0%BA%D1%83%D1%80%D1%82%D0%BA%D0%B0+%D0%B7%D0%B8%D0%BC%D0%BD%D1%8F%D1%8F',
    'https://www.ozon.ru/product/komplekt-noskov-gsd-5-par-1304166484/?advert=AL0AkA9EuB4bHisNQ_AXVeP-NDW-gNdCVNPG5_oT-3hyrnWHtoy_Fw_I5I6GbvyvDkNej-9apCoqQrAAFDnY5nnEzM0WBlHuxcYU20g9dteq-3dYxPLj_G_LM7nZyC0FnMtu32wwXxDoKvBrfVN-GyjyfngKkmrjzx2m7WdETfEKUWh7uJocs1AINtbLxtXKiiZ8VovKGwUXxc7ydOVjKCOK3JUzoOTxRzI4l4BWIUTZVZ-7h9lyaOkgNVegPeokGHo-9ZRHaEQIanKo&avtc=1&avte=2&avts=1727175476'
    'https://www.ozon.ru/product/hoodie-jordan-1329382759/?asb=%252FqU0QcZG6PD0xZriA2YYD2n0lSGtGofArPmDa8XX4iY%253D&asb2=dHBYcTwd59LN7_tLTd1cjyfCKhWfJSDDt4nrfJbeQe9CuHMS1pFetWyjo88TAn2r&avtc=1&avte=2&avts=1727173168&keywords=%D1%85%D1%83%D0%B4%D0%B8+jordan',
    'https://www.ozon.ru/product/komplekt-futbolok-hugo-1607528917/?avtc=1&avte=2&avts=1727174466',
    'https://www.ozon.ru/product/komplekt-noskov-hugo-1474326144/?avtc=1&avte=2&avts=1727174474',
    'https://www.ozon.ru/product/prorezinennyy-chehol-broscorp-dlya-apple-iphone-13-epl-ayfon-13-s-soft-touch-pokrytiem-i-mikrofibroy-380844736/?advert=AL0A0p6I0eK085rFIkyOT-seqC_iTBpxhk-naZZDp3hDcmGtWzoylH9TBhzvp-yvPbmbx5JifpCp8tBorjX4QAPzfDL66GeQjZFUgJEjPoqjIMto48KyqNLZTWXfxq29Ww4t8waXnTNwqPV2w5A7hLdsB1LWmABWwWO1JXCxKAdjivKZuynI8yMBr70qIVDqZA4h9GBUHhJRK4k7E9Cb84ta-KQpSBq0Vvy2uQ2U7nWDuonwuuCYH_Q61uoEMQy_tnanJ8E8XAKCjVLrsZwELpTNoZzSeWcs_0RyBo3OassczrMilWTf8a_jNwx1yf2lPMGNL-IQt1tXquKDkWONo7KVpfz6FFF7x_a0NPdQOmePqM7d7en7L8CyL3rimrjBWyT4YA7C2wCGRo_rV7QxyLh3cE-ng8Y_SRKaabRU7iw&avtc=1&avte=2&avts=1727174490&keywords=%D1%87%D0%B5%D1%85%D0%BE%D0%BB+%D0%BD%D0%B0+%D0%B0%D0%B9%D1%84%D0%BE%D0%BD+13',
    'https://www.ozon.ru/product/chehol-na-ayfon-13-iphone-13-magsave-zelenyy-1601768702/?advert=AL0AK-SX0lKxmc_a0IM_ZjI5Cw9fUTm41Y0sPGfq7rgkfDQoQRUKMTbjmXVBTXZKKgdGzWmtFuwy08g2iqEq1RajD7dtS6etwDSQJTZ8IhPz8eYbpLlwhD3lccS73QKky5ZS5_IO3IypNWpNsTkULOljpxVPcsIMgW_UB2PicBc631dtu9om4cY8zqP4DL1s_TacTysRooWfR71quN2VxeRqxRsLU9XdUxL59H61kFiyQLE6AaH5texo4Sr403uTdMprdQaH32TogO8VtFUFsfoyu9hjuvMrjF7m74cxjElvZqtHJwY9FalwS7fAHXmUIIymInaF_FjG-gexEA1Ux-efye1xn6A93G55Mmz-5jeVUQ4aP_Jjl-AhBdhWGkBfSxLhPwC8AzeHtWDM3zUJe0V9Fs-XmSLfykbgTxtWm5qLttCsIYxRoVP6-g&avtc=1&avte=2&avts=1727174490&keywords=%D1%87%D0%B5%D1%85%D0%BE%D0%BB+%D0%BD%D0%B0+%D0%B0%D0%B9%D1%84%D0%BE%D0%BD+13',
    'https://www.ozon.ru/product/bryuki-sportivnye-nike-w-nsw-style-flc-hr-pant-os-749284686/?advert=AL0ANJPLfLNyJ2l1MGh3FLNnRlzCiURdX2j-5UXxJNEMoZJWMZrW60ME9-hpxafZ6VTJe5FHFXOFe13XdYzTi7DjimVdEAVf1PlIwiupaOe5zXIdU6_-0Di4gv0SqSv8KIOKzAU2lIsls3HX53EETuISw7qIL5ZD-Q8fJS2KFw2iuDvglxfmTaWtYcSBOMcd8JH4KMusFmCJTu3c5X55I8G0Ucd6x7GYz2xhIANmkMvWt5y3lrRsdfJulnWERH8A9SwO5zN2ttMijZ4KvKNiNlDJSAHj4v7CCxWpJLjze8GDYWzCcgaSJEb2xNYSsXpbvZ9W1Ufh5JxNIF6Ywrelo7D1XOaPHrPFgpmYtol9UpKKzmCXQPO4BlM9kSzdj_bG96rwDnbOhLMP-lxnW8qsxjQJiZ7U2BQ&avtc=1&avte=2&avts=1727174550&keywords=%D0%B1%D1%80%D1%8E%D0%BA%D0%B8+%D0%BD%D0%B0%D0%B9%D0%BA',
    'https://www.ozon.ru/product/kostyum-sportivnyy-1425140298/?avtc=1&avte=2&avts=1727174575',
    'https://www.ozon.ru/product/xiaomi-smartfon-redmi-a3x-3-64-gb-zelenyy-1628749061/?advert=AMMAUX7w4j5BqXZ4-bhlv63_mjg1-pFgGq1H95jnYaIp8iVl6X6XCbsi-JRiaH-93DFmx534aQjcVVgRnuqOBVvXoiBGhK8kKmi1wkZZrgJirg2YCHRqebIrAOluJOSSaeursD9hixztaon9iKJtTcnPOGusVwKkaXX5GsB13URjcolfRH6LV6jYDD9vpNcvuPGfjSX6PXSZqZ2konSPR_t1djSd5iX9xMcY0HE6ISbYF53BnDHovNPQkDps7nvBaJb0KjMQSxwZpW9mjIP4sX8pnb6xWN3MxzBcD-ord8wqO7ofOi2KopYRw4aQsmyZUpuI5FRyOHNjBbYfxnz9A_KazDp5Iw4mMm314Y12UbUoUzUh9TLyydQD1qHI-7oH&avtc=1&avte=4&avts=1727707047&keywords=%D1%82%D0%B5%D0%BB%D0%B5%D1%84%D0%BE%D0%BD+xiaomi+redmi'
]


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


def parse_user_reviews(HTML: BeautifulSoup) -> None:
    review_div = HTML.find_all('div', {'data-widget': 'webReviewTabs'})

    if review_div:
        span_elements = review_div[0].find_all('span')
        for index, span in enumerate(span_elements):
            if (len(span.text)) and ('\xa0' in span.text[-1]):
                print(f'-' * 100)
                print(f'{index = }')
                print(f'{str(span.text) = }')
                print(f'{span.get("class") = }')
                print(f'-' * 100)


def get_main_page_reviews(driver: WebDriver, url: str) -> None:
    driver.get(url)
    time.sleep(5)
    scroll_page(driver)
    main_page_html = BeautifulSoup(driver.page_source, 'html.parser')
    parse_user_reviews(main_page_html)


def main():
    driver = init_webdriver()
    for i in range(len(URLS)):
        get_main_page_reviews(driver, URLS[i])


if __name__ == '__main__':
    main()
