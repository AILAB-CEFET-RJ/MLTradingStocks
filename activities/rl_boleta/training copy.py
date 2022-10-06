from data_treatment import treat_data
from stable_baselines3.sac.policies import MlpPolicy
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3 import PPO
import rl_model_menor
from rl_model_menor import ReinforcementLearningAgent
from plot import gross_profit_plot, plot_reward, reward_plot
import csv
import pdb
import numpy as np


def train_agent(training_files, repetitive_iteration_number):

    agg_timesteps = 0
    absolute_initial_balance = 10000.00
    initial_balance = 10000.00
    stp_condition = 0.8
    base_treinamento = []
    episodios_terminais_treino = 0
    recompensas_totais_treino = 0
    valores_iniciais = []

    for file in training_files:
        base_treinamento.append(file)
        training_df = treat_data(file)

        rl_training_agent = ReinforcementLearningAgent(training_df)
        env_training = DummyVecEnv([lambda: rl_training_agent])

        timesteps = int(len(training_df)/10) - 5
        agg_timesteps += timesteps

        env_training.reset()
        
        if file == training_files[0]:
            model = PPO("MlpPolicy", env_training, verbose=1)

        else:
            model.set_env(env_training)

        model.learn(total_timesteps = timesteps)

        initial_balance = rl_training_agent.net_worth
        episodios_terminais_treino += len(rl_training_agent.episodios)
        recompensas_totais_treino += np.sum(rl_training_agent.recompensas_por_acao_episodio)
        valores_iniciais.append(rl_training_agent.initial_amount)

        plot_reward(rl_training_agent.recompensas_por_acao_episodio, 'training', file, repetitive_iteration_number)
        reward_plot(rl_training_agent.recompensas_por_episodio, 'training', file, repetitive_iteration_number)
        gross_profit_plot(rl_training_agent.lucro_bruto, 'training', file, repetitive_iteration_number)


    training_result = {
        'base de treinamento': base_treinamento,
        'passos de treinamento': agg_timesteps,
        'numero da iteracao': repetitive_iteration_number + 1,
        'treinamento - condição de parada': stp_condition,
        'quantidade de episódios terminais treino': episodios_terminais_treino,
        'recompensas treino': recompensas_totais_treino,
        'valor inicial treino': absolute_initial_balance,
        'valor final treino': rl_training_agent.net_worth,
        'lucro/prejuízo treino': (rl_training_agent.lucro_bruto[-1] - initial_balance)
    }

    # pdb.set_trace()

    model.save('rl_trading_stocks')

    del model
    
    return training_result


    # pdb.set_trace()