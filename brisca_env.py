from enum import IntEnum
import random
from typing import Callable

#State = [[c1, c2, c3], c_rule, c_played*] == player's hand, card ruling, card played in turn if any

card_value = {1: 11, 2:0, 3:10, 4:0, 5:0, 6:0, 7:0, 10:2, 11:3, 12:4}

class Suits(IntEnum):
    COINS: 1
    STICKS: 2
    SWORDS: 3
    CUPS: 4

class Card():
    def __init__(self, number: int, suit: Suits, value: int):
        self.number = number
        self.suit = suit
        self.value = value
        self.__inner_value = 0

    def to_tuple(self):
        return (self.number, self.value, int(self.suit))
    
    def __eq__(self, __value: object) -> bool:
        return __value.number == self.number and __value.suit == self.suit and __value.value == self.value

class BriscaEnv():

    def initialize_deck(self):
        self.deck = []
        for suit in Suits:
            for k,v in card_value:
                self.deck.append(
                    Card(k, suit, v)
                )
        random.shuffle(self.deck)

    def set_ruling_suit(self):
        self.ruling_suit = self.deck[-1]

    def __init__(self):
        self.initialize_deck()
        self.set_ruling_suit()
        self.cards_in_play = []
        self.player_points = 0
        self.oponent_points = 0

    def is_game_finished(self, p1_hand: list, p2_hand: list):
        return len(self.deck) + len(p1_hand) + len(p2_hand) == 0

    def get_starting_hand(self):
        return [self.deck.pop(0) for i in range(3)]
    
    def get_round_winner(self, c1: Card, c2: Card):
        '''
        returns true if c1 wins, false otherwise.
        Retuns punctuation of winner
        '''
        self.cards_in_play = []
        if c1.suit == c2.suit:
            if c1.value == c2.value:
                return c1.number > c2.number, 0 #same suit and same value can only be regular cards
            else:
                return c1.value > c2.value, c1.value + c2.value
        else:
            c1.__inner_value = c1.value + 200 if c1.suit == self.ruling_suit else c1.value + 100
            c2.__inner_value = c2.value + 200 if c2.suit == self.ruling_suit else c2.value
            
            return c1.__inner_value > c2.__inner_value, c1.value + c2.value

    def draw(self, hand):
        drawed_card = self.deck.pop(0) if len(self.deck) else None
        if drawed_card != None:
            hand.append(drawed_card)
        return hand

    def play(self, card: Card):
        self.cards_in_play.append(card)
        return self.cards_in_play

    def change_ruling_card(self, hand: list):
        for i, card in enumerate(hand):
            card = Card(*card)
            if card == self.ruling_suit:
                self.ruling_suit, hand[i] = hand[i], self.ruling_suit
        
        return hand

    def step(self, state: list, action: int):
        pass

#TODO: think about only having one play inside step function. reward will always be 0 until the game ends

class RandomOponentBriscaEnv(BriscaEnv):
    def __init__(self):
        super.__init__()
        self.oponent_hand = self.get_starting_hand()

    def step(self, state: list, action: int):
        card_to_play = state[0].pop(action)
        card_to_play = Card(*card_to_play)

        self.play(card_to_play)

        if state[-1] == None: #player hits first
            oponent_card_to_play = self.oponent_hand.pop(random.randint(0,len(self.oponent_hand)-1))
        else:
            oponent_card_to_play = self.cards_in_play[0]

        player_wins, points = self.get_round_winner(card_to_play, oponent_card_to_play)

        state[0] = self.change_ruling_card(state[0])
        self.oponent_hand = self.change_ruling_card(self.oponent_hand)

        if player_wins:
            state[0] = self.draw(state[0])
            self.oponent_hand = self.draw(self.oponent_hand)
            state[-1] = None
            self.player_points += points
        else:
            self.oponent_hand = self.draw(self.oponent_hand)
            state[0] = self.draw(state[0])
            oponent_next_card_to_play = self.oponent_hand.pop(random.randint(0,len(self.oponent_hand)-1))
            state[-1] = oponent_next_card_to_play.to_tuple()
            self.oponent_points += points

        if self.is_game_finished(state[0], self.oponent_hand):
            reward = (self.player_points - self.oponent_points) / abs(self.player_points - self.oponent_points)
        else:
            reward = 0

        return state, reward