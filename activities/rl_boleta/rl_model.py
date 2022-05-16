import gym
from gym import spaces
import random
import numpy as np
from datetime import datetime
import pdb

# Global variables setup
INITIAL_ACCOUNT_BALANCE = 10000.00
MAX_ACCOUNT_BALANCE = 200000.00
MAX_NUM_SHARES = 100000
MAX_SHARE_PRICE = 1000.00
MAX_STEPS = 20000
MAX_TRADES_SHARE = 1000000
STOP_CONDITION = 0.95

max_net_worth = INITIAL_ACCOUNT_BALANCE


class ReinforcementLearningAgent(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, df, mode='training'):
        super(ReinforcementLearningAgent, self).__init__()
        self.df = df
        self.reward_range = (0, MAX_ACCOUNT_BALANCE)
        self.debug = True
        self.qtd_episodios = 0
        self.final_amount = 0
        self.current_observation_price = 0
        self.last_observation_price = 0
        self.counter = 0
        self.mode = mode
        self.deslocamento = 0
        self.episodios = []
        self.passos = []
        self.recompensas_por_acao_episodio = []
        self.recompensas_por_episodio = []
        self.lucro_bruto = []
        self.valor_total = 0.0
        self.qtdes_vendidas = []
        self.stop_condition = STOP_CONDITION
        self.max_net_worth = max_net_worth
        
        # Actions of the format Buy x%, Sell x%, Hold, etc. - [Buy, sell, hold; 0-100%] -> account balance/position size
        self.action_space = spaces.Box(
            low=np.array([0, 0]),
            high=np.array([3, 1]),
            dtype=np.float16)

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
        if self.mode == 'training':
          self.deslocamento = random.randint(50, len(self.df)-10)
        else:
          if self.deslocamento == 0:
            self.deslocamento = 50

        print(f'len(self.df) = {len(self.df)}')
        print(f'self.deslocamento = {self.deslocamento}\n\n\n')

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

        self.current_observation_price = self.df.loc[self.deslocamento]['Last_10_Prices']
        print(f'current_price: {self.current_observation_price}')

        self.last_observation_price = self.df.loc[self.deslocamento - 10]['Last_10_Prices']
        print(f'last_price: {self.last_observation_price}')

        # pdb.set_trace()
        appendix_array = np.array([
            self.balance / MAX_ACCOUNT_BALANCE,
            (self.net_worth - self.balance) / MAX_ACCOUNT_BALANCE,
            self.shares_held / MAX_NUM_SHARES, 0, 0, 0, 0,
        ]).reshape(7,1)
        
        obs = np.append(frame, appendix_array, axis = 1)
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
        if (action[0] < 1 and self.current_observation_price > self.last_observation_price) or (1 < action[0] < 2 and self.current_observation_price < self.last_observation_price) or (action[0] >= 2 and self.current_observation_price < self.last_observation_price):
          reward_step = 1
        elif (action[0] < 1 and self.current_observation_price < self.last_observation_price) or (1 < action[0] < 2 and self.current_observation_price > self.last_observation_price):
          reward_step = -1
        else:
          reward_step = 0

        self.counter += 1
        self.recompensas_por_acao_episodio.append(reward_step)
        self.passos.append(self.counter)
        
        # The episode reward is the rate of the net profit amount and amount invested multiplied by 1000. 
        self.recompensas_por_episodio.append(self.net_profit_amount)

        print(f'len(passos): {len(self.passos)}')
        done = (self.net_worth <= ((INITIAL_ACCOUNT_BALANCE * STOP_CONDITION) or (len(self.passos) == 10240)) and self.mode == 'training')
        
        print(f'Amount Invested: {self.money_invested}')

        if done:
          print('Done')
          self.qtd_episodios += 1
          self.episodios.append([self.deslocamento, self.qtd_episodios])


        next_stage = self._next_observation()
        

        # qtde_episodios = self.qtd_episodios
        return next_stage, reward, done, {}

    def _take_action(self, action):
        # Set the current price to a random price within the time step
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
            self.qtdes_vendidas.append(shares_sold)
            self.balance += shares_sold * current_price
            self.shares_held -= shares_sold
            self.total_shares_sold += shares_sold
            self.total_sales_value += shares_sold * current_price
            self.money_invested = - (shares_sold * current_price)

        self.net_worth = self.balance + self.shares_held * current_price
        self.valor_total = self.net_worth
        print(f'self.balance: {self.balance}')
        print(f'self.shares_held: {self.shares_held}')
        print(f'current_price: {current_price}')
        print(f'self.net_worth: {self.net_worth}')
        self.lucro_bruto.append(self.net_worth)

        self.net_profit_amount = self.net_worth - INITIAL_ACCOUNT_BALANCE
        global final_amount
        final_amount = self.net_worth
        print("-----------------------------------------------------------------------------------------")

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

