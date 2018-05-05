import config
from api.helpers import utils
from api.helpers.model import Model
from api.helpers.singleton import singleton
from api.poker.computer import Computer
from api.poker.computer_action import ComputerAction
from api.poker.state import State


@singleton
class LearningMode:
    def __init__(self):
        self.X = []
        self.Y = []
        self.temp_map = {}
        self.main_index = -1
        if config.LEARNING_MODE:
            self.learning()

    def update_data(self):
        if len(self.temp_map) == 0:
            for player in Computer.players:
                self.temp_map.__setitem__(player.id, [])
        for player in Computer.players:
            t_a = self.temp_map.__getitem__(player.id)
            if config.LEARNING_BOT_MODE:
                a_p = utils.get_array_from_bot(player)
            elif config.LEARNING_MODE:
                a_p = utils.get_array_from_player(player)
            t_a.append(a_p)
            self.temp_map.__setitem__(player.id, t_a)
        if len(Computer.players[0].table) > 4:
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
                self.X.extend(self.temp_map.__getitem__(player.id))

            self.temp_map.clear()

        if len(self.X) > config.FIT_QUANTITY:
            Model.dnn.fit(
                X_inputs=self.X,
                Y_targets=self.Y,
                n_epoch=config.N_EPOCH,
                validation_set=config.VALIDATION_SET,
                show_metric=config.SHOW_METRIC
            )
            self.X.clear()
            self.Y.clear()
            # for tensorboard graph
            # tensorflow.summary.FileWriter('logs', tensorflow.Session().graph)

    def learning(self):
        while True:
            if len(self.X) == 0 and self.main_index > 0:
                Model.dnn.save('saved_dnn/example')
                self.predict()
                exit(0)
            State.set(pre_flop=True)
            for n in range(0, 4):
                ComputerAction.play_stage()
                self.update_data()
            self.main_index += 1
