import random

from termcolor import colored

from api.dnn import config
from api.helpers.singleton import singleton
from api.poker.bank import Bank
from api.poker.computer import Computer
from api.poker.deck import Deck
from api.poker.state import State


@singleton
class ComputerAction(object):
    max_total_points = None
    count_winners = None
    count_winners_final = None
    total_points = None

    def play_stage(self):
        print("-------{}--------".format(State.get()))
        if State.pre_flop:
            self.new_game()
        elif State.flop:
            self.pull_table()
            self.pull_table()
            self.pull_table()
        elif State.turn:
            self.pull_table()
        elif State.river:
            self.pull_table()
        else:
            self.new_game()
        self.compute_points()
        if not State.pre_flop:
            self.print_table()

    def start_game(self):
        while True:
            self.play_stage()

    def new_game(self):
        self.default_deck()
        self.shuffle_ranged_hand()

        temp_ranged_hand = []
        temp_ranged_hand.extend(Computer.ranged_hand)
        for player in Computer.players:
            player.hand.clear()
            player.table.clear()
            for h in range(0, 2):
                card = temp_ranged_hand.pop(0)
                player.hand.append(card)
                Computer.deck.deck.remove(card)

    def compute_count_winners(self):
        self.total_points = [p.get_max_total_point() if not p.get_folded() else 0 for p in Computer.players]
        self.max_total_points = max(self.total_points)
        self.count_winners = self.total_points.count(self.max_total_points)

    def set_points_winner(self):
        has_draw = self.is_draw()
        has_all_in = False
        player_winner = None
        for p in Computer.players:
            if p.get_max_total_point() == self.max_total_points:
                player_winner = p
                if p.get_all_in():
                    has_all_in = True
                    break
        if config.OUTPUT_IN_CONSOLE:
            self.print_winner()
        if has_all_in or has_draw:
            self.set_winners(player_winner)
        else:
            if config.OUTPUT_IN_CONSOLE:
                print(colored('{} get : {} points'.format(player_winner.id, Bank.bank), 'red'))
            player_winner.add_points(Bank.bank)

    def set_winners(self, player):
        if self.is_winners_end():
            return 0
        elif self.max_total_points == player.get_max_total_point():
            if self.is_draw():
                self.set_draw(player)
            elif player.get_all_in():
                if Bank.bank >= player.get_all_in_bank():
                    if config.OUTPUT_IN_CONSOLE:
                        print(colored('{} get : {} points'.format(player.id, player.get_all_in_bank()), 'red'))
                    player.add_points(player.get_all_in_bank())
                    Bank.set_bank(bank=Bank.bank - player.get_all_in_bank())
                else:
                    if config.OUTPUT_IN_CONSOLE:
                        print(colored('{} get : {} points'.format(player.id, Bank.bank), 'red'))
                    player.add_points(Bank.bank)
                    Bank.set_bank(bank=0)
                player.set_all_in(False)
                player.set_null_total_points()
            else:
                if config.OUTPUT_IN_CONSOLE:
                    print(colored('{} get : {} points'.format(player.id, Bank.bank), 'red'))
                player.add_points(Bank.bank)
                Bank.set_bank(bank=0)
                player.set_null_total_points()

            if self.is_winners_end():
                return 0
            for p in Computer.players:
                if p.get_all_in() and not p.folded and p.get_max_total_point() == self.max_total_points:
                    self.set_winners(p)
            for p in Computer.players:
                if not p.folded and p.get_max_total_point() == self.max_total_points:
                    self.set_winners(p)

    def set_draw(self, player):
        if self.is_winners_end():
            return 0
        elif player.get_max_total_point() == self.max_total_points:
            if player.get_all_in():
                if self.count_winners > 1:
                    draw_all_in_bank = player.get_all_in_bank() / self.count_winners
                else:
                    draw_all_in_bank = player.get_all_in_bank()
                print("bad draw")
                if Bank.bank >= draw_all_in_bank:
                    if config.OUTPUT_IN_CONSOLE:
                        print(colored('{} get : {} points'.format(player.id, draw_all_in_bank), 'red'))
                    player.add_points(draw_all_in_bank)
                    Bank.set_bank(bank=Bank.bank - draw_all_in_bank)
                else:
                    if config.OUTPUT_IN_CONSOLE:
                        print(colored('{} get : {} points'.format(player.id, Bank.bank), 'red'))
                    player.add_points(Bank.bank)
                    Bank.set_bank(bank=0)
            else:
                draw_bank = Bank.bank / self.count_winners
                if Bank.bank >= draw_bank:
                    if config.OUTPUT_IN_CONSOLE:
                        print(colored('{} get : {} points'.format(player.id, draw_bank), 'red'))
                    Bank.set_bank(bank=Bank.bank - draw_bank)
                    player.add_points(draw_bank)
                else:
                    if config.OUTPUT_IN_CONSOLE:
                        print(colored('{} get : {} points'.format(player.id, Bank.bank), 'red'))
                    player.add_points(Bank.bank)
                    Bank.set_bank(bank=0)
            player.set_folded()

        if self.is_winners_end():
            return 0
        for p in Computer.players:
            if p.get_all_in() and not p.folded and p.get_max_total_point() == self.max_total_points:
                self.set_draw(p)
        for p in Computer.players:
            if not p.folded and p.get_max_total_point() == self.max_total_points:
                self.set_draw(p)

    def is_winners_end(self):
        self.compute_count_winners()
        return self.count_winners == 0 or Bank.bank == 0 or self.max_total_points == 0

    def is_draw(self):
        self.compute_count_winners()
        if self.count_winners > 1:
            return True
        else:
            return False

    def get_index_winner(self):
        return [player.get_max_total_point() for player in Computer.players].index(self.get_max_point())

    def get_winner(self):
        max_point = self.get_max_point()
        for player in Computer.players:
            if not player.get_folded():
                if player.get_max_total_point() == max_point:
                    return player

    def print_winner(self):
        self.print_scores()
        print(colored('Bank {}'.format(Bank.bank), 'red'))
        if self.is_draw():
            print(colored('draw is winner ', 'red'))
        else:
            print(colored(str(self.get_winner().id) + ' is winner ', 'red'))

    @staticmethod
    def print_table():
        cs = ''
        for c in Computer.players[0].table:
            cs = cs + str(c) + '  '
        print(colored('Table: ' + cs, 'blue'))

    @staticmethod
    def compute_points():
        for player in Computer.players:
            full_hand = []
            full_hand.extend(player.hand)
            full_hand.extend(player.table)
            if State.output_in_console:
                cs = ''
                for c in player.hand:
                    cs = cs + str(c) + '  '
                print(colored('{} : {} \t\t\t\t points : {:.1f}'.format(str(player.id), cs[:-1], player.points),
                              'yellow'))
            Computer.player_sorted_hand = sorted(full_hand, reverse=True)
            Computer.set_player(player=player)
            if not State.pre_flop:
                Computer.is_royal()
            else:
                Computer.is_one()

    @staticmethod
    def do_default_state():
        State.set(pre_flop=True)
        for player in Computer.players:
            if player.dealer:
                Bank.set_bank(bank=0)
                Bank.set_bet(bet=0)
                d = player.get_next()
                d.set_d()
                if config.N_ALL_PLAYERS > 2:
                    sb = d.get_next()
                    sb.set_sb()
                    bb = sb.get_next()
                    bb.set_bb()
                else:
                    bb = d.get_next()
                    bb.set_bb()
                return bb.get_next()

    @staticmethod
    def is_end_game():
        for player in Computer.players:
            if player.points == 0:
                player.get_previous().set_d()
                print(colored('{} leaving game'.format(player.id), 'red'))
                Computer.players.remove(player)
                config.N_ALL_PLAYERS = config.N_ALL_PLAYERS - 1
                if config.N_ALL_PLAYERS == 1:
                    winner = Computer.players[0]
                    print(colored('winner {} with {} points'.format(winner.id, winner.points), 'red'))
                    return False
                continue
            player.folded = False
            player.did_action = False
            player.reset_action_states()
        return True

    @staticmethod
    def end_stage():
        for player in Computer.players:
            player.did_action = False
            player.set_winning_points_all_in()

    @staticmethod
    def is_continue():
        i = 0
        for player in Computer.players:
            if not player.get_folded():
                i = i + 1
        if i == 1:
            for player in Computer.players:
                player.did_action = True
            return False
        else:
            return True

    @staticmethod
    def is_new_game():
        i = 0
        for player in Computer.players:
            if not player.get_folded():
                i = i + 1
        if i == 1:
            return True
        else:
            if not State.river:
                State.next()
            return False

    @staticmethod
    def is_all_did_action():
        return [player.did_action for player in Computer.players].count(True) != config.N_ALL_PLAYERS

    @staticmethod
    def default_deck():
        Computer.deck = Deck()
        Computer.deck.shuffle()

    @staticmethod
    def get_max_point():
        return max([player.get_max_total_point() for player in Computer.players])

    @staticmethod
    def get_max_bank():
        return max([p.get_bank() if p.get_bank() else 0 for p in Computer.players])

    @staticmethod
    def shuffle_ranged_hand():
        random.shuffle(Computer.ranged_hand)

    @staticmethod
    def print_scores():
        for player in Computer.players:
            print(colored(player.get_current_action().combination_str, 'blue'))

    @staticmethod
    def random_dealer():
        Computer.players[random.randint(0, config.N_ALL_PLAYERS - 1)].set_d()

    @staticmethod
    def pull_table():
        card = Computer.deck.pull()
        for player in Computer.players:
            player.table.append(card)
