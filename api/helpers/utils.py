import config
from api.helpers.message import print_error
from api.poker.state import State
from termcolor import colored

def get_array_for_cards_from_map(m=None):
    return get_array_from_stages_for_cards(
        m.get('pf0'), m.get('pf1'), m.get('f0'), m.get('f1'), m.get('f2'), m.get('t'), m.get('r')
    )

def get_colored_card(c=None):
    return colored(str(c), 'green' if c.suit == 's' or c.suit == 'c' else 'red')

def get_array_inputs_cards(player=None):
    hand, table, pf0, pf1, f0, f1, f2, t, r = player.hand, player.table, None, None, None, None, None, None, None
    if len(hand) > 1:
        pf0 = hand[0]
        pf1 = hand[1]
    if len(table) > 2:
        f0 = table[0]
        f1 = table[1]
        f2 = table[2]
    if len(table) > 3:
        t = player.table[3]
    if len(table) > 4:
        r = player.table[4]

    return get_array_from_stages_for_cards(pf0, pf1, f0, f1, f2, t, r)


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
    hand, table, pf0, pf1, f0, f1, f2, t, r = bot.hand, bot.table, None, None, None, None, None, None, None

    if len(hand) > 1:
        pf0 = hand[0]
        pf1 = hand[1]
    if len(table) > 2:
        f0 = table[0]
        f1 = table[1]
        f2 = table[2]
    if len(table) > 3:
        t = table[3]
    if len(table) > 4:
        r = table[4]

    return get_array_from_stages_for_cards_and_action_bot(pf0, pf1, f0, f1, f2, t, r, call_limit, bet_limit)


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


if config.PREDICTING_MODE:
    config.HUMAN_NAMES = {"unknown"}
    config.BOT_NAMES = {}

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

BOT_RANDOM_ACTIONS = config.LEARNING_MODE and config.NN_INPUTS_CARDS_AND_MORE
BOT_CUSTOM_ACTIONS = config.PLAYING_MODE and config.NN_INPUTS_CARDS
BOT_NN_ACTIONS = config.PLAYING_MODE and config.NN_INPUTS_CARDS_AND_MORE
BOT_ALWAYS_SKIP = config.LEARNING_MODE and config.NN_INPUTS_CARDS

if (bool(config.LEARNING_MODE) + bool(config.PLAYING_MODE) + bool(config.PREDICTING_MODE)) != 1:
    print_error("\t\tONLY ONE VARIABLE MAY BE EQUALS TRUE (LEARNING_MODE, PLAYING_MODE, PREDICTING_MODE)")
if (bool(config.NN_INPUTS_CARDS_AND_MORE) + bool(config.NN_INPUTS_CARDS)) != 1:
    print_error("\t\tONLY ONE VARIABLE MAY BE EQUALS TRUE (NN_INPUTS_CARDS_AND_BOT_ACTIONS, NN_INPUTS_CARDS)")
