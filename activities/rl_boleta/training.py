from data_treatment import treat_data
from stable_baselines3.sac.policies import MlpPolicy
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3 import PPO
import rl_model
from rl_model import ReinforcementLearningAgent
from plot import gross_profit_plot, plot_reward, reward_plot
import csv
import pdb

def train_agent(training_files, iteration_number):

    results = []

    for file in training_files:
        training_df = treat_data(file)

        rl_training_agent = ReinforcementLearningAgent(training_df)
        env_training = DummyVecEnv([lambda: rl_training_agent])

        timesteps = int(len(training_df)/10 * 2)

        if file == training_files[0]:
            model = PPO("MlpPolicy", env_training, verbose=1)

        else:
            env_training.reset()
            model.set_env(env_training)

        model.learn(total_timesteps = timesteps)

        plot_reward(rl_training_agent.recompensas_por_acao_episodio, 'training', file, iteration_number)

        reward_plot(rl_training_agent.recompensas_por_episodio, 'training', file, iteration_number)

        gross_profit_plot(rl_training_agent.lucro_bruto, 'training', file, iteration_number)

        result = {
            'base de treinamento': file,
            'treinamento - condição de parada': rl_training_agent.stop_condition,
            'quantidade de episódios terminais treino': len(rl_training_agent.episodios),
            'recompensas treino': sum(rl_training_agent.recompensas_por_acao_episodio),
            'valor inicial treino': rl_training_agent.initial_amount,
            'valor final treino': rl_training_agent.net_worth,
            'lucro/prejuízo treino': (rl_training_agent.lucro_bruto[-1] - rl_training_agent.initial_amount)
        }

        results.append(result)

    model.save('rl_trading_stocks')

    del model
    
    return results

    # print(rl_training_agent.episodios)

    # print(f"A quantidade de terminal conditions (episódios terminais) no treinamento é de {len(rl_training_agent.episodios)}.")

    # plot_reward(rl_training_agent.recompensas_por_acao_episodio, 'training', training_file, iteration_number)

    # reward_plot(rl_training_agent.recompensas_por_episodio, 'training', training_file, iteration_number)

    # gross_profit_plot(rl_training_agent.lucro_bruto, 'training', training_file, iteration_number)


    # pdb.set_trace()