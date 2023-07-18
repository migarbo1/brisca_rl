from .random_oponent_env import RandomOponentBriscaEnv, State

class SamePolicyOponentBriscaEnv(RandomOponentBriscaEnv):

    def get_oponent_card(self, fun_approx = None):
        state = State(self.oponent_hand, self.ruling_suit)
        if len(self.cards_in_play) != 0:
            state.played_card = self.cards_in_play[0]
        return self.oponent_hand.pop(fun_approx.select_action(state))