from reward_zone.i_rewards import IRewards
import random
import math
import pdb


class LocalReward(IRewards):

    def __init__(self, agente):
        self.quantidade_executada = agente.quantidade_executada
        self.current_observation_price = agente.current_observation_price
        self.last_observation_price = agente.last_observation_price
        
    def calculate_reward(self):
        # delay_modifier = (self.step_atual / self.max_steps)
        # reward_step = net_worth * delay_modifier
        
        # Sem aplicar o delay modifier
        reward_step = self.quantidade_executada * (self.current_observation_price - self.last_observation_price)
        return reward_step
