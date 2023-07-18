from .brisca_env import *

class RandomOponentBriscaEnv(BriscaEnv):
    def __init__(self):
        super().__init__()
        self.oponent_hand = self.get_starting_hand()

    def step(self, state: State, action: int, fun_approx = None):
        player_hand = state.hand
        card_to_play =  player_hand.pop(action)

        self.play(card_to_play)

        if state.played_card == None: #player hits first
            oponent_card_to_play = self.get_oponent_card(fun_approx)
        else:
            oponent_card_to_play = self.cards_in_play[0]

        player_wins, points = self.get_round_winner(card_to_play, oponent_card_to_play)

        player_hand = self.change_ruling_card(player_hand)
        self.oponent_hand = self.change_ruling_card(self.oponent_hand)

        if player_wins:
            player_hand = self.draw(player_hand)
            self.oponent_hand = self.draw(self.oponent_hand)
            state.played_card = None
            self.points['player'] += points
        else:
            self.oponent_hand = self.draw(self.oponent_hand)
            player_hand = self.draw(player_hand)
            self.points['rival'] += points
            if not self.is_game_finished(player_hand, self.oponent_hand):
                oponent_next_card_to_play = self.get_oponent_card(fun_approx)
                state.played_card = oponent_next_card_to_play
                self.play(oponent_next_card_to_play)
        
        state.hand = player_hand

        if self.is_game_finished(player_hand, self.oponent_hand):
            reward = self.points['player'] - self.points['rival']
        else:
            reward = 0

        return state, reward
    
    def get_oponent_card(self, fun_approx = None):
        return self.oponent_hand.pop(random.randint(0,len(self.oponent_hand)-1))