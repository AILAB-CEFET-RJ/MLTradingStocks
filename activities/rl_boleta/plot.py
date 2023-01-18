import rl_model as rl_model
import numpy as np
import matplotlib as mp
import matplotlib.pyplot as plt

def plot_reward(rewards_per_action_episode, mode, filename, repetitive_iteration_number):
    cumulative = np.cumsum(rewards_per_action_episode)
    plt.clf()
    plt.plot(cumulative, c='green')
    plt.xlabel('Transições')
    plt.ylabel('Recompensas Acumuladas')
    plt.title(f'Recompensas por Transição (Acumulado)')
    plt.savefig(f'plots/{mode}/recompensas/recom_cum_{filename}_rep{repetitive_iteration_number}.png')

def plot_lucro_liquido(rewards_per_episode, mode, filename, repetitive_iteration_number):
    plt.clf()
    plt.plot(rewards_per_episode)
    plt.xlabel('Transições')
    plt.ylabel('Lucro Líquido da Estratégia')
    plt.title(f'Lucro Líquido por Transição')
    plt.savefig(f'plots/{mode}/lucro_liquido/ll_{filename}_rep{repetitive_iteration_number}.png')

def plot_lucro_bruto(gross_profit, mode, filename, repetitive_iteration_number):
    plt.clf()
    plt.plot(gross_profit)
    plt.xlabel('Transições')
    plt.ylabel('Saldo Total')
    plt.title('Saldo Total da Conta por Transição')
    plt.savefig(f'plots/{mode}/lucro_bruto/luc_brut_{filename}_rep{repetitive_iteration_number}.png')

def plot_qtde_acoes_posse(shares_held, mode, filename, repetitive_iteration_number):
    plt.clf()
    plt.plot(shares_held)
    plt.xlabel('Transições')
    plt.ylabel('Qtde. Ações em Posse')
    plt.title('Qtde. Ações em Posse por Transição')
    plt.savefig(f'plots/{mode}/acoes_em_posse/qtde_acoes_{filename}_rep{repetitive_iteration_number}.png')

def plot_qtde_acumulada_cotas_compradas_vendidas(array_acoes_compradas, array_acoes_vendidas, mode, filename, repetitive_iteration_number):
    cumulative_compradas = np.cumsum(array_acoes_compradas)
    cumulative_vendidas = np.cumsum(array_acoes_vendidas)
    plt.clf()
    plt.plot(cumulative_compradas, c='green', label="compradas")
    plt.plot(cumulative_vendidas, c='red', label="vendidas")
    plt.legend(loc="upper left")
    plt.xlabel('Transições')
    plt.ylabel('Qtde. Ações Negociadas')
    plt.title('Qtde. Ações Negociadas por Transição')
    plt.savefig(f'plots/{mode}/cotas_compradas_vendidas/qtde_acoes_comp_vend_{filename}_{mode}_rep{repetitive_iteration_number}.png')

def plot_qtde_acumulada_decisoes_agente(buy_action_array, hold_action_array, sell_action_array, mode, filename, repetitive_iteration_number):
    cumulative_compras = np.cumsum(buy_action_array)
    cumulative_holds = np.cumsum(hold_action_array)
    cumulative_vendas = np.cumsum(sell_action_array)

    plt.clf()
    plt.plot(cumulative_compras, c='green', label="compra")
    plt.plot(cumulative_vendas, c='red', label="venda")
    plt.plot(cumulative_holds, c='blue', label="hold")
    # plt.plot(cumulative_compras, c='green', label="compra", marker="o")
    # plt.plot(cumulative_vendas, c='red', label="venda", marker="v")
    # plt.plot(cumulative_holds, c='blue', label="hold", marker="s")
    plt.legend(loc="upper left")
    plt.xlabel('Transições')
    plt.ylabel('Valores de Decisões Acumuladas')
    plt.title('Decisões do Agente por Transição')
    plt.savefig(f'plots/{mode}/decisoes_agente/decisoes_agente_{filename}_{mode}_rep{repetitive_iteration_number}.png')
