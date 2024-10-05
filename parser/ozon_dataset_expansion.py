import pandas as pd

from fake_reviews import fake_reviews

user_reviews = []
reviews_date = []
star_reviews = []
text_len = []
written_by_bot = []
has_media = []


def main():
    for review in fake_reviews:
        user_reviews.append(review['user_review'])
        reviews_date.append(review['reviews_date'])
        star_reviews.append(review['star_review'])
        text_len.append(review['text_len'])
        written_by_bot.append(review['written_by_bot'])
        has_media.append(review['has_media'])

    fake_dataset = pd.DataFrame(
        {
            'user_review': user_reviews,
            'review_date': reviews_date,
            'star_review': star_reviews,
            'text_len': text_len,
            'written_by_bot': written_by_bot,
            'has_media': has_media
        }
    )

    fake_dataset.to_csv('fake_reviews.csv')


if __name__ == '__main__':
    main()
