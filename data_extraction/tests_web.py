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
import time
from time import sleep
import codecs
import os
import glob
import gc
from pytz import timezone
from urllib import request


URL = ['https://www.cboe.com/us/equities/market_statistics/book/MSFT/',
       'https://markets.cboe.com/us/equities/market_statistics/book/MSFT',
       'https://markets.cboe.com/us/equities/market_statistics/book/AAPL',
       'https://markets.cboe.com/us/equities/market_statistics/book/TSLA',
       'https://markets.cboe.com/us/equities/market_statistics/book/CSCO',
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


options = FirefoxOptions()
options.add_argument("--headless")

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument('window-size=1920x1080')
# chrome_options.add_argument("--ignore-certificate-errors")

# path = os.getcwd() + "/chromedriver"

for url in URL:
    text_url = url
    print(url)
    stock = text_url.replace("https://markets.cboe.com/us/equities/market_statistics/book/", "")

    driver = webdriver.Firefox(options=options)
    # driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(30)
    print('Antes de pegar a página')
    driver.get(url)
    sleep(10)
    print(driver.page_source)
    driver.execute_script("return document.body.innerHTML")
    print(driver.page_source)

    # element = WebDriverWait(driver, 10).until_not(
    #     EC.text_to_be_present_in_element((By.ID, "bkTimestamp0"), '')
    # )

    # element = WebDriverWait(driver, 20).until_not(
    #     EC.text_to_be_present_in_element((By.CLASS_NAME, "book-viewer__trades-price"), '')
    # )

    # element = WebDriverWait(driver, 20).until(
    #     EC.presence_of_element_located((By.ID, "bkTimestamp0"))
    # )

    element = WebDriverWait(driver, 20).until_not(
        EC.text_to_be_present_in_element((By.ID, "bkTimestamp0"), '0xA0')
    )

    # element = WebDriverWait(driver, 20).until_not(
    #     EC.presence_of_element_located((By.XPATH, "//*[@id='mais-lidas']/ol/li[6]/a"))
    # )

    print(driver.page_source)

    # element = WebDriverWait(driver, 20).until_not(
    #     EC.text_to_be_present_in_element((By.ID, "bkTimestamp0"), ' ')
    # )

    print("OK!")

    teste = os.getcwd() + '/_testeApple' + '_resultado.html'
    print(teste)
    f = open(teste, 'w', encoding="utf8")
    f.write(driver.page_source)
    f.close()
    print("OK!")

    # text0 = driver.find_element_by_id("bkTimestamp0").text
    # print(text0)

    # text = driver.find_element_by_id("ext-gen1057").text
    # print(text)

    # element = WebDriverWait(driver, 20).until(
    #     EC.presence_of_all_elements_located((By.CLASS_NAME, "book-viewer__trades-time"))
    # )

    content = BeautifulSoup(driver.page_source, "html.parser")
    last_updated_time = content.find('span', id="bkTimestamp0")

    print(last_updated_time)

    # teste = os.getcwd() + f'/_{stock}' + '_resultado.html'
    print(teste)
    f = open(teste, 'w', encoding="utf8")
    f.write(driver.page_source)
    f.close()
