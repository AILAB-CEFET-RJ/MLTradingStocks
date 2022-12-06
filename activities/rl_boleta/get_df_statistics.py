import math
import os
import pandas as pd
import pdb
from data_treatment import treat_data

def get_max_values():
    
    shares = 0.0
    prices = 0.0
    time_hour = 0.0
    time_minute = 0.0
    time_second = 0.0
    last_10_prices = 0.0
    last_10_shares = 0.0
    

    for filename in os.scandir('csvs'):

        print(filename)
        df = treat_data(f'{filename.path.replace("csvs/", "")}')

        description = df.describe()

        shares = shares if math.ceil(description['Shares']['max']) < shares else math.ceil(description['Shares']['max'])
        prices = prices if math.ceil(description['Prices']['max']) < prices else math.ceil(description['Prices']['max'])
        time_hour = time_hour if math.ceil(description['Time_Hour']['max']) < time_hour else math.ceil(description['Time_Hour']['max'])
        time_minute = time_minute if math.ceil(description['Time_Minute']['max']) < time_minute else math.ceil(description['Time_Minute']['max'])
        time_second = time_second if math.ceil(description['Time_Second']['max']) < time_second else math.ceil(description['Time_Second']['max'])
        last_10_prices = last_10_prices if math.ceil(description['Last_10_Prices']['max']) < last_10_prices else math.ceil(description['Last_10_Prices']['max'])
        last_10_shares = last_10_shares if math.ceil(description['Last_10_Shares']['max']) < last_10_shares else math.ceil(description['Last_10_Shares']['max'])

        description = description.applymap('{:.2f}'.format)

        with open('df_statistics.txt', 'a', encoding='utf-8') as f:
            f.write(f'--------------------------{filename}--------------------------')
            f.write(description.to_latex())
            f.write('\n\n\n')


    return shares, prices, time_hour, time_minute, time_second, last_10_prices, last_10_shares

get_max_values()