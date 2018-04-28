import random

from api.poker.card import Card
from api.poker.state import State


class Deck(object):
    def __init__(self):
        self.deck = []
        for suit in State.SUITS:
            for rank in State.RANKS:
                self.deck.append(Card(rank, suit))

    def shuffle(self):
        random.shuffle(self.deck)

    def __len__(self):
        return len(self.deck)

    def pull(self):
        if len(self) == 0:
            return None
        else:
            return self.deck.pop(0)
