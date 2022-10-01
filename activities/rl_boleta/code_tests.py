import pandas as pd

outer_df = pd.read_csv(f'csvs/consolidado_teste (02.05 a 13.05).csv', thousands=',', error_bad_lines=False)

outer_df = outer_df.loc[outer_df['Ticker'] == 'AAPL']
outer_df.drop('File Date', axis='columns', inplace=True)
outer_df.drop('Ticker', axis='columns', inplace=True)
outer_df.drop('Day', axis='columns', inplace=True)

apple_sample = outer_df[0:10]
print(apple_sample.to_string(index=False))


# print(apple_sample.T.drop(apple_sample.T.index[0]))
print(apple_sample.T)
