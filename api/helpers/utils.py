import config
from api.poker.state import State


def get_array_inputs_cards(player=None):
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


def get_array_inputs_cards_and_bot_actions(bot=None, call_limit=0, bet_limit=0):
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
    config.NN_INPUTS_CARDS_AND_BOT_ACTIONS = True
    config.NN_INPUTS_CARDS = False
COUNT_PLAYERS = len(config.HUMAN_NAMES)
COUNT_BOT_PLAYERS = len(config.BOT_NAMES)
COUNT_ALL_PLAYERS = COUNT_PLAYERS + COUNT_BOT_PLAYERS

ALL_NAMES = []
ALL_NAMES.extend(config.HUMAN_NAMES)
ALL_NAMES.extend(config.BOT_NAMES)

MAX_LENGTH_NAME = max([len(name) for name in ALL_NAMES])

TEMP_NAMES = []
TEMP_BOT_NAMES = []
for name in config.HUMAN_NAMES:
    if len(name) < MAX_LENGTH_NAME:
        while len(name) != MAX_LENGTH_NAME:
            name = name + " "
    TEMP_NAMES.append(name)
config.HUMAN_NAMES = TEMP_NAMES

for name in config.BOT_NAMES:
    if len(name) < MAX_LENGTH_NAME:
        while len(name) != MAX_LENGTH_NAME:
            name = name + " "
    TEMP_BOT_NAMES.append(name)
config.BOT_NAMES = TEMP_BOT_NAMES

ALL_NAMES = []
ALL_NAMES.extend(config.HUMAN_NAMES)
ALL_NAMES.extend(config.BOT_NAMES)

TEMP_NAMES = config.HUMAN_NAMES.copy()
TEMP_BOT_NAMES = config.BOT_NAMES.copy()

BOT_RANDOM_ACTIONS = config.LEARNING_MODE
BOT_CUSTOM_ACTIONS = config.PLAYING_MODE and config.NN_INPUTS_CARDS
BOT_NN_ACTIONS = config.PLAYING_MODE and config.NN_INPUTS_CARDS_AND_BOT_ACTIONS
