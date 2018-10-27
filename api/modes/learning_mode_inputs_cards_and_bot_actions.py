import config
from api.helpers import utils
from api.helpers.model import Model
from api.helpers.singleton import singleton
from api.poker.core import Core
from api.poker.core_action import CoreAction


@singleton
class LearningModeInputsCardsAndBotActions:
    def __init__(self):
        self.X = []
        self.Y = []
        self.temp_map = {}

    def set_item(self, key, value):
        self.temp_map.__setitem__(key, value)

    def get_item(self, key):
        return self.temp_map.__getitem__(key)

    def action(self):
        Model.init_tf_model_with_input_cards(load=True)
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
                result = [0, 1]
                if player.id == winner.id:
                    result = [1, 0]
                if draw:
                    result = [0, 0]
                for s in range(4):
                    self.Y.append(result)

            for player in Core.players:
                self.X.extend(self.get_item(player.id))
            self.temp_map.clear()

        if len(self.X) > config.FIT_QUANTITY:
            Model.init_tf_model_with_input_cards_and_bot_actions()
            Model.dnn.fit(
                X_inputs=self.X,
                Y_targets=self.Y,
                n_epoch=config.N_EPOCH,
                validation_set=config.VALIDATION_SET,
                show_metric=config.SHOW_METRIC
            )
            Model.dnn.save(config.PATH_NN_INPUTS_CARDS_AND_BOT_ACTIONS)
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
