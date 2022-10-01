import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pymannkendall as mk


# outer_df = pd.read_csv(f'consolidado_treinamento (23.03 a 28.03).csv', thousands=',', error_bad_lines=False)
# outer_df = pd.read_csv(f'consolidado_treinamento (21.02 a 11.03).csv', thousands=',', error_bad_lines=False)
# outer_df = pd.read_csv(f'consolidado_treinamento (18.04 a 29.04).csv', thousands=',', error_bad_lines=False)
# outer_df = pd.read_csv(f'consolidado_treinamento (07.04 a 15.04).csv', thousands=',', error_bad_lines=False)
# outer_df = pd.read_csv(f'consolidado_treinamento (18.01 a 26.01).csv', thousands=',', error_bad_lines=False)
# outer_df = pd.read_csv(f'consolidado_treinamento (10.01 a 14.01).csv', thousands=',', error_bad_lines=False)
# outer_df = pd.read_csv(f'consolidado_treinamento (01.12 a 06.12).csv', thousands=',', error_bad_lines=False)
outer_df = pd.read_csv(f'csvs/consolidado_teste (02.05 a 13.05).csv', thousands=',', error_bad_lines=False)
# outer_df = pd.read_csv(f'', thousands=',', error_bad_lines=False)
outer_df = outer_df.sort_values('File Date')


outer_df['Day'] = [x[0:10] for x in outer_df['Day']]
unique_dates = np.unique(outer_df['Day'])

outer_df = outer_df[outer_df['Ticker'] == 'AAPL']
outer_df = outer_df[outer_df['Prices'] < 1000.00]
outer_df = outer_df[outer_df['Prices'] > 100.00]
outer_df.drop_duplicates()
outer_df.drop('File Date', axis='columns', inplace=True)
outer_df.drop('Ticker', axis='columns', inplace=True)
outer_df.drop('Day', axis='columns', inplace=True)
outer_df.reset_index(drop=True, inplace=True)
outer_df['Shares'] = outer_df['Shares'].astype(float)

precos_tratados = []

for i in range(0, len(outer_df), 10):
    precos_tratados.append(outer_df.loc[i, "Last_10_Prices"])

# print(len(outer_df))
# print(len(precos_tratados))

plt.clf()
plt.ylabel('Cotação (Apple)')
# plt.title('Cotação (Apple) - 18/04/2022 a 29/04/2022')
# plt.title('Cotação (Apple) - 07/04/2022 a 15/04/2022')
# plt.title('Cotação (Apple) - 01/12/2021 a 06/12/2021')
# plt.title('Cotação (Apple) - 02/05/2022 a 13/05/2022')
# plt.title('Cotação (Apple) - 21/02/2022 a 11/03/2022')
# plt.title('Cotação (Apple) - 18/01/2022 a 26/01/2022')
# plt.title('Cotação (Apple) - 10/01/2022 a 14/01/2022')
# plt.title('Cotação (Apple) - 23/03/2022 a 28/03/2022')


# print(outer_df['Last_10_Prices'].values)
data = outer_df['Last_10_Prices'].values
# data = pd.read_csv("consolidado_teste (02.05 a 13.05).csv",parse_dates=['Last_10_Prices'],index_col='Last_10_Prices')

ax = plt.gca()
ax.axes.xaxis.set_visible(False)
ax.axes.yaxis.set_visible(True)

print(type(data))
print(data)

plt.plot(outer_df['Last_10_Prices'])
# plt.plot(precos_tratados)

# data = outer_df['Last_10_Prices']

print(precos_tratados)

trend, h, p, z, Tau, s, var_s, slope, intercept = mk.original_test(precos_tratados)
print(f'trend: {trend}')
print(f'h: {h}')
print(f'p: {p}')
print(f'z: {z}')
print(f'tau: {Tau}')
print(f's: {s}')
print(f'var_s: {var_s}')
print(f'slope: {slope}')
print(f'intercept: {intercept}')