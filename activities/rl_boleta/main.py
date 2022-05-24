from training import train_agent
from testing import test_agent
import csv
from datetime import datetime

header = ['run', 'base de treinamento', 'treinamento - condição de parada', 'quantidade de episódios terminais treino', \
'recompensas treino', 'valor inicial treino', 'valor final treino', 'lucro/prejuízo treino', 'base de teste', \
'quantidade de episódios teste', 'recompensas teste', 'valor inicial teste', 'valor final teste', 'lucro/prejuízo teste', \
'quantidade de passos teste']
files_training = ['consolidado_treinamento (01.12 a 06.12).csv', 'consolidado_teste (10.01 a 14.01).csv', 'consolidado_teste (18.01 a 26.01).csv', 'consolidado_teste (21.02 a 11.03).csv']
files_testing = ['consolidado_teste (23.03 a 28.03).csv']

string_now = datetime.now().strftime('%d_%m_%Y_%H:%M:%S')


# for i in range(2):
#     for file_training in files_training:
#         results_training = train_agent(file_training, i)

#         for file_testing in files_testing:
#             results_testing = test_agent(file_testing, i)
            
#             run = {'run': i + 1}
#             results = {**run, **results_training, **results_testing}
#             if i == 0 and file_testing == files_testing[0]:
#                 mode = 'w'
#             else:
#                 mode = 'a'

#             with open(f'./results/{string_now}.csv', mode, encoding='UTF8', newline='') as file:
#                 writer = csv.DictWriter(file, fieldnames=header)
#                 if i == 0 and file_testing == files_testing[0]:
#                     writer.writeheader()
#                 writer.writerow(results)

training_result = train_agent(files_training, 1)
print(training_result)

testing_result = test_agent(files_testing[0], 1)
print(testing_result)
