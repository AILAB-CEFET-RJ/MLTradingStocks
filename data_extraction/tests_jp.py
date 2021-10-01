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
import random

MAX_THREADS = 10


def scrapper(a):
    threads = MAX_THREADS

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        print("entrou no executor")
        executor.map(processa, a)
    print("executou uma parte")


global total
total = 0
global item
item = 0


def processa(a):
    print(f'Process: {os.getpid()}')
    print(f'Iniciando o processo de: {a}')
    time.sleep(2)
    print(f'Terminou de processar: {a}')
    return a


lista = [10, 20, 340, 5056, 20, 2, 250, 7]
while (True):
    scrapper(lista)
