import pandas as pd

df = pd.read_csv("test.csv", header = 0, parse_dates = True)
print(df.head())