import math
import os
import pandas as pd
import pdb

def get_max_values():
    
    shares = 0.0
    prices = 0.0
    time_hour = 0.0
    time_minute = 0.0
    time_second = 0.0
    last_10_prices = 0.0
    last_10_shares = 0.0
    

    for filename in os.scandir('csvs'):

        df = pd.read_csv(f'{filename.path}', thousands=',', error_bad_lines=False)

        description = df.describe()

        shares = shares if math.ceil(description['Shares']['max']) < shares else math.ceil(description['Shares']['max'])
        prices = prices if math.ceil(description['Prices']['max']) < prices else math.ceil(description['Prices']['max'])
        time_hour = time_hour if math.ceil(description['Time_Hour']['max']) < time_hour else math.ceil(description['Time_Hour']['max'])
        time_minute = time_minute if math.ceil(description['Time_Minute']['max']) < time_minute else math.ceil(description['Time_Minute']['max'])
        time_second = time_second if math.ceil(description['Time_Second']['max']) < time_second else math.ceil(description['Time_Second']['max'])
        last_10_prices = last_10_prices if math.ceil(description['Last_10_Prices']['max']) < last_10_prices else math.ceil(description['Last_10_Prices']['max'])
        last_10_shares = last_10_shares if math.ceil(description['Last_10_Shares']['max']) < last_10_shares else math.ceil(description['Last_10_Shares']['max'])

    return shares, prices, time_hour, time_minute, time_second, last_10_prices, last_10_shares
