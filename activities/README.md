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

## Extração de cotações de ativos (pasta get_quotations)
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
- Função Principal
- Modelo de Reinforcement Learning
- Treinamento de Dados
- Teste de Dados
- Tratamento de Dados (CSV)
- Plotagem de gráficos

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

## Como executar treinamento/teste do modelo
1. Acessar o servidor Aquarii ou Arietis
1.1 No Aquarii, acessar ~/data_extraction/data_extraction/activities/rl_boleta
2. Verificar os screens existentes ('screen -ls' - SEM AS ASPAS)
2.1 Caso exista um screen com o nome x, acessá-lo, por meio do comando 'screen -r x' (SEM AS ASPAS)
2.2 Caso não exista, criar um novo screen com o nome de x e acessá-lo, por meio do comando 'screen -r x' (SEM AS ASPAS)
3. Digitar o comando 'conda activate ai_env' (SEM AS ASPAS), para ativar o ambiente que contém as instalações feitas para rodar treinamentos/testes
4. Acessar a pasta rl_boleta
5. Rodar o comando 'python3 main.py' (SEM AS ASPAS), para realizar o treinamento/teste
5.1 Caso haja a necessidade de alterar os arquivos de treinamento e/ou teste, alterar o arquivo main.py