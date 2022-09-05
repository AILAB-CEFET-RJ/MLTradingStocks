import pandas as pd
import pdb
import numpy as np

quantidade_dias = 0

def treat_data(filename):
    outer_df = pd.read_csv(f'csvs/{filename}', thousands=',', error_bad_lines=False)
    outer_df = outer_df.sort_values('File Date')
    outer_df = outer_df[outer_df['Ticker'] == 'AAPL']
    outer_df = outer_df[outer_df['Prices'] < 1000.00]
    outer_df = outer_df[outer_df['Prices'] > 100.00]
    outer_df.drop_duplicates()
    outer_df.drop('File Date', axis='columns', inplace=True)
    outer_df.drop('Ticker', axis='columns', inplace=True)
    outer_df.drop('Day', axis='columns', inplace=True)
    outer_df.reset_index(drop=True, inplace=True)
    outer_df['Shares'] = outer_df['Shares'].astype(float)

    # print(outer_df.head())
    return outer_df


def treat_testing_data(filename, quantidade_dias_teste, repetitive_iteration_number):
    outer_df = pd.read_csv(f'csvs/{filename}', thousands=',', error_bad_lines=False)
    outer_df = outer_df.sort_values('File Date')


    outer_df['Day'] = [x[0:10] for x in outer_df['Day']]
    unique_dates = np.unique(outer_df['Day'])

    chosen_days = unique_dates[0 : quantidade_dias_teste]
    outer_df = outer_df[outer_df['Day'].isin(chosen_days)]

    # pdb.set_trace()

    outer_df = outer_df[outer_df['Ticker'] == 'AAPL']
    outer_df = outer_df[outer_df['Prices'] < 1000.00]
    outer_df = outer_df[outer_df['Prices'] > 100.00]
    outer_df.drop_duplicates()
    outer_df.drop('File Date', axis='columns', inplace=True)
    outer_df.drop('Ticker', axis='columns', inplace=True)
    outer_df.drop('Day', axis='columns', inplace=True)
    outer_df.reset_index(drop=True, inplace=True)
    outer_df['Shares'] = outer_df['Shares'].astype(float)

    return outer_df


    