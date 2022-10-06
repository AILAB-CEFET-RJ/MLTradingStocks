import pandas as pd
import numpy as np
import pdb

df = pd.read_excel('results/25_08_2022_17:05:09.xlsx')

print(df.head())

description = df[['recompensas treino', 'valor final treino', 'lucro/prejui­zo treino', 'recompensas teste', 'valor final teste', 'lucro/prejui­zo teste']].describe().loc[['mean', 'std', 'min', '25%', '50%', '75%','max']].round(decimals=2)

print(description)

print(description.to_latex())







