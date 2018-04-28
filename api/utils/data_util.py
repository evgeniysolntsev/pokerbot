from api.poker.state import State


def get_array_from_player(player=None):
    temp = [0] * 68

    if len(player.hand) > 1:
        temp[State.RANKS.index(player.hand[0].rank)] = 1
        temp[State.SUITS.index(player.hand[0].suit) + 13] = 1
        temp[State.RANKS.index(player.hand[1].rank)] = 1
        temp[State.SUITS.index(player.hand[1].suit) + 13] = 1
    if len(player.table) > 2:
        temp[State.RANKS.index(player.table[0].rank) + 17] = 1
        temp[State.SUITS.index(player.table[0].suit) + 30] = 1
        temp[State.RANKS.index(player.table[1].rank) + 17] = 1
        temp[State.SUITS.index(player.table[1].suit) + 30] = 1
        temp[State.RANKS.index(player.table[2].rank) + 17] = 1
        temp[State.SUITS.index(player.table[2].suit) + 30] = 1
    if len(player.table) > 3:
        temp[State.RANKS.index(player.table[3].rank) + 34] = 1
        temp[State.SUITS.index(player.table[3].suit) + 47] = 1
    if len(player.table) > 4:
        temp[State.RANKS.index(player.table[4].rank) + 51] = 1
        temp[State.SUITS.index(player.table[4].suit) + 64] = 1

    return temp
