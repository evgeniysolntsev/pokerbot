import config
from api.poker.state import State


def get_array_from_simple_mode(player=None):
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


def get_array_from_mode(bot=None, call_limit=0, bet_limit=0):
    temp = [0] * 268

    if len(bot.hand) > 1:
        temp[State.RANKS.index(bot.hand[0].rank)] = 1
        temp[State.SUITS.index(bot.hand[0].suit) + 13] = 1
        temp[State.RANKS.index(bot.hand[1].rank)] = 1
        temp[State.SUITS.index(bot.hand[1].suit) + 13] = 1
    if len(bot.table) > 2:
        temp[State.RANKS.index(bot.table[0].rank) + 17] = 1
        temp[State.SUITS.index(bot.table[0].suit) + 30] = 1
        temp[State.RANKS.index(bot.table[1].rank) + 17] = 1
        temp[State.SUITS.index(bot.table[1].suit) + 30] = 1
        temp[State.RANKS.index(bot.table[2].rank) + 17] = 1
        temp[State.SUITS.index(bot.table[2].suit) + 30] = 1
    if len(bot.table) > 3:
        temp[State.RANKS.index(bot.table[3].rank) + 34] = 1
        temp[State.SUITS.index(bot.table[3].suit) + 47] = 1
    if len(bot.table) > 4:
        temp[State.RANKS.index(bot.table[4].rank) + 51] = 1
        temp[State.SUITS.index(bot.table[4].suit) + 64] = 1
    temp[68 + call_limit] = 1
    temp[167 + bet_limit] = 1

    return temp


if config.PLAYING_MODE or config.PREDICTING_MODE:
    config.EXTENDED_NN = True
    config.SIMPLE_NN = False
N_PLAYERS = len(config.NAMES)
N_BOT_PLAYERS = len(config.BOT_NAMES)
N_ALL_PLAYERS = N_PLAYERS + N_BOT_PLAYERS
ALL_NAMES = []
ALL_NAMES.extend(config.NAMES)
ALL_NAMES.extend(config.BOT_NAMES)
MAX_LENGTH_NAME = max([len(name) for name in ALL_NAMES])
TEMP_NAMES = []
TEMP_BOT_NAMES = []
for name in config.NAMES:
    if len(name) < MAX_LENGTH_NAME:
        while len(name) != MAX_LENGTH_NAME:
            name = name + " "
    TEMP_NAMES.append(name)
config.NAMES = TEMP_NAMES
for name in config.BOT_NAMES:
    if len(name) < MAX_LENGTH_NAME:
        while len(name) != MAX_LENGTH_NAME:
            name = name + " "
    TEMP_BOT_NAMES.append(name)
config.BOT_NAMES = TEMP_BOT_NAMES
ALL_NAMES = []
ALL_NAMES.extend(config.NAMES)
ALL_NAMES.extend(config.BOT_NAMES)
TEMP_NAMES = config.NAMES.copy()
TEMP_BOT_NAMES = config.BOT_NAMES.copy()
