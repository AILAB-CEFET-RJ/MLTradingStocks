# Aprendizado de Máquina
## Agente de aprendizado por reforço para transações financeiras

> O objetivo principal deste trabalho é o de desenvolver um modelo (agente)
> de Aprendizagem por Reforço que negocie ações de empresas listadas
> nas bolsas estadunidenses, baseando-se em um site aberto (CBOE) para
> acompanhar as cotações de 20 empresas selecionadas, com o objetivo de
> treinar o modelo e posteriormente testá-lo, quanto a seu processo decisório
> de negociações desses ativos.

Este projeto está dividido nas seguintes seções:
- [Extração de cotações de ativos (arquivos salvos em formato html)](https://github.com/MLRG-CEFET-RJ/MLTradingStocks/tree/main/activities/get_quotations)

- [Tratamento dos arquivos HTML salvos e posterior conversão dos dados em arquivo único (extensão csv)](https://github.com/MLRG-CEFET-RJ/MLTradingStocks/tree/main/activities/treatment_extraction)

- [Treinamento e teste dos dados extraídos, para balanceamento e aperfeiçoamento do modelo de Aprendizagem por Reforço](https://github.com/MLRG-CEFET-RJ/MLTradingStocks/tree/main/activities/rl_boleta)

Este trabalho leva em consideração as ações das seguintes empresas negociadas nas bolsas dos Estados Unidos:
- Apple
- Tesla
- Cisco
- Microsoft
- GE
- Ford
- Twitter
- Citigroup
- Freeport-McMoran
- Bank of America
- Coca-Cola
- Intel
- General Motors
- American Airlines
- Norwegian Cruise Line
- JP Morgan
- Pfizer
- Morgan Stanley
- Delta Airlines
- Newmont

## Extração de cotações de ativos (pasta get_quotations, arquivo get_quotations_new_selenium.py)
O arquivo get_quotations_new_selenium.py salva páginas HTML dos ativos listados anteriormente, por meio do acesso ao site CBOE.

O programa começa checando o horário e a data de execução. Caso esteja sendo executado no sábado ou no domingo, o mesmo entra em modo de latência. O mesmo ocorre de segunda a sexta-feira, caso o código seja executado em um horário fora do de operação (ajustado para operar das 09h às 16h, em dias úteis - quando a bolsa norte-americana costuma estar em operação). Quando em modo de latência, o programa realiza checagens de 30 em 30 minutos, com o objetivo de checar se deverá sair ou continuar em modo de latência.

Por outro lado, caso o código não esteja em latência, o trecho principal (referente à coleta dos dados) será executado a cada 2 minutos, por meio da chamada ao método *scrapper*, passando como parâmetros as URL's referentes a cada uma das ações.

O programa utiliza um total de 10 threads, de modo a executar o processamento das páginas de forma paralela. Para cada thread, o programa usa o webdriver do Firefox com a opção *headless*, que impede o navegador de ficar visível (e que foi crucial para este trabalho, visto que o programa roda em um servidor remoto Linux, sem interface gráfica). Após carregar o driver, o programa aguarda 30 segundos (de forma que não haja coleta de página para uma mesma ação mais do que uma vez, dentro de um determinado minuto) e espera os elementos da página serem renderizados, para que páginas vazias não sejam salvas. Caso não haja carregamento de elementos, o programa ainda tenta carregar a página outras 10 vezes.

Por fim, o driver é encerrado e o html (caso tenha sido coletado) é salvo na pasta html.


## Tratamento e conversão dos dados coletados (pasta treatment_extraction)
Para realizar o tratamento e a conversão dos dados nos arquivos .html, há 2 etapas principais:
1. Checagem de consistência e limpeza dos arquivos .html
2. Extração das tags dos arquivos .html

Com relação à checagem de consistência e limpeza dos arquivos HTML, o arquivo *html_files_check.py* é utilizado. O arquivo em questão considera a existência da pasta ***html_files*** (que foi criada no servidor), que contém pastas que representam os dias de coleta de dados. Para cada uma dessas pastas, há os arquivos HTML salvos para cada uma das 20 empresas, para os horários de coleta descritos anteriormente e os intervalos de 2 minutos considerados.

Para cada um dos ativos considerados, o arquivo percorre cada uma das pastas dentro da pasta *html_files* e, dentro de cada uma dessas pastas, verifica se cada um dos arquivos HTML correspondentes ao ativo em questão foram salvos corretamente (considerando arquivos não vazios e com o ativo correspondendo ao ativo salvo no HTML). Os arquivos salvos incorretamente (arquivos vazios ou com dados incorretos) são eliminados.

O arquivo de extração das tags é o *tags_extraction.py*, sendo inicializado chamando a função de checagem dos arquivos HTML, contida no arquivo *html_files_check.py*. Após checagem e sanitização dos arquivos, há novamente o percorrimento da pasta ***html_files***, suas pastas sucessoras e seus arquivos correspondentes. Então, os dados alimentadores do modelo de Reinforcement Learning (Aprendizagem por Reforço) serão moldados, considerando-se a seguinte estrutura:
- Data do Arquivo
- Ticker
- Dia
- Quantidade de Ações (cotas)
- Preços
- Hora
- Minuto
- Segundo
- Últimos 10 preços
- Últimas 10 cotas de ações

Cada uma das colunas é previamente tratada, com remoção de vírgulas de valores, caracteres de espaços de no-break, transposição do vetor de dados e salvamento dos dados ajustados e tratados em arquivos com extensão .csv (*comma separated values*).


## Aplicação de agente de Apredizado por Reforço (pasta rl_boleta)
A seção de Aprendizado por Reforço foi segmentada de acordo com as seguintes funcionalidades:
- Função Principal (arquivo main.py)
- Modelo de Reinforcement Learning (arquivo rl_model.py)
- Treinamento de Dados (arquivo training.py)
- Teste de Dados (arquivo testing.py)
- Tratamento de Dados (CSV) (arquivo data_treatment.py)
- Plotagem de gráficos (arquivo plot.py)
- Análises de ACF (autocorrelação) e PACF (autocorrelação parcial) para os conjuntos de dados (arquivo acf_pacf.py)
- Teste de dados sem treinamento prévio (arquivo brute_testing.py)
- Implementação do teste de Mann-Kendall sobre os conjuntos de dados (arquivo kendall.py)
- Geração de tabelas em Latex com resumos estatísticos (arquivo results_statistics.py)
- Geração de tabelas com resumos estatísticos para os resultados - conjuntos com 50 treinamentos e 50 testes (arquivo results_statistics.py)
- (INACABADO) Simulador de cotações, para facilitar o treinamento do modelo de Aprendizado por Reforço (arquivo stock_simulator.py)

A função principal (*main.py*) é o ponto centralizador, em que são definidos os arquivos csv utilizados para treinamento e teste dos dados salvos nos arquivos CSV. Além disso, neste arquivo são definidas a quantidade de vezes em que treinamentos e testes serão executados, com o objetivo de avaliar a eficácia média e outras observações estatísticas para o modelo utilizado.

O treinamento do modelo, antes de ser inicializado, realiza a leitura dos CSVs e cria um dataframe correspondente, como forma de garantir a consistência e a transmissão de dados. Na sequência, o modelo de Aprendizagem por Reforço é inicializado, passando-se o dataframe obtido do CSV como parâmetro. O modelo então é treinado, por uma quantidade de passos que pode ser variável, e por fim, salvo. Posteriormente, há a realização e o salvamento das plotagens e o retorno da função de treinamento, por meio de um JSON.

A realização de testes do modelo é feita de forma similar, com leitura dos CSVs e criação de dataframes correspondentes, inicialização do agente de testes, carregamento do modelo salvo na parte de treinamento e execução dos testes. Na execução dos testes (assim como no treinamento), os dataframes são segmentados de 10 em 10 colunas, uma vez que cada linha representa:
- Data do Arquivo
- Ticker
- Dia
- Quantidade de Ações (cotas)
- Preços
- Hora
- Minuto
- Segundo
- Últimos 10 preços
- Últimas 10 cotas de ações

E cada coluna representa cada um dos valores das linhas (que chega a 10).
Nos testes, a extensão dos data frames deve ser subtraída de 6, uma vez que os testes começam a partir da sexto observação (pois o programa considera 5 observações anteriores mais a observação atual). Assim, caso a extensão dos dataframes seja total, o programa acabará considerando também as observações iniciais, ou seja, irá das últimas observações para as cinco primeiras, o que estaria fundamentalmente errado.

Após a execução dos testes, há a plotagem dos gráficos e o posterior retorno dos dados, em formato JSON.

Os retornos, tanto do treinamento quanto dos testes, são aglutinados e salvos em um csv consolidado de resultados.

Por fim, o modelo de Aprendizagem por Reforço considera, além da inicialização da classe, as funções de reset, próxima observação, passo, tomada de ação e renderização.


## Como executar treinamento/teste do modelo em um servidor do CEFET
1. Acessar o servidor Aquarii ou Arietis

1.1 No Aquarii, acessar ~/data_extraction/data_extraction/activities/rl_boleta

2. Verificar os screens existentes ('screen -ls' - SEM AS ASPAS)

2.1 Caso exista um screen com o nome x, acessá-lo, por meio do comando 'screen -r x' (SEM AS ASPAS)

2.2 Caso não exista, criar um novo screen com o nome de x e acessá-lo, por meio do comando 'screen -r x' (SEM AS ASPAS)

3. Digitar o comando 'conda activate ai_env' (SEM AS ASPAS), para ativar o ambiente que contém as instalações feitas para rodar treinamentos/testes

4. Acessar a pasta rl_boleta

5. Rodar o comando 'python3 main.py' (SEM AS ASPAS), para realizar o treinamento/teste
5.1 Caso haja a necessidade de alterar os arquivos de treinamento e/ou teste, alterar o arquivo main.py


## Como instalar o projeto em máquinas com Sistema Operacional Linux (distro Ubuntu)
1. Na pasta que o usuário desejar, clonar o projeto, a partir do seguinte comando:

1.1 Via SSH:
> git init
> git clone git@github.com:MLRG-CEFET-RJ/MLTradingStocks.git

1.2 Via HTTPS:
> git init
> git clone https://github.com/MLRG-CEFET-RJ/MLTradingStocks.git

2. Instalar conjunto de pacotes, incluindo o gerenciador de pacotes Conda:
2.1 Instalar o Anaconda ou o Miniconda (versão mais leve) no Linux (seguir os passos no link a seguir):
> https://docs.anaconda.com/anaconda/install/

2.2 Diferença entre Anaconda, Miniconda e Conda:
> https://stackoverflow.com/questions/30034840/what-are-the-differences-between-conda-and-anaconda

3. Instalar os pacotes necessários para rodar o algoritmo de Aprendizagem por Reforço:
3.1 conda install -c conda-forge/label/cf202003 tensorflow
3.2 conda install -c conda-forge stable-baselines3
3.3 conda install -c conda-forge gym
3.4 conda install -c pytorch pytorch

4. Utilizar um ambiente virtual conda, para rodar os algoritmos:
4.1 Criar o ambiente virtual
> https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands

4.2 Ativar o ambiente criado
> https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#activating-an-environment

4.3 Após utilização do ambiente (seja para instalação de dependências, seja para execução de rotinas), desativar o ambiente criado (a desativação não exclui o ambiente, apenas sai dele):
> https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#deactivating-an-environment

Quando o usuário desejar, poderá novamente acessar o ambiente criado, com o comando 'conda activate myenv' (checar a seção 4.2).


5. Com o ambiente Conda criado e ativado, instalar os pacotes necessários para rodar o algoritmo de extração de dados (este passo só é necessário 1 vez, quando o ambiente for acessado pela primeira vez):
5.1 conda install -c conda-forge/label/cf202003 geckodriver
5.2 conda install -c anaconda beautifulsoup4
5.3 conda install -c conda-forge/label/cf202003 firefox
5.4 conda install -c anaconda pandas
5.5 conda install -c anaconda numpy
5.6 conda install -c conda-forge/label/cf202003 selenium


## Como instalar o projeto em máquinas com Sistema Operacional Windows
1. Instalar o ambiente terminal Ubuntu no Windows, seguindo as intruções do link a seguir:
> https://ubuntu.com/tutorials/install-ubuntu-on-wsl2-on-windows-10#1-overview

2. A partir do terminal Ubuntu, escolher/criar a pasta desejada e clonar o repositório:
2.1 Via HTTPS: 
> git init
> git clone https://github.com/MLRG-CEFET-RJ/MLTradingStocks.git

2.2 Via SSH:
> git init
> git clone git@github.com:MLRG-CEFET-RJ/MLTradingStocks.git

3. Seguir os passos 2 a 4, para instalar pacotes e gerenciador de pacotes, além de instalar as dependências para o projeto.


## Como rodar o algoritmo de coleta de dados?
1. Ativar o ambiente Conda criado, caso não esteja ativado

2. Acessar a pasta *get_quotations*, arquivo *get_quotations_new_selenium.py*

3. Executar a rotina em Python, com o comando:
3.1 Comando padrão
> python3 get_quotations_new_selenium.py

3.2 Comando, caso o usuário deseje que a rotina seja executada em modo silencioso e com o log em arquivo .txt:
> nohup python3 get_quotations_new_selenium.py > *nome*.txt


## Como rodar o algoritmo de treinamento e teste dos dados?
1. Ativar o ambiente Conda criado, caso não esteja ativado

2. Acessar a pasta *rl_boleta*, arquivo *main.py*

3. Executar a rotina em Python, com o comando:
3.1 Comando padrão
> python3 main.py

3.2 Comando, caso o usuário deseje que a rotina seja executada em modo silencioso e com o log em arquivo .txt:
> nohup python3 main.py > *nome*.txt


## Como rodar o algoritmo de obtenção de dados estatísticos?
1. Ativar o ambiente Conda criado, caso não esteja ativado

2. Acessar a pasta *rl_boleta*
2.1 Para executar a rotina em Python do arquivo de autocorrelação e autocorrelação parcial, digitar o comando:

2.1.1 Comando padrão
> python3 acf_pacf.py

2.1.2 Comando, caso o usuário deseje que a rotina seja executada em modo silencioso e com o log em arquivo .txt:
> nohup python3 acf_pacf.py > *nome*.txt

2.2 Para executar a rotina em Python do arquivo de aplicação do teste de Mann-Kendall, digitar o comando:

2.2.1 Comando padrão
> python3 kendall.py

2.2.2 Comando, caso o usuário deseje que a rotina seja executada em modo silencioso e com o log em arquivo .txt:
> nohup python3 kendall.py > *nome*.txt

2.3 Para executar a rotina em Python do arquivo de estatísticas dos conjuntos de dados, digitar o comando:

2.3.1 Comando padrão
> python3 get_df_statistics.py

2.3.2 Comando, caso o usuário deseje que a rotina seja executada em modo silencioso e com o log em arquivo .txt:
> nohup python3 get_df_statistics.py > *nome*.txt

2.4 Para executar a rotina em Python do arquivo de estatísticas sobre os resultados obtidos (para o conjunto de treinamentos e testes), digitar o comando:

2.4.1 Comando padrão
> python3 results_statistics.py

2.4.2 Comando, caso o usuário deseje que a rotina seja executada em modo silencioso e com o log em arquivo .txt:
> nohup python3 results_statistics.py > *nome*.txt

2.5 Para executar a rotina em Python do arquivo de simulação de preço de ações, digitar o comando:

2.5.1 Comando padrão
> python3 stock_simulator.py

2.5.2 Comando, caso o usuário deseje que a rotina seja executada em modo silencioso e com o log em arquivo .txt:
> nohup python3 stock_simulator.py > *nome*.txt



## Observação
O projeto completo NÃO foi desenvolvido em nenhum Notebook Jupyter.
