# MLTradingStocks

O algoritmo de Reinforcement Learning aplicado a trading utiliza como base as ações da Apple. De forma que o algoritmo de Machine Learning funcione, a biblioteca stable-baselines3 precisa ser instalada e, para que esta funcione, a biblioteca torch também teve que ser isntalada (versão 1.4.0). Além disso, as bibliotecas gym (para criação de ambiente customizado para o algoritmo de RL), pandas, numpy e random (para análises e tratamentos de dados) também foram utilizadas.

A classe StockTradingEnvironment tem por objetivo criar o ambiente sobre o qual o modelo será treinado para, a partir do treino, adotar as melhores estratégias de ivnestimento para o ativo analisado.

