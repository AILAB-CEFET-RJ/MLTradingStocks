from data_treatment import treat_testing_data
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3 import PPO
import rl_boleta.rl_model as rl_model
from rl_model import ReinforcementLearningEnv
from plot import plot_lucro_bruto, plot_qtde_acumulada_cotas_compradas_vendidas, plot_qtde_acumulada_decisoes_agente, plot_reward, plot_lucro_liquido, plot_qtde_acoes_posse
import csv
import pdb
import os

def test_agent(filename, quantidade_dias_teste, repetitive_iteration_number):

    testing_df = treat_testing_data(filename, quantidade_dias_teste, repetitive_iteration_number)

    rl_testing_agent = ReinforcementLearningEnv('testing', testing_df, 0.0, 0.8, [], [], [], [], 0, 100000, [], [0], [0], [])

    env_teste = DummyVecEnv([lambda: rl_testing_agent])
    observation = env_teste.reset()


    # Load model
    model = PPO.load(f'rl_trading_stocks_iteracao{repetitive_iteration_number}')
    # model = PPO.load(f'rl_trading_stocks_iteracao{repetitive_iteration_number}')

    # pdb.set_trace()

    rewards = []
    episode_reward = 0

    # pdb.set_trace()
    for _ in range(int(len(testing_df)/10) - 6):
        action, _states = model.predict(observation, deterministic=True)
        # print(action)
        observation, reward, done, info = env_teste.step(action)

        episode_reward += reward[0]
        rewards.append(reward[0])
        
        if done or info[0].get('is_success', False):
            print("Reward:", episode_reward, "Success?", info[0].get('is_success', False))
            rewards.append(episode_reward)
            episode_reward = 0.0
            observation = env_teste.reset()

    env_teste.render()


    buy_action_array = []
    hold_action_array = []
    sell_action_array = []

    for action in rl_testing_agent.actions_array:
            buy_action_array.append(1 if 0 < action <= 1 else 0)
            hold_action_array.append(1 if action == 0 else 0)
            sell_action_array.append(1 if -1 <= action < 0 else 0)


    plot_reward(rl_testing_agent.recompensas_por_acao_episodio, 'testing', filename, repetitive_iteration_number)
    plot_lucro_liquido(rl_testing_agent.net_profit_array, 'testing', filename, repetitive_iteration_number)
    plot_lucro_bruto(rl_testing_agent.gross_profit_array, 'testing', filename, repetitive_iteration_number)
    plot_qtde_acoes_posse(rl_testing_agent.shares_held_array, 'testing', filename, repetitive_iteration_number)
    plot_qtde_acumulada_cotas_compradas_vendidas(rl_testing_agent.acoes_compradas, rl_testing_agent.acoes_vendidas, 
    'testing', filename, repetitive_iteration_number)
    plot_qtde_acumulada_decisoes_agente(buy_action_array, hold_action_array, sell_action_array, 'testing', filename, repetitive_iteration_number)

    testing_results = {
        'base de teste': filename,
        'quantidade de dias': quantidade_dias_teste,
        'numero da iteracao teste': repetitive_iteration_number + 1,
        'quantidade de episódios teste': len(rl_testing_agent.episodios),
        'recompensas teste': rl_testing_agent.recompensas_por_acao_episodio[-1],
        'valor inicial teste': rl_testing_agent.initial_amount,
        'valor final teste': rl_testing_agent.gross_profit_array[-1],
        'lucro/prejuízo teste': rl_testing_agent.net_profit_array[-1],
        'quantidade de passos teste': int(len(testing_df)/10) - 6
    }

    env_teste.reset()
    env_teste.close()
    del model

    os.remove(f'rl_trading_stocks_iteracao{repetitive_iteration_number}.zip')

    return testing_results
