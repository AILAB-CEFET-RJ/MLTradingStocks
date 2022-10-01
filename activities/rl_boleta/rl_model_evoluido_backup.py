from multiprocessing import shared_memory
from turtle import delay
import gym
from gym import spaces
import random
import numpy as np
from datetime import datetime
import pdb
import math

# Initial variables setup
MAX_ACCOUNT_BALANCE = 200000.00
MAX_NUM_SHARES = 100000
MAX_SHARE_PRICE = 1000
MAX_STEPS = 20000
MAX_TRADES_SHARE = 10000


class ReinforcementLearningEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    # TESTAR ADICIONAR O ENV NOS PARÂMETROS E RESETAR, NA PARTE DE TESTES
    def __init__(self, mode, df, initial_account_balance=10000.00, stop_condition=0.8, episodios=[], recompensas_por_acao_episodio=[], lucro_bruto=[], lucro_liquido=[], current_step=0):
        super(ReinforcementLearningEnv, self).__init__()
        self.mode = mode
        self.df = df
        self.initial_amount = initial_account_balance
        self.stop_condition = stop_condition
        self.balance = initial_account_balance
        self.net_worth = initial_account_balance
        self.reward_range = (0, MAX_ACCOUNT_BALANCE)
        self.current_observation_price = 0
        self.last_observation_price = 0
        self.deslocamento = 50
        self.passo_atual_total = current_step
        self.passos = []
        self.net_profit_amount = 0
        self.lucro_bruto = lucro_bruto
        self.net_profit_array = lucro_liquido
        self.episodios = episodios
        self.qtd_episodios = len(episodios)
        self.recompensas_por_acao_episodio = recompensas_por_acao_episodio
        self.shares_held = 0
        self.action_type = 0
        self.quantidade_executada = 0
        self.shares_held_array = []
        
        
        # Actions of the format Buy x%, Sell x%, Hold, etc. - [Buy, sell, hold; 0-100%] -> account balance/position size
        # self.action_space = spaces.Box(
        #     low=np.array([-1, 0]),
        #     high=np.array([1, 1]),
        #     dtype=np.float32)
        
        # ['compra/venda', 'porcentagem de compra/venda']
        self.action_space = spaces.Box(
            np.array([-1, 0]),
            np.array([1, 1]))

        self.observation_space = spaces.Box(
            low=0,
            high=1,
            shape=(7, 61),
            dtype=np.float16)


    def reset(self):
        # Reset the state of the environment to an initial state
        if self.mode == 'testing':
            self.deslocamento = 50
            self.initial_amount = 10000.00
            self.balance = 10000.00
            self.net_worth = 10000.00
            self.shares_held = 0
            self.total_shares_sold = 0
            self.total_sales_value = 0
            self.share_price = 0
            self.previous_price = 0
            self.net_profit_amount = 0
            self.stop_condition = 0.8
            self.recompensas_por_acao_episodio = []
            self.lucro_bruto = []
            self.net_profit_array = []
            # pdb.set_trace()
        else:
            self.deslocamento = 50
        
        return self._next_observation()


    def _next_observation(self):
        # Get the data points for the last 5 observations and scale to between 0-1
    
        frame = np.array([
            self.df.loc[self.deslocamento - 50: self.deslocamento + 9, 'Shares'] / MAX_TRADES_SHARE,
            self.df.loc[self.deslocamento - 50: self.deslocamento + 9, 'Prices'] / MAX_SHARE_PRICE,
            self.df.loc[self.deslocamento - 50: self.deslocamento + 9, 'Time_Hour'] / 24,
            self.df.loc[self.deslocamento - 50: self.deslocamento + 9, 'Time_Minute'] / 60,
            self.df.loc[self.deslocamento - 50: self.deslocamento + 9, 'Time_Second'] / 60,
            self.df.loc[self.deslocamento - 50: self.deslocamento + 9, 'Last_10_Prices'] / MAX_SHARE_PRICE,
            self.df.loc[self.deslocamento - 50: self.deslocamento + 9, 'Last_10_Shares'] / MAX_TRADES_SHARE
        ])

        self.current_observation_price = self.df.loc[self.deslocamento]['Last_10_Prices']
        # print(f'current_price: {self.current_observation_price}')

        self.last_observation_price = self.df.loc[self.deslocamento - 10]['Last_10_Prices']
        # print(f'last_price: {self.last_observation_price}')


        appendix_array = np.array([
            self.balance / MAX_ACCOUNT_BALANCE,
            (self.net_worth - self.balance) / MAX_ACCOUNT_BALANCE,
            self.shares_held / MAX_NUM_SHARES, 0, 0, 0, 0,
        ]).reshape(7,1)
        
        obs = np.append(frame, appendix_array, axis = 1)
        return obs

    def step(self, action):
        self.passo_atual_total += 1
        
        # Executa um passo no ambiente
        self._take_action(action)

        # pdb.set_trace()

        # Incrementa o passo
        self.deslocamento += 10

        # Reseta para o início do dataset, caso chegue ao final do dataset
        if self.deslocamento > len(self.df) - 10:
            self.deslocamento = 50

        delay_modifier = (self.passo_atual_total / (len(self.df)/10))

        next_observation = self._next_observation()

        # Normalizar os valores

        # ZONA DE RECOMPENSA:
        # reward = self.net_worth * delay_modifier
        action_reward = (self.current_observation_price - self.last_observation_price) * self.quantidade_executada * delay_modifier
        transition_reward = (self.current_observation_price - self.last_observation_price) * self.shares_held * delay_modifier
        cumulative_reward = self.net_profit_amount * delay_modifier

        # Testing rewards:
        reward_step = 0

        # Ordem diferente de neutra e quantidade comercializada igual a 0 -> Reward negativa
        if self.action_type != 0 and self.quantidade_executada == 0:
            if (self.action_type > 0 and self.current_observation_price > self.last_observation_price):
                reward_step -= 10 * delay_modifier
            elif (self.action_type < 0 and self.current_observation_price < self.last_observation_price):
                if self.shares_held > 0:
                    reward_step -= 1 * abs(transition_reward)
        elif (self.action_type > 0 and self.current_observation_price > self.last_observation_price) or (self.action_type < 0 and self.current_observation_price < self.last_observation_price):
          reward_step += 1 * abs(action_reward)
        elif (self.action_type > 0 and self.current_observation_price < self.last_observation_price) or (self.action_type < 0 and self.current_observation_price > self.last_observation_price):
          reward_step -= 1 * abs(action_reward)

        # Análise relacionada à quantidade mantida pelo agente em um determinado passo
        if self.shares_held > 0:
            reward_step += transition_reward

        # Checa o lucro da estratégia até o presente momento
        reward_step += cumulative_reward

        # pdb.set_trace()

        self.recompensas_por_acao_episodio.append(reward_step)
        
        # The episode reward is the rate of the net profit amount and amount invested multiplied by 1000. 
        self.net_profit_array.append(self.net_profit_amount)

        done = (self.net_worth <= (self.initial_amount * self.stop_condition) )
        
        if done:
          print('Done')
          self.qtd_episodios += 1
          self.episodios.append([self.deslocamento, self.qtd_episodios])

        return next_observation, reward_step, done, {}


    def _take_action(self, action):
        # Set the current price to a random price within the time step
        action_type = action[0]
        amount_bought_or_sold = action[1]
        resultado_acao = []

        if amount_bought_or_sold == 0:
            # if self.mode == 'testing':
            #     print('Pulou')
            #     print(amount_bought_or_sold)
            self.net_worth = self.balance + self.shares_held * self.current_observation_price
            self.lucro_bruto.append(self.net_worth)
        else:
            # COMPRA - Buy amount % of balance in shares
            if action_type > 0:
                tipo_acao = 'compra'
                total_shares_possible_to_buy = int(math.floor(self.balance / self.current_observation_price))
                # if self.mode == 'testing':
                #     print('total_shares_possible_to_buy')
                #     print(total_shares_possible_to_buy)
                shares_bought = math.ceil(total_shares_possible_to_buy * amount_bought_or_sold)
                # if self.mode == 'testing':
                #     print('total_shares_bought')
                #     print(shares_bought)
                buying_cost = shares_bought * self.current_observation_price
                self.balance -= buying_cost
                self.shares_held += shares_bought
                self.action_type = action_type
                self.quantidade_executada = shares_bought

            # VENDA - Sell amount % of shares held
            elif action_type < 0:
                if self.mode == 'testing':
                    print('total shares possible to sell:')
                    print(self.shares_held)
                shares_sold = int(math.ceil(self.shares_held * (amount_bought_or_sold)))
                if self.mode == 'testing':
                    print('shares sold:')
                    print(shares_sold)
                self.balance += shares_sold * self.current_observation_price
                self.shares_held -= shares_sold
            
                self.action_type = action_type
                self.quantidade_executada = shares_sold

            self.shares_held_array.append(self.shares_held)
            self.net_worth = self.balance + self.shares_held * self.current_observation_price
            # if self.mode == 'testing':
            #     print(self.net_worth)
            #     print(self.mode)
            self.lucro_bruto.append(self.net_worth)

            self.net_profit_amount = self.net_worth - self.initial_amount

            return resultado_acao

            



    # Render the environment to the screen
    def render(self, mode='human', close=False):
        print(f'Step: {self.deslocamento}')
        print(f'Balance: {self.balance}')
        print(f'Shares held: {self.shares_held}')
        print(f'Total Shares Sold: {self.total_shares_sold}')
        print(f'Share price: {self.share_price}')
        print(f'Profit: {self.net_profit_amount}')
        print(f'Total Rewards: {np.sum(self.recompensas_por_acao_episodio)}')
        print(f'Array de Lucro Bruto: {self.lucro_bruto}')
