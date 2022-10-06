import random
import math

def reward_zone_1(step_atual, max_steps, current_observation_price, last_observation_price, shares_held, action_type, quantidade_executada):
    # REWARD ZONE:

    reward_step = 0

    delay_modifier = (step_atual / max_steps)

    diferenca_preco = current_observation_price - last_observation_price

    action_reward = 0
    # carry_reward = self.shares_held * diferenca_preco
    carry_reward = 0.5 if ((shares_held * diferenca_preco) >= 0) else -0.5
    # cumulative_reward = self.net_profit_amount / 100
    # cumulative_reward = 1 if self.net_profit_amount > 0 else -1
    # balance_reward = 1 if self.balance > (self.initial_amount / 3) else -1

    

    compra = 0 < action_type < 1
    neutro = action_type == 0
    venda = -1 <= action_type < 0

    # hold_reward = -1 if (self.sem_recursos) else 0

    preco_valorizou = diferenca_preco > 0.0
    preco_desvalorizou = diferenca_preco < 0.0
    preco_manteve = diferenca_preco = 0.0
    preco_diferente = preco_valorizou or preco_desvalorizou

    # Ordem diferente de neutra e quantidade comercializada igual a 0 OU ordem neutra e qtde executada igual a 0 -> Reward negativa
    # if (not neutro and self.quantidade_executada == 0) or (neutro and self.quantidade_executada != 0):
    #     # action_reward -= 1 * abs(carry_reward)
    #     action_reward -= 1

    if (compra and preco_valorizou) or (venda and preco_desvalorizou) or (neutro and preco_manteve):
        # action_reward += self.quantidade_executada * abs(diferenca_preco)
        action_reward = 1 if quantidade_executada != 0 else 0

    elif (compra and preco_desvalorizou) or (venda and preco_valorizou) or (neutro and preco_diferente):
        # action_reward -= self.quantidade_executada * abs(diferenca_preco)
        action_reward = -0.1

    

    # Recompensa o agente, baseado na ação tomada e na quantidade de cotas negociadas
    reward_step = action_reward + carry_reward

    reward_step *= delay_modifier

    return reward_step


def reward_zone_2(step_atual, max_steps, current_observation_price, last_observation_price, shares_held, action_type, quantidade_executada):
    random_reward = random.uniform(-1, 1)
    return random_reward

def reward_zone_net_worth(step_atual, max_steps, net_worth):
    delay_modifier = (step_atual / max_steps)

    # reward_step = net_worth * delay_modifier
    reward_step = net_worth
    return reward_step