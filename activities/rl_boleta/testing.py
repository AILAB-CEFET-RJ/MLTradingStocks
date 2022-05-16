from data_treatment import treat_data
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3 import PPO
import rl_model
from rl_model import ReinforcementLearningAgent
from plot import gross_profit_plot, plot_reward, reward_plot
import csv
import pdb

def test_agent(filename, iteration_number):
    testing_df = treat_data(filename)

    rl_testing_agent = ReinforcementLearningAgent(testing_df, 'test')

    env_teste = DummyVecEnv([lambda: rl_testing_agent])
    obs = env_teste.reset()

    # pdb.set_trace()

    # Load model
    model = PPO.load('rl_trading_stocks', env=env_teste)

    rewards = []
    episode_reward = 0

    for _ in range(int(len(testing_df)/10) - 6):
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, done, info = env_teste.step(action)
        episode_reward += reward[0]
        rewards.append(reward[0])
        

        if done or info[0].get('is_success', False):
            print("Reward:", episode_reward, "Success?", info[0].get('is_success', False))
            rewards.append(episode_reward)
            episode_reward = 0.0
            obs = env_teste.reset()
            # Incrementar episódio
        env_teste.render()


    plot_reward(rl_testing_agent.recompensas_por_acao_episodio, 'testing', filename, iteration_number)
    reward_plot(rl_testing_agent.recompensas_por_episodio, 'testing', filename, iteration_number)
    gross_profit_plot(rl_testing_agent.lucro_bruto, 'testing', filename, iteration_number)

    with open('resultados.csv', 'w') as file:
        file.write(f'base de teste: {filename}\n')
        file.write(f'quantidade de episódios de teste: {len(rl_testing_agent.episodios)}\n')
        file.write(f'recompensas teste: {sum(rl_testing_agent.recompensas_por_acao_episodio)}\n')
        file.write(f'valor inicial teste: {rl_testing_agent.max_net_worth}\n')
        file.write(f'valor final teste: {rl_testing_agent.net_worth}\n')
        file.write(f'lucro/prejuízo teste: {rl_testing_agent.lucro_bruto}\n')
        file.write(f'quantidade de passos teste: {int(len(testing_df)/10) - 6}\n')
