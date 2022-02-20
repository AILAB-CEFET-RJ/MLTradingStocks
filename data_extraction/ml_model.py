# %tensorflow_version 2.x
# ! pip install tensorflow
# !pip install stable-baselines3 gym
# !pip install torch==1.4.0


import gym
from gym import spaces
import random
import numpy as np
import pandas as pd
#import logging
from datetime import datetime
import pickle
import matplotlib.pyplot as plt



#logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

from stable_baselines3.sac.policies import MlpPolicy
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3 import PPO

qtde_episodios=0
episodios = []
passos = []

recompensas_por_acao_episodio = []
rewards_per_episode = []
lucro_bruto = []


INITIAL_ACCOUNT_BALANCE = 10000.00
MAX_ACCOUNT_BALANCE = 200000.00
MAX_NUM_SHARES = 100000
MAX_SHARE_PRICE = 1000.00
MAX_STEPS = 20000
MAX_TRADES_SHARE = 1000000

max_net_worth = INITIAL_ACCOUNT_BALANCE


class StockTradingEnvironment(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, df):
        super(StockTradingEnvironment, self).__init__()
        self.df = df
        self.reward_range = (0, MAX_ACCOUNT_BALANCE)
        self.debug = True
        self.ligado = False
        self.qtd_episodios = 0
        self.final_amount = 0
        self.current_observation_price = 0
        self.last_observation_price = 0
        self.counter = 0
        

        # Actions of the format Buy x%, Sell x%, Hold, etc. - [Buy, sell, hold; 0-100%] -> account balance/position size
        self.action_space = spaces.Box(
            low=np.array([0, 0]),
            high=np.array([3, 1]),
            dtype=np.float16)

        # Prices contain the OHCL values for the last five prices
        self.observation_space = spaces.Box(
            low=0,
            high=1,
            shape=(7, 61),
            dtype=np.float16)

    def reset(self):
        # Reset the state of the environment to an initial state
        self.balance = INITIAL_ACCOUNT_BALANCE
        self.net_worth = INITIAL_ACCOUNT_BALANCE
        self.max_net_worth = INITIAL_ACCOUNT_BALANCE
        self.shares_held = 0
        self.cost_basis = 0
        self.total_shares_sold = 0
        self.total_sales_value = 0
        self.share_price = 0
        self.previous_price = 0
        self.money_invested = 0
        self.net_profit_amount = 0
        
        
        # Set the current step to a random point within the dataframe
        # self.deslocamento = random.randint(0, len(self.df.loc[:, 'Open'].values) - 6)
        self.deslocamento = random.randint(50, len(self.df)-10)

        return self._next_observation()


    def _next_observation(self):
        # Get the data points for the last 5 observations and scale to between 0-1
        
        
        frame = np.array([
            self.df.loc[self.deslocamento - 50: self.deslocamento + 9, 'Shares'] / MAX_TRADES_SHARE,
            self.df.loc[self.deslocamento - 50: self.deslocamento + 9, 'Prices'] / MAX_SHARE_PRICE,
            self.df.loc[self.deslocamento - 50: self.deslocamento + 9, 'Time_Hour'],
            self.df.loc[self.deslocamento - 50: self.deslocamento + 9, 'Time_Minute'],
            self.df.loc[self.deslocamento - 50: self.deslocamento + 9, 'Time_Second'],
            self.df.loc[self.deslocamento - 50: self.deslocamento + 9, 'Last_10_Prices'] / MAX_SHARE_PRICE,
            self.df.loc[self.deslocamento - 50: self.deslocamento + 9, 'Last_10_Shares'].astype(int) / MAX_TRADES_SHARE
        ])

        
        # current_prices_frame = np.array([self.df.loc[self.deslocamento: self.deslocamento + 9, 'Prices']])
        # mean_current_observation = current_prices_frame.mean()

        self.current_observation_price = np.array([self.df.loc[self.deslocamento: self.deslocamento, 'Prices']])[0][0]
        print(f'current_price: {self.current_observation_price}')

        self.last_observation_price = np.array([self.df.loc[self.deslocamento - 10: self.deslocamento - 10, 'Prices']])[0][0]
        print(f'last_price: {self.last_observation_price}')

        # last_prices_frame = np.array([self.df.loc[self.deslocamento - 10: self.deslocamento -1, 'Prices']])
        # mean_last_observation = last_prices_frame.mean()

        # print(f'Mean - Current Observation:\n{mean_current_observation}')
        # print(f'Mean - Last Observation: {mean_last_observation}')


        


        

        # Append additional data and scale each value to between 0-1
        new_array_7x1 = np.array([
            self.balance / MAX_ACCOUNT_BALANCE,
            (self.net_worth - self.balance) / MAX_ACCOUNT_BALANCE,
            self.shares_held / MAX_NUM_SHARES,
            0,
            0,
            0,
            0,
        ]).reshape(7,1)
        
        obs = np.append(frame, new_array_7x1, axis=1)



        return obs

    def step(self, action):
        
        # Execute one time step within the environment
        self._take_action(action)

        
        # Increase step number
        self.deslocamento += 10

        if self.deslocamento > len(self.df) - 10:
            self.deslocamento = 50

        delay_modifier = (self.deslocamento / MAX_STEPS)

        # REWARD ZONE:
        # reward = self.net_worth * delay_modifier
        reward = self.net_profit_amount * delay_modifier
        
        
        # Testing rewards:
        # print(f"Previous price: {self.last_observation_price} - Previous Action: {action[0]}\n Current Price: {self.current_observation_price}")

        if (action[0] < 1 and self.current_observation_price > self.last_observation_price) or (1 < action[0] < 2 and self.current_observation_price < self.last_observation_price) or (action[0] >= 2 and self.current_observation_price < self.last_observation_price):
          reward_step = 1
        elif (action[0] < 1 and self.current_observation_price < self.last_observation_price) or (1 < action[0] < 2 and self.current_observation_price > self.last_observation_price):
          reward_step = -1
        else:
          reward_step = 0

        self.counter += 1
        recompensas_por_acao_episodio.append(reward_step)
        passos.append(self.counter)
        

        # The episode reward is the rate of the net profit amount and amount invested multiplied by 1000. 
        rewards_per_episode.append(self.net_profit_amount)

        # print(f'Action: {action[0]}')
        
        print(f'len(passos): {len(passos)}')
        done = (self.net_worth <= INITIAL_ACCOUNT_BALANCE * 0.95) or (len(passos) == 10240)
        print(f'Done: {done}')
        
        print(f'self.net_worth: {self.net_worth}')
        print(f'Amount Invested: {self.money_invested}')
        
        lucro_bruto.append(self.net_worth)
        print(f'Valor Total do passo {len(lucro_bruto)}: {lucro_bruto[len(lucro_bruto) - 1]}')


        if done:
          print('Done')
          self.qtd_episodios += 1
          episodios.append([self.deslocamento, self.qtd_episodios])


        next_stage = self._next_observation()
        

        # qtde_episodios = self.qtd_episodios
        return next_stage, reward, done, {}

    def _take_action(self, action):
        # Set the current price to a random price within the time step
        # current_price = random.uniform(
        #     self.df.loc[self.deslocamento, 'Open'],
        #     self.df.loc[self.deslocamento, 'Close'])
        current_price = self.df.loc[self.deslocamento, 'Last_10_Prices']
        

        action_type = action[0]
        amount = action[1]

        print(f'Action Type: {action_type}\nAmount: {amount}')
        
        
        if action_type < 1:
            # Buy amount % of balance in shares
            total_possible = int(self.balance / current_price)
            shares_bought = int(total_possible * amount)
            prev_cost = self.cost_basis * self.shares_held
            additional_cost = shares_bought * current_price
            self.money_invested = additional_cost
            self.balance -= additional_cost
            self.cost_basis = (prev_cost + additional_cost) / (self.shares_held + shares_bought)
            self.shares_held += shares_bought

        elif action_type < 2:
            # Sell amount % of shares held
            shares_sold = int(self.shares_held * amount)
            self.balance += shares_sold * current_price
            self.shares_held -= shares_sold
            self.total_shares_sold += shares_sold
            self.total_sales_value += shares_sold * current_price
            self.money_invested = - (shares_sold * current_price)

        self.net_worth = self.balance + self.shares_held * current_price
        self.net_profit_amount = self.net_worth - INITIAL_ACCOUNT_BALANCE
        global final_amount
        final_amount = self.net_worth
        print("-----------------------------------------------------------------------------------------")
        print(self.final_amount)

        if self.net_worth > self.max_net_worth:
            self.max_net_worth = self.net_worth

        if self.shares_held == 0:
            self.cost_basis = 0
        

    def render(self, mode='human', close=False):
        # Render the environment to the screen
        profit = self.net_worth - INITIAL_ACCOUNT_BALANCE

        print(f'Step: {self.deslocamento}')
        print(f'Balance: {self.balance}')
        print(f'Shares held: {self.shares_held}\nTotal Sold: {self.total_shares_sold}')
        print(f'Share price: {self.share_price}')
        print(f'Average cost for held shares: {self.cost_basis}\nTotal sales value: {self.total_sales_value}')
        print(f'Net worth: {self.net_worth}\nMax net worth: {self.max_net_worth}')
        print(f'Profit: {profit}')






