import random

from api.helpers import utils
from api.players.template_bot import TemplateBot


class BotRandomActions(TemplateBot):
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
        # df.loc[df['column_name'] == self.hand[]]
        # self.predict_result = Model.dnn.predict([utils.get_array_inputs_cards(self)])[0][0]
        super().do_action()
