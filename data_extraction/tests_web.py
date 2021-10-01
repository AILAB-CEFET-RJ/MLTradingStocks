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
from urllib import request


URL = "https://markets.cboe.com/us/equities/market_statistics/book/TSLA"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('window-size=1920x1080')
path = os.getcwd() + "\chromedriver"


driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(30)
print('Antes de pegar a página')
driver.get(URL)
driver.execute_script("return document.body.innerHTML")

# element = WebDriverWait(driver, 10).until_not(
#     EC.text_to_be_present_in_element((By.ID, "bkTimestamp0"), '')
# )

# element = WebDriverWait(driver, 20).until_not(
#     EC.text_to_be_present_in_element((By.CLASS_NAME, "book-viewer__trades-price"), '')
# )

element = WebDriverWait(driver, 20).until_not(
    EC.text_to_be_present_in_element((By.ID, "bkTimestamp0"), '0xA0')
)

# text = driver.find_element_by_id("ext-gen1057")
# print(text)

# element = WebDriverWait(driver, 20).until(
#     EC.presence_of_all_elements_located((By.CLASS_NAME, "book-viewer__trades-time"))
# )


content = BeautifulSoup(driver.page_source, "lxml")
last_updated_time = content.find('span', id="bkTimestamp0")

print(last_updated_time)

teste = os.getcwd() + "/resultado.html"
f = open(teste, 'w', encoding="utf8")
f.write(driver.page_source)
f.close()
