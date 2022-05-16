from datetime import datetime
import os
import glob
from bs4 import BeautifulSoup
import codecs
import json


def check_all_folders():

    tickers = ['AAPL','TSLA','CSCO','MSFT','GE','F','TWTR','C','FCX','BAC','KO','INTC','GM','AAL','NCLH','JPM','PFE','MS','DAL','NEM']

    save_file_2 = open('resultado_analise_2.txt', 'w')
    save_error_log = open('log_de_erros.txt', 'w')


    folders = glob.glob(os.getcwd() + '/html_data/*')
    non_conforming_itens = []

    for folder in folders:
        # print(folder)
        for ticker in tickers:
            files = glob.glob(folder + f'/{ticker}_*.html')
            # print(files)

            count = 0
            for file in files:
                print(file)
                count += 1
                html = codecs.open(file, "r", encoding="utf8")
                soup = BeautifulSoup(html.read(), 'html.parser')
                
                try:
                    html_ticker = soup.find(id="symbol0")['value']
                except Exception as e:
                    os.remove(file)
                    save_error_log.write(f'Erro: {e}\nFile: {file}\n\n')
                print(count)
                if html_ticker != ticker:
                    # print(html_ticker)
                    # print(ticker)
                    os.remove(file)
                    non_conforming_itens.append({html_ticker: file})

    save_file_2.write(json.dumps(non_conforming_itens))

    save_error_log.close()
    save_file_2.close()