outer_df = pd.read_csv('consolidado_treinamento.csv', thousands=',', error_bad_lines=False)

outer_df = outer_df.sort_values('File Date')
outer_df = outer_df[outer_df['Ticker'] == 'AAPL']

outer_df.drop_duplicates()
outer_df.drop('File Date', axis='columns', inplace=True)
outer_df.drop('Ticker', axis='columns', inplace=True)
outer_df.drop('Day', axis='columns', inplace=True)
outer_df.reset_index(drop=True, inplace=True)

print(outer_df.head())
# print(outer_df.shape)



# The algorithm require a vectorized environment to run
env_teste = DummyVecEnv([lambda: StockTradingEnvironment(outer_df)])



# Criar env de teste
model = PPO("MlpPolicy", env_teste, verbose=1)
model.learn(total_timesteps=10000)
model.save('teste')

del model

print(episodios)
print(f"A quantidade de terminal conditions (episódios terminais) é {len(episodios)}.")

print(f"Self Net Worth: {final_amount}")

# https://stable-baselines3.readthedocs.io/en/master/guide/examples.html



cumulative = np.cumsum(recompensas_por_acao_episodio)
print(cumulative)
# plot the cumulative function
plt.plot(cumulative, c='blue')


recompensas_por_acao_episodio
sum(recompensas_por_acao_episodio)


