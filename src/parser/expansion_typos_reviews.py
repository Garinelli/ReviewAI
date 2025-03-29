import pandas as pd

from reviews.reviews_with_typos import reviews

user_reviews = []
reviews_date = []
star_reviews = []
text_len = []
written_by_bot = []
has_media = []
def main():
    for review in reviews:
        user_reviews.append(review['user_review'])
        reviews_date.append(review['reviews_date'])
        star_reviews.append(review['star_review'])
        text_len.append(review['text_len'])
        written_by_bot.append(review['written_by_bot'])
        has_media.append(review['has_media'])
    fake_dataset = pd.DataFrame(
        {
            'User review': user_reviews,
            'Review date': reviews_date,
            'Star review': star_reviews,
            'Text length': text_len,
            'Has media': has_media,
            'Written by bot': written_by_bot,
        }
    )

    fake_dataset.to_csv('./dataframes/typos_reviews.csv')


if __name__ == '__main__':
    main()