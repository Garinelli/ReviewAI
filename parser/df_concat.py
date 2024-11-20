import pandas as pd


ozon_df = pd.read_csv("dataframe.csv")
wb_df = pd.read_csv("feedbacks.csv")


fake_reviews_1 = pd.read_csv("fake_feedbacks.csv")
fake_reviews_2 = pd.read_csv("fake_reviews.csv")


main_df = pd.concat([ozon_df, wb_df, fake_reviews_1, fake_reviews_2], axis=0)
main_df.to_csv("main_df_raw.csv", index=False)  # Новый датафрейм

print("Dataframes concatenated successfully!")
