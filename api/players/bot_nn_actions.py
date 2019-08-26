import numpy as np

import config
from api.helpers import utils
from api.helpers.model import Model
from api.players.template_bot import TemplateBot


class BotNNActions(TemplateBot):
    def __init__(self):
        super().__init__()

    def do_action(self):
        if super().is_skip():
            return 0
        self.bet_limit = 0
        self.call_limit = 0
        self.predict_result = 0
        for i in range(50, 100):
            for j in range(i, 100):
                array_for_predict = [
                    utils.get_array_inputs_cards_and_bot_actions(bot=self, call_limit=i, bet_limit=j)
                ]
                predicting_result = Model.dnn.predict(np.array(array_for_predict))[0][1]
                if predicting_result > self.predict_result:
                    self.bet_limit = j
                    self.call_limit = i
                    self.predict_result = predicting_result
        super().do_action()
