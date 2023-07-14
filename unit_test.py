from brisca_env import *
def get_env():
    return RandomOponentBriscaEnv()

def test_init():
    env = get_env()
    assert env.cards_in_play == []
    assert len(env.deck) == 37
    assert len(env.oponent_hand) == 3
    assert env.ruling_card == env.deck[-1]

def test_starting_hand():
    env = get_env()
    hand = env.get_starting_hand()
    assert len(hand) == 3
    assert len(env.deck) == 34

def test_draw():
    env = get_env()
    hand = env.get_starting_hand()
    hand = env.get_starting_hand()
    removed = hand.pop(0)
    hand = env.draw(hand)
    assert removed not in hand
    assert len(hand) == 3

def test_change_ruling_card_greater_than_7_changes_card():
    env = get_env()
    env.deck[-1] = 8
    env.ruling_card = 8
    env.ruling_suit = 0

    hand = [0,6,2]

    hand = env.change_ruling_card(hand)

    assert len(hand) == 3
    assert hand[1] == 8
    assert len(env.deck) == 37
    assert env.deck[-1] == 6

def test_change_ruling_card_greater_than_7_NOT_changes_card():
    env = get_env()
    env.deck[-1] = 8
    env.ruling_card = 8
    env.ruling_suit = 0

    hand = [0,5,2]

    hand_ = env.change_ruling_card(hand)

    assert len(hand) == 3
    assert len(hand_) == 3
    assert hand == hand_

def test_change_ruling_card_smaller_than_7_changes_card():
    env = get_env()
    env.deck[-1] = 5
    env.ruling_card = 5
    env.ruling_suit = 0

    hand = [0,6,1]

    hand = env.change_ruling_card(hand)

    assert len(hand) == 3
    assert hand[2] == 5
    assert len(env.deck) == 37
    assert env.deck[-1] == 1

def test_change_ruling_card_smaller_than_7_NOT_changes_card():
    env = get_env()
    env.deck[-1] = 5
    env.ruling_card = 5
    env.ruling_suit = 0

    hand = [0,4,2]

    hand_ = env.change_ruling_card(hand)

    assert len(hand) == 3
    assert len(hand_) == 3
    assert hand == hand_

def test_get_card_suit_return_coins():
    env = get_env()
    assert env.get_card_suit(5) == 0

def test_get_card_suit_return_swords():
    env = get_env()
    assert env.get_card_suit(15) == 1

def test_get_card_number():
    env = get_env()
    assert env.get_card_number(25) == 5

def test_get_card_value():
    env = get_env()
    assert env.get_card_number(20) == 0
    assert env.get_card_value(20) == 11

def test_get_round_winner_same_suit_same_value_ruling_false():
    env = get_env()
    c1 = 3
    c2 = 4
    env.ruling_suit = 0
    c1_wins, reward = env.get_round_winner(c1, c2)

    assert not c1_wins
    assert reward == 0

def test_get_round_winner_same_suit_same_value_ruling_true():
    env = get_env()
    c1 = 4
    c2 = 3
    env.ruling_suit = 0
    c1_wins, reward = env.get_round_winner(c1, c2)

    assert c1_wins
    assert reward == 0

def test_get_round_winner_same_suit_different_value_ruling_false():
    env = get_env()
    c1 = 3
    c2 = 0
    env.ruling_suit = 0
    c1_wins, reward = env.get_round_winner(c1, c2)

    assert not c1_wins
    assert reward == 11

def test_get_round_winner_same_suit_different_value_ruling_true():
    env = get_env()
    c1 = 0
    c2 = 3

    env.ruling_suit = 0
    c1_wins, reward = env.get_round_winner(c1, c2)

    assert c1_wins
    assert reward == 11

#TODO: more tests