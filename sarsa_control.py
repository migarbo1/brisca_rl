from environments.fixed_behaviour_oponent_env import FixedBehaviourOponentBriscaEnv
from environments.same_policy_oponent_env import SamePolicyOponentBriscaEnv
from environments.random_oponent_env import RandomOponentBriscaEnv
from func_approx import FunctApproxMethodology
from environments.brisca_env import State
import matplotlib.pyplot as plt
import numpy as np
import click
from tqdm import tqdm


@click.command()
@click.option('--e', default=500000, help='number of episodes to run')
@click.option('--l', default=1, help='lambda value for the sarsa control: 0 = sarsa, 1 = monte-carlo')
@click.option('--mode', default='Same_Policy', help='mode for oponent in environment: Same_Policy, Random or Fix_Beh')
def SARSA_control(e, l, mode):
    i = 0
    wins = 0
    points = []

    fun_approx_meth = FunctApproxMethodology()
    while tqdm(i < e):
        environment = get_environment(mode)
        rl_agent_hand = environment.get_starting_hand()

        #initialize S
        st = State(
            rl_agent_hand, 
            environment.ruling_suit, 
            environment.cards_in_play[0] if len(environment.cards_in_play) > 0 else None
        )

        #choose action for selected S
        act = fun_approx_meth.select_action(st)

        while not environment.is_game_finished(st.hand, environment.oponent_hand):
            #take action and observe Reward and New state
            st_, reward = environment.step(st, act, fun_approx_meth)
            
            #choose new action from derived new state
            if not environment.is_game_finished(st_.hand, environment.oponent_hand):
                act_ = fun_approx_meth.select_action(st_)
                delta = (1 - l) * fun_approx_meth.get_q_hat(st_, act_) - fun_approx_meth.get_q_hat(st, act)
                fun_approx_meth.theta += fun_approx_meth.get_alpha() * (reward + delta) * fun_approx_meth.get_feature_vector(st, act)
                act = act_
            else:
                fun_approx_meth.theta += fun_approx_meth.get_alpha() * (reward - fun_approx_meth.get_q_hat(st, act)) * fun_approx_meth.get_feature_vector(st, act)
                act = None
            st = st_

        i += 1
        points.append([environment.points['rl_agent'], environment.points['rival']])
        wins += environment.points['rl_agent'] > environment.points['rival']
    fun_approx_meth.save_weights(mode)
    plot_points(points, mode)
    print(wins)

def get_environment(mode):
    if mode == 'Same_Policy':
        return SamePolicyOponentBriscaEnv()
    
    if mode == 'Random':
        return RandomOponentBriscaEnv()
    
    if mode == 'Fix_Beh':
        return FixedBehaviourOponentBriscaEnv()

def plot_points(points, mode):
    x = np.array(points[len(points)-200:])
    plt.title('Last 200 games point distribution for {} oponent'.format(mode))
    plt.plot(x[:,0], label="rl_agent points")
    plt.plot(x[:,1], label="rival points")
    plt.legend()
    plt.savefig('images/last_200_games_{}_500k_eps.png'.format(mode))

    plt.close()
    plt.cla()
    plt.clf()

    x = np.array(points[:200])
    plt.title('First 200 games point distribution for {} oponent'.format(mode))
    plt.plot(x[:,0], label="rl_agent points")
    plt.plot(x[:,1], label="rival points")
    plt.legend()
    plt.savefig('images/first_200_games_{}_500k_eps.png'.format(mode))

if __name__ == '__main__':
    SARSA_control()
    
