from api.helpers.message import print_error


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
            'h': u"\u2665",
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

    def validate_string(self):
        converted_map = {
            'A': 14,
            'K': 13,
            'Q': 12,
            'J': 11,
            'T': 10,
            '14': 14,
            '13': 13,
            '12': 12,
            '11': 11,
            '10': 10,
            '9': 9,
            '8': 8,
            '7': 7,
            '6': 6,
            '5': 5,
            '4': 4,
            '3': 3,
            '2': 2,
            's': 's',
            'h': 'h',
            'd': 'd',
            'c': 'c'
        }
        rank = converted_map.get(self.rank)
        suit = converted_map.get(self.suit)
        if rank and suit:
            self.rank = rank
            self.suit = suit
        else:
            print_error("Invalid format card")
        return self

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
