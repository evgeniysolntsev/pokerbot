from api.dnn import config
from api.utils.singleton import singleton


@singleton
class State(object):
    n_players = config.N_PLAYERS
    output_in_console = config.OUTPUT_IN_CONSOLE
    output_in_console_comb = config.OUTPUT_IN_CONSOLE_COMB
    RANKS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    SUITS = ['s', 'd', 'h', 'c']
    pre_flop = False
    flop = False
    turn = False
    river = False

    def set(self, pre_flop=False, flop=False, turn=False, river=False):
        self.pre_flop = pre_flop
        self.flop = flop
        self.turn = turn
        self.river = river

    def get(self):
        if self.pre_flop:
            return "PreFlop"
        if self.flop:
            return "Flop"
        if self.turn:
            return "Turn"
        if self.river:
            return "River"

    def next(self):
        if self.pre_flop:
            self.set(flop=True)
        elif self.flop:
            self.set(turn=True)
        elif self.turn:
            self.set(river=True)
        else:
            self.set(pre_flop=True)
