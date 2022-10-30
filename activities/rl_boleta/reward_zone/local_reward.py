from reward_zone.i_rewards import IRewards
import random
import math
import pdb


class LocalReward(IRewards):

    def __init__(self, agente):
        self.step_atual = agente.passo_atual_total
        self.max_steps = agente.max_steps
        self.net_worth = agente.net_worth
        self.net_worth_anterior = agente.net_worth_anterior
        
    def calculate_reward(self):
        delay_modifier = (self.step_atual / self.max_steps)
        # reward_step = net_worth * delay_modifier
        
        # Sem aplicar o delay modifier
        reward_step = self.quantidade_executada * (self.current_observation_price - self.last_observation_price)
        return reward_step
