import pandas as pd

df = pd.read_csv('investments_VC.csv')
df.info()

df['Name'].fillna("NaN", inplace=True)

df.info()