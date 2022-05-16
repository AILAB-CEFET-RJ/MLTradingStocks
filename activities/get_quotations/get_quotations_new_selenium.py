import urllib

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import concurrent.futures
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import date
import time
import calendar
from time import sleep
import codecs
import os
from os import path
import glob
import gc
from pytz import timezone


tz = timezone('US/Eastern')
pd.set_option('display.max_columns', 500)

last_datetime = None


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

URL_dictionary = {'https://markets.cboe.com/us/equities/market_statistics/book/AAPL': 'APPLE INC COM',
        'https://markets.cboe.com/us/equities/market_statistics/book/TSLA': 'TESLA INC COM',
        'https://markets.cboe.com/us/equities/market_statistics/book/CSCO': 'CISCO SYS INC COM',
        'https://markets.cboe.com/us/equities/market_statistics/book/MSFT': 'MICROSOFT CORP COM',
        'https://markets.cboe.com/us/equities/market_statistics/book/GE': 'GENERAL ELECTRIC CO COM NEW',
        'https://markets.cboe.com/us/equities/market_statistics/book/F': 'FORD MTR CO DEL COM',
        'https://markets.cboe.com/us/equities/market_statistics/book/TWTR': 'TWITTER INC COM',
        'https://markets.cboe.com/us/equities/market_statistics/book/C': 'CITIGROUP INC COM NEW',
        'https://markets.cboe.com/us/equities/market_statistics/book/FCX': 'FREEPORT-MCMORAN INC CL B',
        'https://markets.cboe.com/us/equities/market_statistics/book/BAC': 'BK OF AMERICA CORP COM',
        'https://markets.cboe.com/us/equities/market_statistics/book/KO': 'COCA COLA CO COM',
        'https://markets.cboe.com/us/equities/market_statistics/book/INTC': 'INTEL CORP COM',
        'https://markets.cboe.com/us/equities/market_statistics/book/GM': 'GENERAL MTRS CO COM',
        'https://markets.cboe.com/us/equities/market_statistics/book/AAL': 'AMERICAN AIRLS GROUP INC COM',
        'https://markets.cboe.com/us/equities/market_statistics/book/NCLH': 'NORWEGIAN CRUISE LINE HLDG LTD SHS',
        'https://markets.cboe.com/us/equities/market_statistics/book/JPM': 'JPMORGAN CHASE & CO COM',
        'https://markets.cboe.com/us/equities/market_statistics/book/PFE': 'PFIZER INC COM',
        'https://markets.cboe.com/us/equities/market_statistics/book/MS': 'MORGAN STANLEY COM NEW',
        'https://markets.cboe.com/us/equities/market_statistics/book/DAL': 'DELTA AIR LINES INC DEL COM NEW',
        'https://markets.cboe.com/us/equities/market_statistics/book/NEM': 'NEWMONT CORP COM'}

MAX_THREADS = 10


def Load():
    options = FirefoxOptions()
    options.headless = True
    
    driver = webdriver.Firefox(options=options)
    return driver

def Finish(driver):
    driver.close()

def scrapper(URLs):
    threads = MAX_THREADS

    with concurrent.futures.ThreadPoolExecutor(max_workers = threads) as executor:
        print("entrou no executor")
        executor.map(getHTML, URLs)
        time.sleep(2)

    print("executou uma parte")
    return


def getHTML(URL):
    try:
        driver = Load()
    except Exception as e:
        print(e)
    driver.implicitly_wait(30)
    driver.get(URL)
    
    WebDriverWait(driver, 100).until(
        EC.text_to_be_present_in_element((By.ID, "bkCompany0"), URL_dictionary[URL])
    )

    # elemento = driver.find_element_by_id("bkTimestamp0")
    # print(elemento)

    # text = driver.find_element_by_id("ext-gen1057").text
    # print(text)

    content = BeautifulSoup(driver.page_source, "html.parser")
    # print('Pegou a página')


    last_updated_time = content.find('span', id="bkTimestamp0")
    print(f'URL: {URL}\nLast Updated Time: {last_updated_time.contents}')
    content_date = datetime.now(tz).strftime('%Y-%m-%d_%H-%M-%S')

    # Check if last time is not null or empty
    if not last_updated_time.text.strip():
        print(f"Last updated time wasn't caught for {URL}")
        tries = 0
        while not last_updated_time.text.strip() and tries < 11:
            tries += 1
            driver.get(URL)
            content = BeautifulSoup(driver.page_source, "html.parser")
            last_updated_time = content.find('span', id="bkTimestamp0")
            content_date = datetime.now(tz).strftime('%Y-%m-%d_%H-%M-%S')

        if last_updated_time.text.strip():
            print('Last updated time was caught!')
        else:
            print(f'All tries for {URL} have failed.')
            return

    Finish(driver)
    papel = URL.split("/")[-1]

    today_date = date.today().strftime('%d-%m-%Y')

    # Salva HTML na pasta html
    print('Ponto de validação da pasta')
    print(path.exists(today_date + '_html'))
    if path.exists(today_date + '_html'):
        filename = os.getcwd() + f'/{today_date}_html/' + papel + "_" + content_date + ".html"
        f = open(filename, 'w', encoding="utf8")
        f.write(str(content))    
        f.close()
    else:
        os.mkdir(today_date + '_html')
    
    return



def main():
    print('Início da execução do programa')


    # Sempre executa
    while True:
        current_date = date.today()
        day_of_the_week = calendar.day_name[current_date.weekday()]
        # print(day_of_the_week.lower())
        done = (datetime.now(tz).strftime('%H:%M:%S') > upper_limit or datetime.now(tz).strftime('%H:%M:%S') < lower_limit or
                day_of_the_week.lower() == 'saturday' or day_of_the_week.lower() == 'sunday')

        


        while done:
            print('Done')
            current_date = date.today()
            day_of_the_week = calendar.day_name[current_date.weekday()]

            # Sleeps for 30 minutes
            sleep(60*30)

            done = (datetime.now(tz).strftime('%H:%M:%S') > upper_limit or datetime.now(tz).strftime(
                '%H:%M:%S') < lower_limit or day_of_the_week.lower() == 'saturday' or day_of_the_week.lower() == 'sunday')


        while not done:
            done = (datetime.now(tz).strftime('%H:%M:%S') > upper_limit or datetime.now(tz).strftime(
                '%H:%M:%S') < lower_limit)

            minute = datetime.now(tz).minute

            if done:
                pass
            else:
            
                # Realiza as coletas e salva os HTML, de 5 em 5 minutos
                if minute % 2 == 0:
                    print(f"loop de coleta iniciado, em {datetime.now(tz).strftime('%H:%M:%S')}, Eastern Time.")
                    scrapper(URLs)
                    print(datetime.now(tz).strftime('%H:%M:%S'), 'fim deste loop. gc:', gc.get_count())

                    # Garbage collector
                    gc.collect()
                    print(f"Coleta realizada em {datetime.now(tz).strftime('%H:%M:%S')}, Eastern Time.")
                    print(f"Garbage Collector (gc): {gc.get_count()}")
                    sleep(10)
                else:
                    sleep(10)




if (__name__ == '__main__'):
    lower_limit = datetime.strptime('09:00:00', '%H:%M:%S').strftime('%H:%M:%S')
    upper_limit = datetime.strptime('16:00:00', '%H:%M:%S').strftime('%H:%M:%S')
    print(datetime.now(tz).strftime('%H:%M:%S'))
    main()
