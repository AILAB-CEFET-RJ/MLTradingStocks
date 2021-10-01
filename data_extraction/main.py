import urllib

from selenium import webdriver
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
from urllib import request

tz = timezone('US/Eastern')
pd.set_option('display.max_columns', 500)

last_datetime = None

top_shares_formatted = []
top_prices_formatted = []
last_10_times_formatted = []
last_10_prices_formatted = []
last_10_shares_formatted = []
last_booktype = []
last_stock = []
captured_datetime = []

booktype = ['ask', 'ask', 'ask', 'ask', 'ask', 'bid', 'bid', 'bid', 'bid', 'bid']

symbols = ['TSLA', 'CSCO', 'AAPL', 'MSFT', 'GE', 'F', 'TWTR', 'C', 'FCX', 'BAC', 'KO', 'INTC', 'GM', 'AAL', 'NCLH',
           'JPM', 'PFE', 'MS', 'DAL', 'NEM']
# ,	'PYPL',	'CCL',	'WFC',	'HAL',	'AMD',	'VZ',	'CMCSA',	'XOM',	'SLB',	'UBER',	'MU',	'EBAY',	'T',	'MRO',	'MOS']

URLs = ['https://markets.cboe.com/us/equities/market_statistics/book/AAPL',
        'https://markets.cboe.com/us/equities/market_statistics/book/TSLA',
        'https://markets.cboe.com/us/equities/market_statistics/book/CSCO',
        'https://markets.cboe.com/us/equities/market_statistics/book/MSFT',
        'https://markets.cboe.com/us/equities/market_statistics/book/GE',
        'https://markets.cboe.com/us/equities/market_statistics/book/F',
        'https://markets.cboe.com/us/equities/market_statistics/book/TWTR',
        'https://markets.cboe.com/us/equities/market_statistics/book/C',
        'https://markets.cboe.com/us/equities/market_statistics/book/FCX',
        'https://markets.cboe.com/us/equities/market_statistics/book/BAC',
        'https://markets.cboe.com/us/equities/market_statistics/book/KO',
        'https://markets.cboe.com/us/equities/market_statistics/book/INTC',
        'https://markets.cboe.com/us/equities/market_statistics/book/GM',
        'https://markets.cboe.com/us/equities/market_statistics/book/AAL',
        'https://markets.cboe.com/us/equities/market_statistics/book/NCLH',
        'https://markets.cboe.com/us/equities/market_statistics/book/JPM',
        'https://markets.cboe.com/us/equities/market_statistics/book/PFE',
        'https://markets.cboe.com/us/equities/market_statistics/book/MS',
        'https://markets.cboe.com/us/equities/market_statistics/book/DAL',
        'https://markets.cboe.com/us/equities/market_statistics/book/NEM']
MAX_THREADS = 10

done = False


def Load():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('window-size=1920x1080')
    path = os.getcwd() + "\chromedriver"
    # print(f'path: {path}')

    driver = webdriver.Chrome(options=chrome_options)
    # print('OK!')

    return driver


def Finish(driver):
    driver.close()
    driver.quit()


def scrapper(URLs):
    threads = MAX_THREADS

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        print("entrou no executor")
        executor.map(getHTML, URLs)
        time.sleep(3)
        print()
    print("executou uma parte")


def getHTML(URL):
    driver = Load()
    driver.implicitly_wait(5)
    print('Antes de pegar a página')
    driver.get(URL)
    elemento = driver.find_element_by_id("bkTimestamp0")
    print(elemento)

    page = driver.execute_script('return document.body.innerHTML')
    time.sleep(2)
    print('Pegou a página')

    # content = BeautifulSoup(driver.page_source, "lxml")
    content = BeautifulSoup(''.join(page), 'html.parser')
    # page = request.urlopen(URL)
    # content = BeautifulSoup(page)
    # print(f'content: {content}')
    time.sleep(1)
    # print('teste')

    last_updated_time = content.find('span', id="bkTimestamp0")
    # last_updated_time = soup.find(id="bkTimestamp0")
    print(f'URL: {URL}\nLast Updated Time: {last_updated_time.contents}')

    if not last_updated_time.text.strip():  # Check if last time is not null or empty
        print(f"Last updated time wasn't caught for {URL}")
        tries = 0
        while not last_updated_time.text.strip() and tries < 11:
            tries += 1

            papel = URL.split("/")[-1]
            filename_error = os.getcwd() + '/erros_html/' + papel + "_" + datetime.now().strftime(
                '%Y-%m-%d_%H-%M-%S') + ".txt"
            f = open(filename_error, 'w', encoding="utf8")
            f.write(content.text)
            f.close()

            driver.get(URL)
            time.sleep(2)
            content = BeautifulSoup(driver.page_source, "lxml")
            last_updated_time = content.find('span', id="bkTimestamp0")
            time.sleep(2)

        if last_updated_time.text.strip():
            print('Last updated time was caught!')
        else:
            print(f'All tries for {URL} have failed.')

    driver.quit()
    papel = URL.split("/")[-1]

    # salvar HTML
    filename = os.getcwd() + '/html/' + papel + "_" + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + ".html"
    print(f'Filename: {filename}')

    # print("antes de salvar html", papel)
    f = open(filename, 'w', encoding="utf8")
    print("Gerou arquivo html", papel)
    f.write(str(content))
    print("escreveu arquivo html com sucesso", papel)
    f.close()
    pass


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


lower_limit = datetime.strptime('09:30:00', '%H:%M:%S').strftime('%H:%M:%S')
upper_limit = datetime.strptime('22:20:20', '%H:%M:%S').strftime('%H:%M:%S')


def main():
    print('comecou a execucao')
    done = (datetime.now(tz).strftime('%H:%M:%S') > upper_limit or datetime.now(tz).strftime('%H:%M:%S') < lower_limit)

    while not done:
        minute = datetime.now(tz).minute
        second = datetime.now(tz).second

        # print('loop start ', datetime.now(tz).strftime('%H:%M:%S'))
        scrapper(URLs)
        print(datetime.now(tz).strftime('%H:%M:%S'), 'fim deste loop. gc:', gc.get_count())

        # Garbage collector
        gc.collect()
        print(datetime.now(tz).strftime('%H:%M:%S'), 'COLETADO. gc:', gc.get_count())

        if (datetime.now(tz).strftime('%H:%M:%S') > upper_limit):
            done = True
            print('hora fim da coleta')
        else:
            print(f'Não atingiu o horário limite...')

        print(f'minute: {minute}')
        if minute % 2 == 0:
            for ticker in symbols:
                html2csv(ticker)
            print('Arquivos CSV gerados')

    if done:
        if datetime.now(tz).strftime('%H:%M:%S') > upper_limit:
            for ticker in symbols:
                print(ticker, "loading")
                html2csv(ticker)
                print(ticker, "finished")
            print('Arquivos CSV gerados')


if (__name__ == '__main__'):
    main()
