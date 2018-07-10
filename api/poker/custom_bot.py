from api.helpers import utils
from api.helpers.model import Model
from api.poker.template_bot import TemplateBot


class CustomBot(TemplateBot):
    def __init__(self):
        super().__init__()
        self.bet_limit = 75
        self.call_limit = 50

    def do_action(self):
        if super().is_skip():
            return 0
        self.predict_result = Model.dnn.predict([utils.get_array_from_simple_mode(self)])[0][0]
        super().do_action()
