import brisca_env as env
import numpy as np
import random

theta = np.zeros((82,)) # suit + (40)hand + (40)card_played** + index_of_card_to_play
num_actions = 40

def get_epsilon():
    return 0.05

def get_alpha():
    return 0.01

def get_feature_vector(state: env.State, action):
    x = np.zeros(82)
    x[0] = state.ruling_suit
    for c in state.hand:
        x[c] = 1
    x[-1] = action
    if state.played_card != None:
        x[41 + state.played_card] = 1 #set the index of the played card to 1
    return x

def get_q_hat(state: env.State, action):
    x = np.array(get_feature_vector(state, action))
    w = theta.transpose()
    return np.dot(x, w)

def select_action(state: env.State):
    eps = get_epsilon()
    if eps/num_actions + 1-eps > random.random():
        action = get_argmax_q_value(state)
    else:
        action = random.randint(0, len(state.hand))
    return action

def get_argmax_q_value(state: env.State):
    max = -np.inf
    argmax = None
    for action in range(len(state.hand)):
        local_max = get_q_hat(state, action)
        if  local_max > max:
            max = local_max
            argmax = action
    return argmax

def SARSA_control(num_episodes, lam):
    global theta
    theta = np.zeros((82,))
    i = 0
    while i < num_episodes:
        environment = env.RandomOponentBriscaEnv()
        rl_agent_hand = environment.get_starting_hand()

        #initialize S
        st = env.State(
            rl_agent_hand, 
            environment.ruling_suit, 
            environment.cards_in_play[0] if len(environment.cards_in_play) > 0 else None
        )

        print('episode: ',i)
        #choose action for selected S
        act = select_action(st)
        print('selected action', act)

        while not environment.is_game_finished(st.hand, environment.oponent_hand):
            #take action and observe Reward and New state
            st_, reward = environment.step(st, act)
            print('new state', st_)
            
            #choose new action from derived new state
            if not environment.is_game_finished(st_.hand, environment.oponent_hand):
                print('game not finished')
                act_ = select_action(st_)
                print('new action selected', act_)
                delta = (1 - lam) * get_q_hat(st_, act_) - get_q_hat(st, act)
                theta += get_alpha() * (reward + delta) * get_feature_vector(st, act)
                act = act_
                print('parameters updated')
            else:
                print('game finished')
                theta += get_alpha() * (reward - get_q_hat(st, act)) * get_feature_vector(st, act)
                act = None
                print('parameters updated')
            st = st_

        i += 1

    print(environment.points)

if __name__ == '__main__':
    SARSA_control(1, 1) # 1 = monte-carlo
