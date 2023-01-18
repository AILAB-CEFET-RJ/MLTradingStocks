import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from data_treatment import treat_data

files = ['consolidado_treinamento (01.12 a 06.12).csv', 'consolidado_treinamento (10.01 a 14.01).csv', \
    'consolidado_treinamento (18.01 a 26.01).csv', 'consolidado_treinamento (21.02 a 11.03).csv', \
    'consolidado_treinamento (23.03 a 28.03).csv', 'consolidado_treinamento (07.04 a 15.04).csv',
    'consolidado_treinamento (18.04 a 29.04).csv', 'consolidado_teste (02.05 a 13.05).csv']

last_10_treated = []

for file in files:
    treated_df = treat_data(f'{file}')['Last_10_Prices']
    for i in range(10, len(treated_df), 10):
        last_10_treated.append(np.mean(treated_df[i - 10 : i]))

    # print(last_10_treated[0:10])
    acf_plot = plot_acf(last_10_treated, lags=1000)
    # acf_plot = plot_pacf(last_10_treated, lags=20)
    plt.show()
    plt.savefig(f'acf_pacf/acf/{file}.png')
    # plt.savefig(f'acf_pacf/pacf/{file}.png')


