import gym
from gym import spaces
import numpy as np
import pdb
import math
from reward_zone.net_worth_reward import NetWorthReward
from reward_zone.carry_action_reward import CarryAndActionReward
from reward_zone.random_reward import RandomReward
from reward_zone.local_reward import LocalReward
from get_df_statistics import get_max_values

# Função que avalia os valores máximos para cada uma das variáveis dos dataframes
MAX_NUM_SHARES, MAX_SHARE_PRICE, MAX_TIME_HOUR, MAX_TIME_MINUTE, MAX_TIME_SECOND, LAST_10_PRICES, LAST_10_SHARES = get_max_values()

# Quantidade de transições passadas observadas
OBSERVATION_WINDOW = 5

# Initial account variables setup
ABSOLUTE_INITIAL_ACCOUNT = 0.00
MAX_ACCOUNT_BALANCE = 10000.00
MIN_ACCOUNT_BALANCE = -10000.00


class ReinforcementLearningEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    # TESTAR ADICIONAR O ENV NOS PARÂMETROS E RESETAR, NA PARTE DE TESTES
    def __init__(self, mode, df, initial_amount=ABSOLUTE_INITIAL_ACCOUNT, stop_condition=0.8, episodios=[], 
    recompensas_por_acao_episodio=[], lucro_bruto=[], lucro_liquido=[], current_step=0, 
    max_steps=100000, shares_held_array=[], acoes_compradas=[0], acoes_vendidas=[0], actions_array=[]):
        super(ReinforcementLearningEnv, self).__init__()
        self.mode = mode
        self.df = df
        self.initial_amount = initial_amount
        self.stop_condition = stop_condition
        self.balance = initial_amount
        self.net_worth = initial_amount
        self.net_worth_anterior = 0.0
        self.current_observation_price = 0
        self.last_observation_price = 0
        self.deslocamento = OBSERVATION_WINDOW * 10
        self.passo_atual_total = current_step
        self.passos = []
        self.net_profit_amount = 0
        self.gross_profit_array = lucro_bruto
        self.net_profit_array = lucro_liquido
        self.episodios = episodios
        self.qtd_episodios = len(episodios)
        self.recompensas_por_acao_episodio = recompensas_por_acao_episodio
        self.shares_held = 0
        self.action_type = 0
        self.quantidade_executada = 0
        self.shares_held_array = shares_held_array
        self.max_steps = max_steps
        self.acoes_compradas = acoes_compradas
        self.acoes_vendidas = acoes_vendidas
        self.actions_array = actions_array
        
        self.action_space = spaces.Box(low = np.array([-1]),
            high = np.array([1]),
            dtype = np.float16)

        self.observation_space = spaces.Box(
            low=0,
            high=1,
            shape=(7, (10 + OBSERVATION_WINDOW * 10 + 1)),
            dtype=np.float16)


    def reset(self):
        # Reset the state of the environment to an initial state

        self.deslocamento = OBSERVATION_WINDOW * 10
        self.initial_amount = 0.0
        # self.balance = 10000.00
        # self.net_worth = 10000.00
        # self.shares_held = 0
        # self.total_shares_sold = 0
        # self.total_sales_value = 0
        # self.share_price = 0
        # self.previous_price = 0
        # self.net_profit_amount = 0
        # self.stop_condition = 0.8
        # self.recompensas_por_acao_episodio = []
        # self.gross_profit_array = []
        # self.net_profit_array = []
        # self.shares_held_array = []
        # self.acoes_compradas = [0]
        # self.acoes_vendidas = [0]
        # self.actions_array = []
        
        return self._next_observation()


    def _next_observation(self):
        # Get the data points for the last 5 observations and the current one, and scale to between 0-1
    
        frame = np.array([
            self.df.loc[self.deslocamento - (OBSERVATION_WINDOW * 10): self.deslocamento + 9, 'Shares'] / MAX_NUM_SHARES,
            self.df.loc[self.deslocamento - (OBSERVATION_WINDOW * 10): self.deslocamento + 9, 'Prices'] / MAX_SHARE_PRICE,
            self.df.loc[self.deslocamento - (OBSERVATION_WINDOW * 10): self.deslocamento + 9, 'Time_Hour'] / MAX_TIME_HOUR,
            self.df.loc[self.deslocamento - (OBSERVATION_WINDOW * 10): self.deslocamento + 9, 'Time_Minute'] / MAX_TIME_MINUTE,
            self.df.loc[self.deslocamento - (OBSERVATION_WINDOW * 10): self.deslocamento + 9, 'Time_Second'] / MAX_TIME_SECOND,
            self.df.loc[self.deslocamento - (OBSERVATION_WINDOW * 10): self.deslocamento + 9, 'Last_10_Prices'] / LAST_10_PRICES,
            self.df.loc[self.deslocamento - (OBSERVATION_WINDOW * 10): self.deslocamento + 9, 'Last_10_Shares'] / LAST_10_SHARES
        ])

        # pdb.set_trace()

        self.current_observation_price = self.df.loc[self.deslocamento]['Last_10_Prices']

        self.last_observation_price = self.df.loc[self.deslocamento - 10]['Last_10_Prices']

        appendix_array = np.array([
            self.balance / MAX_ACCOUNT_BALANCE,
            (self.net_worth - self.balance) / MAX_ACCOUNT_BALANCE,
            self.shares_held / MAX_NUM_SHARES, 0, 0, 0, 0,
        ]).reshape(7,1)
        
        obs = np.append(frame, appendix_array, axis = 1)

        if np.count_nonzero(frame > 1) > 0:
            pdb.set_trace()

        return obs


    def step(self, action):
        self.passo_atual_total += 1
        
        # Executa um passo no ambiente
        self._take_action(action)

        # Reseta para o início do dataset, caso chegue ao final do dataset (na prática, não deveria continuar, ao chegar ao final)
        if self.deslocamento > len(self.df) - 10:
            self.deslocamento = OBSERVATION_WINDOW * 10

        next_observation = self._next_observation()

        reward = NetWorthReward(self)
        reward_step = reward.calculate_reward()

        self.recompensas_por_acao_episodio.append(reward_step)

        done = (self.net_worth <= MIN_ACCOUNT_BALANCE ) or (self.deslocamento == (len(self.df)) and self.mode == 'training')
        
        if done:
          print('Done')
          self.qtd_episodios += 1
          self.episodios.append([self.deslocamento, self.qtd_episodios])

        return next_observation, reward_step, done, {}


    def _take_action(self, action):
        if action[0] > 0:
            self.action_type = 1
        elif action[0] < 0:
            self.action_type = -1
        else:
            self.action_type = 0

        amount_bought_or_sold = abs(action[0])
        
        self.actions_array.append(self.action_type)
        # print(f'{action_type} - {amount_bought_or_sold}')
        
        self.net_worth_anterior = self.net_worth

        if math.isclose(amount_bought_or_sold, 0.0) or self.action_type == 0:
            self.quantidade_executada = 0
            self.net_worth = self.balance + self.shares_held * self.current_observation_price
            self.gross_profit_array.append(self.net_worth)
            self.net_profit_amount = self.net_worth - ABSOLUTE_INITIAL_ACCOUNT
            self.net_profit_array.append(self.net_profit_amount)
            self.shares_held_array.append(self.shares_held)
            self.acoes_compradas.append(0)
            self.acoes_vendidas.append(0)
        else:
            # COMPRA - Buy amount % of balance in shares
            if self.action_type == 1:
                quantidade_disponivel_compra = abs(MIN_ACCOUNT_BALANCE) + self.balance
                total_shares_possible_to_buy = int(math.floor( quantidade_disponivel_compra / self.current_observation_price))
                
                shares_bought = math.ceil(total_shares_possible_to_buy * amount_bought_or_sold)
                buying_cost = shares_bought * self.current_observation_price
                
                self.balance -= buying_cost
                self.shares_held += shares_bought
                self.quantidade_executada = shares_bought
                self.acoes_compradas.append(shares_bought)
                self.acoes_vendidas.append(0)

            # VENDA - Sell amount % of shares held
            elif self.action_type == -1:
                shares_sold = int(math.ceil(self.shares_held * (amount_bought_or_sold)))
                # print(shares_sold)
                self.balance += shares_sold * self.current_observation_price
                self.shares_held -= shares_sold
                self.quantidade_executada = - shares_sold
                self.acoes_vendidas.append(shares_sold)
                self.acoes_compradas.append(0)

            self.net_worth = self.balance + self.shares_held * self.current_observation_price
            self.net_profit_amount = self.net_worth - ABSOLUTE_INITIAL_ACCOUNT

            self.shares_held_array.append(self.shares_held)
            self.gross_profit_array.append(self.net_worth)
            self.net_profit_array.append(self.net_profit_amount)


        # print(self.deslocamento/10)
        # print(len(self.gross_profit_array))
        
        # if(len(self.gross_profit_array) >=2586):
        #     pdb.set_trace()
        
        # Incrementa o passo
        self.deslocamento += 10


    # Render the environment to the screen
    def render(self, mode='human', close=False):
        print(f'Step: {self.deslocamento}')
        print(f'Balance: {self.balance}')
        print(f'Shares held: {self.shares_held}')
        print(f'Profit: {self.net_profit_amount}')
        print(f'Total Rewards: {np.sum(self.recompensas_por_acao_episodio)}')
        # print(f'Share price: {self.share_price}')
        # print(f'Array de Lucro Bruto: {self.gross_profit_array}')
        # print(f'Array de Compra: {self.acoes_compradas}')
        # print(f'Array de Venda: {self.acoes_vendidas}')
