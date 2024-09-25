import pandas as pd
import requests


def get_respose():
    url = "https://feedbacks1.wb.ru/feedbacks/v1/193361488"  # 13 comments
    # url = "https://feedbacks1.wb.ru/feedbacks/v1/14045631" # 1000 comments

    headers = {
        "Accept": "*/*",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Origin": "https://www.wildberries.by",
        "Referer": "https://www.wildberries.by/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "sec-ch-ua": 'Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "macOS",
    }

    response = requests.get(url=url, headers=headers)

    return response.json()


def prepare_items(response):
    comments = []
    comments_raw = response.get("feedbacks", [])

    if len(comments_raw) > 0:
        for feedback in comments_raw:
            comments.append(
                {
                    "nmId": feedback.get("nmId", None),
                    "text": feedback.get("text", "").replace("\n", "\\n"),
                    "productValuation": feedback.get("productValuation", None),
                    "createdDate": feedback.get("createdDate", None),
                    "photo": feedback.get("photo", []),
                    "answer": (feedback.get("answer", {}) or {})
                    .get("text", "")
                    .replace("\n", "\\n"),
                }
            )

    return comments


def main():
    response = get_respose()
    feedbacks = prepare_items(response)

    pd.DataFrame(feedbacks).to_csv("./parser/feedbacks.csv", index=False)


if __name__ == "__main__":
    main()
