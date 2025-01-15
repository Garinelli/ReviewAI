import pandas as pd
import requests


def get_respose():
    # url = "https://feedbacks1.wb.ru/feedbacks/v1/193361488"  # 13 comments / 214208823
    # url = "https://feedbacks1.wb.ru/feedbacks/v1/14045631"  # 1000 comments
    url = "https://feedbacks2.wb.ru/feedbacks/v1/32359313"  # / 43400117

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


def prepare_items(response, nmId: int):
    comments = []
    comments_raw = response.get("feedbacks", [])

    if len(comments_raw) > 0:
        for feedback in comments_raw:
            if feedback["nmId"] == nmId and len(feedback["text"]):
                comments.append(
                    {
                        "User review": feedback["text"].replace("\n", "\\n"),
                        "Review date": feedback["createdDate"][:10],
                        "Star review": feedback["productValuation"],
                        "Text length": len(feedback["text"]),
                        "Has media": int(bool(feedback.get("photo", []))),
                        "Has answer": int(bool(feedback["answer"])),
                        "Written by bot": 0,
                    }
                )

    return comments


def main():
    response = get_respose()
    feedbacks = prepare_items(response, nmId=43400117)

    pd.DataFrame(feedbacks).to_csv("./parser/wb_reviews.csv", index=False)


if __name__ == "__main__":
    main()
