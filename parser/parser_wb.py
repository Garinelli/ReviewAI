import asyncio

# import requests
# from bs4 import BeautifulSoup
from playwright.async_api import async_playwright


# URL страницы, на которой нужно найти элемент
def get_feedback_link(url: str) -> str:
    url = url[: url.rfind("/")] + "/feedbacks"
    return url


def get_host_wb() -> str:
    return "https://www.wildberries.ru"


async def get_comments(url: str) -> str | None:
    async with async_playwright() as p:
        # Запустим браузер
        browser = await p.chromium.launch()
        # Откроем новую страницу
        page = await browser.new_page()

        # Задайте URL страницы, на которой нужно искать элемент
        await page.goto(url)

        for _ in range(60):
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight*2)")
            await page.wait_for_timeout(500)  # Ждем, чтобы контент успел подгрузиться

            element = await page.query_selector_all(
                ".comments__item.feedback.j-feedback-slide"
            )
            if element and _ == 59:
                break
                # name = await (
                #     await element.query_selector(".feedback__header")
                # ).inner_text()

                # text = await (
                #     await element.query_selector(".feedback__text--item")
                # ).inner_text()

                # date = await (
                #     await element.query_selector(".feedback__date")
                # ).inner_text()

                # rating = (
                #     await (
                #         await element.query_selector(".feedback__rating.stars-line")
                #     ).get_attribute("class")
                # )[-1]

                # photos = await element.query_selector(".feedback__photos") is not None
                # print(name, rating, photos)

        print(len(element))

        # Закроем браузер
        await browser.close()

        return


def main():
    # url = "https://www.wildberries.ru/catalog/243062249/detail.aspx"
    url = "https://www.wildberries.ru/catalog/158911862/detail.aspx?targetUrl=SG"
    # url = edit_link(url)
    # Запускаем асинхронную функцию
    print(asyncio.run(get_comments(get_feedback_link(url))))


if __name__ == "__main__":
    main()
