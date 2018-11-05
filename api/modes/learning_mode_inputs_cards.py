from datetime import datetime

from termcolor import colored

import config
from api.helpers import utils
from api.helpers.model import Model
from api.helpers.singleton import singleton
from api.poker.core import Core
from api.poker.core_action import CoreAction


@singleton
class LearningModeInputsCards:
    def __init__(self):
        self.X = []
        self.Y = []
        self.temp_map = {}
        self.start_time = datetime.now().minute

    def set_item(self, key, value):
        self.temp_map.__setitem__(key, value)

    def get_item(self, key):
        return self.temp_map.__getitem__(key)

    def action(self):
        self.do_learning()

    def update_data(self):
        if len(self.temp_map) == 0:
            for player in Core.players:
                self.set_item(player.id, [])
        for player in Core.players:
            temp_array = self.get_item(player.id)
            temp_array.append(utils.get_array_inputs_cards(player))
            self.set_item(player.id, temp_array)

        if len(Core.players[0].table) > 4 or CoreAction.is_new_game():
            draw = CoreAction.is_draw()
            winner = CoreAction.get_winner()

            for player in Core.players:
                result = [0., 1.]
                if player.id == winner.id:
                    result = [1., 0.]
                if draw:
                    result = [0., 0.]
                for s in range(4):
                    self.Y.append(result)

            for player in Core.players:
                self.X.extend(self.get_item(player.id))
            self.temp_map.clear()
        len_x = len(self.X)
        if (len_x % 100000) == 0:
            print("Size of data : {}".format(colored(len_x, 'red')))
        if len_x > config.FIT_QUANTITY:
            print("End data generation with {} minutes".format(colored(datetime.now().minute - self.start_time, "red")))
            Model.init_tf_model_with_input_cards()
            Model.dnn.fit(
                X_inputs=self.X,
                Y_targets=self.Y,
                n_epoch=config.N_EPOCH,
                validation_set=config.VALIDATION_SET,
                batch_size=config.BATCH_SIZE,
                show_metric=config.SHOW_METRIC
            )
            Model.dnn.save(config.PATH_NN_INPUTS_CARDS)
            print("End fitting model with {} minutes".format(colored(datetime.now().minute - self.start_time, "red")))
            return False
        else:
            return True
            # tensorflow.summary.FileWriter('logs', tensorflow.Session().graph)

    def do_learning(self):
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