plt.plot(rewards_per_episode)
plt.title('Lucro Total da Estratégia')


from scipy.signal import savgol_filter
import numpy as np
import matplotlib.pyplot as plt

# plt.plot(lucro_bruto)
plt.plot(savgol_filter(lucro_bruto, 101, 2))

plt.title('Valor Total')


outer_df_after = pd.read_csv('consolidado_real.csv', thousands=',', error_bad_lines=False)

outer_df_after = outer_df_after.sort_values('File Date')
outer_df_after = outer_df_after[outer_df_after['Ticker'] == 'AAPL']

outer_df_after.drop_duplicates()
outer_df_after.drop('File Date', axis='columns', inplace=True)
outer_df_after.drop('Ticker', axis='columns', inplace=True)
outer_df_after.drop('Day', axis='columns', inplace=True)
outer_df_after.reset_index(drop=True, inplace=True)


env_real = DummyVecEnv([lambda: StockTradingEnvironment(outer_df_after)])

obs = env_real.reset()

# Load model
model = PPO.load("teste", env=env_teste)

# Evaluate the agent
rewards = []
episode_reward = 0


for _ in range(700):
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, done, info = env_real.step(action)
    # print(f'Reward: {reward[0]}')
    episode_reward += reward[0]
    rewards.append(reward[0])

    if done or info[0].get('is_success', False):
        print("Reward:", episode_reward, "Success?", info[0].get('is_success', False))
        rewards.append(episode_reward)
        episode_reward = 0.0
        obs = env_real.reset()
        # Incrementar episódio
    env_real.render()

print(f'Rewards: {rewards}')
print(f'Episode Reward: {episode_reward}')