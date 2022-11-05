import pandas as pd

df = pd.read_csv("weekly data/Sept 2022/Sept.9.22.csv")
df = df.sort_values(by="score", ascending=False)
print(df.head(20))