import config
from api.helpers import utils
from api.helpers.model import Model
from api.helpers.singleton import singleton
from api.poker.computer import Computer
from api.poker.computer_action import ComputerAction


@singleton
class LearningModeInputsCards:
    def __init__(self):
        self.X = []
        self.Y = []
        self.temp_map = {}

    def set_item(self, key, value):
        self.temp_map.__setitem__(key, value)

    def get_item(self, key):
        return self.temp_map.__getitem__(key)

    def action(self):
        self.do_learning()

    def update_data(self):
        if len(self.temp_map) == 0:
            for player in Computer.players:
                self.set_item(player.id, [])
        for player in Computer.players:
            temp_array = self.get_item(player.id)
            temp_array.append(utils.get_array_inputs_cards(player))
            self.set_item(player.id, temp_array)

        if len(Computer.players[0].table) > 4 or ComputerAction.is_new_game():
            draw = ComputerAction.is_draw()
            winner = ComputerAction.get_winner()

            for player in Computer.players:
                result = [0, 1]
                if player.id == winner.id:
                    result = [1, 0]
                if draw:
                    result = [0, 0]
                for s in range(4):
                    self.Y.append(result)

            for player in Computer.players:
                self.X.extend(self.get_item(player.id))
            self.temp_map.clear()

        if len(self.X) > config.FIT_QUANTITY:
            Model.init_tf_model_with_input_cards()
            Model.dnn.fit(
                X_inputs=self.X,
                Y_targets=self.Y,
                n_epoch=config.N_EPOCH,
                validation_set=config.VALIDATION_SET,
                show_metric=config.SHOW_METRIC
            )
            Model.dnn.save(config.PATH_NN_INPUTS_CARDS)
            return False
        else:
            return True
            # tensorflow.summary.FileWriter('logs', tensorflow.Session().graph)

    def do_learning(self):
        ComputerAction.random_dealer()
        while self.update_data():
            ComputerAction.set_points_winner()
            ComputerAction.is_end_game()
            first = ComputerAction.do_default_state()
            for stage in range(4):
                ComputerAction.next_stage()
                player = first
                while ComputerAction.is_continue() and ComputerAction.is_all_did_action():
                    if not player.did_action:
                        player.do_action()
                    player = player.get_next()
                ComputerAction.end_stage()
                if ComputerAction.is_new_game():
                    break
