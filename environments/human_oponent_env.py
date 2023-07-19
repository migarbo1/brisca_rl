from .random_oponent_env import RandomOponentBriscaEnv
from environments.brisca_env import Suits
from environments.brisca_env import State

card_real_num = [1,2,3,4,5,6,7,10,11,12]

class HumanOponentEnvironment(RandomOponentBriscaEnv):

    def step(self, state: State, action: int, fun_approx = None):
        print('ruling card: ', card_to_text(self.ruling_card))
        player_hand = state.hand
        card_to_play =  player_hand.pop(action)

        self.play(card_to_play)

        print('cards in play: ', None if len(self.cards_in_play) == 0 else card_to_text(self.cards_in_play[0]))

        agent_hits_first = False
        if state.played_card == None: #rl_agent hits first
            oponent_card_to_play = self.get_oponent_card(fun_approx)
            agent_hits_first = True
            self.play(oponent_card_to_play)
        else:
            print('RL agent played card: ', card_to_text(card_to_play))
            #oponent_card_to_play = self.cards_in_play[0]

        first_card_wins, points = self.get_round_winner(*self.cards_in_play)

        print('+{} for {}'.format(points, 'RL agent' if self.rl_agent_wins(first_card_wins, agent_hits_first) else 'YOU'))

        player_hand = self.change_ruling_card(player_hand)
        self.oponent_hand = self.change_ruling_card(self.oponent_hand)

        if self.rl_agent_wins(first_card_wins, agent_hits_first):
            player_hand = self.draw(player_hand)
            self.oponent_hand = self.draw(self.oponent_hand)
            state.played_card = None
            self.points['rl_agent'] += points
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
            reward = self.points['rl_agent'] - self.points['rival']
        else:
            reward = 0

        return state, reward

    def get_oponent_card(self, no_used = None):
        print('cards in hand: ', [card_to_text(c) for c in self.oponent_hand])
        card_to_play = -1
        while card_to_play == -1 or card_to_play >= len(self.oponent_hand):
            print('Introduce the index of the card you want to play:')
            card_to_play = int(input()) -1
        return self.oponent_hand.pop(card_to_play)
    
def card_to_text(card):
    card_num = card % 10
    card_suit = Suits(card // 10)
    return '{}-{}'.format(card_real_num[card_num], card_suit.name)
