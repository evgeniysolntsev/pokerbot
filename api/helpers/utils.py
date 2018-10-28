from termcolor import colored

import config
from api.poker.state import State


def get_array_for_cards_from_map(m=None):
    return get_array_from_stages_for_cards(
        m.get('pf0'), m.get('pf1'), m.get('f0'), m.get('f1'), m.get('f2'), m.get('t'), m.get('r')
    )


def get_array_inputs_cards(player=None):
    return get_array_from_stages_for_cards(
        player.hand[0], player.hand[1], player.table[0], player.table[1], player.table[2], player.table[3],
        player.table[4]
    )


def get_array_from_stages_for_cards(pf0, pf1, f0, f1, f2, t, r):
    temp = [0] * 68

    if pf0 and pf1:
        temp[State.RANKS.index(pf0.rank)] = 1
        temp[State.SUITS.index(pf0.suit) + 13] = 1
        temp[State.RANKS.index(pf1.rank)] = 1
        temp[State.SUITS.index(pf1.suit) + 13] = 1
    if f0 and f1 and f2:
        temp[State.RANKS.index(f0.rank) + 17] = 1
        temp[State.SUITS.index(f0.suit) + 30] = 1
        temp[State.RANKS.index(f1.rank) + 17] = 1
        temp[State.SUITS.index(f1.suit) + 30] = 1
        temp[State.RANKS.index(f2.rank) + 17] = 1
        temp[State.SUITS.index(f2.suit) + 30] = 1
    if t:
        temp[State.RANKS.index(t.rank) + 34] = 1
        temp[State.SUITS.index(t.suit) + 47] = 1
    if r:
        temp[State.RANKS.index(r.rank) + 51] = 1
        temp[State.SUITS.index(r.suit) + 64] = 1

    return temp


def get_array_inputs_cards_and_bot_actions(bot=None, call_limit=0, bet_limit=0):
    return get_array_from_stages_for_cards_and_action_bot(
        bot.hand[0], bot.hand[1], bot.table[0], bot.table[1], bot.table[2], bot.table[3], bot.table[4], call_limit,
        bet_limit
    )


def get_array_for_cards_and_action_bot_from_map(m=None):
    return get_array_from_stages_for_cards_and_action_bot(
        m.get('pf0'), m.get('pf1'), m.get('f0'), m.get('f1'), m.get('f2'), m.get('t'), m.get('r')
    )


def get_array_from_stages_for_cards_and_action_bot(pf0, pf1, f0, f1, f2, t, r, call_limit=0, bet_limit=0):
    temp = [0] * 268

    if pf0 and pf1:
        temp[State.RANKS.index(pf0.rank)] = 1
        temp[State.SUITS.index(pf0.suit) + 13] = 1
        temp[State.RANKS.index(pf1.rank)] = 1
        temp[State.SUITS.index(pf1.suit) + 13] = 1
    if f0 and f1 and f2:
        temp[State.RANKS.index(f0.rank) + 17] = 1
        temp[State.SUITS.index(f0.suit) + 30] = 1
        temp[State.RANKS.index(f1.rank) + 17] = 1
        temp[State.SUITS.index(f1.suit) + 30] = 1
        temp[State.RANKS.index(f2.rank) + 17] = 1
        temp[State.SUITS.index(f2.suit) + 30] = 1
    if t:
        temp[State.RANKS.index(t.rank) + 34] = 1
        temp[State.SUITS.index(t.suit) + 47] = 1
    if r:
        temp[State.RANKS.index(r.rank) + 51] = 1
        temp[State.SUITS.index(r.suit) + 64] = 1
    temp[68 + call_limit] = 1
    temp[167 + bet_limit] = 1

    return temp


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

BOT_RANDOM_ACTIONS = config.LEARNING_MODE and config.NN_INPUTS_CARDS_AND_BOT_ACTIONS
BOT_CUSTOM_ACTIONS = config.PLAYING_MODE and config.NN_INPUTS_CARDS
BOT_NN_ACTIONS = config.PLAYING_MODE and config.NN_INPUTS_CARDS_AND_BOT_ACTIONS
BOT_ALWAYS_SKIP = config.LEARNING_MODE and config.NN_INPUTS_CARDS

if (bool(config.LEARNING_MODE) + bool(config.PLAYING_MODE) + bool(config.PREDICTING_MODE)) != 1:
    print(colored("\t\tONLY ONE VARIABLE MAY BE EQUALS TRUE (LEARNING_MODE, PLAYING_MODE, PREDICTING_MODE)", "red"))
    exit(0)
if (bool(config.NN_INPUTS_CARDS_AND_BOT_ACTIONS) + bool(config.NN_INPUTS_CARDS)) != 1:
    print(colored("\t\tONLY ONE VARIABLE MAY BE EQUALS TRUE (NN_INPUTS_CARDS_AND_BOT_ACTIONS, NN_INPUTS_CARDS)", "red"))
    exit(0)
