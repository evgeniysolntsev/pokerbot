class Card(object):
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        converted_map = {
            14: 'A',
            13: 'K',
            12: 'Q',
            11: 'J',
            10: 'T',
            's': u"\u2660",
            'h': u"\u2764",
            'd': u"\u2666",
            'c': u"\u2663"
        }
        rank = converted_map.get(self.rank)
        suit = converted_map.get(self.suit)
        if not rank:
            rank = self.rank
        if not suit:
            suit = self.suit
        return str(rank) + str(suit)

    def rank_str(self):
        converted_map = {
            14: 'A',
            13: 'K',
            12: 'Q',
            11: 'J',
            10: 'T'
        }
        rank = converted_map.get(self.rank)
        if not rank:
            rank = self.rank
        return str(rank)

    def suit_str(self):
        converted_map = {
            's': u"\u2660",
            'h': u"\u2764",
            'd': u"\u2666",
            'c': u"\u2663"
        }
        suit = converted_map.get(self.suit)
        if not suit:
            suit = self.suit
        return str(suit)

    def __eq__(self, other):
        return self.rank == other.rank

    def __ne__(self, other):
        return (self.rank != other.rank) or (self.suit != other.suit)

    def __lt__(self, other):
        return self.rank < other.rank

    def __le__(self, other):
        return self.rank <= other.rank

    def __gt__(self, other):
        return self.rank > other.rank

    def __ge__(self, other):
        return self.rank >= other.rank
