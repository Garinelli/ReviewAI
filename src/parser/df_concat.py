import pandas as pd


ozon_df = pd.read_csv('dataframes/dataframe.csv')
wb_df = pd.read_csv('dataframes/feedbacks.csv')


fake_reviews_1 = pd.read_csv('dataframes/fake_feedbacks.csv')
fake_reviews_2 = pd.read_csv('dataframes/fake_reviews.csv')
reviews_with_typos = pd.read_csv('dataframes/typos_reviews.csv')

main_df = pd.concat([ozon_df, wb_df, fake_reviews_1, fake_reviews_2, reviews_with_typos], axis=0)
main_df.to_csv('./dataframes/main_df.csv', index=False)