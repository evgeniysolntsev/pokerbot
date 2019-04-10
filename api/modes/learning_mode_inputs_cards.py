from datetime import datetime

from pandas.io.json import json_normalize
from termcolor import colored

import config
from api.helpers.singleton import singleton
from api.poker.core import Core
from api.poker.core_action import CoreAction


@singleton
class LearningModeInputsCards:
    def __init__(self):
        self.X = []
        self.Y = []
        self.count_iteration = 0
        self.start_time = datetime.now()
        self.comb_map = {}
        self.max_size = 5570000

    def set_item(self, key, value):
        try:
            if len(self.comb_map) < self.max_size:
                self.comb_map.__setitem__(key, value)
            else:
                self.set_item_after_max_size(key, value)
        except MemoryError:
            print("MemoryError")
            self.set_item_after_max_size(key, value)

    def set_item_after_max_size(self, key, value):
        found = self.get_item(key)
        if found:
            self.comb_map.__setitem__(key, value)

    def get_item(self, key):
        return self.comb_map.get(key)

    def update_poker_map_by_comb(self, comb, player, winner, draw):
        found_comb_json = self.get_item(comb)
        count_win = 1 if not draw and player.id == winner.id else 0
        count_draw = 1 if draw else 0
        count_lose = 1 if not draw and player.id != winner.id else 0
        if found_comb_json:
            count_win = count_win + found_comb_json['count_win']
            count_draw = count_draw + found_comb_json['count_draw']
            count_lose = count_lose + found_comb_json['count_lose']
        game_result_in_json = {
            "comb": comb,
            "count_win": count_win,
            "count_draw": count_draw,
            "count_lose": count_lose,
        }
        self.set_item(comb, game_result_in_json)

    def update_data(self):
        if len(Core.players[0].table) > 4 or CoreAction.is_new_game():
            draw = CoreAction.is_draw()
            winner = CoreAction.get_winner()
            for player in Core.players:
                self.update_poker_map_by_comb(player.get_hand_str(), player, winner, draw)
                self.update_poker_map_by_comb(player.get_flop_str(), player, winner, draw)
                self.update_poker_map_by_comb(player.get_turn_str(), player, winner, draw)
                self.update_poker_map_by_comb(player.get_river_str(), player, winner, draw)
            now_time = datetime.now()
            run_time = (now_time - self.start_time).seconds
            if run_time % 10000 == 0 or len(self.comb_map) > self.max_size:
                print(len(self.comb_map))
                comb_map_values = self.comb_map.values()
                complete_values = []
                for value in comb_map_values:
                    if (value['count_win'] + value['count_draw'] + value['count_lose']) > 3:
                        complete_values.append(value)
                self.comb_map.clear()
                for value in complete_values:
                    self.set_item(value['comb'], value)
                print(run_time)
                print(len(self.comb_map))
            if run_time > 345600:
                comb_map_values = self.comb_map.values()
                complete_values = []
                for value in comb_map_values:
                    if (value['count_win'] + value['count_draw'] + value['count_lose']) > 8:
                        complete_values.append(value)

                df = json_normalize(complete_values)
                df.to_csv("C:\\Users\\usr\\Documents\poker_comb.csv")
                exit(0)
                self.comb_map.clear()
        if self.count_iteration > config.FIT_QUANTITY:
            print("End data generation with {} minutes".format(colored(datetime.now() - self.start_time, "red")))
            return False
        else:
            return True

    def do_play(self):
        CoreAction.random_dealer()
        while self.update_data():
            CoreAction.set_points_winner()
            CoreAction.is_end_game()
            first = CoreAction.do_default_state()
            for stage in range(4):
                CoreAction.next_stage()
                player = first
                while CoreAction.is_continue() and CoreAction.is_all_did_action():
                    if not player.did_action:
                        player.do_action()
                    player = player.get_next()
                CoreAction.end_stage()
                if CoreAction.is_new_game():
                    break
