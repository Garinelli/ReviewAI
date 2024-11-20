from pathlib import Path
import pandas as pd

path = Path(__file__).parent

ozon_df = pd.read_csv(f"{path}/dataframe.csv")
wb_df = pd.read_csv(f"{path}/feedbacks.csv")


fake_reviews_1 = pd.read_csv(f"{path}/fake_feedbacks.csv")
fake_reviews_2 = pd.read_csv(f"{path}/fake_reviews.csv")


main_df = pd.concat([ozon_df, wb_df, fake_reviews_1, fake_reviews_2], axis=0)
main_df.to_csv(f"{path}/main_df_raw.csv", index=False)  # Новый датафрейм

print("Dataframes concatenated successfully!")
