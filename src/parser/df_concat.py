import pandas as pd


ozon_df = pd.read_csv('dataframes/ozon_reviews.csv')
wb_df = pd.read_csv('dataframes/wb_reviews.csv')


fake_reviews = pd.read_csv('dataframes/fake_reviews.csv')
reviews_with_typos = pd.read_csv('dataframes/typos_reviews.csv')

main_df = pd.concat([ozon_df, wb_df, fake_reviews, reviews_with_typos], axis=0)
main_df.to_csv('./dataframes/main_df.csv', index=False)

