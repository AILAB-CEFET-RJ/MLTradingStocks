from data_treatment import treat_data
from stable_baselines3.sac.policies import MlpPolicy
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3 import PPO
import rl_model
from rl_model import ReinforcementLearningAgent
from plot import gross_profit_plot, plot_reward, reward_plot
import csv
import pdb

def train_agent(training_file, iteration_number):
    training_df = treat_data(training_file)

    rl_training_agent = ReinforcementLearningAgent(training_df)

    env_training = DummyVecEnv([lambda: rl_training_agent])

    model = PPO("MlpPolicy", env_training, verbose=1)
    model.learn(total_timesteps=2000)
    model.save('rl_trading_stocks')

    del model

    # pdb.set_trace()
    print(rl_training_agent.episodios)

    print(f"A quantidade de terminal conditions (episódios terminais) no treinamento é de {len(rl_training_agent.episodios)}.")

    plot_reward(rl_training_agent.recompensas_por_acao_episodio, 'training', training_file, iteration_number)

    reward_plot(rl_training_agent.recompensas_por_episodio, 'training', training_file, iteration_number)

    gross_profit_plot(rl_training_agent.lucro_bruto, 'training', training_file, iteration_number)

    with open('resultados.csv', 'w') as file:
        file.write(f'base de treinamento: {training_file}\n')
        file.write(f'treinamento - condição de parada: {rl_training_agent.stop_condition}\n')
        file.write(f'quantidade de episódios terminais treino: {len(rl_training_agent.episodios)}\n')
        file.write(f'recompensas treino: {sum(rl_training_agent.recompensas_por_acao_episodio)}\n')
        file.write(f'valor inicial treino: {rl_training_agent.max_net_worth}\n')
        file.write(f'valor final treino: {rl_training_agent.net_worth}\n')
        file.write(f'lucro/prejuízo treino: {rl_training_agent.lucro_bruto}\n')
