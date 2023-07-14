from enum import IntEnum
import random
'''
cards will be represented as integer. 
Leftmost number will be the suit of the card (see enum)
next number will be the card index sorted from 1 to 12 (excluding 8 and 9 since its spanish deck)
last digits will be the value of the card (explained in the readme) 
'''

card_value = {0: 11, 1:0, 2:10, 3:0, 4:0, 5:0, 6:0, 7:2, 8:3, 9:4}

class Suits(IntEnum):
    COINS: 0
    SWORDS: 1
    CUPS: 2
    STICKS: 3


class State():
    def __init__(self, hand: list, ruling_suit: int, played_card: int = None):
        self.hand = hand
        self.ruling_suit = ruling_suit
        self.played_card = played_card

class BriscaEnv():
    def initialize_deck(self):
        self.deck = [i for i in range(0,40)]
        random.shuffle(self.deck)


    def __init__(self):
        self.initialize_deck()
        self.ruling_card = self.deck[-1]
        self.ruling_suit = self.get_card_suit(self.ruling_card)
        self.points = {'player': 0, 'rival': 0}
        self.cards_in_play = []


    def get_starting_hand(self):
        return [self.deck.pop(0) for i in range(3)]
    

    def draw(self, hand):
        drawed_card = self.deck.pop(0) if len(self.deck) else None
        if drawed_card != None:
            hand.append(drawed_card)
        return hand
    

    def play(self, c):
        self.cards_in_play.append(c)
    

    def change_ruling_card(self, hand: list):
        if len(hand) > 0 and len(self.deck) > 0:
            changing_card = 6 if self.get_card_number(self.ruling_card) > 6 else 1
            for i, card in enumerate(hand):
                card_suit = self.get_card_suit(card)
                if card_suit == self.ruling_suit and self.get_card_number(card) == changing_card:
                    self.ruling_card, hand[i] = hand[i], self.ruling_card
                    self.deck[-1] = self.ruling_card
                    break
        return hand
    

    def get_card_suit(self, c):
        return c//10
    

    def get_card_number(self, c):
        return c%10
    

    def get_card_value(self, c):
        return card_value[self.get_card_number(c)]


    def get_round_winner(self, c1, c2):
        '''
        returns true if c1 wins, false otherwise.
        Retuns punctuation of winner
        '''
        
        c1_suit = self.get_card_suit(c1)
        c2_suit = self.get_card_suit(c2)

        c1_value = self.get_card_value(c1)
        c2_value = self.get_card_value(c2)
        
        c1_number = self.get_card_number(c1)
        c2_number = self.get_card_number(c2)

        self.cards_in_play = []
        if c1_suit == c2_suit:
            if c1_value == c2_value:
                return c1_number > c2_number, 0 #same suit and same value can only be regular cards
            else:
                return c1_value > c2_value, c1_value + c2_value
        else:
            c1_round_value = c1_value + 100 if c1_suit == self.ruling_suit else c1_value + 50
            c2_round_value = c2_value + 100 if c2_suit == self.ruling_suit else c2_value
            
            return c1_round_value > c2_round_value, c1_value + c2_value


    def is_game_finished(self, p1_hand: list, p2_hand: list):
        return len(self.deck) == 0 and len(p1_hand) == len(p2_hand) == 0



class RandomOponentBriscaEnv(BriscaEnv):
    def __init__(self):
        super().__init__()
        self.oponent_hand = self.get_starting_hand()

    def step(self, state: State, action: int):
        player_hand = state.hand
        card_to_play =  player_hand.pop(action)

        self.play(card_to_play)

        if state.played_card == None: #player hits first
            oponent_card_to_play = self.oponent_hand.pop(random.randint(0,len(self.oponent_hand)-1))
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
                oponent_next_card_to_play = self.oponent_hand.pop(random.randint(0,len(self.oponent_hand)-1))
                state.played_card = oponent_next_card_to_play
                self.play(oponent_next_card_to_play)
        
        state.hand = player_hand

        if self.is_game_finished(player_hand, self.oponent_hand):
            #reward = (self.points['player'] - self.points['rival']) / abs(self.points['player'] - self.points['rival'])
            reward = self.points['player'] - self.points['rival']
        else:
            reward = 0

        return state, reward