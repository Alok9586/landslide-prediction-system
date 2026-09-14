import pandas as pd
df = pd.read_csv("data/nasa_landslide_catalog.csv")
print(df.columns.tolist())
print(df.head())