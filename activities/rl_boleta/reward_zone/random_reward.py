from reward_zone.i_rewards import IRewards
import random
import math


class RandomReward(IRewards):
    
    def __init__(self, agente):
        self.step_atual = agente.passo_atual_total
        self.max_steps = agente.max_steps
        self.current_observation_price = agente.current_observation_price
        self.last_observation_price = agente.last_observation_price
        self.shares_held = agente.shares_held
        self.action_type = agente.action_type
        self.quantidade_executada = agente.quantidade_executada

    def calculate_reward(self):
        random_reward = random.uniform(-1, 1)
        return random_reward
