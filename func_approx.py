import numpy as np 
import random
from environments.brisca_env import State

class FunctApproxMethodology():

    def __init__(self, path = None) -> None:
        self.theta = np.zeros((82,)) if path == None else self.load_weights(path) # suit + (40)hand + (40)card_played** + index_of_card_to_play
        self.num_actions = 40

    def get_epsilon(self):
        return 0.05

    def get_alpha(self):
        return 0.01

    def get_feature_vector(self, state: State, action):
        x = np.zeros(82)
        x[0] = state.ruling_suit
        for c in state.hand:
            x[c] = 1
        x[-1] = action
        if state.played_card != None:
            x[41 + state.played_card] = 1 #set the index of the played card to 1
        return x

    def get_q_hat(self, state: State, action):
        x = np.array(self.get_feature_vector(state, action))
        w = self.theta.transpose()
        return np.dot(x, w)

    def select_action(self, state: State):
        eps = self.get_epsilon()
        if eps/self.num_actions + 1-eps > random.random():
            action = self.get_argmax_q_value(state)
        else:
            action = random.randint(0, len(state.hand)-1)
        return action

    def get_argmax_q_value(self, state: State):
        max = -np.inf
        argmax = None
        for action in range(len(state.hand)):
            local_max = self.get_q_hat(state, action)
            if  local_max > max:
                max = local_max
                argmax = action
        return argmax
    
    def save_weights(self, filename = 'weights/same_policy_weights.npy'):
        with open(filename, 'wb') as file:
            np.save(file, self.theta)

    def load_weights(self, filename):
        with open(filename, 'wb') as file:
            return np.load(file)