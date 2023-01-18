from data_treatment import treat_data
from stable_baselines3.sac.policies import MlpPolicy
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3 import PPO, A2C, DDPG, TD3
from sb3_contrib import TQC, TRPO
from rl_model import ReinforcementLearningEnv
from plot import plot_lucro_bruto, plot_qtde_acumulada_cotas_compradas_vendidas, plot_qtde_acumulada_decisoes_agente, plot_reward, plot_lucro_liquido, plot_qtde_acoes_posse

DIAS_TESTE = 7


def train_agent(training_files, repetitive_iteration_number):

    agg_timesteps = 0
    absolute_initial_balance = 0.00
    initial_amount = 0.0
    balance = initial_amount
    stp_condition = 0.8
    base_treinamento = []
    episodios_terminais_treino = 0
    episodios = []
    recompensas_por_acao_episodio = []
    lucro_bruto = []
    lucro_liquido = []
    current_step = 0
    shares_held_array = []
    acoes_compradas = []
    acoes_vendidas = []
    actions_array = []

    max_steps = 0
    for file in training_files:
        training_df = treat_data(file)
        timesteps = int(len(training_df)/10)
        max_steps += timesteps


    for file in training_files:

        # pdb.set_trace()
        base_treinamento.append(file)

        training_df = treat_data(file)
        timesteps = int(2*int(len(training_df)/10))

        index = training_files.index(file)

        rl_training_agent = ReinforcementLearningEnv('training', training_df, initial_amount, stp_condition, episodios, 
        recompensas_por_acao_episodio, lucro_bruto, lucro_liquido, current_step, max_steps, shares_held_array, acoes_compradas, 
        acoes_vendidas, actions_array)
        
        env_training = DummyVecEnv([lambda: rl_training_agent])

        # env_training.reset()
        if index == 0:
            # model = PPO("MlpPolicy", env_training, verbose=1)
            model = TRPO("MlpPolicy", env_training, verbose=1)

        else:
            model.set_env(env_training)

        # model.set_random_seed(seed=5)
        # pdb.set_trace()
        model.learn(total_timesteps = timesteps)

        # pdb.set_trace()
        initial_amount = rl_training_agent.net_worth
        balance = rl_training_agent.balance
        episodios_terminais_treino += len(rl_training_agent.episodios)
        episodios = rl_training_agent.episodios
        recompensas_por_acao_episodio = rl_training_agent.recompensas_por_acao_episodio
        lucro_bruto = rl_training_agent.gross_profit_array
        lucro_liquido = rl_training_agent.net_profit_array
        # pdb.set_trace()
        
        current_step = rl_training_agent.passo_atual_total
        shares_held_array = rl_training_agent.shares_held_array
        acoes_compradas = rl_training_agent.acoes_compradas
        acoes_vendidas = rl_training_agent.acoes_vendidas
        actions_array = rl_training_agent.actions_array

        buy_action_array = []
        hold_action_array = []
        sell_action_array = []

        for action in actions_array:
            buy_action_array.append(1 if 0 < action <= 1 else 0)
            hold_action_array.append(1 if action == 0 else 0)
            sell_action_array.append(1 if -1 <= action < 0 else 0)


        # if training_files.index(file) == (len(training_files) - 1):
        plot_reward(recompensas_por_acao_episodio, 'training', file, repetitive_iteration_number)
        plot_lucro_liquido(lucro_liquido, 'training', file, repetitive_iteration_number)
        plot_lucro_bruto(lucro_bruto, 'training', file, repetitive_iteration_number)
        plot_qtde_acoes_posse(rl_training_agent.shares_held_array, 'training', file, repetitive_iteration_number)
        plot_qtde_acumulada_cotas_compradas_vendidas(acoes_compradas, acoes_vendidas, 'training', file, repetitive_iteration_number)
        plot_qtde_acumulada_decisoes_agente(buy_action_array, hold_action_array, sell_action_array, 'training', file, repetitive_iteration_number)

        env_training.close()

    model.save(f'rl_trading_stocks_iteracao{repetitive_iteration_number}')


    training_testing_results = {
        'base de treinamento': base_treinamento,
        'passos de treinamento': agg_timesteps,
        'numero da iteracao': repetitive_iteration_number + 1,
        'treinamento - condição de parada': stp_condition,
        'quantidade de episódios terminais treino': episodios_terminais_treino,
        'recompensas treino': recompensas_por_acao_episodio[-1],
        'valor inicial treino': absolute_initial_balance,
        'valor final treino': lucro_bruto[-1],
        'lucro/prejuízo treino': lucro_liquido[-1]
    }

    # testing_results = test_agent(testing_files[0], model, DIAS_TESTE, repetitive_iteration_number)

    # training_testing_results.update(testing_results)



    # pdb.set_trace()

    del model
    
    return training_testing_results


    # pdb.set_trace()