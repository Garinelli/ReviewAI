from reviews.reviews import reviews
import pandas as pd

user_reviews = []
summaries = []

def main():
    for review in reviews:
        user_reviews.append(review["reviews"])
        summaries.append(review["summary"])

    transformer_dataset = pd.DataFrame(
        {
            'Reviews': user_reviews,
            'Summary': summaries,
        }
    )

    transformer_dataset.to_csv('./dataframes/transformer_df.csv')

if __name__ == "__main__":
    main()

