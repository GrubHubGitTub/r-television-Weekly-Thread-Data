import pandas as pd

df = pd.read_csv("shows.csv")
df = df.sort_values(by="score", ascending=False)
print(df.head(20))