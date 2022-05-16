import pandas as pd

def treat_data(filename):
    outer_df = pd.read_csv(filename, thousands=',', error_bad_lines=False)
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