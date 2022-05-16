from cgi import test
import rl_model
from training import train_agent
from testing import test_agent
import csv

header = ['base de treinamento', 'treinamento - condição de parada', 'quantidade de episódios terminais treino', \
'recompensas treino', 'valor inicial treino', 'valor final treino', 'lucro/prejuízo treino', 'base de teste', \
'quantidade de episódios teste', 'recompensas teste', 'valor inicial teste', 'valor final teste', 'lucro/prejuízo teste', \
'quantidade de passos teste']

for i in range(1):
    train_agent('consolidado_treinamento (01.12 a 06.12).csv', i)

    test_agent('consolidado_teste (10.01 a 14.01).csv', i)
#     test_agent('consolidado_teste (18.01 a 26.01).csv')
#     test_agent('consolidado_teste (21.02 a 11.03).csv')
#     test_agent('consolidado_teste (23.03 a 28.03).csv')


# train_agent('consolidado_treinamento (01.12 a 06.12).csv')

# test_agent('consolidado_teste (10.01 a 14.01).csv')
