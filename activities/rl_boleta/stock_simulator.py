#%% import packages
import numpy as np

#%% Definicao da classe
class Stock:
    def __init__(self, S0, mu, sigma):
        self.S0 = S0         # Preco incial da acao que voce esta simulando NO INICIO DO DIA (abertura do pregao)
        self.mu = mu         # Retorno esperado da acao ao longo de um dia (CUIDADO! Nao inserir um valor muito alto)
        self.sigma = sigma   # Volatilidade intradia da acao
        
    def sim_path(self, T, N):
        t = np.linspace(0, T, N + 1)
        dt = T / N
        power = (self.mu - 0.5 * self.sigma**2) * dt + self.sigma * np.sqrt(dt) * np.random.randn(N)
        sim_path = np.append([1], np.exp(power)).cumprod() * self.S0
        self.t = t
        self.price = sim_path
        
# Volatilidade intradiária para a Apple
# https://www.alphaquery.com/stock/AAPL/volatility-option-statistics/30-day/historical-volatility
#%% Example
aapl = Stock(177.83, .005, .10)       # Cria uma instancia da classe Stock, com um preco inicial S0, um retorno esperado no dia e a volatilidade intradia
aapl.sim_path(5, 6 * 60 * 60)     # Simula um caminho possivel de precos para o tempo T = 1 dia, com N intervalos de 6 horas * 60 minutos * 60 segundos
aapl.price                        # Retorna o caminho simulado 
print(aapl.price)
