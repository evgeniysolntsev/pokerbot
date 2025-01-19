import random
from os import system

import psycopg2
from termcolor import colored

import config
from api.helpers import utils
from api.helpers.singleton import singleton
from api.players.template_bot import TemplateBot
from api.poker.bank import Bank
from api.poker.core import Core
from api.poker.deck import Deck
from api.poker.state import State


@singleton
class CoreAction(object):
    count_game = 0
    max_total_points = None
    count_winners = None
    count_winners_final = None
    total_points = None
    conn = None
    cursor = None
    template_insert_sql = "insert INTO smev_service.test_table(action_preflop,action_flop,action_turn,action_river,stage,hand_0,hand_1,table_0,table_1,table_2,table_3,table_4,predict_preflop,predict_flop,predict_turn,predict_river,win,number) values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');"

    def playing(self):
        clear = lambda: system('cls')
        clear()
        self.random_dealer()
        while self.is_end_game():
            first = self.do_default_state()
            for stage in range(4):
                self.next_stage()
                player = first
                while self.is_continue() and self.is_all_did_action():
                    if not player.did_action:
                        player.do_action()
                    player = player.get_next()
                self.end_stage()
                if self.is_new_game():
                    break
            players = self.set_points_winner()
            self.save_result(players)

    def save_result(self, players):
        if self.conn is None:
            self.conn = psycopg2.connect(dbname='smev_service_db', user='smev_service_user',
                                         password='smev_service_user_password', host='localhost')
        commit = False
        winner = self.get_winner()
        for player in players:
            state = player.get_current_state()
            if player.hand[0].rank < 10 or player.hand[1].rank < 10:
                continue
            win = False
            if player == winner:
                win = True
            preflop = player.get_action_state_by_key('PreFlop')
            if preflop.action == 'fold':
                continue
            flop = player.get_action_state_by_key('Flop')
            turn = player.get_action_state_by_key('Turn')
            river = player.get_action_state_by_key('River')
            if preflop.predict == 0:
                continue

            sql = self.template_insert_sql.format(
                preflop.action, flop.action, turn.action, river.action, state,
                self.get_str_card(player.hand[0]),
                self.get_str_card(player.hand[1]),
                self.get_str_card(player.table[0]) if len(player.table) > 0 else '',
                self.get_str_card(player.table[1]) if len(player.table) > 1 else '',
                self.get_str_card(player.table[2]) if len(player.table) > 2 else '',
                self.get_str_card(player.table[3]) if len(player.table) > 3 else '',
                self.get_str_card(player.table[4]) if len(player.table) > 4 else '',
                preflop.predict, flop.predict, turn.predict, river.predict, win, self.count_game
            )
            self.conn.cursor().execute(sql)
            commit = True
        try:
            if commit is True:
                self.conn.commit()
        except:
            # в случае сбоя подключения будет выведено сообщение в STDOUT
            print('Can`t establish connection to database')

    def get_str_card(self, card):
        if card is None:
            return ''
        return str(card.rank) + str(card.suit)

    def next_stage(self):
        if config.OUTPUT_IN_CONSOLE:
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
        if not State.pre_flop and config.OUTPUT_IN_CONSOLE:
            self.print_table()

    def new_game(self):
        self.default_deck()
        self.shuffle_ranged_hand()
        self.count_game = self.count_game + 1
        for player in Core.players:
            player.hand.clear()
            player.table.clear()
            if utils.BOT_RANDOM_ACTIONS:
                player.refresh_limits()
            for h in range(0, 2):
                card = Core.deck.pull()
                player.hand.append(card)

    def compute_count_winners(self):
        self.total_points = [p.get_max_total_point() if not p.get_folded() else 0 for p in Core.players]
        self.max_total_points = max(self.total_points)
        self.count_winners = self.total_points.count(self.max_total_points)

    def set_points_winner(self):
        has_draw = self.is_draw()
        has_all_in = False
        player_winner = None
        for p in Core.players:
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
                self.convert_get_message(player_winner.id, Bank.bank)
            player_winner.add_points(Bank.bank)
        return Core.players

    def set_winners(self, player):
        if self.is_winners_end():
            return 0
        elif self.max_total_points == player.get_max_total_point():
            if self.is_draw():
                self.set_draw(player)
            elif player.get_all_in():
                if Bank.bank >= player.get_all_in_bank():
                    if config.OUTPUT_IN_CONSOLE:
                        self.convert_get_message(player.id, player.get_all_in_bank())
                    player.add_points(player.get_all_in_bank())
                    Bank.set_bank(bank=Bank.bank - player.get_all_in_bank())
                else:
                    if config.OUTPUT_IN_CONSOLE:
                        self.convert_get_message(player.id, Bank.bank)
                    player.add_points(Bank.bank)
                    Bank.set_bank(bank=0)
                player.set_all_in(False)
                player.set_null_total_points()
            else:
                if config.OUTPUT_IN_CONSOLE:
                    self.convert_get_message(player.id, Bank.bank)
                player.add_points(Bank.bank)
                Bank.set_bank(bank=0)
                player.set_null_total_points()

            if self.is_winners_end():
                return 0
            for p in Core.players:
                if p.get_all_in() and not p.get_folded() and p.get_max_total_point() == self.max_total_points:
                    self.set_winners(p)
            for p in Core.players:
                if not p.get_folded() and p.get_max_total_point() == self.max_total_points:
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
                if Bank.bank >= draw_all_in_bank:
                    if config.OUTPUT_IN_CONSOLE:
                        self.convert_get_message(player.id, draw_all_in_bank)
                    player.add_points(draw_all_in_bank)
                    Bank.set_bank(bank=Bank.bank - draw_all_in_bank)
                else:
                    if config.OUTPUT_IN_CONSOLE:
                        self.convert_get_message(player.id, Bank.bank)
                    player.add_points(Bank.bank)
                    Bank.set_bank(bank=0)
            else:
                draw_bank = Bank.bank / self.count_winners
                if Bank.bank >= draw_bank:
                    if config.OUTPUT_IN_CONSOLE:
                        self.convert_get_message(player.id, draw_bank)
                    Bank.set_bank(bank=Bank.bank - draw_bank)
                    player.add_points(draw_bank)
                else:
                    if config.OUTPUT_IN_CONSOLE:
                        self.convert_get_message(player.id, Bank.bank)
                    player.add_points(Bank.bank)
                    Bank.set_bank(bank=0)
            player.set_null_total_points()
            player.set_folded()

        if self.is_winners_end():
            return 0
        for p in Core.players:
            if p.get_all_in() and not p.get_folded() and p.get_max_total_point() == self.max_total_points:
                self.set_draw(p)
        for p in Core.players:
            if not p.get_folded() and p.get_max_total_point() == self.max_total_points:
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
        return [player.get_max_total_point() for player in Core.players].index(self.get_max_comb_point())

    def get_winner(self):
        max_point = self.get_max_comb_point()
        for player in Core.players:
            if not player.get_folded():
                if player.get_max_total_point() == max_point:
                    return player

    def print_winner(self):
        self.print_scores()
        print(colored('Bank {:.1f}'.format(Bank.bank), 'red'))
        if self.is_draw():
            print(colored('draw is winner ', 'red'))
        else:
            print(colored(str(self.get_winner().id) + ' is winner ', 'red'))

    @staticmethod
    def print_table():
        cs = ''
        for c in Core.players[0].table:
            cs = cs + colored(str(c), 'green' if c.suit == 's' or c.suit == 'c' else 'red') + '  '
        print('Table: ' + cs)

    @staticmethod
    def compute_points():
        for player in Core.players:
            full_hand = []
            full_hand.extend(player.hand)
            full_hand.extend(player.table)
            if State.output_in_console and not player.get_folded():
                i = 0
                cs = ''
                for c in player.hand:
                    i = i + 1
                    cs = cs + '['
                    if isinstance(player, TemplateBot) and not config.ONLY_TEST_INFO_CARD:
                        c = '? '
                        cs = cs + '' + colored('{}'.format(str(c)), 'blue')
                    else:
                        cs = cs + '' + colored('{}'.format(str(c)),
                                               'green' if c.suit == 's' or c.suit == 'c' else 'red')
                    cs = cs + ']'

                print('{}:{}'.format(str(player.id), cs))
                print(colored('points : [{:.1f}]'.format(player.points), 'white'))
            Core.player_sorted_hand = sorted(full_hand, reverse=True)
            Core.set_player(player=player)
            if not State.pre_flop:
                Core.is_royal()
            else:
                Core.is_one()

    @staticmethod
    def do_default_state():
        State.set(pre_flop=True)
        for player in Core.players:
            if player.dealer:
                Bank.set_bank(bank=0)
                Bank.set_bet(bet=0)
                d = player.get_next()
                d.set_d()
                if utils.COUNT_ALL_PLAYERS > 2:
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
        removed_players = []
        for player in Core.players:
            if player.points == 0:
                if config.ETERNAL_MODE_AFTER_LOSING_PLAYER_ADDING_POINTS:
                    player.points = 50
                    if config.OUTPUT_IN_CONSOLE:
                        print(colored('{} refresh points'.format(player.id), 'red'))
                else:
                    player.get_previous().set_d()
                    if config.OUTPUT_IN_CONSOLE:
                        print(colored('{} leaving game'.format(player.id), 'red'))
                    removed_players.append(player)
                continue
            player.reset_action_states()
        for player in removed_players:
            Core.players.remove(player)
            utils.COUNT_ALL_PLAYERS = utils.COUNT_ALL_PLAYERS - 1
            if utils.COUNT_ALL_PLAYERS == 1:
                if config.ETERNAL_MODE:
                    utils.COUNT_ALL_PLAYERS = utils.COUNT_PLAYERS + utils.COUNT_BOT_PLAYERS
                    utils.TEMP_NAMES = config.HUMAN_NAMES.copy()
                    utils.TEMP_BOT_NAMES = config.BOT_NAMES.copy()
                    Core.players = []
                    Core.init_players()
                    CoreAction.random_dealer()
                    if config.OUTPUT_IN_CONSOLE:
                        print(colored('new game is start', 'red'))
                else:
                    winner = Core.players[0]
                    if config.OUTPUT_IN_CONSOLE:
                        print(colored('winner {} with {:.1f} points'.format(winner.id, winner.points), 'red'))
                    input("Game over")
                    return False
        return True

    @staticmethod
    def end_stage():
        for player in Core.players:
            player.did_action = False
            player.set_winning_points_all_in()

    @staticmethod
    def is_continue():
        i = 0
        for player in Core.players:
            if not player.get_folded():
                i = i + 1
        if i == 1:
            for player in Core.players:
                player.did_action = True
            return False
        else:
            return True

    @staticmethod
    def is_new_game():
        i = 0
        for player in Core.players:
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
        return [player.did_action for player in Core.players].count(True) != utils.COUNT_ALL_PLAYERS

    @staticmethod
    def default_deck():
        Core.deck = Deck()
        Core.deck.shuffle()

    @staticmethod
    def get_max_comb_point():
        return max([player.get_max_total_point() if not player.get_folded() else 0 for player in Core.players])

    @staticmethod
    def get_max_comb_level():
        return max([player.get_max_comb_level() if not player.get_folded() else 0 for player in Core.players])

    @staticmethod
    def get_max_points_in_bank():
        return max([p.get_cur_points_in_bank() if p.get_cur_points_in_bank() else 0 for p in Core.players])

    @staticmethod
    def shuffle_ranged_hand():
        random.shuffle(Core.ranged_hand)

    @staticmethod
    def print_scores():
        if State.river:
            for player in Core.players:
                print(colored(player.get_current_action().combination_str, 'blue'))

    @staticmethod
    def random_dealer():
        Core.players[random.randint(0, utils.COUNT_ALL_PLAYERS - 1)].set_d()

    @staticmethod
    def pull_table():
        card = Core.deck.pull()
        for player in Core.players:
            player.table.append(card)

    @staticmethod
    def convert_get_message(playerId=None, points=None):
        print(colored('{} get : {:.1f} points'.format(playerId, points), 'red'))
