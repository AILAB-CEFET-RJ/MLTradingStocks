import urllib

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import concurrent.futures
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import time
import codecs
import os
import glob
import gc
from pytz import timezone


tz = timezone('US/Eastern')
pd.set_option('display.max_columns', 500)



def html2csv(papel):
# Read html file
    last_datetime = None
    current_datetime = None
    top_shares_formatted = []
    top_prices_formatted = []
    last_10_times_formatted = []
    last_10_prices_formatted = []
    last_10_shares_formatted = []
    last_booktype = []
    last_stock = []
    captured_datetime = []

    filenames = glob.glob(os.getcwd() + '/html/' + papel + "_" + datetime.now().strftime('%Y-%m-%d') + '*.html')
    print(f"comecou a ler arquivos html\nFilename: {filenames}")

    for file in filenames:
        print(f'File:{file}')
        print("antes do codec")
        html = codecs.open(file, "r", encoding="utf8")
        print("pós leitura do codec html")
        soup = BeautifulSoup(html.read(), 'html.parser')
        # print(f'Soup:\n{soup}')

        print("gerou o content bs4 html")

        converted_text = soup.find('span', id='bkTimestamp0').text.replace(" US/Eastern", "")
        last_updated_datetime = datetime.now(tz).strftime('%Y-%m-%d') + " " + converted_text
        print(f'Last Updated Datetime: {last_updated_datetime}')

        current_datetime = datetime.strptime(last_updated_datetime, '%Y-%m-%d %H:%M:%S')

        print(f'Current Datetime: {current_datetime}')

        if (last_datetime is None) or (current_datetime > last_datetime):
            last_datetime = current_datetime

            stock = [papel for i in range(10)]

            ask_shares = []
            tds_ask_shares = soup.findAll('td', attrs={'class': 'book-viewer__ask book-viewer__ask-shares'})
            for i in tds_ask_shares:
                ask_shares.append(i.text.replace(u"\xa0", u" "))

            ask_prices = []
            tds_ask_prices = soup.findAll('td',
                                          attrs={'class': 'book-viewer__ask book-viewer__ask-price book-viewer-price'})
            for i in tds_ask_prices:
                ask_prices.append(i.text.replace(u"\xa0", u" "))

            bid_shares = []
            tds_bid_shares = soup.findAll('td', attrs={'class': 'book-viewer__bid book-viewer__bid-shares'})
            for i in tds_bid_shares:
                bid_shares.append(i.text.replace(u"\xa0", u" "))

            bid_prices = []
            tds_bid_prices = soup.findAll('td',
                                          attrs={'class': 'book-viewer__bid book-viewer__bid-price book-viewer-price'})
            for i in tds_bid_prices:
                bid_prices.append(i.text.replace(u"\xa0", u" "))

            last_10_times = []
            tds_last_10_times = soup.findAll('td', attrs={'class': 'book-viewer__trades-time'})
            for i in tds_last_10_times:
                last_10_times.append(i.text.replace(u"\xa0", u" "))

            last_10_prices = []
            tds_last_10_prices = soup.findAll('td', attrs={'class': 'book-viewer__trades-price'})
            for i in tds_last_10_prices:
                last_10_prices.append(i.text.replace(u"\xa0", u" "))

            last_10_shares = []

            tds_last_10_shares = soup.findAll('td', attrs={'class': 'book-viewer__trades-shares'})
            for i in tds_last_10_shares:
                last_10_shares.append(i.text.replace(u"\xa0", u" "))

            for i in range(len(last_10_times)):
                captured_datetime.append(current_datetime.strftime('%Y-%m-%d %H:%M:%S'))
                if i < 5:
                    top_shares_formatted.append(ask_shares[i])
                else:
                    top_shares_formatted.append(bid_shares[i - 5])

                if i < 5:
                    top_prices_formatted.append(ask_prices[i])
                else:
                    top_prices_formatted.append(bid_prices[i - 5])

                last_10_times_formatted.append(last_10_times[i])
                last_10_prices_formatted.append(last_10_prices[i])
                last_10_shares_formatted.append(last_10_shares[i])
                last_booktype.append(booktype[i])
                last_stock.append(stock[i])

            df = pd.DataFrame(
                {'Stock': last_stock, 'Book 5 Top Shares': top_shares_formatted,
                 'Book 5 Top Prices': top_prices_formatted,
                 'Last 10 Trades Time': last_10_times_formatted, 'Last 10 Trades Price': last_10_prices_formatted,
                 'Last 10 Trades Share': last_10_shares_formatted, 'Type': last_booktype,
                 'Captured Datetimes': captured_datetime})

            csvfilename = os.getcwd() + "/data/" + papel + "_trades_" + datetime.now().strftime(
                '%Y-%m-%d_%H-%M-%S') + ".csv"
            print(f'csvfilename: {csvfilename}')

            if os.path.exists(csvfilename):
                dfOld = pd.read_csv(csvfilename)
                dfNew = dfOld.append(df, ignore_index=True)
                dfNew = dfNew.drop_duplicates()
                dfNew.to_csv(csvfilename, index=False, encoding='utf-8')
            else:
                df.to_csv(csvfilename, index=False, encoding='utf-8')
            print("salvou o arquivo csv", papel)
        else:
            print("não salvou")