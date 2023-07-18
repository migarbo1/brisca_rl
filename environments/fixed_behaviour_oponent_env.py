from .random_oponent_env import RandomOponentBriscaEnv

class FixedBehaviourOponentBriscaEnv(RandomOponentBriscaEnv):
    def get_oponent_card(self, fun_approx = None):
        card_2_play = 0
        max_points = -1
        win = False

        if len(self.cards_in_play) == 0:
            return self.oponent_hand.pop(self.get_lowest_value_card())
        else:
            for i, c in enumerate(self.oponent_hand):
                win, points = self.get_round_winner(self.cards_in_play[0], c, reset_cards=False)
                if win and points > max_points:
                    card_2_play = i

            if not win and card_2_play == 0: #can't win with any card
                return self.oponent_hand.pop(self.get_lowest_value_card())
            
            return self.oponent_hand.pop(card_2_play)

    def get_lowest_value_card(self):
        min_val = 100000
        index = 0
        for i, c in enumerate(self.oponent_hand):
            c_value = self.get_card_value(c) + 100 if self.get_card_suit == self.ruling_suit else self.get_card_value(c) + 50
            if c_value < min_val:
                index = i
        return index