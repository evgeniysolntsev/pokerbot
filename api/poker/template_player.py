import config
from api.helpers import utils
from api.poker.bank import Bank
from api.poker.state import State
from api.poker.state_action import ActionState


class TemplatePlayer:
    def __init__(self):
        self.id = None
        self.points = config.START_POINTS
        self.hand = []
        self.table = []
        self.dealer = False
        self.small_blind = False
        self.big_blind = False
        self.did_action = False
        self.all_in_bank = None
        self.action_states = {
            "PreFlop": ActionState(),
            "Flop": ActionState(),
            "Turn": ActionState(),
            "River": ActionState()
        }

    def __lt__(self, other):
        return self.id < other.id

    def get_points(self):
        return self.points

    def set_points(self, points=None):
        self.points = points

    def add_points(self, points=None):
        self.points = self.points + points

    def sub_points(self, points=None):
        self.points = self.points - points

    def set_hand(self, hand=None):
        self.hand = hand

    def set_table(self, table=None):
        self.table = table

    def set_full_combination(self, total_point=None, comb_level=None, hand=None):
        current_action = self.get_current_action()
        current_action.total_point = total_point
        if config.OUTPUT_IN_CONSOLE:
            combination_map = {
                1: '{} combination: high {}{}{}{}{}',
                2: '{} combination: one pair {}{} with high {}{}{}',
                3: '{} combination: two pair {}{}{}{} with high {}',
                4: '{} combination: three of kind {}{}{} with high {}{}',
                5: '{} combination: straight {}{}{}{}{}',
                6: '{} combination: flush {}{}{}{}{}',
                7: '{} combination: full house {}{}{}{}{}',
                8: '{} combination: four {}{}{}{} with high {}',
                9: '{} combination: straight flush {}{}{}{}{}',
                10: '{} combination: royal flush {}{}{}{}{}',
            }
            current_action.combination_str = combination_map.get(comb_level).format(
                self.id,
                str(hand[0]) if len(hand) > 0 else '',
                str(hand[1]) if len(hand) > 1 else '',
                str(hand[2]) if len(hand) > 2 else '',
                str(hand[3]) if len(hand) > 3 else '',
                str(hand[4]) if len(hand) > 4 else ''
            )

    def get_max_total_point(self):
        if self.get_folded():
            return 0
        else:
            return max([state.total_point for state in self.action_states.values()])

    def set_player_state(self, d=False, sb=False, bb=False):
        self.dealer = d
        self.small_blind = sb
        self.big_blind = bb

    def get_action_state_by_key(self, key):
        return self.action_states.__getitem__(key)

    def get_current_action(self):
        return self.action_states.__getitem__(State.get())

    def reset_action_states(self):
        self.action_states = {
            "PreFlop": ActionState(),
            "Flop": ActionState(),
            "Turn": ActionState(),
            "River": ActionState()
        }
        self.did_action = False
        self.all_in_bank = None

    def set_d(self):
        self.set_player_state(d=True)

    def set_sb(self):
        self.set_player_state(sb=True)
        self.pre_game_take_points()

    def set_bb(self):
        self.set_player_state(bb=True)
        self.pre_game_take_points()

    def set_cur_points_in_bank(self, points_in_bank):
        self.get_current_action().points_in_bank = self.get_current_action().points_in_bank + points_in_bank

    def set_all_in(self, all_in=True):
        self.get_current_action().all_in = all_in

    def set_null_total_points(self):
        for state in self.action_states.values():
            state.total_point = 0

    def set_folded(self, folded=True):
        self.get_current_action().folded = folded

    def set_all_in_bank(self, bank=None):
        self.all_in_bank = bank

    def set_winning_points_all_in(self):
        if self.get_all_in() and not self.get_all_in_bank():
            all_in_bank = 0
            from api.poker.computer import Computer
            for p in Computer.players:
                if p.get_total_bank() >= self.get_total_bank():
                    all_in_bank_p = self.get_total_bank()
                else:
                    all_in_bank_p = p.get_total_bank()
                all_in_bank = all_in_bank + all_in_bank_p
            self.set_all_in_bank(all_in_bank)

    def get_cur_points_in_bank(self):
        return self.get_current_action().points_in_bank

    def get_total_bank(self):
        total_bank = 0
        for state in self.action_states.values():
            if state.points_in_bank:
                total_bank = total_bank + state.points_in_bank
        return total_bank

    def get_all_in_bank(self):
        return self.all_in_bank

    def get_all_in(self):
        for state in self.action_states.values():
            if state.all_in:
                return True
        return False

    def get_folded(self):
        for state in self.action_states.values():
            if state.folded:
                return True
        return False

    def pre_game_take_points(self):
        if self.small_blind:
            sb_points = Bank.step / 2
            if self.points > sb_points:
                self.points = self.points - sb_points
                self.get_current_action().points_in_bank = Bank.step / 2
                Bank.set_sb()
            else:
                self.get_current_action().points_in_bank = self.points
                Bank.add_to_bank(points=self.points)
                self.points = 0
        elif self.big_blind:
            if self.points > Bank.step:
                self.points = self.points - Bank.step
                self.get_current_action().points_in_bank = Bank.step
                Bank.set_bb()
            else:
                self.get_current_action().points_in_bank = self.points
                Bank.add_to_bank(points=self.points)
                self.points = 0

    def do_bet(self, bet=None):
        from api.poker.computer_action import Computer
        from api.poker.computer_action import ComputerAction
        bet = float(bet)
        max_bet = ComputerAction.get_max_points_in_bank()
        if max_bet != 0 and bet < (max_bet * 2):
            if max_bet * 2 >= self.points:
                bet = self.points
            else:
                bet = max_bet * 2
        if bet > self.points:
            bet = self.points
            Bank.add_to_bank(bet)
            self.set_all_in()
            self.points = 0
        elif bet <= max_bet:
            if max_bet >= self.points:
                bet = self.points
                Bank.add_to_bank(bet)
                self.set_all_in()
                self.points = 0
            else:
                bet = max_bet
                Bank.add_to_bank(bet)
                self.points = self.points - bet
            self.set_cur_points_in_bank(bet)
            if config.OUTPUT_IN_CONSOLE:
                print('{} call: {}'.format(self.id, bet))
            return 0
        elif bet > max_bet:
            self.points = self.points - bet
            Bank.add_to_bank(bet)
        for player in Computer.players:
            player.did_action = False
        self.set_cur_points_in_bank(bet)
        Bank.set_bet(bet=bet)
        self.did_action = True
        if config.OUTPUT_IN_CONSOLE:
            print('{} bet: {}'.format(self.id, self.get_cur_points_in_bank()))

    def do_call(self):
        from api.poker.computer_action import ComputerAction
        max_bet = ComputerAction.get_max_points_in_bank()
        cur_points = self.get_cur_points_in_bank()
        if (cur_points >= max_bet and cur_points >= Bank.step) or max_bet < Bank.step:
            if config.OUTPUT_IN_CONSOLE:
                print('{} check'.format(self.id))
            return 0
        if max_bet < Bank.step:
            max_bet = Bank.step
        if self.points > max_bet:
            if cur_points != 0:
                max_bet = max_bet - cur_points
            self.set_cur_points_in_bank(max_bet)
            Bank.add_to_bank(points=max_bet)
            self.sub_points(max_bet)
        else:
            max_bet = self.points
            self.set_all_in()
            self.set_cur_points_in_bank(max_bet)
            Bank.add_to_bank(points=max_bet)
            self.points = 0
        if config.OUTPUT_IN_CONSOLE:
            print('{} call: {}'.format(self.id, max_bet))

    def do_fold(self):
        from api.poker.computer_action import ComputerAction
        if self.get_all_in():
            if config.OUTPUT_IN_CONSOLE:
                print('{} all_in'.format(self.id))
            return 0
        elif self.get_cur_points_in_bank() == ComputerAction.get_max_points_in_bank():
            if config.OUTPUT_IN_CONSOLE:
                print('{} check'.format(self.id))
            return 0
        self.set_folded()
        self.set_null_total_points()

        if config.OUTPUT_IN_CONSOLE:
            print('{} fold'.format(self.id))

    def get_next(self):
        from api.poker.computer import Computer
        player_index = Computer.players.index(self)
        player_next_index = player_index + 1
        if player_next_index < utils.N_ALL_PLAYERS:
            return Computer.players[player_next_index]
        else:
            return Computer.players[0]

    def get_previous(self):
        from api.poker.computer import Computer
        player_index = Computer.players.index(self)
        player_previous_index = player_index - 1
        if player_previous_index >= 0:
            return Computer.players[player_previous_index]
        else:
            return Computer.players[utils.N_ALL_PLAYERS - 1]

    def is_next(self):
        from api.poker.computer import Computer
        i = 0
        j = 0
        for player in Computer.players:
            if not player.get_folded():
                i = i + 1
            if player.get_all_in():
                j = j + 1
        return self.get_folded() or self.get_all_in() or i - j == 1

    def is_skip(self):
        self.did_action = True
        if self.is_next():
            return True
