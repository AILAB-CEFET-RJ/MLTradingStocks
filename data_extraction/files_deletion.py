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


filenames = glob.glob(os.getcwd() + '/data/' + '*.csv')


for file in filenames:
    os.remove(file)


print('Good Job!')
