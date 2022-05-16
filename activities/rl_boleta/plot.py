import rl_model
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

def plot_reward(rewards_per_action_episode, mode, filename, iteration_number):
    cumulative = np.cumsum(rewards_per_action_episode)
    plt.clf()
    plt.plot(cumulative, c='green')
    plt.xlabel('Passos')
    plt.ylabel('Recompensas Acumuladas')
    plt.title(f'Função de Recompensa por Episódio (Acumulado)')
    plt.savefig(f'plots/{mode}/cumulative_rewards_plot_{filename}_i{iteration_number}.png')

def reward_plot(rewards_per_episode, mode, filename, iteration_number):
    plt.clf()
    plt.plot(rewards_per_episode)
    plt.xlabel('Passos')
    plt.ylabel('Lucro Líquido da Estratégia')
    plt.title(f'Lucro Líquido por Passo')
    plt.savefig(f'plots/{mode}/rewperepi_{filename}_i{iteration_number}.png')

def gross_profit_plot(gross_profit, mode, filename, iteration_number):
    plt.clf()
    plt.plot(savgol_filter(gross_profit, 101, 2))
    plt.xlabel('Passos')
    plt.ylabel('Saldo Total')
    plt.title('Saldo Total da Conta por Passo')
    plt.savefig(f'plots/{mode}/gross_profit_plot_{filename}_i{iteration_number}.png')
