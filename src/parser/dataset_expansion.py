from random import randint
import pandas as pd

from reviews.fake_reviews import fake_reviews

user_reviews = []
reviews_date = []
star_reviews = []
text_len = []
written_by_bot = []
has_media = []
has_answer = []

def main():
    for review in fake_reviews:
        user_reviews.append(review['user_review'])
        reviews_date.append(review['reviews_date'])
        star_reviews.append(review['star_review'])
        text_len.append(review['text_len'])
        written_by_bot.append(review['written_by_bot'])
        has_media.append(review['has_media'])
        has_answer.append(randint(0, 1))
    fake_dataset = pd.DataFrame(
        {
            'User review': user_reviews,
            'Review date': reviews_date,
            'Star review': star_reviews,
            'Text length': text_len,
            'Has media': has_media,
            "Has answer": has_answer,
            'Written by bot': written_by_bot,
        }
    )

    fake_dataset['User review'] = fake_dataset['User review'].str.lower()
    fake_dataset.drop_duplicates(subset=['User review'], keep='first', inplace=True)
    fake_dataset.to_csv('./dataframes/fake_reviews.csv')


if __name__ == '__main__':
    main()
