import pandas as pd

df = pd.read_csv('data\ICRISAT-District Level Data.csv')
unique_names = df['Dist Name'].unique()
print(unique_names)