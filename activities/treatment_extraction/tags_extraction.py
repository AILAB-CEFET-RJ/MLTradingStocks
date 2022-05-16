from datetime import datetime
import os
import glob
from bs4 import BeautifulSoup
import codecs
import numpy as np
from numpy.core.numeric import full
from numpy.lib.function_base import append
from numpy.lib.npyio import savetxt
import pandas as pd
from pandas.core.base import DataError
from html_files_check import check_all_folders


check_all_folders()

folders = glob.glob(os.getcwd() + '/html_data/*/')
# folders = glob.glob(os.getcwd() + '/training_data/*/')

for folder in folders:
    try:
        print(f'Folder: {folder}')

        filenames = glob.glob(folder + '*.html')

        # print(f'Filenames: {filenames}')


        for file in filenames:
            print(f'File: {file}')
            file_date = []
            ticker = []
            day = []
            ask_shares = []
            ask_prices = []
            bid_shares = []
            bid_prices = []

            negotiation_prices = []
            negotiation_shares = []

            last_10_times_hours = []
            last_10_times_minutes = []
            last_10_times_seconds = []
            last_10_prices = []
            last_10_shares = []

            final_array = []


            print(file)
            html = codecs.open(file, "r", encoding="utf8")
            print("pós leitura do codec html")
            soup = BeautifulSoup(html.read(), 'html.parser')

            tds_ask_shares = soup.findAll('td', attrs={'class': 'book-viewer__ask book-viewer__ask-shares'})
            tds_ask_prices = soup.findAll('td', attrs={'class': 'book-viewer__ask book-viewer__ask-price book-viewer-price'})
            tds_bid_shares = soup.findAll('td', attrs={'class': 'book-viewer__bid book-viewer__bid-shares'})
            tds_bid_prices = soup.findAll('td', attrs={'class': 'book-viewer__bid book-viewer__bid-price book-viewer-price'})
            tds_last_10_times = soup.findAll('td', attrs={'class': 'book-viewer__trades-time'})
            tds_last_10_prices = soup.findAll('td', attrs={'class': 'book-viewer__trades-price'})
            tds_last_10_shares = soup.findAll('td', attrs={'class': 'book-viewer__trades-shares'})

            for i in tds_ask_shares:
                ask_shares.append(i.text.replace(u"\xa0", u"0").replace(",",""))
            ask_shares = list(map(int, ask_shares))
            print(ask_shares)

            for i in tds_bid_shares:
                bid_shares.append(i.text.replace(u"\xa0", u"0").replace(",",""))
            bid_shares = list(map(int, bid_shares))
            print(bid_shares)

            negotiation_shares = ask_shares + bid_shares
            print(f'negoshares: {negotiation_shares}')


            for i in tds_ask_prices:
                ask_prices.append(i.text.replace(u"\xa0", u"0").replace(",",""))
            ask_prices = list(map(float, ask_prices))
            print(ask_prices)

            for i in tds_bid_prices:
                bid_prices.append(i.text.replace(u"\xa0", u"0").replace(",",""))
            bid_prices = list(map(float, bid_prices))
            print(bid_prices)

            negotiation_prices = ask_prices + bid_prices


            for i in tds_last_10_times:
                try:
                    beginning = len(folder)
                    end = len(file)

                    tail_string = file[beginning : end]
                    date = tail_string.split("_")[1]
            
                    # print(f'i: ({i.text})')
                    print(i.text == " ")
                    hour = i.text.split(":")[0]
                    minute = i.text.split(":")[1]
                    second = i.text.split(":")[2]
                    last_10_times_hours.append(hour.replace(u"\xa0", u"0").replace(",",""))
                    last_10_times_minutes.append(minute.replace(u"\xa0", u"0").replace(",",""))
                    last_10_times_seconds.append(second.replace(u"\xa0", u"0").replace(",",""))
                    
                    full_date = date + ' ' + hour + ':' + minute + ':' + second
                    day.append(datetime.strptime(full_date, '%Y-%m-%d %H:%M:%S'))
                except:
                    last_10_times_hours.append('0')
                    last_10_times_minutes.append('0')
                    last_10_times_seconds.append('0')
                    full_date = date + ' 00:00:00'
                    
                    day.append(datetime.strptime(full_date, '%Y-%m-%d %H:%M:%S'))
                
            last_10_times_hours = list(map(int, last_10_times_hours))
            last_10_times_minutes = list(map(int, last_10_times_minutes))
            last_10_times_seconds = list(map(int, last_10_times_seconds))
            
            for i in tds_last_10_prices:
                last_10_prices.append(i.text.replace(u"\xa0", u"0").replace(",",""))

            last_10_prices = list(map(float, last_10_prices))
            # print(last_10_prices)


            for i in tds_last_10_shares:
                last_10_shares.append(i.text.replace(u"\xa0", u"0").replace(",",""))

            last_10_shares = list(map(int, last_10_shares))
            # print(last_10_shares)


            tail_string = file[beginning : end - 5]
            # print(tail_string)
            company = tail_string.split("_")[0]
            # print(f'Company: {company}')
            ticker = [company for x in range(10)]

            
            beginning = len(folder)
            # beginning = len(os.getcwd() + '/html/')
            end = len(file)
            
            tail_string = file[beginning : end]
            date = tail_string.split("_")[1]
            hour = tail_string.split("_")[2].split("-")[0]
            minute = tail_string.split("_")[2].split("-")[1]
            second = tail_string.split("_")[2].split("-")[2].split(".")[0]
            
            full_date = date + ' ' + hour + ':' + minute + ':' + second
            
            for _ in range(10):
                file_date.append(datetime.strptime(full_date, '%Y-%m-%d %H:%M:%S'))
            
            
            final_array = np.vstack((file_date, ticker, day, negotiation_shares, negotiation_prices, last_10_times_hours, last_10_times_minutes, last_10_times_seconds, last_10_prices, last_10_shares))
            final_array = np.transpose(final_array)
            final_array_pd = pd.DataFrame(final_array, columns=['File Date','Ticker','Day', 'Shares','Prices','Time_Hour','Time_Minute','Time_Second','Last_10_Prices','Last_10_Shares'])

            print(final_array_pd)


            # final_array_pd.to_csv('testando.csv')

            filepath = os.getcwd() + '/consolidado_treinamento.csv'
            # print(filepath)

            if os.path.exists(filepath):
                dfOld = pd.read_csv('consolidado_treinamento.csv')
                dfNew = dfOld.append(final_array_pd, ignore_index=False)
                dfNew.to_csv('consolidado_treinamento.csv', index=False, encoding='utf-8')
            else:
                final_array_pd.to_csv('consolidado_treinamento.csv', index=False, encoding='utf-8')
                
    except Exception as e:
        print(e)
        continue
