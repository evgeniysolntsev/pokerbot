import random

from api.helpers import utils
from api.helpers.model import Model
from api.poker.template_bot import TemplateBot


class RandomBot(TemplateBot):
    def __init__(self):
        super().__init__()
        self.bet_limit = random.randint(0, 100)
        self.call_limit = random.randint(0, self.bet_limit)

    def refresh_limits(self):
        self.bet_limit = random.randint(0, 100)
        self.call_limit = random.randint(0, self.bet_limit)

    def do_action(self):
        if super().is_skip():
            return 0
        self.predict_result = Model.dnn.predict([utils.get_array_from_simple_mode(self)])[0][0]
        super().do_action()
