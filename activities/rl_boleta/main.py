from cgi import test
import rl_model
from training import train_agent
from testing import test_agent
import csv
from datetime import datetime

header = ['base de treinamento', 'treinamento - condição de parada', 'quantidade de episódios terminais treino', \
'recompensas treino', 'valor inicial treino', 'valor final treino', 'lucro/prejuízo treino', 'base de teste', \
'quantidade de episódios teste', 'recompensas teste', 'valor inicial teste', 'valor final teste', 'lucro/prejuízo teste', \
'quantidade de passos teste']

string_now = datetime.now().strftime('%d_%m_%Y_%H:%M:%S')


for i in range(1):
    results_training = train_agent('consolidado_treinamento (01.12 a 06.12).csv', i)

    results_testing = test_agent('consolidado_teste (10.01 a 14.01).csv', i)
#     test_agent('consolidado_teste (18.01 a 26.01).csv')
#     test_agent('consolidado_teste (21.02 a 11.03).csv')
#     test_agent('consolidado_teste (23.03 a 28.03).csv')
    
    results = {**results_training, **results_testing}
    if i == 0:
        mode = 'w'
    else:
        mode = 'a'

    with open(f'{string_now}.csv', mode, encoding='UTF8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        writer.writerow(results)
