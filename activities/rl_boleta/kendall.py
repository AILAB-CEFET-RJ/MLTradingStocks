import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pymannkendall as mk
import os


for filename in os.scandir('csvs'):

    outer_df = pd.read_csv(f'{filename.path}', thousands=',', error_bad_lines=False)
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

    plt.clf()
    plt.ylabel('Cotação (Apple)')

    data = outer_df['Last_10_Prices'].values

    ax = plt.gca()
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(True)

    trend, h, p, z, Tau, s, var_s, slope, intercept = mk.original_test(precos_tratados)

    with open('kendall_results.txt', 'a', encoding='utf-8') as f:
        f.write(f'--------------------------{filename}--------------------------\n')
        f.write(f'{str(data)}\n')
        f.write(f'{str(precos_tratados)}\n')
        f.write(f'trend: {trend}\n')
        f.write(f'h: {h}\n')
        f.write(f'p: {p}\n')
        f.write(f'z: {z}\n')
        f.write(f'tau: {Tau}\n')
        f.write(f's: {s}\n')
        f.write(f'var_s: {var_s}\n')
        f.write(f'slope: {slope}\n')
        f.write(f'intercept: {intercept}\n')
        f.write('\n\n\n')

    # print(f'{str(filename.path)}')
    dates = str(filename.path).replace('csvs/', '').replace('.csv', '').replace('.','/')
    start = str(dates).index('(') + 1
    stop = str(dates).index(')')
    dates = f'{dates[start : stop]}'
    dates = dates.split(' a ')
    
    plt.plot(outer_df['Last_10_Prices'])
    plt.title(f'Cotação (Apple) - {dates[0]}/2022 a {dates[1]}/2022')

    date_1_point = dates[0].replace('/', '.')
    date_2_point = dates[1].replace('/', '.')
    plt.savefig(f'cotacoes/({date_1_point} a {date_2_point}).png')
