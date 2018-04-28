import random

from api.dnn import config
from api.poker.bot import Bot
from api.poker.card import Card
from api.poker.deck import Deck
from api.poker.state import State
from api.utils.singleton import singleton


@singleton
class Computer(object):
    xY5x10 = 3712930
    xY5x9 = 3341637
    xY5x8 = 2970344
    xY5x7 = 2599051
    xY5x6 = 2227758
    xY5x5 = 1856465
    xY5x4 = 1485172
    xY5x3 = 1113879
    xY5x2 = 742586
    xY5 = 371293
    xY4 = 28561
    xY3 = 2197
    xY2 = 169
    xY1 = 13

    comb_level_number_map = {
        1: xY5,
        2: xY5x2,
        3: xY5x3,
        4: xY5x4,
        5: xY5x5,
        6: xY5x6,
        7: xY5x7,
        8: xY5x8,
        9: xY5x9,
        10: xY5x10
    }

    def __init__(self):
        self.deck = Deck
        self.player = Bot
        self.player_sorted_hand = []
        self.players = []
        self.ranged_hand = []
        State.set(pre_flop=True)
        for suit in State.SUITS:
            for rank in config.RANGE_HAND:
                card = Card(rank, suit)
                self.ranged_hand.append(card)

        random.shuffle(self.ranged_hand)

        for n in range(0, State.n_players):
            self.players.append(Bot())
        self.players = sorted(self.players, reverse=True)

    def set_deck(self, deck=None):
        self.deck = deck

    def set_player(self, player=None):
        self.player = player

    def get_total_point(self, comb_level=None, hand=None, sort=True):
        s0 = self.comb_level_number_map[comb_level]
        if sort:
            th = sorted(hand, reverse=True)
        else:
            th = hand

        s1 = (th[0].rank * self.xY4
              ) + (th[1].rank * self.xY3
                   ) + (th[2].rank * self.xY2
                        ) + (th[3].rank * self.xY1
                             ) + th[4].rank
        return s0 + s1

    def get_pre_flop_total_point(self, comb_level=None, hand=None):
        s0 = self.comb_level_number_map[comb_level]
        th = sorted(hand, reverse=True)
        s1 = (th[0].rank * self.xY1) + th[1].rank

        return s0 + s1

    def find_straight_with_out_low_ace(self, flush=False, royal=False):
        b = False
        s = []
        if not royal:
            cnt = 3
        else:
            cnt = 1
        for i in range(cnt):
            if b:
                break
            s.clear()
            ist = 0
            cr = self.player_sorted_hand[i].rank
            cs = self.player_sorted_hand[i].suit
            ic = 0
            for c in self.player_sorted_hand:
                if ist == 5:
                    b = True
                    break
                elif ((i == 1 or i == 2) and ic == 0) or (i == 2 and ic == 1):
                    ic += 1
                    continue
                elif c.rank == cr and (not flush or c.suit == cs):
                    ist += 1
                    cr -= 1
                    s.append(c)
                if ist == 5:
                    b = True
                    break
                ic += 1

        return s

    def find_straight_with_low_ace(self, flush=False):
        s = []
        for i in range(3):
            c = self.player_sorted_hand[i]
            if c.rank != 14:
                break
            s.clear()
            ish = 5
            cs = self.player_sorted_hand[i].suit
            s.append(c)
            for x in self.player_sorted_hand:
                if x.rank == ish and (not flush or x.suit == cs):
                    s.append(x)
                    ish -= 1

            s = sorted(s)
            if len(s) == 5:
                break

        return s

    def find_comb_by_name(self, two_pair=False, three=False, full_house=False):
        lr, lc, ct, cth, found_cards, tsh, it, ith = [], [], [], [], [], [c for c in self.player_sorted_hand], 0, 0

        for c in self.player_sorted_hand:
            lr.append(c.rank)
        for r in set(lr):
            lc.append([lr.count(r), r])
        for c in sorted(lc, reverse=True):
            if not three and c[0] == 2:
                it += 1
                ct.append(c[1])
            elif (three or full_house) and c[0] == 3:
                ith += 1
                cth.append(c[1])
        if full_house:
            if (it == 1 or it == 2) and ith == 1:
                t = []
                th = []
                for c in self.player_sorted_hand:
                    if len(t) == 1 and len(th) == 1:
                        break
                    elif c.rank == ct[0]:
                        t.append(c)
                    elif c.rank == cth[0]:
                        th.append(c)
                found_cards.extend(th)
                found_cards.extend(t)
            elif ith == 2:
                for c in self.player_sorted_hand:
                    if c.rank == cth[0] or c.rank == cth[1]:
                        found_cards.append(c)
                found_cards = sorted(found_cards, reverse=True)
                found_cards = found_cards[:-1]
        elif three:
            if ith == 1:
                for c in self.player_sorted_hand:
                    if c.rank == cth[0]:
                        found_cards.append(c)
                        tsh.remove(c)
                found_cards.append(tsh[0])
                found_cards.append(tsh[1])
        elif two_pair:
            if it == 3:
                thtp = []
                for c in self.player_sorted_hand:
                    if c.rank == ct[0] or c.rank == ct[1] or c.rank == ct[2]:
                        thtp.append(c)
                for c in sorted(thtp, reverse=True):
                    if len(found_cards) == 4:
                        break
                    found_cards.append(c)
                    tsh.remove(c)
                found_cards.append(tsh[0])
            elif it == 2:
                for c in self.player_sorted_hand:
                    if c.rank == ct[0] or c.rank == ct[1]:
                        found_cards.append(c)
                        tsh.remove(c)
                found_cards.append(tsh[0])
        elif it == 1:
            if State.pre_flop:
                return self.player_sorted_hand
            for c in self.player_sorted_hand:
                if c.rank == ct[0]:
                    found_cards.append(c)
                    tsh.remove(c)
            found_cards.append(tsh[0])
            found_cards.append(tsh[1])
            found_cards.append(tsh[2])

        return found_cards

    def is_royal(self):
        flag = False
        comb_level = 10
        royal = []
        if self.player_sorted_hand[0].rank == 14:
            royal = self.find_straight_with_out_low_ace(flush=True, royal=True)
        if len(royal) == 5:
            flag = True

        if flag:
            total_point = self.get_total_point(comb_level=comb_level, hand=royal)
            if State.output_in_console_comb:
                print('Royal Flush')

            self.player.set_total_point(total_point=total_point)
        else:
            self.is_straight_flush()

    def is_straight_flush(self):
        flag = False
        comb_level = 9
        sort = True
        straight_flush = self.find_straight_with_out_low_ace(flush=True)
        if len(straight_flush) == 5:
            flag = True
        elif self.player_sorted_hand[0].rank == 14:
            straight_flush = self.find_straight_with_low_ace(flush=True)
            if len(straight_flush) == 5:
                flag = True
                sort = False
        if flag:
            total_point = self.get_total_point(comb_level=comb_level, hand=straight_flush, sort=sort)
            if State.output_in_console_comb:
                print('Straight Flush')
            self.player.set_total_point(total_point=total_point)
        else:
            self.is_four()

    def is_four(self):
        flag = False
        comb_level = 8
        temp_four = self.player_sorted_hand
        four = []
        for i in range(4):
            if flag:
                break
            four.clear()
            cr = self.player_sorted_hand[i].rank
            cnt = 0
            for c in self.player_sorted_hand:
                if c.rank == cr:
                    cnt += 1
                    four.append(c)
            if cnt == 4:
                flag = True
                for f in four:
                    temp_four.remove(f)
                four.append(temp_four[0])
                break
            else:
                flag = False
        if flag:
            total_point = self.get_total_point(comb_level=comb_level, hand=four)
            if State.output_in_console_comb:
                print('Four of a Kind')
            self.player.set_total_point(total_point=total_point)
        else:
            self.is_full()

    def is_full(self):
        flag = False
        comb_level = 7
        full = self.find_comb_by_name(full_house=True)
        if len(full) == 5:
            flag = True
        if flag:
            total_point = self.get_total_point(comb_level=comb_level, hand=full, sort=False)
            if State.output_in_console_comb:
                print('Full House')
            self.player.set_total_point(total_point=total_point)
        else:
            self.is_flush()

    def is_flush(self):
        flag = False
        comb_level = 6
        flush = []

        for i in range(len(self.player_sorted_hand)):
            if flag:
                break
            flush.clear()
            ifl = 0
            cs = self.player_sorted_hand[i].suit
            ic = 0
            for c in self.player_sorted_hand:
                if ifl == 5:
                    flag = True
                    break
                elif ((i == 1 or i == 2) and ic == 0) or (i == 2 and ic == 1):
                    ic += 1
                    continue
                elif c.suit == cs:
                    flush.append(c)
                    ifl += 1
                if ifl == 5:
                    flag = True
                    break
                ic += 1
        if flag:
            total_point = self.get_total_point(comb_level=comb_level, hand=flush)
            if State.output_in_console_comb:
                print('Flush')
            self.player.set_total_point(total_point=total_point)
        else:
            self.is_straight()

    def is_straight(self):
        flag = False
        comb_level = 5
        sort = True
        straight = self.find_straight_with_out_low_ace()
        if len(straight) == 5:
            flag = True
        elif self.player_sorted_hand[0].rank == 14:
            straight = self.find_straight_with_low_ace()
            if len(straight) == 5:
                flag = True
                sort = False
        if flag:
            total_point = self.get_total_point(comb_level=comb_level, hand=straight, sort=sort)
            if State.output_in_console_comb:
                print('Straight')
            self.player.set_total_point(total_point=total_point)
        else:
            self.is_three()

    def is_three(self):
        flag = False
        comb_level = 4
        three = self.find_comb_by_name(three=True)
        if len(three) == 5:
            flag = True
        if flag:
            total_point = self.get_total_point(comb_level=comb_level, hand=three, sort=False)
            if State.output_in_console_comb:
                print('Three of a Kind')
            self.player.set_total_point(total_point=total_point)
        else:
            self.is_two()

    def is_two(self):
        flag = False
        comb_level = 3
        two = self.find_comb_by_name(two_pair=True)
        if len(two) == 5:
            flag = True
        if flag:
            total_point = self.get_total_point(comb_level=comb_level, hand=two, sort=False)
            if State.output_in_console_comb:
                print('Two Pair')
            self.player.set_total_point(total_point=total_point)
        else:
            self.is_one()

    def is_one(self):
        flag = False
        comb_level = 2
        one = self.find_comb_by_name()
        if len(one) == 5 or (len(one) == 2 and State.pre_flop):
            flag = True
        if flag:
            if not State.pre_flop:
                total_point = self.get_total_point(comb_level=comb_level, hand=one, sort=False)
            else:
                total_point = self.get_pre_flop_total_point(comb_level=comb_level, hand=one)
            if State.output_in_console_comb:
                print('One Pair')
            self.player.set_total_point(total_point=total_point)
        else:
            self.is_high()

    def is_high(self):
        comb_level = 1
        if not State.pre_flop:
            total_point = self.get_total_point(comb_level=comb_level, hand=self.player_sorted_hand)
        else:
            total_point = self.get_pre_flop_total_point(comb_level=comb_level, hand=self.player_sorted_hand)
        if State.output_in_console_comb:
            print('High Card')
        self.player.set_total_point(total_point=total_point)
