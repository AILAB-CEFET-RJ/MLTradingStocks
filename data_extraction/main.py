import urllib

# import chromedriver_binary

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import concurrent.futures
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import time
from time import sleep
import codecs
import os
import glob
import gc
from pytz import timezone

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


symbols = ['AAPL', 'TSLA', 'CSCO', 'MSFT', 'GE', 'F', 'TWTR', 'C', 'FCX', 'BAC', 'KO', 'INTC', 'GM', 'AAL', 'NCLH', 'JPM',
           'PFE', 'MS', 'DAL', 'NEM']


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


def Load():
    options = FirefoxOptions()
    options.add_argument("--headless")

    driver = webdriver.Firefox(options=options)
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
    return


def getHTML(URL):
    driver = Load()
    driver.implicitly_wait(30)
    print('Antes de pegar a página')
    driver.get(URL)
    driver.execute_script("return document.body.innerHTML")

    element = WebDriverWait(driver, 20).until_not(
        EC.text_to_be_present_in_element((By.ID, "bkTimestamp0"), '0xA0')
    )

    elemento = driver.find_element_by_id("bkTimestamp0")
    print(elemento)

    text = driver.find_element_by_id("ext-gen1057").text
    print(text)

    content = BeautifulSoup(driver.page_source, "html.parser")

    print('Pegou a página')

    # content = BeautifulSoup(driver.page_source, "lxml")
    # content = BeautifulSoup(''.join(page), 'html.parser')
    # page = request.urlopen(URL)
    # content = BeautifulSoup(page)
    # print(f'content: {content}')
    # time.sleep(1)
    # print('teste')

    last_updated_time = content.find('span', id="bkTimestamp0")
    print(f'URL: {URL}\nLast Updated Time: {last_updated_time.contents}')

    # Check if last time is not null or empty
    if not last_updated_time.text.strip():
        print(f"Last updated time wasn't caught for {URL}")
        tries = 0
        while not last_updated_time.text.strip() and tries < 11:
            tries += 1
            driver.get(URL)
            content = BeautifulSoup(driver.page_source, "html.parser")
            last_updated_time = content.find('span', id="bkTimestamp0")

        if last_updated_time.text.strip():
            print('Last updated time was caught!')
        else:
            print(f'All tries for {URL} have failed.')

    Finish(driver)
    papel = URL.split("/")[-1]

    # Salva HTML
    filename = os.getcwd() + '/html/' + papel + "_" + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + ".html"
    print(f'Filename: {filename}')

    f = open(filename, 'w', encoding="utf8")
    print("Gerou arquivo html", papel)
    f.write(str(content))
    print("escreveu arquivo html com sucesso -", papel)
    f.close()
    # pass
    return


def html2csv(papel):
    # Read html files
    filenames = glob.glob(os.getcwd() + '/html/' + '*.html')

    booktype = ['ask', 'ask', 'ask', 'ask', 'ask', 'bid', 'bid', 'bid', 'bid', 'bid']

    for file in filenames:
        papel = str(os.path.basename(file)).split('_')[0]

        print(f'File:{file}')
        print(f'Papel: {papel}')

        html = codecs.open(file, "r", encoding="utf8")
        soup = BeautifulSoup(html.read(), 'html.parser')

        converted_time_text = soup.find('span', id='bkTimestamp0').text.replace(" US/Eastern", "")

        last_updated_datetime = datetime.today().strftime('%Y-%m-%d') + " " + converted_time_text
        print(f'Last Updated Datetime: {last_updated_datetime}')

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

        captured_datetime = []
        top_shares_formatted = []
        top_prices_formatted = []
        last_10_times_formatted = []
        last_10_prices_formatted = []
        last_10_shares_formatted = []
        last_booktype = []
        last_stock = []
        current_datetime = datetime.strptime(last_updated_datetime, '%Y-%m-%d %H:%M:%S')

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

        # csvfilename = os.getcwd() + "/data/" + papel + "_trades_" + current_datetime.strftime(
        #     '%Y-%m-%d_%H-%M-%S') + ".csv"
        csvfilename = os.getcwd() + "/data/" + papel + "_trades_" + current_datetime.strftime(
            '%Y-%m-%d') + ".csv"
        print(f'csvfilename: {csvfilename}')

        if os.path.exists(csvfilename):
            print('EXISTS ALREADY!!!')
            dfOld = pd.read_csv(csvfilename)
            dfNew = dfOld.append(df, ignore_index=True)
            dfNew = dfNew.drop_duplicates()
            dfNew.to_csv(csvfilename, index=False, encoding='utf-8')
        else:
            df.to_csv(csvfilename, index=False, encoding='utf-8')
        print("salvou o arquivo csv", papel)



def erase_htmls():
    filenames = glob.glob(os.getcwd() + '/data/' + '*.csv')

    for file in filenames:
        os.remove(file)

    print('HTML files deleted')





def main():
    print('Início da execução do programa')


    # Sempre executa
    while True:
        done = (datetime.now(tz).strftime('%H:%M:%S') > upper_limit or datetime.now(tz).strftime('%H:%M:%S') < lower_limit or
                datetime.today().weekday() == 5 or datetime.today().weekday() == 6)

        while done:
            print('Done')

            # Sleeps for 30 minutes
            sleep(60*30)

            done = (datetime.now(tz).strftime('%H:%M:%S') > upper_limit or datetime.now(tz).strftime(
                '%H:%M:%S') < lower_limit or datetime.today().weekday() == 5 or datetime.today().weekday() == 6)


        while not done:
            done = (datetime.now(tz).strftime('%H:%M:%S') > upper_limit or datetime.now(tz).strftime(
                '%H:%M:%S') < lower_limit)

            minute = datetime.now(tz).minute

            # De 2 em 2 minutos (para minutos pares) realiza as coletas e salva os HTML:
            if minute % 2 == 0:
                print(f"loop de coleta iniciado, em {datetime.now(tz).strftime('%H:%M:%S')}, Eastern Time.")
                scrapper(URLs)
                print(datetime.now(tz).strftime('%H:%M:%S'), 'fim deste loop. gc:', gc.get_count())

                # Garbage collector
                gc.collect()
                print(f"Coleta realizada em {datetime.now(tz).strftime('%H:%M:%S')}, Eastern Time.")
                print(f"Garbage Collector (gc): {gc.get_count()}")

            if done:
                for ticker in symbols:
                    html2csv(ticker)
                print(f'Arquivos CSV gerados para {ticker}')




if (__name__ == '__main__'):
    lower_limit = datetime.strptime('08:00:00', '%H:%M:%S').strftime('%H:%M:%S')
    upper_limit = datetime.strptime('20:00:00', '%H:%M:%S').strftime('%H:%M:%S')
    main()
