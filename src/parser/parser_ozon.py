import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from selenium_stealth import stealth

driver = webdriver.Chrome()

stealth(driver,
        vendor='Google Inc.',
        platform='Win32',
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine")

driver.get("https://www.ozon.ru/product/tecno-smartfon-spark-30c-8-256-gb-chernyy-1713666000/")

time.sleep(5)
current_height = driver.execute_script("return window.scrollY;")
while True:
    driver.execute_script("window.scrollBy(0, 350)")
    time.sleep(0.1)
    if current_height == driver.execute_script("return window.scrollY;"):
        break
    current_height = driver.execute_script("return window.scrollY;")

main_page_html = BeautifulSoup(driver.page_source, 'html.parser')

review_div = main_page_html.find_all('div', {'data-widget': 'webReviewTabs'})

if review_div:
    span_elements = review_div[0].find_all('span')
    for index, span in enumerate(span_elements):
        if (len(span.text)) and ('\xa0' in span.text[-1]):
            print(f'-' * 100)
            print(f'{index = }')
            print(f'{str(span.text) = }')
            print(f'{span.get("class") = }')
            print(f'-' * 100)
