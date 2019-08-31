import random

import numpy as np

from api.helpers import utils
from api.helpers.model import Model
from api.players.template_bot import TemplateBot


class BotCustomActions(TemplateBot):
    def __init__(self):
        super().__init__()
        self.bet_limit = 95
        self.call_limit = 85

    def do_action(self):
        self.bet_limit = random.randint(90, 100)
        self.call_limit = random.randint(75, self.bet_limit)
        if super().is_skip():
            return 0
        self.predict_result = Model.dnn.predict(np.array([utils.get_array_inputs_cards(self)]))[0][1]
        super().do_action()
